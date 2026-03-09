"""REST API wrapper for adkcode — production-ready API with ADK web UI.

Provides REST endpoints for external clients (LINE bot, Slack, custom frontend)
while sharing sessions with the ADK web UI.

Endpoints:
  GET  /           — ADK web UI (dev UI for testing)
  POST /session    — Create session
  GET  /session/{id} — Get session info
  DELETE /session/{id} — Delete session
  POST /session/{id}/message — Send prompt, get response
  POST /session/{id}/abort — Cancel running task
"""

import os
import time
import uuid
import logging
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel
from google.genai import types

# Change to workspace dir before importing agent (so AGENTS.md loads correctly)
os.chdir("/workspace")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
PORT = int(os.environ.get("PORT", 8000))

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


# --- Session tracking ---
session_map: dict[str, dict] = {}


class CreateSessionRequest(BaseModel):
    title: str = ""
    user_id: str = ""


class MessageRequest(BaseModel):
    content: str


@app.post("/session")
async def create_session(req: CreateSessionRequest = CreateSessionRequest()):
    session_id = f"s-{int(time.time())}-{uuid.uuid4().hex[:6]}"
    user_id = "user"

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
    }

    logger.info(f"Created session: {session_id}")
    return {"id": session_id, "user_id": user_id}


@app.get("/session/{session_id}")
async def get_session(session_id: str):
    info = session_map.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Session not found")
    return info


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    if session_id in session_map:
        del session_map[session_id]
    return {"deleted": True}


@app.post("/session/{session_id}/message")
async def send_message(session_id: str, req: MessageRequest):
    info = session_map.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Session not found")

    if info["status"] == "running":
        raise HTTPException(status_code=409, detail="Session is busy")

    info["status"] = "running"
    start = time.time()

    try:
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=req.content)],
        )

        result_text = ""
        runner = await get_runner()

        async for event in runner.run_async(
            user_id=info["user_id"],
            session_id=session_id,
            new_message=content,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            result_text += part.text

        if not result_text:
            result_text = "(no response)"

        duration_ms = int((time.time() - start) * 1000)
        logger.info(f"[{session_id}] done: {duration_ms}ms, {len(result_text)} chars")

        return {
            "result": result_text,
            "session_id": session_id,
            "is_error": False,
            "duration_ms": duration_ms,
        }

    except Exception as e:
        logger.error(f"[{session_id}] error: {e}")
        return {
            "result": str(e),
            "session_id": session_id,
            "is_error": True,
            "duration_ms": int((time.time() - start) * 1000),
        }
    finally:
        info["status"] = "idle"


@app.post("/session/{session_id}/abort")
async def abort_session(session_id: str):
    info = session_map.get(session_id)
    if not info:
        raise HTTPException(status_code=404, detail="Session not found")
    info["status"] = "idle"
    return {"aborted": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
