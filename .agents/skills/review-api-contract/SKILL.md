---
name: review-api-contract
description: Review FastAPI request and response changes for invoice contract drift.
---

# Review API Contract

Use this when a diff touches `packages/api` or web API calls.

## Steps

1. Read `packages/api/AGENTS.md`.
2. Compare request fields, response fields, and JSON value types.
3. Confirm money values remain decimal strings.
4. Verify API tests and e2e coverage still assert visible totals.
5. Flag duplicated engine math or undocumented response drift.

## Output

List contract risks first, then missing tests, then any safe refactor notes.
