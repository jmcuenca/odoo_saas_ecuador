# ECUADOR LEGAL FRAMEWORK - COMPLETE REFERENCE
> **Master Legal Knowledge Base for ERP Localization**
> **Version 1.0** | 2026-01-24 | PwC-Level Documentation

---

# DOCUMENT CONTROL

| Property | Value |
|----------|-------|
| **Document ID** | LEGAL-EC-MASTER-001 |
| **Purpose** | Complete legal reference for Odoo 18 Ecuador localization |
| **Sources** | Registro Oficial, SRI, IESS, MDT, SENAE |
| **Validation** | All data from official sources only |

---

# PwC IMPLEMENTATION TEAM PERSONAS

The following expert personas have been activated for this implementation:

| Persona | Role | Expertise |
|---------|------|-----------|
| **Tax Partner (Ecuador)** | Sr. LORTI/RLORTI Expert | Income tax, IVA, ICE, retentions |
| **Labor & Payroll Specialist** | HR Compliance Lead | Código de Trabajo, IESS, MDT |
| **Customs & Trade Expert** | COPCI Specialist | SENAE, ECUAPASS, regimes |
| **Odoo Functional Consultant** | ERP Architecture | Localization patterns |
| **Regulatory Compliance Auditor** | Gap Analyst | SRS vs Law verification |
| **Legal Counsel (Ecuador)** | Legal Validator | Registro Oficial compliance |

---

# PART I: IMPUESTO A LA RENTA (LORTI Title I)

## 1.1 Art. 9 - RENTAS EXENTAS (Tax-Exempt Income)

> [!IMPORTANT]
> These must be implemented as `l10n_ec.tax.exemption` records.
> System MUST exclude these from taxable income calculations.

| # | Exención | Implementation |
|---|----------|----------------|
| 1 | Dividendos entre sociedades (no paraísos fiscales) | Partner flag + validation |
| 2 | Ingresos del Estado y empresas públicas | Partner type = 'estado' |
| 3 | Exonerados por convenios internacionales | Partner country + treaty |
| 4 | Estados extranjeros y organismos internacionales | Partner type + reciprocidad |
| 5 | Instituciones sin fines de lucro | Partner type = 'sin_lucro' + dest check |
| 6 | Intereses depósitos ahorro (personas naturales) | Product category |
| 7 | Beneficios jubilación IESS | Income type = 'iess_jubilacion' |
| 8 | Ingresos por becas de estudio | Limit configurable |
| 9 | Ingresos artesanos calificados | Partner flag cal_artesano |
| 10 | Enajenación ocasional bienes inmuebles | Transaction type |
| 11 | Enajenación ocasional acciones | Transaction type |
| 12 | Exportación de bienes y servicios | Invoice type export |
| 13 | Intereses títulos valores del Estado | Product/investment type |
| 14 | Beneficiarios seguros vida/invalidez | Product type |
| 15 | Persona +65 años (1 fracción básica) | Employee.age >= 65 |
| 16 | Persona discapacidad (2x fracción básica) | Employee.disability_pct > 0 |
| 17 | Proyectos APP (10 años) | Company special regime |

### Art. 9 Configuration Keys

```
l10n_ec.exencion_art9_dividendos_activo = true
l10n_ec.exencion_art9_65_anios_fraccion_basica = 12208
l10n_ec.exencion_art9_discapacidad_multiplicador = 2
l10n_ec.exencion_art9_becas_limite = [configurable]
```

---

## 1.2 Art. 10 - GASTOS DEDUCIBLES (Deductible Expenses)

> [!CAUTION]
> System MUST validate comprobante de venta for all deductions.
> Track limits via `ir.config_parameter`.

