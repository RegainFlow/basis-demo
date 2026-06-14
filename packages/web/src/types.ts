export interface LineItem {
  description: string;
  quantity: string;
  unit_price: string;
  tax_rate: string;
}

export interface DraftLineItem extends LineItem {
  id: string;
}

export interface CalculatedLineItem extends LineItem {
  category:
    | "Software"
    | "Meals"
    | "Travel"
    | "Office Supplies"
    | "Professional Services"
    | "Uncategorized";
  subtotal: string;
  tax: string;
  total: string;
}

export interface InvoiceRequest {
  line_items: LineItem[];
}

export interface InvoiceTotals {
  line_items: CalculatedLineItem[];
  subtotal: string;
  tax: string;
  total: string;
}
