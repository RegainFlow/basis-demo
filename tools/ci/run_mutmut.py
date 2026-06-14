from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ENGINE_PACKAGE = Path("packages/invoice-engine")
ENGINE_SRC = ENGINE_PACKAGE / "src" / "invoice_engine"
PYPROJECT = ENGINE_PACKAGE / "pyproject.toml"


def run(
    command: list[str],
    *,
    check: bool = True,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=check, cwd=cwd, text=True)


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
        ENGINE_SRC.as_posix(),
    ]
    diff = subprocess.run(
        diff_command,
        check=True,
        capture_output=True,
        text=True,
    )
    changed_files = []
    for line in diff.stdout.splitlines():
        path = Path(line.strip().replace("\\", "/"))
        if path.suffix != ".py":
            continue
        changed_files.append(path.relative_to(ENGINE_PACKAGE).as_posix())
    return changed_files


def with_only_mutate(paths: list[str]) -> str:
    original = PYPROJECT.read_text(encoding="utf-8")
    only_mutate = (
        "only_mutate = [\n"
        + "".join(f"    {json.dumps(path)},\n" for path in paths)
        + "]\n"
    )
    return original.replace("[tool.mutmut]\n", f"[tool.mutmut]\n{only_mutate}", 1)


def assert_clean_mutation_stats() -> None:
    run(["mutmut", "export-cicd-stats"], cwd=ENGINE_PACKAGE)
    stats_path = ENGINE_PACKAGE / "mutants/mutmut-cicd-stats.json"
    stats = json.loads(stats_path.read_text(encoding="utf-8"))
    failing = {
        key: stats[key]
        for key in ("survived", "no_tests", "suspicious", "timeout", "segfault")
        if stats.get(key, 0)
    }
    if failing:
        print(f"Mutation gate failed: {failing}", file=sys.stderr)
        run(["mutmut", "results"], cwd=ENGINE_PACKAGE)
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
        run(["mutmut", "run"], cwd=ENGINE_PACKAGE)
        assert_clean_mutation_stats()
    finally:
        PYPROJECT.write_text(original_pyproject, encoding="utf-8")


if __name__ == "__main__":
    main()
