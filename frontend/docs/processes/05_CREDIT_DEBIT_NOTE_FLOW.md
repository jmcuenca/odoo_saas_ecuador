# SRI Credit/Debit Note Flow (Golden Path)
> **Persona**: Accountant / Sales Manager
> **Scope**: Notas de Crédito (Returns/Discounts) & Notas de Débito
> **Legal Basis**: Reglamento Comprobantes de Venta

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant O as Odoo
    participant S as SRI Service
    participant C as Customer

    Note over U, O: Scenario: Correcting an Invoice
    U->>O: Select Original Invoice
    U->>O: Click "Add Credit Note"
    O->>O: Link to Original ID (001-001-12345)

    Note over O, O: Phase 1: Calculation
    alt Full Refund
        O->>O: Reverse All Lines
        O->>O: Reverse Taxes (IVA/ICE)
    else Partial Discount
        O->>O: Calculate Difference
        O->>O: Adjust Tax Base
    end

    Note over O, S: Phase 2: Emission
    U->>O: Post
    O->>O: Generate NC XML (04)
    O->>O: Sign XML
    O->>S: Transmit
    S-->>O: AUTORIZADO

    Note over O, O: Phase 3: Reconciliation
    O->>O: Reconcile NC against Original Invoice
    O->>O: Balance = 0 (or reduced)
```
