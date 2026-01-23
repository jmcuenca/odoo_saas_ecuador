const { test, expect } = require('@playwright/test');

test.describe('SRI Electronic Invoicing Flow', () => {

    test.beforeEach(async ({ page }) => {
        // 1. Login
        await page.goto('/web/login');
        await page.fill('input[name="login"]', 'admin');
        await page.fill('input[name="password"]', 'admin');
        await page.click('button[type="submit"]');
        await expect(page).toHaveURL(/web/);
    });

    test('Create Invoice and Send to SRI', async ({ page }) => {
        // Monitor Console Errors
        page.on('console', msg => {
            if (msg.type() === 'error')
                console.log(`Error text: "${msg.text()}"`);
            else
                console.log(`Console: "${msg.text()}"`);
        });

        // 2. Go to Invoicing (Deep Link with Wait)
        // Wait for Home Action (Discuss) to settle
        await page.waitForTimeout(5000);
        console.log('Navigating to Invoicing Action...');

        // Force navigation
        await page.goto('/web#cids=1&action=account.action_move_out_invoice_type');

        // Wait for valid view
        // .o_list_view or .o_kanban_view
        try {
            await expect(page.locator('.o_list_view, .o_kanban_view')).toBeVisible({ timeout: 15000 });
        } catch (e) {
            console.log('View not visible. URL:', page.url());
            console.log('Page content snippet:', (await page.content()).slice(0, 1000));
            throw e;
        }

        // 3. Create New Invoice
        // Try multiple selectors for "New"
        // Odoo 18: btn-primary, name="create"? or just text "New"
        // In Kanban, it's also "New".
        const newBtn = page.getByRole('button', { name: 'New' });
        await expect(newBtn).toBeVisible();
        await newBtn.click();

        // 4. Fill Partner
        // Wait for form view
        await expect(page.locator('.o_form_view')).toBeVisible();

        const partnerInput = page.locator('div[name="partner_id"] input').first();
        await partnerInput.click();
        await partnerInput.fill('Consumidor Final');
        await page.waitForTimeout(2000); // Wait for search
        await page.keyboard.press('Enter');

        // 5. Add Line
        // If "Add a line" exists
        const addLine = page.getByRole('button', { name: 'Add a line' });
        if (await addLine.isVisible()) {
            await addLine.click();
        } else {
            // Maybe it's one2many list adding?
            // Click the product field directly if row exists
            // But usually we need to add row first.
            console.log('Add a line button not found, trying invoice_line_ids click');
            await page.click('div[name="invoice_line_ids"]');
        }

        const productInput = page.locator('div[name="product_id"] input').first();
        await productInput.fill('Test Product');
        await page.waitForTimeout(2000); // Wait for product search
        await page.keyboard.press('Enter');

        // 6. Confirm (Post)
        await page.getByRole('button', { name: 'Confirm' }).click();

        // 7. Verify Status is Posted
        await expect(page.locator('div[name="state"]')).toContainText('Posted');

        // 8. Send to SRI
        const sendBtn = page.getByRole('button', { name: 'Send to SRI' });
        await expect(sendBtn).toBeVisible();
        await sendBtn.click();

        // 9. Assert SRI Status
        // Wait for any change
        await page.waitForTimeout(2000);
        await expect(page.locator('div[name="l10n_ec_sri_status"]')).not.toContainText('Draft');
    });

});
