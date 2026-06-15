# Session Mining Workflow

Mine local Codex logs for repeated human corrections, then decide which lessons
should become durable repo guidance, skills, or deterministic rules.

This workflow reads logs from the presenter machine at demo time. Do not commit
raw session logs to the repository.

## Run

```bash
python tools/session-mining/mine_codex_logs.py
```

By default the script reads `~/.codex/history.jsonl`, redacts long snippets, and
prints repeated correction-like prompts grouped by normalized wording.

Optional flags:

```bash
python tools/session-mining/mine_codex_logs.py --limit 1000
python tools/session-mining/mine_codex_logs.py --history C:\Users\you\.codex\history.jsonl
python tools/session-mining/mine_codex_logs.py --min-count 2
```

## Triage

- Repo-wide convention: update AGENTS guidance or policy prose.
- Repeated workflow: create or improve a skill.
- Mechanically checkable invariant: add CI or Semgrep.
- One-off preference: leave it in the thread.
