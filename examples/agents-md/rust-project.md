# AGENTS.md — Rust Project

## Stack
- Rust 1.75+ (2021 edition)
- Tokio async runtime
- Axum (web framework)
- SQLx (database)
- Serde (serialization)

## Code Style
- Run `cargo fmt` before committing
- Run `cargo clippy` — fix all warnings
- Prefer `&str` over `String` in function parameters
- Use `thiserror` for library errors, `anyhow` for application errors
- Avoid `.unwrap()` — use `?` operator or handle errors explicitly

## Project Structure
```
src/
├── main.rs
├── lib.rs
├── routes/       # HTTP handlers
├── models/       # Data structures
├── db/           # Database queries
├── error.rs      # Error types
└── config.rs     # Configuration
```

## Commands
- Build: `cargo build`
- Run: `cargo run`
- Test: `cargo test`
- Lint: `cargo clippy -- -D warnings`
- Format: `cargo fmt`

## Rules
- All public functions must have doc comments (`///`)
- Use `#[derive(Debug, Clone, Serialize, Deserialize)]` on data types
- Never use `unsafe` without a comment explaining why
- Keep functions under 50 lines
- Integration tests go in `tests/` directory
