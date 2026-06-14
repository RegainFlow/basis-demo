---
name: review-currency-math
description: Review money math for decimal safety, cent rounding, and intent tests.
---

# Review Currency Math

1. Trace every arithmetic input into the domain layer.
2. Reject float, binary rounding, or unquantized money.
3. Confirm exact-cent tests cover tie cases.
4. Report findings first, with file and line references.
