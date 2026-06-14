# Currency Policy

Invoice arithmetic must use `Decimal`, not `float`.

Round money with `ROUND_HALF_EVEN` and quantize final display amounts to cents.
Line subtotals and line tax are rounded before invoice totals are summed.

JSON payloads carry money, quantity, and tax rates as decimal strings. Reject
JSON float values instead of silently converting them.
