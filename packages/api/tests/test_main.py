import pytest
from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_healthz() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_invoices_returns_decimal_string_totals() -> None:
    response = client.post(
        "/invoices",
        json={
            "line_items": [
                {
                    "description": "SaaS platform license",
                    "quantity": "1",
                    "unit_price": "10.005",
                    "tax_rate": "0",
                }
            ]
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["subtotal"] == "10.00"
    assert body["tax"] == "0.00"
    assert body["total"] == "10.00"
    assert body["line_items"][0]["category"] == "Software"


@pytest.mark.parametrize("unit_price", [4.25, 4])
def test_rejects_json_number_money_fields(unit_price: float | int) -> None:
    response = client.post(
        "/invoices",
        json={
            "line_items": [
                {
                    "description": "Coffee meeting",
                    "quantity": "1",
                    "unit_price": unit_price,
                    "tax_rate": "0",
                }
            ]
        },
    )

    assert response.status_code == 422
