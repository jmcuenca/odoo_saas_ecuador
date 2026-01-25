# SRS: ECUADOR INCOME TAX ENGINE 2026 (Impuesto a la Renta)
> **SRS-009** | Version 1.0 | 2026-01-25
> **Legal Basis**: Resolución NAC-DGERCGC25-00000043 (Tables 2026), LORTI Art. 10 (Gastos Personales)

---

# 1. OVERVIEW

## 1.1 Purpose
To implement a "Best in Class" calculation engine for **Impuesto a la Renta (IR)** for employees (Relación de Dependencia). The system must handle the **2026 Progressive Table** and the **Rebaja por Gastos Personales** (Tax Credit) based on **Family Loads**, replacing the legacy "deductible expense" methodology.

## 1.2 Scope
- **Inputs**: Projected Annual Income, Family Loads, Projected Expenses (GP).
- **Process**: Compute "Impuesto Causado" -> Compute "Rebaja GP" -> Result "Impuesto a Retener".
- **Outputs**: Monthly retention amount, Form 107.

---

# 2. ALGORITHMS

## 2.1 Step 1: Annual Income Projection
```python
Annual_Income = (Monthly_Wage * 12) + Overtime + Commissions + Bonuses
# Note: Decimals (13th/14th) and Reserve Funds are EXEMPT (LORTI Art. 9).
# IESS Personal (9.45%) is DEDUCTIBLE.
Net_Taxable_Base = Annual_Income - (Annual_Income * 0.0945)
```

## 2.2 Step 2: Impuesto Causado (2026 Table)
Apply `Net_Taxable_Base` to the SRI 2026 Table (NAC-DGERCGC25-00000043).

| Basic Fraction | Excess Until | Basic Tax | Marginal % |
|----------------|--------------|-----------|------------|
| 0 | 12,208 | 0 | 0% |
| 12,208 | 15,549 | 0 | 5% |
| 15,549 | 20,188 | 167 | 10% |
| 20,188 | 26,700 | 631 | 12% |
| 26,700 | 35,136 | 1,412 | 15% |
| 35,136 | 46,575 | 2,678 | 20% |
| 46,575 | 62,005 | 4,965 | 25% |
| 62,005 | 82,679 | 8,823 | 30% |
| 82,679 | 109,956 | 15,025 | 35% |
| 109,956 | Infinity | 24,572 | 37% |

## 2.3 Step 3: Rebaja por Gastos Personales (Tax Credit)

### A. Determine Maximum Basket Limit (Canasta Básica)
Based on `l10n_ec_family_loads` (Cargas Familiares).
*Canasta Básica Enero 2026 Estimate*: **$798.25** (Using $800 as conservative placeholder for Logic, needs Config Param).
*LORTI Rule*: 18% of (N * Canastas).

| Family Loads | Multiplier (N Canastas) | Formula | Max Rebate (Est. @ $800) |
|--------------|-------------------------|---------|--------------------------|
| 0 | 7 | (7 * 800) * 18% | $1,008.00 |
| 1 | 9 | (9 * 800) * 18% | $1,296.00 |
| 2 | 11 | (11 * 800) * 18% | $1,584.00 |
| 3 | 14 | (14 * 800) * 18% | $2,016.00 |
| 4 | 17 | (17 * 800) * 18% | $2,448.00 |
| 5+ | 20 | (20 * 800) * 18% | $2,880.00 |
| **Catastrophic Disease** | 20 (Special) | (20 * 800) * 18% | $2,880.00 |

### B. Calculate Actual Rebate
```python
Min_Gp_Or_Basket = min(Projected_Expenses, (N_Canastas * Cost_Canasta))
Rebaja = Min_Gp_Or_Basket * 18%
```

## 2.4 Step 4: Final Tax
```python
Impuesto_Renta_Annual = max(0, Impuesto_Causado - Rebaja)
Monthly_Retention = Impuesto_Renta_Annual / 12
```

---

# 3. DATA MODEL REQUIREMENTS

## 3.1 `hr.employee`
- `l10n_ec_family_loads` (Integer): Verified dependents.
- `l10n_ec_catastrophic_disease` (Boolean): Triggers Max Rebate.

## 3.2 `hr.contract`
- `l10n_ec_projected_expenses` (Monetary): Formulario GP input.

## 3.3 `ir.config_parameter`
- `l10n_ec.sri_canasta_basica` (Float): $798.25 (Jan 2026).
- `l10n_ec.sri_tax_table_2026` (JSON): The progressive table structure.

---

# 4. DOCUMENT CONTROL

| Property | Value |
|----------|-------|
| **Document ID** | SRS-IR-2026-001 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Legal Basis** | NAC-DGERCGC25-00000043 |