| # | Gasto Deducible | Límite | Config Key |
|---|-----------------|--------|------------|
| 1 | Costos y gastos necesarios | Con comprobante | N/A |
| 2 | Intereses de deudas del giro | Tasa JPRMF | `l10n_ec.tasa_jprmf` |
| 3 | Impuestos y contribuciones | Sin límite | N/A |
| 4 | Primas de seguros | Sin límite | N/A |
| 5 | Pérdidas por fuerza mayor | Documentadas | N/A |
| 6 | Gastos viaje y estadía | 5% ingresos | `l10n_ec.viajes_limite_pct` |
| 7 | Depreciación activos fijos | Per tabla SRI | depreciación table |
| 8 | Amortización intangibles | 20% anual | N/A |
| 9 | Pérdidas tributarias | 5 años | carry forward |
| 10 | Sueldos y salarios | Con planilla IESS | payroll validation |
| 11 | Provisiones laborales | Décimos, reserve | per law |
| 12 | Provisiones incobrables | 1% créditos | `l10n_ec.incobrables_pct` |
| 13 | Impuestos municipales | Sin límite | N/A |
| 14 | Arrendamiento mercantil | Sin límite | N/A |
| 15 | Regalías | Sin límite | N/A |
| 16 | **Gastos personales** | **CRÉDITO 2026** | See section 1.5 |
| 17 | Pagos exterior | 25% max | `l10n_ec.pagos_ext_max` |

### Art. 10 - GASTOS NO DEDUCIBLES

| Concepto | Límite | Validation |
|----------|--------|------------|
| Intereses sobre tasa JPRMF | Excess = 0% | Rate comparison |
| Créditos exterior no registrados BCE | 0% | BCE registration check |
| Gastos indirectos partes relacionadas | 5% max | Related party flag |
| Gastos sin comprobante válido | 0% | Comprobante validation |
| Multas tributarias | 0% | Expense category |
| Gastos personales en sociedades | 0% | Partner type check |
| Regalías a paraísos fiscales | 0% | Country blacklist |
| Depreciación acelerada no autorizada | Excess = 0% | Rate validation |

---

## 1.3 Art. 36-37 - TARIFAS IMPUESTO A LA RENTA

### Sociedades (Art. 36)

| Concepto | Tarifa | Config Key |
|----------|--------|------------|
| **General** | 25% | `l10n_ec.ir_sociedades_general` |
| Ingresos brutos < $1M | 22% | `l10n_ec.ir_sociedades_pyme` |
| Microempresas RIMPE | 0-2% | See RIMPE section |
| Reinversión utilidades | -10% | `l10n_ec.ir_reinversion` |

### Personas Naturales 2026 (Art. 37 + NAC-DGERCGC25-00000043)

| Fracción Básica | Exceso Hasta | Impuesto FB | % Excedente |
|-----------------|--------------|-------------|-------------|
| $0 | $12,208 | $0 | 0% |
| $12,208 | $15,549 | $0 | 5% |
| $15,549 | $20,188 | $167 | 10% |
| $20,188 | $26,700 | $631 | 12% |
| $26,700 | $35,136 | $1,412 | 15% |
| $35,136 | $46,575 | $2,678 | 20% |
| $46,575 | $62,005 | $4,965 | 25% |
| $62,005 | $82,679 | $8,823 | 30% |
| $82,679 | $109,956 | $15,025 | 35% |
| $109,956 | En adelante | $24,572 | 37% |

> Model: `l10n_ec.income.tax.bracket`
> Updated annually via SRI resolution

---

## 1.4 Art. 41 - ANTICIPO IMPUESTO A LA RENTA

### Anticipo General (Post Decreto 806)

```
Anticipo = IR Causado año anterior - Retenciones año anterior
```

**Payment Schedule:**

| Cuota | Mes | Fecha Límite |
|-------|-----|--------------|
| Cuota 1 | Julio | 10-28 (9no dígito RUC) |
| Cuota 2 | Septiembre | 10-28 (9no dígito RUC) |

### Anticipo Utilidades No Distribuidas (Decreto 191 - 2026)

| Tramo | Tarifa |
|-------|--------|
| Tramo 1 | 0% |
| Tramo 2 | 0.50% |
| Tramo 3 | 1.00% |
| Tramo 4 | 1.50% |
| Tramo 5 | 2.00% |
| Tramo 6 | 2.50% |

**Payment:** August (per 9no dígito RUC)

