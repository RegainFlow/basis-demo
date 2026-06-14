from invoice_engine.line_items import LineItem, calculate_invoice, calculate_line_item
from invoice_engine.rounding import round_to_cents


def test_decorative_assert_exists() -> None:
    # Decorative weak test: proves a symbol exists but kills no meaningful mutant.
    assert round_to_cents


def test_decorative_assert_truthy() -> None:
    # Decorative weak test: truthiness says nothing about invoice math correctness.
    item = LineItem(description="SaaS", quantity="1", unit_price="1")
    result = calculate_invoice([item])
    assert result


def test_decorative_mirrors_implementation() -> None:
    # Decorative weak test: mirrors the implementation instead of asserting intent.
    item = LineItem(description="SaaS", quantity="2", unit_price="3.00")
    expected = round_to_cents(item.quantity * item.unit_price)
    assert calculate_line_item(item).subtotal == expected
