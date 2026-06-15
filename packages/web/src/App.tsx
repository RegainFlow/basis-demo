import { Calculator, FileUp, Plus, RotateCcw, Trash2 } from "lucide-react";
import { ChangeEvent, useMemo, useRef, useState } from "react";

import { calculateInvoice } from "./api";
import { sampleInvoice } from "./sampleInvoice";
import type { DraftLineItem, InvoiceRequest, InvoiceTotals } from "./types";

function newLineItem(): DraftLineItem {
  return {
    id: crypto.randomUUID(),
    description: "",
    quantity: "1",
    unit_price: "0.00",
    tax_rate: "0",
  };
}

function withIds(invoice: InvoiceRequest): DraftLineItem[] {
  return invoice.line_items.map((item) => ({
    id: crypto.randomUUID(),
    ...item,
  }));
}

function toRequest(lineItems: DraftLineItem[]): InvoiceRequest {
  return {
    line_items: lineItems.map(({ id: _id, ...item }) => item),
  };
}

export default function App() {
  const [lineItems, setLineItems] = useState<DraftLineItem[]>(
    withIds(sampleInvoice)
  );
  const [totals, setTotals] = useState<InvoiceTotals | null>(null);
  const [status, setStatus] = useState("Ready");
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const canRemove = lineItems.length > 1;
  const requestPayload = useMemo(() => toRequest(lineItems), [lineItems]);

  function updateLine(
    id: string,
    field: keyof Omit<DraftLineItem, "id">,
    value: string
  ) {
    setLineItems((current) =>
      current.map((item) =>
        item.id === id ? { ...item, [field]: value } : item
      )
    );
  }

  function addLine() {
    setLineItems((current) => [...current, newLineItem()]);
    setTotals(null);
  }

  function removeLine(id: string) {
    setLineItems((current) =>
      current.length === 1 ? current : current.filter((item) => item.id !== id)
    );
    setTotals(null);
  }

  function resetSample() {
    setLineItems(withIds(sampleInvoice));
    setTotals(null);
    setError(null);
    setStatus("Ready");
  }

  async function handleUpload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    try {
      const parsed = JSON.parse(await file.text()) as InvoiceRequest;
      if (!Array.isArray(parsed.line_items) || parsed.line_items.length === 0) {
        throw new Error("Missing line_items");
      }
      setLineItems(withIds(parsed));
      setTotals(null);
      setError(null);
      setStatus(`Loaded ${file.name}`);
    } catch {
      setError("Upload must be an invoice JSON file with line_items.");
    } finally {
      event.target.value = "";
    }
  }

  async function submitInvoice() {
    setStatus("Calculating");
    setError(null);

    try {
      const response = await calculateInvoice(requestPayload);
      setTotals(response);
      setStatus(`Calculated #${response.invoice_id}`);
    } catch (caught) {
      const message =
        caught instanceof Error ? caught.message : "Invoice calculation failed";
      setError(message);
      setStatus("Needs review");
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Basis Demo</p>
          <h1>Invoice Review</h1>
        </div>
        <div className="toolbar" aria-label="Invoice actions">
          <input
            ref={fileInputRef}
            className="file-input"
            type="file"
            accept="application/json,.json"
            onChange={handleUpload}
            data-testid="invoice-upload"
          />
          <button
            type="button"
            className="icon-button"
            title="Upload invoice JSON"
            aria-label="Upload invoice JSON"
            onClick={() => fileInputRef.current?.click()}
          >
            <FileUp size={18} />
          </button>
          <button
            type="button"
            className="icon-button"
            title="Reset sample invoice"
            aria-label="Reset sample invoice"
            onClick={resetSample}
          >
            <RotateCcw size={18} />
          </button>
          <button
            type="button"
            className="primary-button"
            onClick={submitInvoice}
            data-testid="calculate-invoice"
          >
            <Calculator size={18} />
            Calculate
          </button>
        </div>
      </header>

      <section className="workbench" aria-label="Invoice line items">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Description</th>
                <th>Quantity</th>
                <th>Unit price</th>
                <th>Tax rate</th>
                <th aria-label="Actions" />
              </tr>
            </thead>
            <tbody>
              {lineItems.map((item, index) => (
                <tr key={item.id}>
                  <td>
                    <input
                      aria-label={`Line ${index + 1} description`}
                      value={item.description}
                      onChange={(event) =>
                        updateLine(item.id, "description", event.target.value)
                      }
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`Line ${index + 1} quantity`}
                      value={item.quantity}
                      onChange={(event) =>
                        updateLine(item.id, "quantity", event.target.value)
                      }
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`Line ${index + 1} unit price`}
                      value={item.unit_price}
                      onChange={(event) =>
                        updateLine(item.id, "unit_price", event.target.value)
                      }
                    />
                  </td>
                  <td>
                    <input
                      aria-label={`Line ${index + 1} tax rate`}
                      value={item.tax_rate}
                      onChange={(event) =>
                        updateLine(item.id, "tax_rate", event.target.value)
                      }
                    />
                  </td>
                  <td className="row-actions">
                    <button
                      type="button"
                      className="icon-button"
                      title="Remove line"
                      aria-label={`Remove line ${index + 1}`}
                      disabled={!canRemove}
                      onClick={() => removeLine(item.id)}
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <button type="button" className="secondary-button" onClick={addLine}>
          <Plus size={18} />
          Add line
        </button>
      </section>

      <section className="summary-band" aria-label="Invoice totals">
        <div>
          <p className="label">Status</p>
          <strong>{status}</strong>
        </div>
        <div>
          <p className="label">Subtotal</p>
          <strong>{totals ? totals.subtotal : "--"}</strong>
        </div>
        <div>
          <p className="label">Tax</p>
          <strong>{totals ? totals.tax : "--"}</strong>
        </div>
        <div className="grand-total" data-testid="invoice-total">
          <p className="label">Total</p>
          <strong>
            <span className="money-symbol">$</span>
            {totals ? totals.total : "--"}
          </strong>
        </div>
      </section>

      {error ? (
        <p className="error" role="alert">
          {error}
        </p>
      ) : null}
    </main>
  );
}
