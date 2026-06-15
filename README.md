# Basis Demo

Teaching monorepo for a live Codex workshop with an accounting-AI audience.

Attendees start from the intentionally under-governed branch:

```bash
git checkout demo-0/bad-state
```

That branch has planted defects and weak verification. Each later demo branch
keeps the previous lesson's fixes and adds the next guardrail.

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

## Demo Branches

| Branch                     | State                                                        |
| -------------------------- | ------------------------------------------------------------ |
| `demo-0/bad-state`         | All planted defects, weak tests, no durable guardrails       |
| `demo-1/currency-fixed`    | Currency bug fixed with exact-cent behavior coverage         |
| `demo-2/tests-fixed`       | Decorative tests replaced with behavior tests                |
| `demo-3/architecture-fixed`| Web/API boundary policy added and violation repaired         |
| `demo-4/semgrep-rule`      | Human float-to-Decimal feedback encoded as a deterministic rule |
| `demo-5/ui-fixed`          | Browser-verified total dollar-sign styling repaired          |
| `demo-6/risk-tier`         | Risk-tier triage skill added                                 |
| `demo-7/flywheel`          | Session mining added as the improvement intake path          |
| `main`                     | Clean final reference state                                  |

## Repo Map

- `packages/invoice-engine`: Invoice math and categorization.
- `packages/api`: FastAPI boundary that computes invoice totals.
- `packages/web`: Vite/React invoice review UI.
- `e2e`: Playwright integration path through web and API.
- `exercises`: Hands-on prompts that follow the branch sequence.
