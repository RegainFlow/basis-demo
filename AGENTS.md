# Basis Demo Agent Guide

This is a small teaching monorepo for an accounting-AI Codex workshop. Keep code
clear, conventional, and small enough to discuss live.

## Repo Map

- `packages/invoice-engine`: Decimal invoice math and expense categorization.
- `packages/api`: FastAPI business boundary over `invoice_engine`.
- `packages/web`: Vite/React invoice review UI.
- `e2e`: Playwright upload/edit/calculate path.
- `.agents/docs`: Policy prose referenced by review and implementation rules.
- `.agents/skills`: Reusable workshop skills.

## Package Routing

- Read `packages/invoice-engine/AGENTS.md` before changing invoice math.
- Read `packages/api/AGENTS.md` before changing HTTP payloads or FastAPI routes.
- Read `packages/web/AGENTS.md` before changing UI behavior or styling.

## Verification

Run the narrowest relevant check first, then the root gate before commit:

- Python format: `npm run format:python`
- Python lint: `npm run lint:python`
- Python tests: `npm run test:python`
- Web build: `npm run build:web`
- E2E: `npm run e2e`

## Rules

- Follow `.agents/docs/currency.md`: use `Decimal`, `ROUND_HALF_EVEN`, and cent
  quantization for money. Never use float for invoice arithmetic.
- Follow `.agents/docs/testing.md`: tests express intent. Write the failing test
  first when fixing behavior.
- Keep one concern per PR. Aim for diffs a reviewer can understand within about
  400 changed lines.
- Use synthetic data only.
