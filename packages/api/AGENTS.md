# API Context

This package is the HTTP boundary over `invoice_engine`.

- Keep money fields as decimal strings on the wire.
- Let FastAPI/Pydantic return validation errors for invalid payloads.
- Do not duplicate invoice math here; call `calculate_invoice`.
- Update API tests and e2e coverage when request or response shape changes.
