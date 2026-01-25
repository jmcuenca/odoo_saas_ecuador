# SRI Electronic Invoice Process Flow (Golden Path)
> **Persona**: Process Architect / SRI Expert
> **Scope**: Invoice Emission (Factura Electrónica)

```mermaid
sequenceDiagram
    autonumber
    participant U as User (Accountant)
    participant O as Odoo (Account.Move)
    participant V as Validator (L10n_EC Logic)
    participant X as XML Builder (Jinja2)
    participant S as Signer (XAdES-BES)
    participant API as SRI webService (SOAP)
    participant C as Customer

    Note over U, O: Phase 1: Creation & Validation
    U->>O: Create Draft Invoice
    O->>V: Check RUC/Cedula Algorithm
    V-->>O: Valid
    O->>V: Check ICE Rates & Codes
    V-->>O: Valid
    U->>O: Click "POST" (Confirm)
    O->>O: Assign Sequence (001-001-000012345)

    Note over O, S: Phase 2: EDI Generation
    O->>O: Generate Access Key (49 digits)
    O->>X: Render XML (factura_v2.1.0)
    X-->>O: XML Content
    O->>S: Request Signature (P12 Certificate)
    S-->>O: Signed XML

    Note over O, API: Phase 3: Transmission (Synchronous)
    O->>API: Send RECEPCION (Signed XML)
    API-->>O: Response: RECIBIDA

    loop Every 2 Seconds
        O->>API: Send AUTORIZACION (Access Key)
        API-->>O: Status (AUTORIZADO / REJECTED)
        opt If Authorized
            O->>O: Update State -> SENT
            O->>O: Attach XML to Invoice
            break
        end
    end

    Note over O, C: Phase 4: Delivery
    O->>O: Generate RIDE (PDF)
    O->>C: Email (PDF + Signed XML)
```
