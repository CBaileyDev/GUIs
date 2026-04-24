#!/usr/bin/env node
const path = require('path');
const fs = require('fs');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const HEADLESS = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const ROOT = path.resolve(__dirname, '..');

const TARGETS = [];
for (const bucket of ['styles', 'internal', 'external']) {
  const dir = path.join(ROOT, bucket);
  if (!fs.existsSync(dir)) continue;
  for (const name of fs.readdirSync(dir)) {
    const folder = path.join(dir, name);
    const html = path.join(folder, 'index.html');
    if (fs.existsSync(html)) TARGETS.push({ bucket, name, folder, html });
  }
}

const argNames = process.argv.slice(2);
const selected = argNames.length
  ? TARGETS.filter(t => argNames.includes(t.name) || argNames.includes(`${t.bucket}/${t.name}`))
  : TARGETS;

const INTERNAL_VIEWPORT = { width: 1200, height: 780 };
const DEFAULT_VIEWPORT = { width: 1200, height: 800 };

(async () => {
  const browser = await chromium.launch({ executablePath: HEADLESS, args: ['--no-sandbox'] });
  try {
    for (const t of selected) {
      const viewport = t.bucket === 'internal' ? INTERNAL_VIEWPORT : DEFAULT_VIEWPORT;
      const ctx = await browser.newContext({ viewport, deviceScaleFactor: 1 });
      const page = await ctx.newPage();
      try {
        await page.goto('file://' + t.html, { waitUntil: 'networkidle', timeout: 30000 });
      } catch (e) {
        await page.goto('file://' + t.html, { waitUntil: 'domcontentloaded', timeout: 15000 });
      }
      await page.waitForTimeout(400);
      const outPath = path.join(t.folder, 'preview.png');
      if (t.bucket === 'internal') {
        await page.screenshot({ path: outPath, fullPage: false });
      } else {
        const card = await page.$('.card, .window, .card-wrap, body > .container, body');
        const box = card ? await card.boundingBox() : null;
        if (box) {
          const h = Math.min(Math.max(box.y + box.height + 40, 600), 1600);
          await ctx.close();
          const ctx2 = await browser.newContext({ viewport: { width: 1200, height: Math.ceil(h) }, deviceScaleFactor: 1 });
          const page2 = await ctx2.newPage();
          await page2.goto('file://' + t.html, { waitUntil: 'networkidle', timeout: 30000 }).catch(() =>
            page2.goto('file://' + t.html, { waitUntil: 'domcontentloaded', timeout: 15000 }));
          await page2.waitForTimeout(400);
          await page2.screenshot({ path: outPath, fullPage: false });
          await ctx2.close();
          console.log(`${t.bucket}/${t.name} -> ${outPath} (h=${Math.ceil(h)})`);
          continue;
        } else {
          await page.screenshot({ path: outPath, fullPage: false });
        }
      }
      await ctx.close();
      console.log(`${t.bucket}/${t.name} -> ${outPath}`);
    }
  } finally {
    await browser.close();
  }
})();
