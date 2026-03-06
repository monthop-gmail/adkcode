# AGENTS.md — Next.js Project

## Stack
- Next.js 14 (App Router)
- TypeScript (strict mode)
- Tailwind CSS
- Prisma ORM + PostgreSQL

## Code Style
- Use functional components only, no class components
- Prefer server components by default, add "use client" only when needed
- Use named exports, not default exports
- File naming: kebab-case for files, PascalCase for components

## Project Structure
```
src/
├── app/          # App router pages & layouts
├── components/   # Reusable UI components
├── lib/          # Utilities, helpers, db client
├── actions/      # Server actions
└── types/        # TypeScript type definitions
```

## Commands
- Dev server: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint`
- Format: `npx prettier --write .`
- DB migrate: `npx prisma migrate dev`

## Rules
- Never use `any` type — use `unknown` and narrow with type guards
- Always validate user input with Zod schemas
- Use `next/image` for all images
- API routes must return proper HTTP status codes
- Keep components under 150 lines, extract sub-components if larger
