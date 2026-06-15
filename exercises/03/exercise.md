# Exercise 03: Add The Architecture Rule

Start from `demo-2/tests-fixed`. The web UI still bypasses the API by using a
local invoice calculator. Add the smallest deterministic rule that catches that
boundary breach, then repair the UI to call `src/api.ts`.

Tasks:

- Make the rule fail before the repair.
- Repair web code so it calls the API instead of local invoice math.
- Run `npm run semgrep` and `npm run build:web`.
