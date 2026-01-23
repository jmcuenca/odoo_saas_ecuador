// @ts-check
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
    testDir: './specs',
    timeout: 60000,
    fullyParallel: true,
    retries: 1,
    workers: 1, // Sequential for Odoo state capability
    reporter: 'html',
    use: {
        baseURL: 'http://localhost:24500',
        trace: 'on-first-retry',
        video: 'retain-on-failure',
        screenshot: 'only-on-failure',
        ignoreHTTPSErrors: true,
    },
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
    ],
});
