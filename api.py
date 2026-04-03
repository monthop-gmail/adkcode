"""REST API wrapper for adkcode — production-ready API with ADK web UI.

Provides REST endpoints for external clients (LINE bot, Slack, custom frontend)
while sharing sessions with the ADK web UI.

Endpoints:
  GET  /                          — ADK web UI (dev UI for testing)
  POST /session                   — Create session
  GET  /session/{id}              — Get session info
  DELETE /session/{id}            — Delete session
  POST /session/{id}/message      — Send prompt, get JSON response
  GET  /session/{id}/stream       — SSE stream of agent events (connect before sending)
  POST /session/{id}/abort        — Cancel running task
  POST /api/query                 — Stateless one-shot query (no session management)
"""

import asyncio
import json
import os
import time
import uuid
import logging
from pathlib import Path

from fastapi import Depends, HTTPException, Request, Security
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from google.genai import types

# Change to workspace dir before importing agent (so AGENTS.md loads correctly)
os.chdir("/workspace")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Config ---
API_PASSWORD = os.environ.get("ADKCODE_API_PASSWORD", "")
PROMPT_TIMEOUT_MS = int(os.environ.get("ADKCODE_PROMPT_TIMEOUT_MS", "120000"))
PORT = int(os.environ.get("PORT", 8000))

# --- Build ADK app with shared session service ---
from google.adk.sessions import InMemorySessionService
from google.adk.cli.fast_api import (
    AdkWebServer,
    AgentLoader,
    InMemoryCredentialService,
    LocalEvalSetsManager,
    LocalEvalSetResultsManager,
    create_artifact_service_from_options,
    create_memory_service_from_options,
)

AGENTS_DIR = "/app"

# Shared session service — used by both ADK web UI and REST endpoints
session_service = InMemorySessionService()

agent_loader = AgentLoader(agents_dir=AGENTS_DIR)
artifact_service = create_artifact_service_from_options(
    base_dir=AGENTS_DIR, artifact_service_uri=None, strict_uri=False, use_local_storage=True,
)
memory_service = create_memory_service_from_options(base_dir=AGENTS_DIR, memory_service_uri=None)
credential_service = InMemoryCredentialService()
eval_sets_manager = LocalEvalSetsManager(agents_dir=AGENTS_DIR)
eval_set_results_manager = LocalEvalSetResultsManager(agents_dir=AGENTS_DIR)

adk_web_server = AdkWebServer(
    agent_loader=agent_loader,
    session_service=session_service,
    artifact_service=artifact_service,
    memory_service=memory_service,
    credential_service=credential_service,
    eval_sets_manager=eval_sets_manager,
    eval_set_results_manager=eval_set_results_manager,
    agents_dir=AGENTS_DIR,
)

# Get web assets dir for ADK web UI
WEB_ASSETS_DIR = Path(os.path.dirname(__file__)) / "browser"
try:
    import google.adk.cli as adk_cli
    WEB_ASSETS_DIR = Path(os.path.dirname(adk_cli.__file__)) / "browser"
except Exception:
    pass

app = adk_web_server.get_fast_api_app(
    allow_origins=["*"],
    web_assets_dir=WEB_ASSETS_DIR if WEB_ASSETS_DIR.exists() else None,
)

# --- Use the SAME runner as web UI ---
async def get_runner():
    return await adk_web_server.get_runner_async("adkcode")


# --- Auth ---
_bearer = HTTPBearer(auto_error=False)

async def verify_auth(credentials: HTTPAuthorizationCredentials = Security(_bearer)):
    if not API_PASSWORD:
        return  # auth disabled
    token = credentials.credentials if credentials else None
    if token != API_PASSWORD:
        raise HTTPException(status_code=401, detail={"error": "Unauthorized", "code": "AUTH_REQUIRED"})


# --- Session state ---
session_map: dict[str, dict] = {}
session_locks: dict[str, asyncio.Lock] = {}  # per-session request queue

def _get_lock(session_id: str) -> asyncio.Lock:
    if session_id not in session_locks:
        session_locks[session_id] = asyncio.Lock()
    return session_locks[session_id]


# --- SSE event subscribers ---
# Maps session_id → list of asyncio.Queue for SSE subscribers
session_subscribers: dict[str, list[asyncio.Queue]] = {}

def _publish_event(session_id: str, event: dict):
    for q in session_subscribers.get(session_id, []):
        try:
            q.put_nowait(event)
        except asyncio.QueueFull:
            pass  # drop if subscriber is slow


# --- Pydantic models ---
class CreateSessionRequest(BaseModel):
    title: str = ""
    user_id: str = ""


class MessageRequest(BaseModel):
    content: str


class QueryRequest(BaseModel):
    content: str


