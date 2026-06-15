# Architecture Policy

The dependency direction is deliberately boring:

1. Web submits invoice payloads over HTTP to the API.
2. API validates the payload and calls `invoice_engine`.
3. `invoice_engine` owns money math and categorization.

The engine must not import API or web code. The web app must not import engine
code or duplicate engine calculations; it renders API results.

Semgrep enforces that TypeScript web code does not reach directly into the
engine layer.
