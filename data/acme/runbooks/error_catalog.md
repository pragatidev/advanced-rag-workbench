# Platform error catalog

## General guidance

When a fault appears in logs, restart the worker and check the last fifty lines. Most error codes in general are transient. Do not page the on-call person for a single retryable failure. Collect the request id, the region, and the timestamp before you open a ticket.

## TS-999

TS-999 means the billing ledger rejected a duplicate invoice id. TS-999 is not retryable. Open a ticket with the invoice hash and the merchant account. The runbook owner is billing-ops. The exact token TS-999 is the lookup key.
