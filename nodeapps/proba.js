    const puppeteer = require("puppeteer");

async () => {
        const browser = await puppeteer.launch();

        const page = await browser.newpage();

        await page.goto('https://google.com', {waitUntil: 'networkidle2'});
        const pdf = await page.pdf ({
           path: 'page.pdf',
           printBackground: true,
           format: 'A111'
        });
        return pdf

    await browser.close();

};
