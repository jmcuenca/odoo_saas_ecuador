# VIBE CODING RULES & ODOO 18 STANDARDS
> **Authority**: 10-Persona Implementation Team
> **Enforcement**: AUTOMATIC & MANDATORY

## 1. Odoo 18 Technical Mandates
All code must comply with Odoo 18 breaking changes.

### ❌ FORBIDDEN (Deprecated)
- **`<tree>`**: Replaced by `<list>`.
- **`attrs="{...}"`**: Replaced by `invisible="..."` or `readonly="..."` (Python domains).
- **`states="..."`**: Removed. Use `invisible` or `readonly` domains.
- **`@api.one`**: Removed (iterate `self` instead).
- **Manual Translation (`trans=True`)**: Use `_()` or `lazy_gettext`.

### ✅ REQUIRED (Standard)
- **Review Views**: ALWAYS start with `<list>` for list views.
- **Domains**: Use Python syntax for domains in XML `invisible="state == 'draft'"`.
- **Models**: Explicitly define `_description` for all models.
- **Reporting**: Use `ir.actions.report` with `report_type="qweb-pdf"`.

## 2. Vibe Coding Rules (Philosophy)
- **NO PLACEHOLDERS**: Never write `pass`, `# TODO`, or `return True`. Implement the logic.
- **REAL DATA ONLY**: Use actual SRI codes (Table 19, 21, 6), not `"TEST_CODE"`.
- **CONFIG DRIVEN**: Hardcoded rates = FAILURE. Use `ir.config_parameter`.
- **DOCUMENTATION**: Every module requires a `README.rst` or `__manifest__.py` description.

## 3. Testing Standards
- **Wait for Docker**: Verify against the REAL container (`docker compose exec`).
- **Clean State**: Tests must run on a database seeded with `l10n_ec` data.
- **E2E**: Use Playwright for Critical User Journeys (Emission, Retention).
- **Unit**: Use `odoo-bin --test-enable` for Tax/Calculation logic.

## 4. Architecture Standards
- **Modules**: 1 Feature = 1 Module (`l10n_ec_ice`, `l10n_ec_rimpe`).
- **Dependencies**: Explicitly list all dependent modules (e.g., `account`, `l10n_ec`).
- **Security**: EVERY model must have `ir.model.access.csv`.

**Signed:**
*Dr. Fernando Vega (Technical Architect)*
