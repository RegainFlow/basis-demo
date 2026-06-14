---
name: write-tests
description: Add behavior-focused tests that express expected outcomes instead of implementation details.
---

# Write Tests

Use this before implementing behavior in this repo.

## Steps

1. Read `.agents/docs/testing.md`.
2. Choose the smallest user-visible or domain-visible behavior.
3. Assert concrete outputs, not mirrored formulas.
4. Include boundary cases for currency ties, validation, or API shape.
5. Keep decorative weak tests out of mutation evidence.

## Output

Name the behavior covered, why the assertion is meaningful, and the command to
run it.
