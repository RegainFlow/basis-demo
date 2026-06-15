from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CORRECTION_HINTS = (
    "actually",
    "also",
    "before",
    "dont",
    "don't",
    "instead",
    "make sure",
    "never",
    "not",
    "rather",
    "should",
    "shouldnt",
    "shouldn't",
    "we need",
)


@dataclass(frozen=True)
class Prompt:
    session_id: str
    text: str


def default_history_path() -> Path:
    return Path.home() / ".codex" / "history.jsonl"


def normalize(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"`[^`]+`", "<code>", lowered)
    lowered = re.sub(r"\b\d+\b", "<num>", lowered)
    lowered = re.sub(r"[^a-z0-9<>']+", " ", lowered)
    words = lowered.split()
    return " ".join(words[:28])


def read_prompts(path: Path, limit: int) -> list[Prompt]:
    if not path.exists():
        raise FileNotFoundError(f"Codex history file not found: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()
    selected = lines[-limit:] if limit > 0 else lines
    prompts: list[Prompt] = []

    for line in selected:
        try:
            row: dict[str, Any] = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = str(row.get("text", "")).strip()
        if not text:
            continue
        prompts.append(Prompt(session_id=str(row.get("session_id", "")), text=text))

    return prompts


def looks_like_correction(text: str) -> bool:
    lowered = text.lower()
    return any(hint in lowered for hint in CORRECTION_HINTS)


def artifact_hint(text: str) -> str:
    lowered = text.lower()
    if "semgrep" in lowered or "rule" in lowered or "never" in lowered:
        return "CI/Semgrep rule"
    if "agents.md" in lowered or "policy" in lowered or "make sure" in lowered:
        return "AGENTS guidance"
    if "skill" in lowered or "workflow" in lowered:
        return "skill"
    return "review manually"


def snippet(text: str) -> str:
    collapsed = re.sub(r"\s+", " ", text).strip()
    return collapsed[:220] + ("..." if len(collapsed) > 220 else "")


def safe_print(value: str = "") -> None:
    print(value.encode("ascii", errors="backslashreplace").decode("ascii"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Mine local Codex history logs.")
    parser.add_argument("--history", type=Path, default=default_history_path())
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--min-count", type=int, default=2)
    args = parser.parse_args()

    prompts = [
        prompt
        for prompt in read_prompts(args.history, args.limit)
        if looks_like_correction(prompt.text)
    ]
    groups: dict[str, list[Prompt]] = defaultdict(list)
    for prompt in prompts:
        groups[normalize(prompt.text)].append(prompt)

    repeated = {
        key: values
        for key, values in groups.items()
        if len({value.session_id for value in values}) >= args.min_count
        or len(values) >= args.min_count
    }

    safe_print(f"History: {args.history}")
    safe_print(f"Correction-like prompts scanned: {len(prompts)}")
    safe_print(f"Repeated candidates: {len(repeated)}")
    safe_print()

    if not repeated:
        safe_print(
            "No repeated correction candidates found. "
            "Lower --min-count or increase --limit."
        )
        return 0

    counts = Counter({key: len(values) for key, values in repeated.items()})
    for index, (key, count) in enumerate(counts.most_common(8), start=1):
        values = repeated[key]
        safe_print(
            f"{index}. {artifact_hint(values[-1].text)} candidate ({count} hits)"
        )
        safe_print(f"   Pattern: {key}")
        safe_print(f"   Latest: {snippet(values[-1].text)}")
        safe_print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