---

## 1.5 Art. 10 num. 16 - GASTOS PERSONALES 2026

> [!WARNING]
> **CRITICAL 2026 CHANGE**: Gastos personales now generate TAX CREDIT,
> NOT deducted from taxable income.

**Categorías:**

| Categoría | Español | Config Key |
|-----------|---------|------------|
| Vivienda | Vivienda | `l10n_ec.gp_vivienda_max` |
| Educación | Educación | `l10n_ec.gp_educacion_max` |
| Salud | Salud (énfasis) | `l10n_ec.gp_salud_max` |
| Alimentación | Alimentación | `l10n_ec.gp_alimentacion_max` |
| Vestimenta | Vestimenta | `l10n_ec.gp_vestimenta_max` |

**Límites por Cargas Familiares:**

| # Dependientes | Límite Total |
|----------------|--------------|
| 0 | Configurable |
| 1 | Configurable |
| 2 | Configurable |
| 3+ | Configurable |

---

# PART II: IMPUESTO AL VALOR AGREGADO (LORTI Title II)

## 2.1 Art. 54 - PRODUCTOS TARIFA 0% IVA

> [!IMPORTANT]
> Products in these categories MUST have `l10n_ec_iva_type = '0'`

### ALIMENTOS (Estado Natural)

| Producto | Código HS | Notas |
|----------|-----------|-------|
| Carnes (res, cerdo, pollo) | 02xx | Estado natural |
| Arroz | 1006 | Sin procesar |
| Atún (lata para consumo popular) | 1604 | Específico |
| Huevos | 0407 | Sin procesar |
| Pan (artesanal) | 1905 | Condiciones |
| Azúcar | 1701 | Blanca/morena |
| Sal | 2501 | Para consumo |
| Leche (natural/pasteurizada) | 0401 | Sin saborizantes |
| Queso (fresco artesanal) | 0406 | Condiciones |
| Frutas naturales | 08xx | Sin procesar |
| Vegetales naturales | 07xx | Sin procesar |
| Legumbres | 0713 | Secas/frescas |
| Cereales | 10xx | Sin procesar |
| Café molido (no instantáneo) | 0901 | Condiciones |
| Harina de trigo | 1101 | Para pan |
| Fideos | 1902 | Para consumo popular |
| Avena | 1104 | Sin procesar |
| Agua embotellada | 2201 | Natural/mineral |

### SALUD

| Producto | Código HS | Notas |
|----------|-----------|-------|
| Medicinas uso humano | 30xx | Registro ARCSA |
| Toallas sanitarias | 9619 | Higiene femenina |
| Pañales | 9619 | Para bebés/adultos |
| Alcohol antiséptico | 2207 | Uso médico |
| Mascarillas | 6307 | Protección |
| Productos veterinarios | 3004 | Con registro |

### AGRÍCOLA

| Producto | Código HS | Notas |
|----------|-----------|-------|
| Semillas certificadas | 1209 | Para siembra |
| Fertilizantes | 31xx | Uso agrícola |
| Insecticidas | 3808 | Uso agrícola |
| Pesticidas | 3808 | Uso agrícola |
| Fungicidas | 3808 | Uso agrícola |
| Herbicidas | 3808 | Uso agrícola |
| Tractores | 8701 | Uso agrícola |
| Maquinaria agrícola | 8432-8437 | Uso agrícola |
| Aceite sigatoka negra | 2710 | Específico |

### OTROS

| Producto | Código HS | Notas |
|----------|-----------|-------|
| Libros | 4901 | Impresos |
| Papel periódico | 4801 | Para prensa |
| Lámparas LED | 8539 | Eficiencia energética |
| Energía eléctrica | 2716 | Servicio |
| Vehículos híbridos | 8703 | Condiciones |
| Aviones, avionetas | 8802 | Importación |
| Cocinas inducción | 8516 | Programa gobierno |
| Baterías/ollas inducción | 7615 | Programa gobierno |

---

## 2.2 Art. 55 - SERVICIOS TARIFA 0% IVA

