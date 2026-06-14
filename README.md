# Basis Demo

Teaching monorepo for a live Codex workshop with an accounting-AI audience. The
repo starts clean on `main`: no planted bugs, no architecture violations, and no
intentional UI regressions.

## Quickstart

Prerequisites: Python 3.12, `uv`, Node 20, and npm.

```bash
uv sync --all-packages --group dev
npm install
npm --workspace e2e exec -- playwright install chromium
npm run check
```

Run the app locally:

```bash
npm run dev:api
npm run dev:web
```

Then open `http://127.0.0.1:5173`.

Useful checks:

```bash
npm run format:python
npm run lint:python
npm run semgrep
npm run architecture
npm run test:python
npm run build:web
npm run e2e
```

Mutation testing uses `mutmut`, which runs in Linux or WSL. The GitHub merge
gate runs it on Ubuntu.

## Workshop Run-Of-Show

This curriculum assumes 120 minutes.

| Time    | Segment                                  | Repo surface                                             |
| ------- | ---------------------------------------- | -------------------------------------------------------- |
| 0-10    | Clean repo tour and rules of engagement  | `README.md`, `PLAN.md`, `.agents/`                       |
| 10-25   | Money math and tests-as-intent           | `packages/invoice-engine/`                               |
| 25-40   | API contract and architecture boundary   | `packages/api/`, `importlinter.cfg`                      |
| 40-55   | Review UI and e2e confidence             | `packages/web/`, `e2e/`                                  |
| 55-70   | Static policy gates                      | `.semgrep/rules.yml`, `.github/workflows/merge-gate.yml` |
| 70-90   | Codex review routing and skills          | `AGENTS.md`, `.agents/skills/`                           |
| 90-105  | Session mining and recurring corrections | `tools/session-mining/`                                  |
| 105-120 | Take-home exercises and Q&A              | `exercises/`, `templates/`                               |

Codex code review is configured through the native GitHub integration in Codex
settings. Use `@codex review` on a pull request after the repository is connected
to Codex cloud; the workflow gate stays secret-free and deterministic.

## Demo Tag Map

These are placeholders for later workshop checkpoints. Do not create the bug tags
on clean `main`.

| Tag                             | Meaning                                       |
| ------------------------------- | --------------------------------------------- |
| `demo/0-clean`                  | Green main scaffold                           |
| `demo/1-weak-tests`             | Decorative tests fail to catch a regression   |
| `demo/2-currency-bug`           | Float or half-up rounding regression          |
| `demo/3-architecture-violation` | Web reaches around the API boundary           |
| `demo/4-api-drift`              | API payload no longer matches UI expectations |
| `demo/5-ui-bug`                 | Total dollar-sign color is no longer green    |

## Repo Map

- `packages/invoice-engine`: Decimal-safe invoice math and categorization.
- `packages/api`: FastAPI boundary that computes invoice totals.
- `packages/web`: Vite/React invoice review UI.
- `e2e`: Playwright integration path through web and API.
- `.agents`: Codex guidance, policy prose, and workshop skills.
- `templates`: Portable gate and skill kit for attendees.
- `tools/session-mining`: Synthetic session log and mining workflow.
