# Acceptance 04: Human Feedback Rule

Expected outcome:

- `.semgrep/rules.yml` keeps the web-boundary rule and adds currency rules for
  `float(...)` and `round(...)` in `packages/invoice-engine/src/**`.
- The repeated human feedback is encoded as deterministic CI policy instead of
  relying on memory.
- `exercises/04/artifacts/` mirrors the Semgrep rule file after this lesson.

Verification:

```bash
npm run semgrep
npm run check
```