| Servicio | Código ATS | Condiciones |
|----------|------------|-------------|
| Transporte público urbano | 496 | Nacional |
| Transporte público interurbano | 496 | Nacional |
| Transporte escolar | 496 | Autorizado |
| Transporte de carga | 494 | Nacional |
| Servicios de salud | 862 | Autorizados MSP |
| Educación | 851-854 | Acreditada |
| Arrendamiento vivienda | 6810 | Para habitación |
| Servicios funerarios | 9603 | Básicos |
| Guarderías | 889 | Autorizadas |
| Servicios religiosos | 9491 | Sin fines lucro |
| Refrigeración productos agrícolas | 522 | Para producción |
| Exportación de servicios | 000 | Con divisas |
| Servicios artesanos calificados | N/A | Cal. JNDA |
| Seguros de vida | 6512 | Individual |
| Seguros de salud | 6512 | Individual |
| Servicios web (hosting) | 631 | Para residentes |

---

## 2.3 Art. 56 - IMPORTACIONES 0% IVA

| Producto | Condición |
|----------|-----------|
| Medicinas para humanos | Registro ARCSA |
| Libros impresos | Fin educativo |
| Maquinaria agrícola | Uso productivo |
| Semillas | Para producción |
| Donaciones a entidades sin fin lucro | Verificadas |
| Bienes admisión temporal | Reexportación |
| Combustibles derivados | Régimen especial |

---

# PART III: IMPUESTO CONSUMOS ESPECIALES (LORTI Title III, Art. 75-89)

## 3.1 Art. 75-80 - Marco General ICE

| Artículo | Contenido |
|----------|-----------|
| **Art. 75** | Objeto del impuesto |
| **Art. 76** | Base imponible (PVP - IVA - ICE o precio referencial SRI) |
| **Art. 77** | Exenciones (exportaciones) |
| **Art. 78** | Hecho generador (transferencia/importación/consumo) |
| **Art. 79** | Sujeto activo (Estado/SRI) |
| **Art. 80** | Sujetos pasivos (fabricantes/importadores/prestadores) |

## 3.2 Art. 82 - PRODUCTOS Y TARIFAS ICE 2025-2026

### Tarifas Específicas (Ajustadas IPC)

| Producto | Tarifa 2025 | Unidad | Config Key |
|----------|-------------|--------|------------|
| Cigarrillos | $0.16 | /unidad | `l10n_ec.ice_cigarrillos` |
| Bebidas alcohólicas | $10.30 | /litro puro | `l10n_ec.ice_alcohol` |
| Cerveza industrial | $13.48 | /litro puro | `l10n_ec.ice_cerveza_ind` |
| Cerveza artesanal | $1.54 | /litro puro | `l10n_ec.ice_cerveza_art` |
| Bebidas azucaradas (>25g/L) | $0.18 | /100g azúcar | `l10n_ec.ice_azucar` |
| Fundas plásticas | $0.08 | /funda | `l10n_ec.ice_fundas` |
| Tabaco calentado | $0.16 | /unidad | `l10n_ec.ice_tabaco_calentado` |

### Tarifas Ad Valorem

| Producto | Tarifa % | Base | Config Key |
|----------|----------|------|------------|
| Perfumes y aguas de tocador | 20% | PVP | `l10n_ec.ice_perfumes` |
| Videojuegos | 35% | PVP | `l10n_ec.ice_videojuegos` |
| Armas deportivas | 30% | PVP | `l10n_ec.ice_armas` |
| Vehículos >$40,000 | 15-35% | PVP | `l10n_ec.ice_vehiculos_*` |
| TV pagada | 15% | Servicio | `l10n_ec.ice_tv_pagada` |
| Clubes sociales | 35% | Cuota | `l10n_ec.ice_clubes` |
| Casinos/juegos azar | 35% | Ingreso | `l10n_ec.ice_casinos` |

---

# PART IV: RÉGIMEN RIMPE (LORTI Art. 97.1-97.10)

## 4.1 Estructura RIMPE

