# Acceptance 02: Test Quality

Expected outcome:

- `packages/invoice-engine/tests/test_weak.py` is removed.
- Replacement tests assert domain behavior with concrete expected cents.
- No test computes expected values by calling the same helper or formula being
  tested.
- The suite still covers rounding ties, per-line total behavior, categorization,
  float rejection, and empty invoices.

Verification:

```bash
npm run test:python
```
