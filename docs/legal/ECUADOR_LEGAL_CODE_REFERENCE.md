# 🇪🇨 ECUADOR COMPLETE LEGAL CODE REFERENCE FOR ERP

> **Document Type**: Legal Compliance Matrix
> **Verified Date**: January 25, 2026
> **Sources**: lexis.com.ec, sri.gob.ec, trabajo.gob.ec, iess.gob.ec, aduana.gob.ec, supercias.gob.ec

---

## PART I: TAX LEGISLATION (SRI)

### LEY ORGÁNICA DE RÉGIMEN TRIBUTARIO INTERNO (LORTI)
**Registro Oficial Suplemento 463, 17-nov-2004 | Última reforma: 2026**

| Article | Requirement | ERP Module | Field/Function |
|:--------|:------------|:-----------|:---------------|
| Art. 19 | Obligación de llevar contabilidad | `account` | Chart of Accounts |
| Art. 20 | Principios contables | `account` | NIIF compliance |
| Art. 28 num. 6 | Depreciación activos fijos | `account_asset` | Depreciation calc |
| Art. 37 | IR Sociedades 25% | `account` | Tax computation |
| Art. 43-44 | Retención en la fuente IR | `l10n_ec_withholding` | Withholding 1-10% |
| Art. 50 | Retención IVA | `l10n_ec_withholding` | IVA 30%/70%/100% |
| Art. 52-54 | Hecho generador IVA | `account` | Tax on sales |
| Art. 64 | Facturación obligatoria | `l10n_ec_edi` | Electronic invoice |
| Art. 65 | Base imponible IVA | `account` | Tax base calc |
| Art. 103 | Declaraciones mensuales | `l10n_ec_reports` | Form 103/104 |
| Art. 107 | Anexo Transaccional (ATS) | `l10n_ec_reports` | ATS XML |

### RESOLUCIONES SRI 2025-2026

| Resolution | Date | Requirement | Module |
|:-----------|:-----|:------------|:-------|
| NAC-DGERCGC25-00000014 | Ene 2025 | Facturación electrónica inmediata | `l10n_ec_edi` |
| NAC-DGERCGC25-00000017 | Ene 2025 | Anulación CF prohibida | `l10n_ec_edi` |
| NAC-DGERCGC20-00000061 | 2020 | Tabla retenciones IVA | `l10n_ec_withholding` |
| NAC-DGERCGC15-00000284 | 2015 | Formato ATS | `l10n_ec_reports` |

---

## PART II: LABOR LEGISLATION

### CÓDIGO DEL TRABAJO
**Registro Oficial Suplemento 167, 16-dic-2005 | Última reforma: 2024**

| Article | Requirement | ERP Module | Implementation |
|:--------|:------------|:-----------|:---------------|
| Art. 12-17 | Contrato individual escrito | `hr_contract` | Contract template |
| Art. 42 | Obligaciones patronales | `hr` | Employee records |
| Art. 47-55 | Jornada de trabajo | `hr_attendance` | Clock in/out |
| Art. 55 | Horas suplementarias 50% | `hr_attendance` | Overtime calc |
| Art. 55 | Horas extraordinarias 100% | `hr_attendance` | Overtime calc |
| Art. 69-78 | Vacaciones 15 días | `hr_holidays` | Leave management |
| Art. 71 | +1 día por año >5 años | `hr_holidays` | Seniority bonus |
| Art. 80 | Remuneración | `l10n_ec_hr_payroll` | Salary processing |
| Art. 97-104 | Utilidades 15% | `l10n_ec_hr_payroll` | Profit sharing |
| Art. 111 | Décimo tercero | `l10n_ec_hr_payroll` | 13th salary |
| Art. 113 | Décimo cuarto | `l10n_ec_hr_payroll` | 14th salary |
| Art. 196-198 | Fondos de reserva | `l10n_ec_hr_payroll` | Reserve funds 8.33% |

### DECRETOS EJECUTIVOS SSO

