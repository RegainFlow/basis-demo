import tomllib
from pathlib import Path, PurePosixPath

from mutmut.utils.format_utils import get_mutant_name

MUTMUT_CONFIG = Path("packages/invoice-engine/pyproject.toml")


def test_mutmut_source_paths_match_imported_module_names() -> None:
    config = tomllib.loads(MUTMUT_CONFIG.read_text(encoding="utf-8"))
    mutmut = config["tool"]["mutmut"]
    source_path = PurePosixPath(mutmut["source_paths"][0])
    source_file = source_path / "invoice_engine" / "line_items.py"

    mutant_name = get_mutant_name(Path(source_file), "x_calculate_invoice")

    assert mutant_name == "invoice_engine.line_items.x_calculate_invoice"


def test_mutmut_copies_selected_tests_into_mutant_workspace() -> None:
    config = tomllib.loads(MUTMUT_CONFIG.read_text(encoding="utf-8"))
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
