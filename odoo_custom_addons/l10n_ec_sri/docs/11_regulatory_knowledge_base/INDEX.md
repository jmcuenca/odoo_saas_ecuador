# REGULATORY KNOWLEDGE BASE INDEX
## Ecuador ERP Localization Reference

**Created**: 2026-01-22
**Purpose**: Verified regulatory reference for AI agents and developers

---

## KNOWLEDGE BASE ENTRIES

| Entry ID | File | Topic | Verification Status |
|:---------|:-----|:------|:--------------------|
| **KB-SRI-001** | [KB_SRI_ELECTRONIC_INVOICING.md](./KB_SRI_ELECTRONIC_INVOICING.md) | SRI E-Invoicing, Ficha Técnica, XSD versions | ✅ VERIFIED |
| **KB-LABOR-001** | [KB_LABOR_SBU_DECIMOS.md](./KB_LABOR_SBU_DECIMOS.md) | SBU 2026, Décimo 13/14 calculations | ✅ VERIFIED |
| **KB-IESS-001** | [KB_IESS_CONTRIBUTIONS.md](./KB_IESS_CONTRIBUTIONS.md) | IESS contribution rates | ⚠️ VERIFY |
| **KB-TAX-001** | [KB_TAX_RATES_WITHHOLDINGS.md](./KB_TAX_RATES_WITHHOLDINGS.md) | IVA, IR withholding codes | ✅ VERIFIED |

---

## KEY VERIFIED VALUES FOR 2026

| Parameter | Value | Source | Date Verified |
|:----------|:------|:-------|:--------------|
| **SBU** | $482.00 | Acuerdo Ministerial | Jan 2026 |
| **IVA Standard** | 15% | LORTI | Jan 2026 |
| **IVA Construction** | 5% | LORTI | Jan 2026 |
| **IESS Personal** | 9.45% | Ley Seg. Social | Jan 2026 |
| **IESS Patronal** | 12.15% | Ley Seg. Social | Jan 2026 |
| **Ficha Técnica** | v2.32 | SRI (Nov 2025) | Jan 2026 |
| **CF Limit** | $50.00 | UAFE | Jan 2026 |
| **Décimo 13 Deadline** | Dec 24 | CT Art. 95-96 | Jan 2026 |
| **Décimo 14 (Coast)** | Mar 15 | CT Art. 97 | Jan 2026 |
| **Décimo 14 (Sierra)** | Aug 15 | CT Art. 97 | Jan 2026 |

---

## OFFICIAL SOURCES

| Source | URL | Content |
|:-------|:----|:--------|
| **SRI** | https://www.sri.gob.ec | Tax regulations, e-invoicing |
| **IESS** | https://www.iess.gob.ec | Social security |
| **Min. Trabajo** | https://www.trabajo.gob.ec | Labor law |
| **Super. Compañías** | https://portal.supercias.gob.ec | Company regulations |
| **Ecuador Legal** | https://www.ecuadorlegalonline.com | Legal reference |

---

## USAGE INSTRUCTIONS

### For AI Agents
When answering questions about Ecuador ERP localization:
1. Check this knowledge base FIRST
2. Cite the KB entry ID in responses
3. Note verification status
4. Flag items marked ⚠️ VERIFY for user confirmation

### For Developers
When implementing l10n_ec modules:
1. Use values from this knowledge base
2. Store configurable parameters (SBU, rates) in system settings
3. Design for annual updates (SBU changes every year)
4. Implement validation based on documented rules

---

## VERIFICATION SCHEDULE

| Entry | Next Review |
|:------|:------------|
| KB-SRI-001 | 2026-07-01 |
| KB-LABOR-001 | 2027-01-01 |
| KB-IESS-001 | 2026-02-01 |
| KB-TAX-001 | 2026-07-01 |

---

**Knowledge Base Maintainer**: Implementation Team
**Last Updated**: 2026-01-22
