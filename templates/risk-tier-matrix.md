# Risk Tier Matrix

| Tier     | Definition                                          | Examples                     | Required Checks                    |
| -------- | --------------------------------------------------- | ---------------------------- | ---------------------------------- |
| Own      | Local, reversible, low ambiguity                    | Copy edit, isolated UI label | Narrow tests                       |
| Review   | Domain, API, architecture, or visible behavior risk | Money math, endpoint shape   | Package checks and peer review     |
| Delegate | Broad, credentialed, or release-sensitive           | Migration, auth change       | Plan, owner review, staged rollout |
