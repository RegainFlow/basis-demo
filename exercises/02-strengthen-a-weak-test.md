# Exercise 02: Strengthen A Weak Test

Choose one decorative test in `packages/invoice-engine/tests/test_weak.py` and
rewrite it as a real behavior test in `test_line_items.py`.

Acceptance:

- The new test asserts a specific expected value.
- The decorative file still contains exactly three weak tests on clean main.
- Pytest passes.
