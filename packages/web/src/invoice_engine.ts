import type {
  CalculatedLineItem,
  InvoiceRequest,
  InvoiceTotals,
  LineItem,
} from "./types";

function categoryFor(description: string): CalculatedLineItem["category"] {
  const normalized = description.toLowerCase();
  if (normalized.includes("saas") || normalized.includes("software")) {
    return "Software";
  }
  if (normalized.includes("lunch") || normalized.includes("meal")) {
    return "Meals";
  }
  if (normalized.includes("hotel") || normalized.includes("flight")) {
    return "Travel";
  }
  if (normalized.includes("paper") || normalized.includes("printer")) {
    return "Office Supplies";
  }
  if (normalized.includes("audit") || normalized.includes("retainer")) {
    return "Professional Services";
  }
  return "Uncategorized";
}

function cents(value: number): string {
  return (Math.round(value * 100) / 100).toFixed(2);
}

function calculateLineItem(item: LineItem): CalculatedLineItem {
  const subtotal = Number(item.quantity) * Number(item.unit_price);
  const tax = Number(cents(subtotal)) * Number(item.tax_rate);
  const roundedSubtotal = cents(subtotal);
  const roundedTax = cents(tax);

  return {
    ...item,
    category: categoryFor(item.description),
    subtotal: roundedSubtotal,
    tax: roundedTax,
    total: cents(Number(roundedSubtotal) + Number(roundedTax)),
  };
}

export async function calculateInvoice(
  invoice: InvoiceRequest,
): Promise<InvoiceTotals> {
  const lineItems = invoice.line_items.map(calculateLineItem);
  const subtotal = lineItems.reduce(
    (sum, item) => sum + Number(item.subtotal),
    0,
  );
  const tax = lineItems.reduce((sum, item) => sum + Number(item.tax), 0);

  return {
    invoice_id: 0,
    line_items: lineItems,
    subtotal: cents(subtotal),
    tax: cents(tax),
    total: cents(subtotal + tax),
  };
}
