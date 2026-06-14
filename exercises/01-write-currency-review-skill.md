# Exercise 01: Write A Currency Review Skill

Create a skill that reviews money math changes. It should trigger on invoice
engine diffs, inspect rounding policy, and output findings first.

Acceptance:

- Mentions Decimal and `ROUND_HALF_EVEN`.
- Requires exact expected-cent tests.
- Separates findings from summary.
