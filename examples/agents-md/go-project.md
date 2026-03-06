# AGENTS.md — Go Project

## Language & Runtime
- Go 1.22+
- Use `go mod tidy` after adding dependencies

## Code Style
- Follow standard Go conventions (gofmt, golint)
- Use meaningful variable names, avoid single-letter names except in loops
- Error handling: always check errors, never use `_` to discard them
- Prefer returning errors over using panic

## Project Structure
- `cmd/` — entrypoints
- `internal/` — private packages
- `pkg/` — public reusable packages
- `api/` — API definitions (proto, OpenAPI)

## Testing
- Write table-driven tests
- Run tests with: `go test ./...`
- Run linter with: `golangci-lint run`
- Minimum 80% coverage for new code

## Git
- Commit messages: imperative mood, e.g. "Add user auth" not "Added user auth"
- Never commit vendor/ directory
- Never commit .env or secrets