| Decree | Date | Requirement | Module |
|:-------|:-----|:------------|:-------|
| DE 255 | May 2024 | SSO obligatorio | `hr_attendance` |
| Acuerdo MDT-2024-196 | Oct 2024 | 35 obligaciones SSO | `maintenance` |

---

## PART III: SOCIAL SECURITY (IESS)

### LEY DE SEGURIDAD SOCIAL
**Registro Oficial Suplemento 465, 30-nov-2001 | Última reforma: 2024**

| Article | Requirement | Rate | Module |
|:--------|:------------|:-----|:-------|
| Art. 73 | Aporte patronal | 11.15% | `l10n_ec_hr_payroll` |
| Art. 73 | Aporte personal | 9.45% | `l10n_ec_hr_payroll` |
| Art. 74 | Afiliación obligatoria día 1 | - | `hr_contract` |
| Art. 159 | SECAP | 0.5% | `l10n_ec_hr_payroll` |
| Art. 159 | IECE | 0.5% | `l10n_ec_hr_payroll` |

---

## PART IV: CUSTOMS (SENAE)

### CÓDIGO ORGÁNICO DE PRODUCCIÓN, COMERCIO E INVERSIONES (COPCI)
**Registro Oficial Suplemento 351, 29-dic-2010 | Reforma: 14-ene-2026**

| Article | Requirement | Module | Implementation |
|:--------|:------------|:-------|:---------------|
| Art. 108-109 | Declaración aduanera obligatoria | `l10n_ec_customs` | DAU model |
| Art. 110 | Clases de declaración | `l10n_ec_customs` | DAU types |
| Art. 111 | Plazo declaración (15 días) | `l10n_ec_customs` | Date validation |
| Art. 117-119 | Aforo documental/físico | `l10n_ec_customs` | Inspection status |
| Art. 142-145 | Régimen depósito temporal | `l10n_ec_customs` | Warehouse regime |
| Art. 147-150 | Admisión temporal | `l10n_ec_customs` | Temporary import |
| Art. 154-157 | Transformación | `l10n_ec_customs` | Manufacturing |
| Art. 183-190 | Zonas Francas | `l10n_ec_customs` | Free zone calc |
| Art. 216 lit. l | Ad Valorem 0-40% | `l10n_ec_customs` | Tariff by HS code |
| Art. 89-94 | Agentes de aduana | `purchase` | Broker partner |

### TRIBUTOS ADUANEROS

| Tax | Law | Rate | Base | Module |
|:----|:----|:-----|:-----|:-------|
| Ad Valorem | COPCI Art. 216 | 0-40% | CIF | `l10n_ec_customs` |
| FODINFA | Ley Especial | 0.5% | CIF | `l10n_ec_customs` |
| IVA Import | LORTI Art. 70 | 15% | CIF+duties | `l10n_ec_customs` |
| ISD | LORTI Art. 75 | 5%/2.5%/0% | Payment | `l10n_ec_customs` |

> [!CAUTION]
> **COLOMBIA 30% TARIFF - NOT OFFICIAL**
>
> The reported "30% security tariff on Colombia imports" is **NOT published in the Registro Oficial**.
> This information is from news reports ONLY. **DO NOT implement until officially published.**
>
> Always verify laws at: https://www.registroficial.gob.ec/

### INFRACCIONES ADUANERAS

| Type | Sanction | Law | Module |
|:-----|:---------|:----|:-------|
| Declaración falsa | 30% valores | COPCI Art. 190 | `l10n_ec_customs` |
| Contrabando | 1-5 años + 3x valor | COPCI Art. 301-305 | - |
| No conservar docs | Multa administrativa | Res. SENAE-2025-0076 | `l10n_ec_customs` |

---

## PART V: MANUFACTURING & QUALITY

### LEY DEL SISTEMA ECUATORIANO DE CALIDAD
**Registro Oficial 26, 22-feb-2007**

| Article | Requirement | Module |
|:--------|:------------|:-------|
| Art. 31-40 | Control calidad obligatorio | `quality` |
| Art. 50 | Sello INEN | `quality` |

### REGLAMENTOS TÉCNICOS INEN

