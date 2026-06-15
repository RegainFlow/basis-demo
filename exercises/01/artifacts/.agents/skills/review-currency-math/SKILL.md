---
name: review-currency-math
description: Review invoice math changes with a tech-lead focus on Decimal safety, cent rounding, and accounting intent.
---

# Review Currency Math

Use a direct tech-lead voice. Treat money correctness as production risk.

## Steps

1. Read `.agents/docs/currency.md` and the changed invoice-engine files.
2. Trace every arithmetic input from API or tests into `Decimal`.
3. Confirm rounding uses `ROUND_HALF_EVEN` and cent quantization.
4. Check tests for exact expected cents, including tie cases.
5. Call out float conversion, mirrored tests, and unrounded totals as findings.

## Output

Lead with findings by severity. If no issue is found, say that and name the
tests or commands that reduce remaining risk.
