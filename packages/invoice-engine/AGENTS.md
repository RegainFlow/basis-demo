# Invoice Engine Context

This package owns invoice arithmetic and categorization.

- Use `Decimal` for quantity, unit price, tax rate, subtotal, tax, and total.
- Round line subtotal and line tax to cents with `ROUND_HALF_EVEN`.
- Keep models independent of FastAPI and web code.
- Add exact-cent tests for every money behavior change.
- Decorative weak tests belong only in `tests/test_weak.py`.
