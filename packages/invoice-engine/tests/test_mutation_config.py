import tomllib
from pathlib import Path, PurePosixPath


def test_mutmut_copies_selected_tests_into_mutant_workspace() -> None:
    config = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    mutmut = config["tool"]["mutmut"]
    copied_paths = [PurePosixPath(path) for path in mutmut.get("also_copy", [])]
    selected_tests = [
        PurePosixPath(path)
        for path in mutmut["pytest_add_cli_args_test_selection"]
        if path.endswith(".py")
    ]

    missing = [
        str(test_path)
        for test_path in selected_tests
        if not any(
            copied_path == test_path or copied_path in test_path.parents
            for copied_path in copied_paths
        )
    ]

    assert not missing, (
        f"mutmut runs pytest from mutants/, so selected tests must be copied: {missing}"
    )
