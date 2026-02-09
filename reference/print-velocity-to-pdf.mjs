#!/usr/bin/env node
/**
 * One-off: generate PDF of ECOSYSTEM_VELOCITY_AND_VALUE.html
 * Run: node reference/print-velocity-to-pdf.mjs
 */
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, 'ECOSYSTEM_VELOCITY_AND_VALUE.html');
const pdfPath = path.join(__dirname, 'ECOSYSTEM_VELOCITY_AND_VALUE.pdf');
const fileUrl = 'file://' + htmlPath;

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(fileUrl, { waitUntil: 'networkidle' });
await page.waitForTimeout(3500);
await page.emulateMedia({ media: 'print' });
await page.pdf({
  path: pdfPath,
  format: 'A4',
  printBackground: true,
  margin: { top: '16px', right: '16px', bottom: '16px', left: '16px' }
});
await browser.close();
console.log('PDF written:', pdfPath);
