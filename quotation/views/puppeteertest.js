const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch()
    const page = await browser.newPage()
    await page.goto('http://127.0.0.1:8000/quotation/quotationprint/60/')
    await page.pdf({path: 'medium2.pdf', format: 'A4'})
    await browser.close()
})()
