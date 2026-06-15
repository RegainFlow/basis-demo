from decimal import Decimal

import pytest
from invoice_engine.categorize import categorize_expense
from invoice_engine.line_items import LineItem, calculate_invoice, calculate_line_item
from pydantic import ValidationError


def test_bankers_rounding_ties_to_even_cent() -> None:
    item = LineItem(description="SaaS subscription", quantity="1", unit_price="10.005")

    result = calculate_line_item(item)

    assert result.subtotal == Decimal("10.00")
    assert result.tax == Decimal("0.00")
    assert result.total == Decimal("10.00")


def test_invoice_totals_round_each_line_before_summing() -> None:
    items = [
        LineItem(
            description="SaaS platform license",
            quantity="2",
            unit_price="19.995",
            tax_rate="0.0825",
        ),
        LineItem(
            description="Team lunch",
            quantity="3",
            unit_price="8.335",
            tax_rate="0",
        ),
    ]

    result = calculate_invoice(items)

    assert result.subtotal == Decimal("64.99")
    assert result.tax == Decimal("3.30")
    assert result.total == Decimal("68.29")
    assert [line.category for line in result.line_items] == ["Software", "Meals"]


def test_line_total_uses_rounded_subtotal_and_tax() -> None:
    item = LineItem(
        description="Audit support retainer",
        quantity="2",
        unit_price="75.005",
        tax_rate="0.0825",
    )

    result = calculate_line_item(item)

    assert result.subtotal == Decimal("150.01")
    assert result.tax == Decimal("12.38")
    assert result.total == Decimal("162.39")


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
