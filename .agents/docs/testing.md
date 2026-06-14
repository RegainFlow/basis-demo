# Testing Policy

Tests are executable intent, not decoration.

For behavior changes:

1. Write or update a focused test with specific expected values.
2. See it fail for the intended reason.
3. Implement the smallest clear fix.
4. Run the narrow package check, then the root gate.

Weak tests may exist only when clearly labeled as teaching examples. They must
not be counted as mutation-testing evidence.
