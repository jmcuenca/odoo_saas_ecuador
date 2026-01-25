# SRS: ECUADOR RIMPE REGIME MODULE
> **SRS-008** | Version 1.0 | 2026-01-24
> **Legal Basis**: LORTI Art. 97.1-97.10, RIMPE Regulations

---

# DOCUMENT CONTROL

| Property | Value |
|----------|-------|
| **Document ID** | SRS-RIMPE-EC-001 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Classification** | Internal |
| **Legal Basis** | LORTI Art. 97.1-97.10 |
| **Regulatory Authority** | SRI |

---

# 1. OVERVIEW

## 1.1 Purpose
This module implements the **Régimen Simplificado para Emprendedores y Negocios Populares (RIMPE)** for Odoo 18. It handles special retention rules, tax limitations, and exclusive document types ("Notas de Venta") for RIMPE taxpayers.

## 1.2 Scope
- **Partner Classification**: RIMPE categorization (Business Popular vs Entrepreneur).
- **Document Types**: Handling "Nota de Venta" (Document Type 02).
- **Withholding Rules**: Special 0% and 1% retention logic.
- **Reporting**: Exclusion from standard Form 104 for Business Popular.

## 1.3 Key Legal Definitions (2026)

| Category | Gross Income | Document | IVA | Retention Rec'd |
|----------|--------------|----------|-----|-----------------|
| **Negocio Popular** | $0 - $20,000 | Nota de Venta | N/A (Included) | 0% (Rule 332B) |
| **Emprendedor** | $20,001 - $300,000 | Factura | 12%/15% | 1% (Rule 343A) |

---

# 2. DATA MODELS

## 2.1 Partner Extension (`res.partner`)

| Field Name | Code Field (`l10n_ec_rimpe/models/res_partner.py`) | Type | Description |
|------------|--------------------------------------------------|------|-------------|
| RIMPE Regime | `l10n_ec_rimpe_type` | Selection | `none`, `entrepreneur`, `popular_business` |
| Start Date | `l10n_ec_rimpe_start_date` | Date | Start of regime |
| End Date | `l10n_ec_rimpe_end_date` | Date | End of regime (3-year limit check) |

---

# 3. FUNCTIONAL LOGIC

## 3.1 Purchase Logic (Vendor Bills)
When receiving a bill from a RIMPE partner:

### Case A: Vendor is "Negocio Popular"
1. **Document Type**: Must be `02` (Nota de Venta) or `01` (Factura - rare).
2. **IVA**: If Type 02, entered amount includes IVA. Logic must segregate internally for cost, but **NO IVA CREDIT** is allowed.
3. **Retention**:
   - Income Tax: **0%** (Code 332B).
   - IVA: **0%** (No retention allowed).

### Case B: Vendor is "Emprendedor"
1. **Document Type**: Must be `01` (Factura).
2. **IVA**: Standard calculation (15%).
3. **Retention**:
   - Income Tax: **1%** (Code 343A) on Goods/Services.
   - IVA: Standard retention rules apply (can be retained).

## 3.2 Sales Logic (Customer Invoices)
If the Odoo Company is RIMPE:

### Case A: Company is "Negocio Popular"
1. **Document Type**: Issues `Nota de Venta` (Type 02).
2. **IVA**: Does not break down IVA.
3. **Electronic Invoicing**: **NOT REQUIRED** (Physical notes allowed), but if using Odoo, must issue Electronic Invoice labeled "Contribuyente Negocio Popular - Régimen RIMPE".

### Case B: Company is "Emprendedor"
1. **Document Type**: Issues `Factura` (Type 01).
2. **Legends**: XML must include "Contribuyente Régimen RIMPE".
3. **IVA**: Breaks down IVA 15%.

---

# 4. REPORTING REQUIREMENTS

## 4.1 ATS (Anexo Transaccional)
- **Partner Type**: Must report correct `tpIdProv` for RIMPE.
- **Retentions**: Must use codes 332B / 343A.
- **Type 02 Documents**: Reported in Compras, but with 0% tax credit.

## 4.2 Form 103 (Retentions)
- New columns/codes for RIMPE retentions.

---

# 5. CONFIGURATION
- **Retention Codes**:
  - `332B`: RIMPE Negocio Popular (0%)
  - `343A`: RIMPE Emprendedor (1%)
- **Taxpayer Type**: Configuration on `res.company`.

---

# 6. ACCEPTANCE CRITERIA (VERIFIED IN CODE)
1. [x] Can set Partner as "RIMPE Negocio Popular" (See `res.partner.l10n_ec_rimpe_type`).
2. [x] Purchase Journal prevents standard IVA Credit for Type 02 (See `account.move` constraints).
3. [x] Automatic Retention creates Code 332B (0%) (See `account_retention.py`).
4. [x] Automatic Retention creates Code 343A (1%) (See `account_retention.py`).
5. [x] XML Generator adds `<infoAdicional>` (See `l10n_ec.sri.xml`).
