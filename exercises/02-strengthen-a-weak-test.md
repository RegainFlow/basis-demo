# Exercise 02: Replace Decorative Tests

Start from `demo-1/currency-fixed`. Review
`packages/invoice-engine/tests/test_weak.py` and replace the teaching-only weak
tests with behavior coverage.

Acceptance:

- The new tests assert concrete expected values.
- No test mirrors the implementation formula.
- `npm run test:python` passes.
