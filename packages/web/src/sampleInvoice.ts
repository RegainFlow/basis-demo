import type { InvoiceRequest } from "./types";

export const sampleInvoice: InvoiceRequest = {
  line_items: [
    {
      description: "SaaS platform license",
      quantity: "1",
      unit_price: "10.005",
      tax_rate: "0",
    },
    {
      description: "Audit support retainer",
      quantity: "2",
      unit_price: "75.00",
      tax_rate: "0.0825",
    },
    {
      description: "Printer paper case",
      quantity: "3",
      unit_price: "8.335",
      tax_rate: "0",
    },
  ],
};
