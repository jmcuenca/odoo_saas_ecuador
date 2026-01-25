# SRI Delivery Guide Flow (Guía de Remisión)
> **Persona**: Logistics Manager
> **Scope**: Transport of Goods (Guía de Remisión)
> **Legal Basis**: Reglamento Comprobantes de Venta (Art. 19), NAC-DGERCGC21-00000032

```mermaid
sequenceDiagram
    autonumber
    participant U as Logistics User
    participant O as Odoo
    participant S as SRI Service
    participant D as Driver/Carrier

    Note over U, O: Link to Invoice
    U->>O: Select Invoice(s) / Transfer
    U->>O: Create "Guía de Remisión"
    O->>O: Validate Data:
    O->>O: - Carrier (Transportista) RUC
    O->>O: - License Plate (Placa)
    O->>O: - Start/End Dates
    O->>O: - Route (Partida / Llegada)

    Note over O, S: Emission
    U->>O: Confirm
    O->>O: Generate XML (Type 06)
    O->>O: Sign XML
    O->>S: Transmit RECEPCION
    S-->>O: RECIBIDA
    O->>S: Check AUTORIZACION
    S-->>O: AUTORIZADO

    Note over O, D: Transport
    O->>O: Generate RIDE (PDF w/ QR)
    O->>D: Handover Physical/Digital Copy
    Note right of D: Must carry during transit
```
