# Basis Demo Scaffold Plan

## Summary

Build a small Python + TypeScript teaching monorepo from an empty `main`, using
`uv` for Python and npm workspaces for TypeScript. Commit this plan first, then
scaffold the repo and commit once all checks pass.

Important scope decisions:

- Omit the reporting/automation area from this scaffold.
- Teach Codex review as native GitHub code review integration outside CI, not as
  a `codex-action` workflow job.
- CI uses four staged jobs: `format-static`, `architecture`, `tests-mutation`,
  and `e2e`.

## Key Implementation Choices

- Use a root `uv` workspace with Python 3.12 packages for `invoice-engine` and
  `api`, plus npm workspaces on Node 20 for `packages/web` and e2e tooling.
- Commit `uv.lock` and `package-lock.json`.
- `invoice-engine` uses Pydantic models, `Decimal`, `ROUND_HALF_EVEN`, and
  per-line rounding before summing invoice totals.
- JSON money, tax, and quantity fields are decimal strings. Validate nonempty
  descriptions, `quantity > 0`, `unit_price >= 0`, and `0 <= tax_rate <= 1`.
- Category rules use description keywords and the taxonomy: Software, Meals,
  Travel, Office Supplies, Professional Services, and Uncategorized.
- API exposes `GET /healthz` and `POST /invoices`; web calls it via
  `VITE_API_BASE_URL` with a localhost default.
- Web UI supports JSON upload, editable/add/remove line rows, submit-to-API
  totals, and a green `$` styled by one CSS custom property.
- Add root `AGENTS.md` as a discovery pointer, full `.agents/AGENTS.md`,
  package-level `AGENTS.md` files, `.agents/docs/`, and runnable-style skill
  `SKILL.md` workflows.
- `templates/` contains full generic portable versions of the gate, import
  rules, Semgrep rules, skills, and rollout/risk docs.
- `tools/session-mining/` contains a short synthetic repeated float-to-Decimal
  correction log and mining workflow.
- `exercises/` contains five concise numbered take-home stubs.
- README is a 120-minute curriculum with quickstart, run-of-show, native Codex
  review setup notes, and placeholder tag map `demo/0-clean` through
  `demo/5-ui-bug`.

## Gate And Checks

- `format-static`: `ruff format --check`, `ruff check`, and Semgrep rules for
  web-boundary violations plus no `eval`/`exec`.
- `architecture`: `lint-imports` checks Python layering for
  `api -> invoice_engine`; TypeScript web-to-engine boundaries are enforced by
  Semgrep.
- `tests-mutation`: run all pytest tests, then mutmut. On `main`, mutate all
  real `invoice_engine` code; on PRs, scope to changed invoice-engine files and
  skip cleanly if none changed. Mutmut runner uses real behavior tests only, not
  decorative weak tests.
- `e2e`: run FastAPI and Vite, upload JSON, edit one row, submit, assert
  displayed total, and always save/upload a final screenshot artifact.
- After each package implementation, run the relevant package checks before
  moving on.

## Tests

- `test_line_items.py` contains real behavior tests with exact cent totals,
  including a banker's rounding case such as `10.005` that only passes with
  `ROUND_HALF_EVEN`.
- `test_weak.py` contains exactly three clearly commented decorative tests:
  assert-exists, assert-truthy, and mirrors-implementation. They pass under
  pytest and are excluded from mutmut credit.
- API gets a minimal FastAPI TestClient test for `POST /invoices`.
- Web gets TypeScript build coverage through npm scripts and integration
  coverage through Playwright.
- Full final verification: root lint/static, architecture, pytest, mutmut, web
  build, and e2e.

## Assumptions

- No real customer, vendor, or financial data is used; all invoices and sessions
  are synthetic.
- No actual demo tags are created during scaffold; README lists placeholders
  only.
- The final Git history should be two commits: initial `PLAN.md`, then the green
  scaffold.
- Git commands should use a per-command `safe.directory` override because the
  repo has sandbox ownership warnings.
