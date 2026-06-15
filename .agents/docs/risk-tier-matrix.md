# Risk Tier Matrix

Use blast radius, reversibility, and verifiability to decide how much human
ownership a change needs.

| Tier | Meaning | Examples | Required checks |
| ---- | ------- | -------- | --------------- |
| Own | Local, reversible, highly verifiable | Copy edit, isolated UI label | Narrow checks |
| Review | Domain, API, architecture, or visible behavior risk | Money math, endpoint shape | Package checks and reviewer |
| Delegate | Broad, release-sensitive, or hard to prove mechanically | Migration, auth, dependency bump | Plan, owner review, staged rollout |

Currency math is review-mandatory in this repo because wrong cents are a
business correctness failure.
