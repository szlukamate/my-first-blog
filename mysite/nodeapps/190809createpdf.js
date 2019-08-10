var myArgs = process.argv.slice(2);
console.log('myArgs: ', myArgs);
// myArgs[0]: path
// myArgs[1]: pdffilename
// myArgs[2]: applicableipaddress (local vs. AWS)
// myArgs[3]: docid

const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(' http://' + myArgs[2] + ':8000/quotation/quotationprint/' + myArgs[3] + '/', {waitUntil: 'networkidle2'});
  await page.pdf({path: '' + myArgs[0] + myArgs[1], format: 'A4'});

  await browser.close();
})();
