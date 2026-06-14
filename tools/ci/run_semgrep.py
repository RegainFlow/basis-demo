from __future__ import annotations

import subprocess
import sys


def main() -> None:
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
