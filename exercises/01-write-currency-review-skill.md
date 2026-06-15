# Exercise 01: Catch The Currency Bug

Start from `demo-0/bad-state`. Find why the invoice tests are green even though
line subtotal rounding is wrong.

Acceptance:

- Identify the float or Python rounding path.
- Add one exact-cent behavior test that fails before the fix.
- Fix the implementation with `Decimal`, cent quantization, and
  `ROUND_HALF_EVEN`.
