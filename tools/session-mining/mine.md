# Session Mining Workflow

Use `sample-session.log` to identify recurring corrections and decide the right
durable Codex surface.

## Prompt

Read the session log and extract repeated reviewer corrections. For each pattern,
answer:

1. What rule was repeated?
2. Which repo surface should preserve it: AGENTS rule, skill, CI gate, or no
   durable artifact?
3. What exact wording or workflow should be added?

## Triage

- If the correction is a repo-wide convention, update AGENTS guidance.
- If it is a repeated workflow, create or improve a skill.
- If it can be mechanically checked, add a CI or Semgrep rule.
- If it is a one-off preference, leave it in the current thread only.
