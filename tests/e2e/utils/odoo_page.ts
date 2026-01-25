import { Page, expect } from '@playwright/test';

export class OdooPage {
    readonly page: Page;
    readonly baseURL: string;

    constructor(page: Page) {
        this.page = page;
        this.baseURL = 'http://localhost:24500';
    }

    async login(user: string = 'admin', pass: string = 'admin') {
        await this.page.goto(this.baseURL + '/web/login');
        await this.page.getByLabel('Email').fill(user);
        await this.page.getByLabel('Password').fill(pass);
        await this.page.getByRole('button', { name: 'Log in' }).click();
        await expect(this.page).toHaveURL(/.*web#.*/); // Wait for dashboard
    }

    async openApp(appName: string) {
        await this.page.getByTitle('Home Menu').click();
        await this.page.getByRole('menuitem', { name: appName }).click();
    }
}
