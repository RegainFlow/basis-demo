from decimal import ROUND_HALF_EVEN, Decimal

CENT = Decimal("0.01")


def round_to_cents(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_EVEN)
