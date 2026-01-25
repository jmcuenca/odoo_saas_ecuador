# SRI Liquidation of Purchases Flow (Golden Path)
> **Persona**: Purchasing Manager / Accountant
> **Scope**: Liquidación de Compras de Bienes y Prestación de Servicios
> **Legal Basis**: Reglamento Comprobantes de Venta (Art. 13)

```mermaid
sequenceDiagram
    autonumber
    participant U as Purchaser
    participant O as Odoo
    participant S as SRI Service
    participant V as Vendor (No RUC)

    Note over U, V: Context: Vendor has no RUC / Cannot Issue Invoice
    U->>O: Create "Liquidación de Compra"
    O->>O: Verify Vendor Identity (Cédula)

    Note over O, O: Phase 1: Taxes & Withholding
    O->>O: Calculate IVA (15%) -> Assumed by Company?
    O->>O: Calculate IR Withholding (Usually 100% assumption or specific table)
    O->>O: Calculate IVA Withholding (100% required)

    Note over O, S: Phase 2: Emission (Self-Issuance)
    U->>O: Post
    O->>O: Generate XML
    O->>O: Sign XML (Company Certificate)
    O->>S: Transmit RECEPCION
    S-->>O: RECIBIDA
    O->>S: Check AUTORIZACION
    S-->>O: AUTORIZADO

    Note over O, V: Phase 3: Payment
    O->>V: Pay Net Amount
    O->>S: Declare in ATS (Code 03)
```
