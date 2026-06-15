from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def main() -> None:
    config_path = Path(".semgrep/rules.yml")
    if not config_path.exists() or re.fullmatch(
        r"\s*rules:\s*\[\]\s*", config_path.read_text(encoding="utf-8")
    ):
        print("Semgrep is skipped because no rules are configured yet.")
        return

    if sys.platform.startswith("win"):
        print("Semgrep is skipped on native Windows; CI runs it on Ubuntu.")
        return

    subprocess.run(
        [
            "semgrep",
            "--config",
            ".semgrep/rules.yml",
            "--error",
            "--metrics=off",
            "--disable-version-check",
            "packages",
            "e2e",
            "tools",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
