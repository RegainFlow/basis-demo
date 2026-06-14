---
name: repro-test
description: Turn a reported bug into a small failing test before changing implementation.
---

# Repro Test

Use this when a behavior report is vague or a fix lacks a failing test.

## Steps

1. Restate the expected behavior in one sentence.
2. Add the smallest test that fails for the reported reason.
3. Run only that test and capture the failure.
4. Implement the fix after the failure is proven.
5. Rerun the narrow test and the relevant package suite.

## Output

Report the failing test name, the original failure, the fix, and the passing
verification command.
