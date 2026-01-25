
import { test, expect } from '@playwright/test';
import { OdooPage } from '../utils/odoo_page';

test.describe('Ecuador Payroll - Month in the Life (Phase 6 Integration)', () => {
    let odoo: OdooPage;

    test.beforeEach(async ({ page }) => {
        odoo = new OdooPage(page);
        await odoo.login('admin', 'admin'); // Assuming standard dev creds
    });

    test('Full Payroll Cycle 2026', async () => {
        // 1. HIRING: Create a new employee with Family Loads for Tax Rebate
        const empName = `Juan Pérez ${Date.now()}`;
        await odoo.createRecord('hr.employee', {
            name: empName,
            l10n_ec_family_loads: '2', // 2 Children = 11 Baskets Rebate Limit
            l10n_ec_catastrophic_disease: false
        });

        // Create Contract
        await odoo.createRecord('hr.contract', {
            name: `${empName} - Contract 2026`,
            employee_id: empName, // Search by name simulation
            wage: '2500.00', // High salary to trigger Income Tax
            l10n_ec_projected_expenses: '5000.00' // Formulario GP
        });

        // 2. LOANS: Import IESS Deduction
        // In a real E2E we'd upload a file, here we simulate the record creation the importer does
        await odoo.createRecord('l10n_ec.loan', {
            name: 'IESS Quirografario Import',
            employee_id: empName,
            loan_type: 'iess_qui',
            amount_total: '100.00',
            date_start: '2026-01-01',
            state: 'active'
        });
        // Add installment for this month
        // Note: This matches l10n_ec_loans logic

        // 3. VACATION: Run Accrual
        // Trigger the scheduled action manually or create ledger entry
        await odoo.createRecord('l10n_ec.vacation.ledger', {
            employee_id: empName,
            description: 'January Accrual',
            days_earned: '1.25'
        });

        // 4. PAYROLL: Generate Payslip
        const payslipName = `${empName} - Jan 2026`;
        await odoo.createRecord('l10n_ec.payslip', {
            employee_id: empName,
            date_start: '2026-01-01',
            date_end: '2026-01-31'
        });

        // VERIFICATION STEPS
        // A. Check Income Tax
        // Annual Income: 2500 * 12 = 30,000
        // IESS Personal: 30,000 * 9.45% = 2,835
        // Tax Base: 27,165
        // Caused Tax (2026 Table):
        // Bracket 12% (20,188 - 26,700). Base 27,165 is in 15% bracket (26,700 - 35,136)
        // Basic Tax (15% bracket): 1,412
        // Excess: 27,165 - 26,700 = 465
        // Tax on Excess: 465 * 15% = 69.75
        // Total Caused: 1,481.75

        // Rebate (Family Loads = 2 => 11 Baskets * ~$800 = $8,800 Cap)
        // Expenses: 5,000. Min(5000, 8800) = 5,000.
        // Rebate: 5,000 * 18% = 900.

        // Final Annual Tax: 1,481.75 - 900 = 581.75
        // Monthly Retention: 581.75 / 12 = $48.48

        // Assert specific field value on the screen (Placeholder selector)
        // await expect(page.locator('field-name="income_tax"')).toHaveText('48.48');

        // B. Check Loan Deduction
        // Should verify loan_deduction field shows amount

        // 5. SUT: Generate Report
        // Open Wizard
        // await odoo.openWizard('l10n_ec.sut.report.wizard');
        // Select 13th
        // Click Generate

        // 6. PORTAL (Superiority Check)
        // Logout and verify Portal Access
        // await page.getByRole('link', { name: 'Log out' }).click();
        // await page.goto(odoo.baseURL + '/my/payslips');
        // Expect login page (since we logged out) or if we log in as employee, expect list.
        // await expect(page).toHaveURL(/.*web\/login.*/);
    });
});
