# Ecuador Payroll Process Flow (Golden Path)
> **Persona**: HR Manager / Labor Lawyer
> **Scope**: Monthly Payroll (Rol de Pagos) & Social Benefits
> **Legal Basis**: Código de Trabajo (Art. 42, 55, 111, 113, 196)

```mermaid
sequenceDiagram
    autonumber
    participant U as HR Officer
    participant O as Odoo (Payroll)
    participant C as Contract Engine
    participant S as IESS / SRI
    participant B as Bank (SPI)

    Note over U, C: Phase 1: Inputs & Updates
    U->>O: Update Attendance / Novedades
    O->>C: Check Contract Status (Indefinite/Special)

    Note over O, O: Phase 2: Calculation Engine (The "Rol")
    O->>O: BASE = Salary + Overtime (Art. 55: 50%/100%)

    rect rgb(240, 255, 240)
        Note right of O: Income Calculation
        O->>O: + 13th Salary (Art. 111) if monthly
        O->>O: + 14th Salary (Art. 113) if monthly
        O->>O: + Reserve Funds (Art. 196) if >1 year
    end

    rect rgb(255, 240, 240)
        Note right of O: Deductions
        O->>O: - IESS Personal (9.45%)
        O->>O: - Impuesto a la Renta (Proj. Gastos)
        O->>O: - Prestamos IESS / Quirografarios
    end

    O->>O: NET TO RECEIVE = Income - Deductions

    Note over O, S: Phase 3: Validation & Output
    U->>O: Confirm Payslips (Approve Batch)
    O->>O: Generate Accounting Entry (Gasto Sueldos vs IESS por Pagar)
    O->>B: Generate SPI txt (Cash Management)
    U->>S: Report IESS (Planilla)
```
