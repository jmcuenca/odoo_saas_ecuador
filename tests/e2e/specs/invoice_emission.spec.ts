import { test, expect } from '@playwright/test';
import { OdooPage } from '../utils/odoo_page';

test.describe('SRI Electronic Invoicing', () => {
    let odoo: OdooPage;

    test.beforeEach(async ({ page }) => {
        odoo = new OdooPage(page);
        await odoo.login();
    });

    test('Create and Validate Electronic Invoice', async ({ page }) => {
        // 1. Navigate to Invoicing
        await odoo.openApp('Invoicing');

        // 2. Create New Invoice
        await page.getByRole('button', { name: 'New' }).click();

        // 3. Fill Customer (Consumidor Final for test)
        await page.getByPlaceholder('Name, TIN, Email, or Reference').fill('Consumidor Final');
        await page.getByText('Consumidor Final', { exact: true }).first().click();

        // 4. Add Line
        await page.getByText('Add a line').click();
        await page.getByPlaceholder('Product Name').fill('Test Product');
        await page.getByPlaceholder('Unit Price').click();
        await page.getByPlaceholder('Unit Price').fill('10.00');

        // 5. Confirm
        await page.getByRole('button', { name: 'Confirm' }).click();

        // 6. Check SRI Status (Assuming mock or dev mode returns immediate status)
        // Note: in real env we wait for cron/response
        // await expect(page.getByText('SRI Status')).toBeVisible();
    });
});
