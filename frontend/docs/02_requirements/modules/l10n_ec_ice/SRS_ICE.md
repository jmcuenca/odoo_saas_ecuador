# SRS: ECUADOR ICE MANAGEMENT MODULE (Impuesto Consumos Especiales)
> **SRS-007** | Version 1.0 | 2026-01-24
> **Legal Basis**: LORTI Title III (Art. 75-89), SRI Resolutions 2025

---

# DOCUMENT CONTROL

| Property | Value |
|----------|-------|
| **Document ID** | SRS-ICE-EC-001 |
| **Version** | 1.0 |
| **Status** | Draft |
| **Classification** | Internal |
| **Legal Basis** | LORTI Title III (Art. 75-89) |
| **Regulatory Authority** | SRI |

---

# 1. OVERVIEW

## 1.1 Purpose
This module implements the **Impuesto a los Consumos Especiales (ICE)** management system for Odoo 18. Expenses and Sales taxes must be calculated based on **specific tariffs** (monetary/unit) and **ad valorem rates** (percentage/value), strictly following LORTI Art. 82.

## 1.2 Scope
- **Configuration**: ICE Codes, Tariffs, Exemptions.
- **Product Master**: ICE classification fields.
- **Sales/Purchases**: Automatic calculation.
- **Reporting**: Form 104 & ATS integration.

## 1.3 Key Legal Parameter (2025-2026)
> [!IMPORTANT]
> All rates must be fetched from `ir.config_parameter`. NO HARDCODING.

| Group | Codes | Base | Type |
|-------|-------|------|------|
| **Cigarettes** | 3011 | Unit | Specific ($0.16) |
| **Alcohol** | 3031 | Liters Pure Alcohol | Specific ($10.30) |
| **Beer (Ind)** | 3041 | Liters Pure Alcohol | Specific ($13.48) |
| **Beer (Art)** | 3043 | Liters Pure Alcohol | Specific ($1.54) |
| **Sugary Drinks** | 3053 | g/100g sugar | Specific ($0.18) |
| **Plastic Bags** | 3680 | Unit | Specific ($0.08) |
| **Vehicles** | 3092 | PVP | Ad Valorem (Variable) |
| **Perfumes** | 3072 | PVP | Ad Valorem (20%) |
| **Video Games** | 3650 | PVP | Ad Valorem (35%) |
| **Firearms** | 3610 | PVP | Ad Valorem (30%) |

---

# 2. DATA MODELS

## 2.1 ICE Category (`l10n_ec.ice.category`)
Master data for ICE codes defined by SRI.

| Field | Type | Description |
|-------|------|-------------|
| `code` | Char | 3-4 digit SRI code (e.g., 3011) |
| `name` | Char | Description (e.g., Cigarrillos Rubios) |
| `type` | Selection | `specific`, `ad_valorem`, `mixed` |
| `rate_type` | Selection | `percent`, `amount` |
| `active` | Boolean | True |

## 2.2 Product Template Extension (`product.template`)

| Field | Type | Description |
|-------|------|-------------|
| `l10n_ec_ice_category_id` | Many2one | Link to ICE Category |
| `l10n_ec_ice_unit_content` | Float | For specific ICE (e.g., liters of alcohol, grams of sugar) |
| `l10n_ec_pvp` | Monetary | Precio Venta Público (Base for Ad Valorem) |

---

# 3. FUNCTIONAL LOGIC

## 3.1 Calculation Algorithms

### Specific Rate (e.g., Plastic Bags, Cigarettes)
```python
ICE = Quantity * Specific_Rate
# Example: 1000 bags * $0.08 = $80.00
```

### Specific Rate with Content (e.g., Alcohol, Sugar)
```python
# Alcohol
ICE = Quantity * Volume_Liters * Alcohol_Degree * Specific_Rate
# Example: 100 bottles (750ml, 40%)
# 100 * 0.75 * 0.40 * $10.30 = $309.00

# Sugar
ICE = Quantity * (Sugar_Content_Grams / 100) * Specific_Rate
```

### Ad Valorem (e.g., Perfumes, Video Games)
```python
Base = PVP / (1 + IVA_Rate) # Ex-factory price derived or defined
ICE = Base * Ad_Valorem_Rate
# OR if Base is Ex-Factory
ICE = (Ex_Factory * 1.25) * Ad_Valorem_Rate # 1.25 presuntive margin
```

## 3.2 Invoice Line Logic
When a product with `l10n_ec_ice_category_id` is selected:
1. System checks `type` of ICE.
2. If `specific`: Computes based on Qty * Rate.
3. If `ad_valorem`: Computes based on Price * Rate.
4. Adds ICE amount to `price_subtotal` (but tracks separately for tax reporting).
5. **CRITICAL**: IVA is calculated ON TOP of ICE.
   `IVA Base = Price + ICE`

---

# 4. REPORTING REQUIREMENTS

## 4.1 Form 104 (IVA+ICE Declaration)
- **Casillero 601-609**: Operations subject to ICE.
- **Casillero 699**: Total ICE Payable.

## 4.2 ATS (Anexo Transaccional)
- `<detalleImpuestos>` node MUST include ICE breakdown.
- Code `3` for ICE.

---

# 5. CONFIGURATION
- **Menu**: Accounting -> Configuration -> Localization -> ICE Codes
- **Load Data**: CSV file `data/l10n_ec.ice.category.csv` pre-populated with 2026 codes.

---

# 6. ACCEPTANCE CRITERIA
1. [ ] Can configure a product "Cerveza Artesanal" with $1.54/L rate.
2. [ ] Invoice line correctly calculates ICE based on liters/alcohol %.
3. [ ] IVA is calculated on (Base + ICE).
4. [ ] ATS XML generated includes ICE codes.
5. [ ] Form 104 report shows correct ICE totals.
