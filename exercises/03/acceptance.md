# Acceptance 03: Architecture Rule

Expected outcome:

- `.semgrep/rules.yml` contains `basis.web-no-direct-invoice-engine-import`.
- Web code imports `calculateInvoice` from `./api`, not a local engine shim.
- `packages/web/src/invoice_engine.ts` is removed.
- The architecture policy says web submits invoice payloads over HTTP to the
  API, and the API calls `invoice_engine`.
- `exercises/03/artifacts/` mirrors the architecture policy and Semgrep rule
  added by this lesson.

Verification:

```bash
npm run semgrep
npm run build:web
```
