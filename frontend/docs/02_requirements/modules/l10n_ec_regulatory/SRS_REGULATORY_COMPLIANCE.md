# SRS: ECUADOR REGULATORY COMPLIANCE EXTENSION
> **SRS-010** | Version 1.0 | 2026-01-24
> **Legal Basis**: Supercias NIIF, UAFE RESU, LOPDP, LORTI Liquidaciones

---

# 1. OVERVIEW

## 1.1 Purpose
This module implements the **Critical Regulatory Pillars** beyond standard tax compliance:
1.  **Supercias Financial Reporting**: NIIF/XBRL specific structures.
2.  **UAFE Anti-Money Laundering**: RESU Reporting for obligated subjects.
3.  **Strict Purchasing**: Liquidación de Compras logic (100% Retention).
4.  **Data Privacy**: LOPDP consent management.

## 1.2 Scope
- **Financial Reports**: Estado de Situación Financiera, Resultado Integral, Flujo de Efectivo, Cambios en Patrimonio.
- **UAFE**: Identification of threshold transactions (> $10k) and RESU generation.
- **Purchasing**: Logic for "Liquidación de Compras" (Doc Type 03) with informal vendors.
- **Privacy**: Consent fields and anonymization actions for partners.

---

# 2. SUPERCIAS COMPLIANCE (NIIF/XBRL)

## 2.1 Financial Statements Structure
Odoo's standard reports do NOT match Supercias format. This module implements:
- **Taxonomies**: Mapping Odoo Accounts -> Supercias Codes (e.g., `101.01.01`).
- **XBRL Tags**: For future interoperability.
- **Specific Reports**:
    1.  **Estado de Situación Financiera (Balance Sheet)**: Classified Current/Non-Current.
    2.  **Estado de Resultado Integral (P&L)**: Function of Expense method.
    3.  **Estado de Flujo de Efectivo**: Direct/Indirect method support.
    4.  **Estado de Cambios en el Patrimonio**: Capital, Reserves, Earnings.

## 2.2 Functional Logic
- **Mapping Wizard**: UI to map CoA to Supercias Codes.
- **Validation**: Check for "Square Balance" (`Activo = Pasivo + Patrimonio`) per Supercias rules.
- **Export**: Excel/PDF formats compliant with Supercias upload template.

---

# 3. UAFE COMPLIANCE (Prevención Lavado Activos)

## 3.1 RESU Report (Reporte de Operaciones)
**Obligated Subjects**: Real Estate, Vehicle Dealers, Notaries, etc.
**Threshold**: Cash/Crypto transactions > $10,000 (usually).

## 3.2 Data Models
`res.partner`:
- `l10n_ec_uafe_obligated`: Boolean.
- `l10n_ec_pep`: Boolean (Politically Exposed Person).

`account.payment`:
- `l10n_ec_uafe_monitor`: Flag for transactions exceeding threshold.

## 3.3 Functional Logic
- **Monitoring**: Real-time check of Payment or Invoice Total > Threshold.
- **RESU Generator**: Monthly XML/TXT report generation for UAFE SISLAFT.
- **Blacklist Check**: Optional integration with CONSEP/OFAC lists (Future Scope).

---

# 4. LIQUIDACIÓN DE COMPRAS (Informal Sector)

## 4.1 Logic
When buying from a person **without RUC** (or incapable of invoicing):
1.  **Issuer**: The COMPANY acts as the issuer.
2.  **Document Type**: `03` (Liquidación de Compra).
3.  **Retention**: **MANDATORY 100% IVA Retention**.
4.  **Income Tax Retention**: Standard rules apply (usually 0% or low, verifying specific code).
5.  **Limits**: Validation of annual limits per supplier (if applicable per SRI Res).

## 4.2 Configuration
- `l10n_ec.retention_liquidation_code` = `332` (or specific code).
- `l10n_ec.retention_iva_liquidation` = `100%`.

---

# 5. DATA PRIVACY (LOPDP - Ecuador GDPR)

## 5.1 Consent Management
`res.partner`:
- `l10n_ec_lopdp_consent`: Boolean.
- `l10n_ec_lopdp_date`: Date verification.
- `l10n_ec_lopdp_channel`: Selection (Email, Physical, Web).

## 5.2 Rights of the Subject (ARCO)
- **Anonymization Wizard**: "Right to be Forgotten". Replaces PII with `***` while keeping accounting integrity.
- **Access Report**: One-click PDF of all stored data for a partner.

---

# 6. ACCEPTANCE CRITERIA
1.  [ ] **Supercias**: Can generate "Estado de Situación Financiera" with valid mapping.
2.  [ ] **UAFE**: System flags a $15,000 cash payment for review.
3.  [ ] **Purchasing**: "Liquidación de Compra" automatically applies 100% IVA Retention.
4.  [ ] **Privacy**: Partner form shows LOPDP consent status.