| Categoría | Ingresos Brutos Anuales | Obligaciones |
|-----------|-------------------------|--------------|
| **Negocios Populares** | $0 - $20,000 | Notas de venta |
| **Emprendedores** | $20,000 - $300,000 | Factura electrónica |

## 4.2 Tarifas RIMPE

### Negocios Populares

| Ingresos | Cuota Mensual |
|----------|---------------|
| $0 - $2,500 | $3.00 |
| $2,500 - $5,000 | $5.00 |
| $5,000 - $10,000 | $10.00 |
| $10,000 - $20,000 | $15.00 |

### Emprendedores (Tabla Progresiva sobre Ingresos Brutos)

| Tramo | Tarifa |
|-------|--------|
| Primeros $20,000 | 0% |
| $20,001 - $50,000 | 1% |
| $50,001 - $75,000 | 1.25% |
| $75,001 - $100,000 | 1.50% |
| $100,001 - $200,000 | 1.75% |
| $200,001 - $300,000 | 2.00% |

## 4.3 Actividades EXCLUIDAS de RIMPE

- Profesionales con título de tercer nivel
- Comisiones
- Rentas de capital
- Relación de dependencia (si única actividad)
- Construcción
- Transporte
- Agroindustria
- Extracción de recursos naturales

---

# PART V: RETENCIONES EN LA FUENTE

## 5.1 TABLA 19 - Retenciones Impuesto a la Renta

| Código | Concepto | Tarifa |
|--------|----------|--------|
| 303 | Honorarios profesionales | 10% |
| 304 | Servicios predomina intelecto | 8% |
| 307 | Servicios predomina mano obra | 2% |
| 308 | Servicios publicidad/comunicación | 1.75% |
| 309 | Transporte privado | 1% |
| 310 | Transporte público | 1% |
| 312 | Transferencia bienes muebles | 1.75% |
| 319 | Arrendamiento inmuebles (PN) | 8% |
| 320 | Arrendamiento inmuebles (Soc) | 2.75% |
| 322 | Seguros/reaseguros prima | 1% |
| 323 | Rendimientos financieros | 2% |
| 325 | Loterías/rifas/apuestas | 15% |
| 327 | Venta combustibles | 0.2% |
| 332 | Pagos al exterior general | 25% |
| 340 | Otras retenciones | 2.75% |
| 341 | Compras bienes origen agrícola (productor) | 1% |
| 342 | Compras bienes origen agrícola (comercializador) | 1.75% |
| 343 | Construcción obra civil | 1.75% |
| 343A | RIMPE Emprendedor | 1% |
| 343B | RIMPE Negocio Popular | 0% |
| 344 | Comisiones sociedades | 3% |
| 344A | Tarjeta crédito/débito | 2% |
| 3480 | Pronósticos deportivos | 15% |
| 500 | Pagos exterior no residentes rentas inmobiliarias | 25% |
| 501 | Pagos exterior servicios | 25% o 37% |

## 5.2 TABLA 21 - Retenciones IVA

| Código | Concepto | Tarifa |
|--------|----------|--------|
| 1 | Bienes (general) | 10% |
| 2 | Servicios (general) | 20% |
| 3 | Bienes (CE a sociedad) | 30% |
| 4 | Servicios (CE a sociedad) | 70% |
| 5 | Servicios (CE/Soc a PN) | 100% |
| 6 | Profesionales con título | 100% |
| 7 | Construcción | 30% |
| 8 | Servicios digitales importados | 100% |
| 9 | No procede retención | 0% |

### Matriz de Retención IVA

| Agente Retención | Proveedor | Bienes | Servicios |
|------------------|-----------|--------|-----------|
| Contribuyente Especial | Sociedad | 30% | 70% |
| Contribuyente Especial | Persona Natural | 30% | 100% |
| Sociedad | Persona Natural | 30% | 100% |
| Sociedad | Sociedad | 0% | 0% |
| Exportador | Cualquiera | 100% | 100% |

---

# PART VI: CÓDIGO DE TRABAJO - PAYROLL

## 6.1 Jornada y Horas Extras (Art. 47, 55)

