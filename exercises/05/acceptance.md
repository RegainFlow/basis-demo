# Acceptance 05: Session Mining

Expected outcome:

- No raw or fake session log is committed to the repository.
- `tools/session-mining/mine_codex_logs.py` reads local Codex history from
  `~/.codex/history.jsonl` by default.
- The output identifies repeated correction-like prompts from the presenter's
  actual logs.
- Mechanical invariants should become Semgrep or CI rules.
- Repeated review workflows should become skills.
- Broad repo conventions should become AGENTS guidance or policy prose.
- One-off preferences should stay in the thread.

Verification:

```bash
python tools/session-mining/mine_codex_logs.py
npm run check
```
