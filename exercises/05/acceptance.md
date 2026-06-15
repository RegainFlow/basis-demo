# Acceptance 05: Browser UI Verification

Expected outcome:

- `--total-symbol-color` is restored to the green brand token `#11845b`.
- The Playwright e2e test asserts both the visible total and the rendered dollar
  sign color.
- `exercises/05/artifacts/` mirrors the UI and e2e files used by this lesson.

Verification:

```bash
npm run build:web
npm run e2e
```
