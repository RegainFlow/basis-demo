# Acceptance 01: Currency Bug

Expected outcome:

- Root `AGENTS.md` routes work to package-specific AGENTS files.
- `packages/invoice-engine/AGENTS.md`, `packages/api/AGENTS.md`, and
  `packages/web/AGENTS.md` describe local package rules.
- `.agents/docs/currency.md` and `.agents/skills/review-currency-math/SKILL.md`
  exist before the currency fix.
- The bug is the conversion of invoice arithmetic through `float()` and Python
  `round()`.
- A meaningful test asserts banker’s rounding for an exact cent tie, such as
  `10.005 -> 10.00`.
- `calculate_line_item` uses `round_to_cents(item.quantity * item.unit_price)`.
- Money arithmetic remains Decimal-backed and quantized to cents.

Verification:

```bash
npm run test:python
```
