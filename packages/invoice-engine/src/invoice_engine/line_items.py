from decimal import Decimal, InvalidOperation
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from invoice_engine.categorize import ExpenseCategory, categorize_expense
from invoice_engine.rounding import round_to_cents


def _parse_decimal(value: Any) -> Decimal:
    if isinstance(value, float):
        raise ValueError("Use decimal strings, not floats, for invoice arithmetic.")
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid decimal value: {value!r}") from exc


class LineItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    description: str = Field(min_length=1)
    quantity: Decimal = Field(gt=Decimal("0"))
    unit_price: Decimal = Field(ge=Decimal("0"))
    tax_rate: Decimal = Field(default=Decimal("0"), ge=Decimal("0"), le=Decimal("1"))
    discount_rate: Decimal = Field(
        default=Decimal("0"),
        ge=Decimal("0"),
        le=Decimal("1"),
    )

    @field_validator("description", mode="before")
    @classmethod
    def _strip_description(cls, value: Any) -> str:
        description = str(value).strip()
        if not description:
            raise ValueError("description is required")
        return description

    @field_validator(
        "quantity",
        "unit_price",
        "tax_rate",
        "discount_rate",
        mode="before",
    )
    @classmethod
    def _parse_decimal_fields(cls, value: Any) -> Decimal:
        return _parse_decimal(value)


class CalculatedLineItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    description: str
    category: ExpenseCategory
    quantity: Decimal
    unit_price: Decimal
    tax_rate: Decimal
    discount_rate: Decimal
    subtotal: Decimal
    tax: Decimal
    total: Decimal


class InvoiceTotals(BaseModel):
    model_config = ConfigDict(frozen=True)

    line_items: tuple[CalculatedLineItem, ...]
    subtotal: Decimal
    tax: Decimal
    total: Decimal


def calculate_line_item(item: LineItem) -> CalculatedLineItem:
    gross_subtotal = item.quantity * item.unit_price
    discounted_subtotal = gross_subtotal * (Decimal("1") - item.discount_rate)
    subtotal = Decimal(str(round(float(discounted_subtotal), 2)))
    tax = round_to_cents(subtotal * item.tax_rate)
    total = subtotal + tax

    return CalculatedLineItem(
        description=item.description,
        category=categorize_expense(item.description),
        quantity=item.quantity,
        unit_price=item.unit_price,
        tax_rate=item.tax_rate,
        discount_rate=item.discount_rate,
        subtotal=subtotal,
        tax=tax,
        total=total,
    )


def calculate_invoice(line_items: list[LineItem]) -> InvoiceTotals:
    if not line_items:
        raise ValueError("invoice requires at least one line item")

    calculated = tuple(calculate_line_item(item) for item in line_items)
    subtotal = sum((line.subtotal for line in calculated), Decimal("0.00"))
    tax = sum((line.tax for line in calculated), Decimal("0.00"))

    return InvoiceTotals(
        line_items=calculated,
        subtotal=round_to_cents(subtotal),
        tax=round_to_cents(tax),
        total=round_to_cents(subtotal + tax),
    )
