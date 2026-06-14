from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ENGINE_SRC = Path("packages/invoice-engine/src/invoice_engine")
PYPROJECT = Path("pyproject.toml")


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, text=True)


def changed_engine_files() -> list[str]:
    if os.environ.get("GITHUB_EVENT_NAME") != "pull_request":
        return []

    base_ref = os.environ.get("GITHUB_BASE_REF")
    if not base_ref:
        return []

    diff_command = [
        "git",
        "diff",
        "--name-only",
        f"origin/{base_ref}...HEAD",
        "--",
        str(ENGINE_SRC),
    ]
    diff = subprocess.run(
        diff_command,
        check=True,
        capture_output=True,
        text=True,
    )
    return [
        line.strip().replace("\\", "/")
        for line in diff.stdout.splitlines()
        if line.strip().endswith(".py")
    ]


def with_only_mutate(paths: list[str]) -> str:
    original = PYPROJECT.read_text(encoding="utf-8")
    only_mutate = (
        "only_mutate = [\n"
        + "".join(f"    {json.dumps(path)},\n" for path in paths)
        + "]\n"
    )
    return original.replace("[tool.mutmut]\n", f"[tool.mutmut]\n{only_mutate}", 1)


def assert_clean_mutation_stats() -> None:
    run(["mutmut", "export-cicd-stats"])
    stats_path = Path("mutants/mutmut-cicd-stats.json")
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
    failing = {
        key: stats[key]
        for key in ("survived", "no_tests", "suspicious", "timeout", "segfault")
        if stats.get(key, 0)
    }
    if failing:
        print(f"Mutation gate failed: {failing}", file=sys.stderr)
        run(["mutmut", "results"])
        raise SystemExit(1)


def main() -> None:
    if sys.platform.startswith("win"):
        print("mutmut does not support native Windows; run this check in Linux or WSL.")
        return

    original_pyproject = PYPROJECT.read_text(encoding="utf-8")
    changed_files = changed_engine_files()

    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        if not changed_files:
            print("No changed invoice-engine files; skipping mutation run.")
            return
        PYPROJECT.write_text(with_only_mutate(changed_files), encoding="utf-8")

    try:
        run(["mutmut", "run"])
        assert_clean_mutation_stats()
    finally:
        PYPROJECT.write_text(original_pyproject, encoding="utf-8")


if __name__ == "__main__":
    main()
