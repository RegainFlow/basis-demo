import json
import sqlite3

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


def test_post_invoices_persists_submission_and_totals(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "invoices.sqlite3"
    monkeypatch.setenv("BASIS_DB_PATH", str(db_path))

    response = client.post(
        "/invoices",
        json={
            "line_items": [
                {
                    "description": "Audit support retainer",
                    "quantity": "2",
                    "unit_price": "75.00",
                    "tax_rate": "0.0825",
                }
            ]
        },
    )

    assert response.status_code == 200
    assert response.json()["invoice_id"] == 1

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute(
            "select id, request_json, totals_json from invoices"
        ).fetchall()

    assert len(rows) == 1
    row_id, request_json, totals_json = rows[0]
    assert row_id == 1
    assert json.loads(request_json)["line_items"][0]["description"] == (
        "Audit support retainer"
    )
    assert json.loads(totals_json)["total"] == "162.38"


def test_rejects_json_number_money_fields(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "invoices.sqlite3"
    monkeypatch.setenv("BASIS_DB_PATH", str(db_path))

    response = client.post(
        "/invoices",
        json={
            "line_items": [
                {
                    "description": "Coffee meeting",
                    "quantity": "1",
                    "unit_price": 4.25,
                    "tax_rate": "0",
                }
            ]
        },
    )

    assert response.status_code == 422
    assert not db_path.exists()
