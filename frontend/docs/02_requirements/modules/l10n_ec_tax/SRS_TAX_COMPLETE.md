# SRS: ECUADOR TAX COMPLIANCE MODULE (Income Tax & Deductions)
> **SRS-009** | Version 2.0 | 2026-01-24
> **Legal Basis**: LORTI Art. 9, 10, 36-37 (2026 Updates)

---

# 1. OVERVIEW

## 1.1 Purpose
This module implements the **Income Tax (Impuesto a la Renta)** logic for Odoo 18. It handles **Tax-Exempt Income** (Rentas Exentas) and **Deductible Expenses** (Gastos Deducibles) with strict limits, ensuring compliance with LORTI Art. 9 and Art. 10.

## 1.2 Scope
- **Classification**: Tagging accounts/products as Exempt or Deductible.
- **Limits**: Enforcing limits on specific deduction categories (Travel, Management fees).
- **Calculation**: Corporate Income Tax (25% / 22% / RIMPE).
- **Reporting**: Form 101/102 generation infrastructure.

---

# 2. LEGAL REQUIREMENTS (2026)

## 2.1 Art. 9: Rentas Exentas (Exempt Income)
The following income sources MUST NOT be included in the taxable base:

| Category | Implementation |
|----------|----------------|
| **Dividendos** | Exempt if distributed to non-tax-haven (Rule 9.1) |
| **IESS Benefits** | 100% Exempt (Rule 9.7) |
| **Occasional Real Estate** | Exempt (Rule 9.10) |
| **Decimo Tercero/Cuarto** | Exempt (Rule 9.11) |
| **Travel Expenses** | Exempt up to 5% of taxable income |

## 2.2 Art. 10: Gastos Deducibles (Deductible Expenses)
Expenses are deductible ONLY if they generate taxable income and have valid documentation.

| Category | Limit | Config Key |
|----------|-------|------------|
| **Travel (Viaje)** | Max 3% of taxable income | `l10n_ec_deduct_travel_max` |
| **Management Fees** | Max 20% of general expenses | `l10n_ec_deduct_mgmt_max` |
| **Royalties** | Max 20% of taxable income | `l10n_ec_deduct_royalty_max` |
| **Provisions (Bad Debt)** | 1% of credit portfolio | `l10n_ec_deduct_bad_debt` |
| **Interest** | Net Interest < 20% EBITDA | `l10n_ec_deduct_interest_cap` |

---

# 3. DATA MODELS

## 3.1 Account Account Extension (`account.account`)

| Field | Type | Description |
|-------|------|-------------|
| `l10n_ec_tax_type` | Selection | `taxable_income`, `exempt_income`, `deductible_expense`, `non_deductible_expense` |
| `l10n_ec_deduction_limit_id` | Many2one | Link to deduction limit rule |

## 3.2 Deduction Limit Rule (`l10n_ec.deduction.limit`)

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char | e.g., "Limit 3% Travel" |
| `basis` | Selection | `taxable_income`, `total_expenses`, `credit_portfolio`, `ebitda` |
| `percentage` | Float | Percentage limit (e.g., 3.0) |
| `active` | Boolean | True |

---

# 4. FUNCTIONAL LOGIC

## 4.1 Corporate Income Tax Calculation
At fiscal year end, the system calculates:

1. **Total Income** = Sum(Income Accounts)
2. **Exempt Income** = Sum(Income Accounts where `l10n_ec_tax_type` = `exempt`)
3. **Total Expenses** = Sum(Expense Accounts)
4. **Non-Deductible (Direct)** = Sum(Expense Accounts where `l10n_ec_tax_type` = `non_deductible`)
5. **Non-Deductible (Limit Exceeded)**:
   - For each limit rule, calculate Max Deductible.
   - If Actual > Max, difference is Non-Deductible.
6. **Taxable Base** = (Total Income - Exempt Income) - (Total Expenses - Non Deductible)

## 4.2 Posting Income Tax
- Creates a journal entry:
  - Debit: Income Tax Expense
  - Credit: Income Tax Payable

---

# 5. CONFIGURATION
- **Menu**: Accounting -> Configuration -> Localization -> Tax Rules
- **Pre-loaded Data**: 2026 Limitations based on LORTI Art. 10.

---

# 6. ACCEPTANCE CRITERIA
1. [ ] Can tag an account as "Exempt Income".
2. [ ] Travel expenses exceeding 3% of income are automatically flagged as non-deductible in reporting.
3. [ ] Dividends from local companies (non-tax haven) are treated as exempt.
4. [ ] Bad debt provision exceeding 1% is disallowed.
