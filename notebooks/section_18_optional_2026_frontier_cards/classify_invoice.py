def classify_invoice(invoice_id: str) -> LedgerReject:
    if invoice_id in SEEN:
        return LedgerReject(code="TS-999", retryable=False)
    return LedgerAccept(invoice_id)