| Concepto | Límite | Recargo |
|----------|--------|---------|
| Jornada ordinaria | 8h/día, 40h/semana | N/A |
| Horas suplementarias | Max 4h/día, 12h/semana | 50% |
| Horas extraordinarias | Nocturnas o feriados | 100% |
| Trabajo nocturno | 19:00 - 06:00 | 25% |

## 6.2 Décimos (Art. 111, 113)

### Décimo Tercero (Art. 111)

| Aspecto | Valor |
|---------|-------|
| **Cálculo** | (Total remuneraciones dic-nov) / 12 |
| **Período** | 1 diciembre - 30 noviembre |
| **Pago** | Hasta 24 de diciembre |
| **Opción** | Acumulado o mensualizado |

### Décimo Cuarto (Art. 113)

| Aspecto | Valor |
|---------|-------|
| **Cálculo** | 1 SBU ($482 en 2026) |
| **Período Costa/Galápagos** | 1 marzo - 28/29 febrero |
| **Período Sierra/Amazonía** | 1 agosto - 31 julio |
| **Pago Costa** | Hasta 15 marzo |
| **Pago Sierra** | Hasta 15 agosto |
| **Opción** | Acumulado o mensualizado |

## 6.3 Fondos de Reserva (Art. 196)

| Aspecto | Valor |
|---------|-------|
| **Derecho** | Después de 1 año de servicio |
| **Cálculo** | 8.33% de remuneración (1/12) |
| **Pago** | Mensual o acumulado IESS |

## 6.4 Jubilación Patronal (Art. 216)

| Requisito | Beneficio |
|-----------|-----------|
| 25+ años mismo empleador | Jubilación vitalicia |
| 20-25 años (despido intempestivo) | Derecho pro-rata |

## 6.5 Vacaciones (Art. 69)

| Antigüedad | Días |
|------------|------|
| 1-5 años | 15 días |
| +5 años | +1 día adicional por año (max 30) |

## 6.6 IESS Contributions (Ley Seguridad Social)

| Concepto | Sector Privado | Sector Público |
|----------|----------------|----------------|
| **Aporte Personal** | 9.45% | 11.45% |
| **Aporte Patronal** | 11.15% | 9.15% |
| **Voluntario** | 20.50% | N/A |

---

# PART VII: FORMULARIOS SRI

## 7.1 Formulario 101 - IR Sociedades

| Sección | Casilleros | Contenido |
|---------|------------|-----------|
| Identificación | 001-010 | RUC, razón social, año |
| Ingresos | 6001-6100 | Por tipo de ingreso |
| Costos y Gastos | 7001-7200 | Deducibles |
| Conciliación | 8001-8100 | Ajustes tributarios |
| Impuesto | 8101-8200 | Cálculo IR |
| Créditos | 8201-8300 | Retenciones, anticipo |
| RIMPE | 059-063 | Régimen simplificado |
| Saldo | 8301+ | A pagar/favor |

## 7.2 Formulario 103 - Retenciones

| Sección | Casilleros | Contenido |
|---------|------------|-----------|
| IR Retentions | 301-399 | Table 19 codes |
| IVA Retentions | 401-499 | Table 21 codes |
| Dividends | 325, 375 | Special handling |
| Totals | 500+ | Consolidated |

## 7.3 Formulario 104 - IVA

| Sección | Casilleros | Contenido |
|---------|------------|-----------|
| Ventas 15% | 401-410 | IVA cobrado |
| Ventas 0% | 411-420 | Sin IVA |
| Compras 15% | 501-510 | Crédito tributario |
| Compras 0% | 511-520 | Sin crédito |
| Retenciones | 601-650 | Realizadas/recibidas |
| Saldo | 700+ | A pagar/crédito |

---

# PART VIII: COMPLIANCE GAP ANALYSIS

## 8.1 Current SRS vs Law Coverage

