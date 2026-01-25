# COMPLIANCE AUDIT MATRIX - 100% TARGET
> **Audit Date**: 2026-01-24
> **Auditor**: PwC Compliance Persona
> **Target**: 100% Legal Coverage before Coding

## 1. LORTI TITLE I - IMPUESTO A LA RENTA (Income Tax)

| Article | Topic | Status | SRS Location | Gap |
|---------|-------|--------|--------------|-----|
| Art. 1-8 | General/Residency | ✅ | SRS_TAX | None |
| Art. 9 | Rentas Exentas | ⚠️ | SRS_TAX | **Missing specific validations for Num 15 (Elderly), 16 (Disability), 18 (Cultura), 19 (Insurance)** |
| Art. 10 | Gastos Deducibles | ⚠️ | SRS_TAX | **Missing specific limits for Num 7 (Amortization), 11 (Bad Debt details), 15 (Promotion)** |
| Art. 13 | Pagos al Exterior | ❌ | **MISSING** | Need detailed logic for withholding & deductibility limits |
| Art. 19 | Anticipo IR | ❌ | **MISSING** | Need precise calculation formula post-Decreto 806 |
| Art. 36 | Tarifa Sociedades | ✅ | SRS_TAX | Covered |
| Art. 37 | Tarifa Personas | ✅ | SRS_TAX | 2026 Tables covered |
| Art. 39-49 | Contabilidad | ❌ | **MISSING** | Need NIIF to NEC mapping logic |

## 2. LORTI TITLE II - IVA (Value Added Tax)

| Article | Topic | Status | SRS Location | Gap |
|---------|-------|--------|--------------|-----|
| Art. 52-54 | Objeto/Transfers | ✅ | SRS_TAX | Covered |
| Art. 55 | Servicios 0% | ❌ | **MISSING** | **Need detailed list of all 20+ service categories with UNSPSC codes** |
| Art. 56 | Importaciones | ❌ | **MISSING** | Need mapping to Customs Regimes (10, 70 etc) |
| Art. 57 | Crédito Tributario | ❌ | **MISSING** | **Critical logic for Proportionality Factor (Factor de Proporcionalidad)** |
| Art. 63 | Declaración | ✅ | SRS_SRI | Covered (F104) |
| Art. 69 | Agentes Retención | ✅ | SRS_WITHHOLDING | Covered |

## 3. LORTI TITLE III - ICE (Special Consumption)

| Article | Topic | Status | SRS Location | Gap |
|---------|-------|--------|--------------|-----|
| Art. 75-81 | General | ✅ | SRS_ICE | Covered |
| Art. 82 | Tarifas | ⚠️ | SRS_ICE | **Check specific codes for "Focos Incandescentes" and "Armas" detailed specs** |

## 4. LORTI TITLE IV - RIMPE

| Article | Topic | Status | SRS Location | Gap |
|---------|-------|--------|--------------|-----|
| Art. 97.1-10 | RIMPE Rules | ✅ | SRS_RIMPE | Covered |

## 5. CÓDIGO DE TRABAJO (Labor)

| Article | Topic | Status | SRS Location | Gap |
|---------|-------|--------|--------------|-----|
| Art. 42 | Empleador Obligations | ❌ | **MISSING** | RDEP generation, Utility Sharing (Utilidades) |
| Art. 55 | Horas Extras | ❌ | **MISSING** | **Detailed calculation vs SBU for Nocturnal/Weekend** |
| Art. 95 | Salario Digno | ❌ | **MISSING** | Compensación Económica calculus |
| Art. 111/113 | Décimos | ❌ | **MISSING** | Accumulation vs Monthly logic |
| Art. 196 | Fondos Reserva | ❌ | **MISSING** | IESS integration logic |
| Art. 216 | Jubilación Patronal | ❌ | **MISSING** | Actuarial calculation placeholder |

## 6. COPCI (Trade)

| Article | Topic | Status | SRS Location | Gap |
|---------|-------|--------|--------------|-----|
| Lib V | Regimenes | ❌ | **MISSING** | Detailed status flows for Regimes 10, 70, 21 |
| - | Liquidación | ❌ | **MISSING** | Prorating weight/value for freight/insurance |

---

# ACTION PLAN FOR 100%
1. **UPDATE SRS_TAX**: Add Art 13, 19, 39-49 details.
2. **UPDATE SRS_TAX**: Add Art 56, 57 (Proportionality Factor).
3. **UPDATE SRS_HR_PAYROLL**: Add Art 42, 55, 95, 111, 113, 196, 216 details.
4. **UPDATE SRS_IMPORT_EXPORT**: Add Regimes detailed flows & Liquidation logic.
