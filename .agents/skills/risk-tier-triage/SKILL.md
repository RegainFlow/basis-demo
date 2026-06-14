---
name: risk-tier-triage
description: Given a diff, propose Own, Review, or Delegate tier with concise reasoning.
---

# Risk Tier Triage

Classify a proposed change before implementation or review.

## Tiers

- Own: local, reversible, well-tested, no money or contract risk.
- Review: touches money, API shape, architecture, CI, or user-visible totals.
- Delegate: broad refactor, unclear requirements, external credentials, or
  release coordination.

## Steps

1. Identify changed surfaces.
2. Map risks to the tier definitions.
3. Name the required verification commands.
4. Recommend the smallest safe PR boundary.

## Output

Return one tier, the reason, and the required checks.
