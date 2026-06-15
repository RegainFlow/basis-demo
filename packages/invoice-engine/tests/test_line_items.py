import pytest
from invoice_engine.categorize import categorize_expense
from invoice_engine.line_items import LineItem, calculate_invoice
from pydantic import ValidationError


@pytest.mark.parametrize(
    ("description", "category"),
    [
        ("audit support retainer", "Professional Services"),
        ("printer paper case", "Office Supplies"),
        ("hotel for client visit", "Travel"),
        ("miscellaneous reimbursement", "Uncategorized"),
    ],
)
def test_categorizes_expenses_from_description(description: str, category: str) -> None:
    assert categorize_expense(description) == category


def test_rejects_float_inputs_for_money_math() -> None:
    with pytest.raises(ValidationError, match="decimal strings"):
        LineItem(description="Coffee meeting", quantity="1", unit_price=4.25)


def test_rejects_empty_invoice() -> None:
    with pytest.raises(ValueError, match="at least one line item"):
        calculate_invoice([])
