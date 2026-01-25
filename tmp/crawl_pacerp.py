import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        # Launch browser (Chromium)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()

        target_url = "https://pacerp.ec"
        print(f"Crawling {target_url}...")

        try:
            response = await page.goto(target_url, timeout=30000, wait_until='networkidle')
            status = response.status
            print(f"Status Code: {status}")

            # Screenshot for verification
            await page.screenshot(path="tmp/pacerp_home.png")

            # Content
            content = await page.content()
            with open("tmp/pacerp_dump.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("HTML dumped to tmp/pacerp_dump.html")

            # Deep Link: Personal y Rol de Pagos (if link exists)
            # Try to find links related to "Rol", "Nomina", "Recursos Humanos"
            links = await page.evaluate('''
                () => {
                    return Array.from(document.querySelectorAll('a')).map(a => ({
                        text: a.innerText,
                        href: a.href
                    }));
                }
            ''')

            print(f"Found {len(links)} links. Scanning for Payroll keywords...")
            for link in links:
                txt = link['text'].lower()
                if any(x in txt for x in ['rol', 'nómina', 'personal', 'humanos']):
                    print(f"Promising Link: {link['text']} -> {link['href']}")
                    # We could follow these recursively but for now listing them is enough for the report

        except Exception as e:
            print(f"Error scraping: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