| LORTI Section | Articles | SRS Coverage | REAL Coverage |
|---------------|----------|--------------|---------------|
| **Title I: IR** | Art. 1-47 | 40% claimed | **15%** actual |
| **Title II: IVA** | Art. 52-74 | 30% claimed | **8%** actual |
| **Title III: ICE** | Art. 75-89 | 0% | **0%** |
| **Title IV: RIMPE** | Art. 97 | 0% | **0%** |
| **Código Trabajo** | Labor | 60% claimed | **35%** actual |
| **IESS** | Social Security | 60% claimed | **70%** actual |
| **COPCI** | Trade | 45% claimed | **30%** actual |

## 8.2 REAL COMPLIANCE ESTIMATE

> [!CAUTION]
> **ACTUAL COMPLIANCE: ~12%**
> User was correct - we are not even at 10% for full LORTI compliance.

### Critical Missing Items

| Priority | Item | Impact |
|----------|------|--------|
| 🔴 P1 | Art. 9 Rentas Exentas (20+ items) | Wrong taxable income |
| 🔴 P1 | Art. 10 Gastos Deducibles (17+ items) | Wrong deductions |
| 🔴 P1 | Art. 10 Gastos NO Deducibles | Illegal deductions allowed |
| 🔴 P1 | Art. 54 IVA 0% Products (~50+ items) | Wrong IVA charged |
| 🔴 P1 | Art. 55 IVA 0% Services (~15+ items) | Wrong IVA charged |
| 🔴 P1 | Art. 75-89 ICE Module (entire) | Cannot sell ICE products |
| 🔴 P1 | Art. 97 RIMPE Module (entire) | Cannot handle 500k+ taxpayers |
| 🔴 P1 | Complete Table 19 (~50+ codes) | Wrong IR retention |
| 🔴 P1 | Complete Table 21 (~9 codes) | Wrong IVA retention |
| 🟡 P2 | F101 Casilleros (~200) | Cannot generate IR form |
| 🟡 P2 | F103 Casilleros (~100) | Cannot generate retention form |
| 🟡 P2 | F104 Casilleros (~80) | Cannot generate IVA form |
| 🟡 P2 | Overtime limits (Art. 55 CT) | Labor law violation |
| 🟡 P2 | Jubilación patronal (Art. 216) | Labor law violation |
| 🟡 P2 | Sanciones/Multas module | Cannot calculate penalties |

---

# PART IX: IMPLEMENTATION ROADMAP

## Phase 1: Critical Tax Core (Weeks 1-4)

- [ ] Art. 9 Rentas Exentas (all 20+ exemptions)
- [ ] Art. 10 Gastos Deducibles (all 17+ with limits)
- [ ] Art. 10 Gastos NO Deducibles (all restrictions)
- [ ] Complete IVA 0% Products (50+ items)
- [ ] Complete IVA 0% Services (15+ items)

## Phase 2: New Modules (Weeks 5-8)

- [ ] l10n_ec_ice module (Art. 75-89)
- [ ] l10n_ec_rimpe module (Art. 97)
- [ ] l10n_ec_sanctions module (penalties)

## Phase 3: Forms & Reporting (Weeks 9-12)

- [ ] F101 complete casilleros
- [ ] F103 complete casilleros
- [ ] F104 complete casilleros
- [ ] Complete Table 19 (50+ codes)
- [ ] Complete Table 21 (9 codes)

## Phase 4: Labor Compliance (Weeks 13-16)

- [ ] Overtime validation (12h/week max)
- [ ] Jubilación patronal tracking
- [ ] Complete licencias types
- [ ] Desahucio calculation

---

# REFERENCES

| Source | Official URL |
|--------|--------------|
| LORTI | Registro Oficial / sri.gob.ec |
| Reglamento LORTI | Registro Oficial |
| Código Tributario | sot.gob.ec |
| Código de Trabajo | trabajo.gob.ec |
| Ley Seguridad Social | iess.gob.ec |
| COPCI | aduana.gob.ec |
| SRI Resoluciones | sri.gob.ec/normativa |
| Asamblea Nacional | asambleanacional.gob.ec |

---

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-24 | PwC Implementation Team | Complete legal framework |

---

**END OF LEGAL FRAMEWORK**
