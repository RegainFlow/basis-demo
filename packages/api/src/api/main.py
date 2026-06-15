from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from invoice_engine import LineItem, calculate_invoice
from pydantic import BaseModel, Field

from api.storage import save_invoice_submission

app = FastAPI(title="Basis Demo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class InvoiceRequest(BaseModel):
    line_items: list[LineItem] = Field(min_length=1)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/invoices")
def create_invoice(invoice: InvoiceRequest) -> dict[str, Any]:
    totals = calculate_invoice(invoice.line_items)
    request_payload = invoice.model_dump(mode="json")
    totals_payload = totals.model_dump(mode="json")
    invoice_id = save_invoice_submission(request_payload, totals_payload)
    return {"invoice_id": invoice_id, **totals_payload}