# --- Helpers ---
async def _run_agent(session_id: str, user_id: str, content: str) -> tuple[str, bool]:
    """Run the agent and publish SSE events. Returns (result_text, is_error)."""
    result_text = ""
    is_error = False

    content_obj = types.Content(
        role="user",
        parts=[types.Part.from_text(text=content)],
    )

    try:
        runner = await get_runner()
        timeout_s = PROMPT_TIMEOUT_MS / 1000

        async with asyncio.timeout(timeout_s):
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content_obj,
            ):
                # Publish tool/text events to SSE subscribers
                if hasattr(event, "content") and event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text and not event.is_final_response():
                            _publish_event(session_id, {
                                "type": "text_delta",
                                "content": part.text,
                                "session_id": session_id,
                            })

                if event.is_final_response():
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                result_text += part.text
                                _publish_event(session_id, {
                                    "type": "message.final",
                                    "content": part.text,
                                    "session_id": session_id,
                                })

    except TimeoutError:
        result_text = f"Request timed out after {PROMPT_TIMEOUT_MS}ms"
        is_error = True
        _publish_event(session_id, {"type": "error", "content": result_text, "session_id": session_id})
    except Exception as e:
        result_text = str(e)
        is_error = True
        _publish_event(session_id, {"type": "error", "content": result_text, "session_id": session_id})

    _publish_event(session_id, {"type": "done", "session_id": session_id})

    if not result_text:
        result_text = "(no response)"

    return result_text, is_error


# --- Endpoints ---

@app.post("/session", dependencies=[Depends(verify_auth)])
async def create_session(req: CreateSessionRequest = CreateSessionRequest()):
    session_id = f"s-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    user_id = req.user_id or "user"

    await session_service.create_session(
        app_name="adkcode",
        user_id=user_id,
        session_id=session_id,
    )

    session_map[session_id] = {
        "id": session_id,
        "user_id": user_id,
        "created_at": time.time(),
        "status": "idle",
        "message_count": 0,
    }

    logger.info(f"Created session: {session_id}")
    return {"id": session_id, "user_id": user_id}


@app.get("/session/{session_id}", dependencies=[Depends(verify_auth)])
async def get_session(session_id: str):
    info = session_map.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail={"error": "Session not found", "code": "SESSION_NOT_FOUND"})
    return info


@app.delete("/session/{session_id}", dependencies=[Depends(verify_auth)])
async def delete_session(session_id: str):
    session_map.pop(session_id, None)
    session_locks.pop(session_id, None)
    session_subscribers.pop(session_id, None)
    return {"deleted": True}


@app.post("/session/{session_id}/message", dependencies=[Depends(verify_auth)])
async def send_message(session_id: str, req: MessageRequest):
    info = session_map.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail={"error": "Session not found", "code": "SESSION_NOT_FOUND"})

    lock = _get_lock(session_id)
    if lock.locked():
        raise HTTPException(status_code=409, detail={"error": "Session is busy", "code": "SESSION_BUSY"})

    start = time.time()
    async with lock:
        info["status"] = "running"
        try:
            result_text, is_error = await _run_agent(session_id, info["user_id"], req.content)
            info["message_count"] = info.get("message_count", 0) + 1
        finally:
            info["status"] = "idle"

    duration_ms = int((time.time() - start) * 1000)
    logger.info(f"[{session_id}] done: {duration_ms}ms, {len(result_text)} chars")

    return {
        "result": result_text,
        "session_id": session_id,
        "is_error": is_error,
        "duration_ms": duration_ms,
    }


@app.get("/session/{session_id}/stream", dependencies=[Depends(verify_auth)])
async def stream_session(session_id: str, request: Request):
    """SSE endpoint — subscribe to real-time events for a session."""
    if session_id not in session_map:
        raise HTTPException(status_code=404, detail={"error": "Session not found", "code": "SESSION_NOT_FOUND"})

    queue: asyncio.Queue = asyncio.Queue(maxsize=128)
    if session_id not in session_subscribers:
        session_subscribers[session_id] = []
    session_subscribers[session_id].append(queue)

    async def event_generator():
        try:
            # Send connected event
            yield f"data: {json.dumps({'type': 'server.connected', 'session_id': session_id})}\n\n"

            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {json.dumps(event)}\n\n"
                    if event.get("type") == "done":
                        break
                except asyncio.TimeoutError:
                    # Send heartbeat
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
        finally:
            if session_id in session_subscribers:
                try:
                    session_subscribers[session_id].remove(queue)
                except ValueError:
                    pass

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/session/{session_id}/abort", dependencies=[Depends(verify_auth)])
async def abort_session(session_id: str):
    info = session_map.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail={"error": "Session not found", "code": "SESSION_NOT_FOUND"})
    info["status"] = "idle"
    _publish_event(session_id, {"type": "aborted", "session_id": session_id})
    return {"aborted": True}


@app.post("/api/query", dependencies=[Depends(verify_auth)])
async def query(req: QueryRequest):
    """Stateless one-shot query — creates a temporary session, runs, returns result."""
    session_id = f"q-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    user_id = "user"

    await session_service.create_session(
        app_name="adkcode",
        user_id=user_id,
        session_id=session_id,
    )

    start = time.time()
    result_text, is_error = await _run_agent(session_id, user_id, req.content)
    duration_ms = int((time.time() - start) * 1000)

    # Cleanup temp session
    await session_service.delete_session(
        app_name="adkcode", user_id=user_id, session_id=session_id
    )

    return {
        "result": result_text,
        "is_error": is_error,
        "duration_ms": duration_ms,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
