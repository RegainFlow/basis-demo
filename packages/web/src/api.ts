import type { InvoiceRequest, InvoiceTotals } from "./types";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function calculateInvoice(
  invoice: InvoiceRequest,
): Promise<InvoiceTotals> {
  const response = await fetch(`${API_BASE_URL}/invoices`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(invoice),
  });

  if (!response.ok) {
    throw new Error(`Invoice calculation failed with ${response.status}`);
  }

  return response.json();
}