| RTE | Products | Module |
|:----|:---------|:-------|
| 142 RTE obligatorios | Manufactura regulada | `mrp` |
| NTE INEN ISO 9001 | Sistema gestión calidad | `quality` |
| NTE INEN ISO 22000 | Gestión seguridad alimentos | `quality` |

### ARCSA (Control Sanitario)

| Resolution | Requirement | Module |
|:-----------|:------------|:-------|
| Resolución 067 | BPM alimentos obligatorio | `quality` |
| Normativa Técnica Sanitaria | Registro sanitario | `mrp` |

---

## PART VI: COMMERCIAL LAW

### LEY DE COMPAÑÍAS
**Registro Oficial 312, 5-nov-1999 | Reforma: 2023**

| Article | Requirement | Module |
|:--------|:------------|:-------|
| Art. 289-295 | Estados financieros SCVS | `account` |
| Art. 290 | Presentación abril 30 | `l10n_ec_reports` |
| Art. 432-433 | Libro de actas | `documents` |

### SUPERINTENDENCIA DE COMPAÑÍAS (SCVS)

| Requirement | Frequency | Module |
|:------------|:----------|:-------|
| Balance general NIIF | Anual | `account` |
| Estado resultados | Anual | `account` |
| Flujo efectivo | Anual | `account` |
| Notas estados financieros | Anual | `account` |

---

## PART VII: TRANSPORT & LOGISTICS

### LEY ORGÁNICA DE TRANSPORTE TERRESTRE (LOTTTSV)
**Registro Oficial Suplemento 398, 7-ago-2008**

| Article | Requirement | Module |
|:--------|:------------|:-------|
| Art. 45-52 | Registro vehículos comerciales | `fleet` |
| Art. 79 | Licencia transporte carga | `fleet` |

### GUÍA DE REMISIÓN

| Law | Requirement | Module |
|:----|:------------|:-------|
| COPCI Art. 142 | Documento transporte interno | `l10n_ec_stock` |
| Res. SRI | Guía electrónica | `l10n_ec_stock` |

---

## SUMMARY: COMPLETE MODULE STACK

| Module | Primary Law | Key Articles | Status |
|:-------|:------------|:-------------|:-------|
| `account` | LORTI + Ley Compañías | Art. 19-20, 289-295 | ✅ |
| `account_asset` | LORTI | Art. 28 num. 6 | ⚠️ ADD |
| `l10n_ec_edi` | LORTI + NAC-DGERCGC25-17 | Art. 64, Res. 2025 | ✅ |
| `l10n_ec_withholding` | LORTI | Art. 43-50 | ✅ |
| `l10n_ec_reports` | LORTI + Ley Compañías | Art. 103-107, 290 | ✅ |
| `hr` | Código Trabajo | Art. 42 | ✅ |
| `hr_contract` | Código Trabajo + IESS | Art. 12-17, 74 | ✅ |
| `hr_attendance` | Código Trabajo + DE 255 | Art. 47-55 | ⚠️ ADD |
| `hr_holidays` | Código Trabajo | Art. 69-78 | ⚠️ ADD |
| `hr_expense` | LORTI | Art. 10 num. 9 | ⚠️ ADD |
| `l10n_ec_hr_payroll` | Código Trabajo + IESS | Art. 73, 97-113, 196 | ✅ |
| `l10n_ec_customs` | COPCI | Art. 108-190, 216 | ✅ |
| `mrp` | INEN + ARCSA | RTE + BPM | ⚠️ ADD |
| `quality` | Ley Calidad + ARCSA | Art. 31-40, Res. 067 | ⚠️ ADD |
| `maintenance` | DE 255 + MDT-2024-196 | Art. 5-8 | ⚠️ ADD |
| `fleet` | LOTTTSV | Art. 45-52, 79 | ⚠️ ADD |
| `l10n_ec_stock` | COPCI + SRI | Art. 142 | ✅ |

---

## DISCLAIMER

> This document is for reference only. Consult licensed Ecuador attorneys for legal advice.
> Laws subject to change. Last verified: January 25, 2026
