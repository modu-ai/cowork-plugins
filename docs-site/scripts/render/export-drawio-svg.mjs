// drawio .html (CDN viewer-static.min.js) → SVG 추출
// 사용: node export-drawio-svg.mjs
import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const DIAGRAMS_DIR = '/Users/goos/MoAI/MoAI-Cowork-Plugins/docs-site/static/diagrams';
const htmlFiles = fs.readdirSync(DIAGRAMS_DIR).filter(f => f.endsWith('.html')).sort();

console.error(`대상: ${htmlFiles.length}개 drawio HTML`);

const results = [];

async function renderOne(f) {
  const slug = f.replace(/\.html$/, '');
  const fileUrl = 'file://' + path.join(DIAGRAMS_DIR, f);
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-extensions'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 1200, deviceScaleFactor: 2 });
  try {
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.waitForFunction(
      () => { const svg = document.querySelector('div.mxgraph svg'); return svg && svg.children.length > 0; },
      { timeout: 25000 }
    );
    await new Promise(r => setTimeout(r, 1200));
    const svg = await page.evaluate(() => {
      const el = document.querySelector('div.mxgraph svg');
      if (!el) return null;
      const clone = el.cloneNode(true);
      let w = parseFloat(clone.getAttribute('width'));
      let h = parseFloat(clone.getAttribute('height'));
      let vb = clone.getAttribute('viewBox');
      if (!vb || !w || !h) {
        try {
          const bbox = el.getBBox();
          w = w || Math.ceil(bbox.width + bbox.x);
          h = h || Math.ceil(bbox.height + bbox.y);
          if (!vb) vb = `0 0 ${Math.ceil(w)} ${Math.ceil(h)}`;
        } catch (e) { /* fallback 유지 */ }
      }
      clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      clone.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink');
      clone.setAttribute('width', w);
      clone.setAttribute('height', h);
      if (vb) clone.setAttribute('viewBox', vb);
      return clone.outerHTML;
    });
    if (svg && svg.length > 50) {
      const out = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + svg;
      fs.writeFileSync(path.join(DIAGRAMS_DIR, slug + '.svg'), out);
      return { slug, ok: true, bytes: out.length };
    }
    return { slug, ok: false, err: 'svg empty' };
  } catch (e) {
    return { slug, ok: false, err: e.message.split('\n')[0].slice(0, 120) };
  } finally {
    await page.close().catch(() => {});
    await browser.close().catch(() => {});
  }
}

for (const f of htmlFiles) {
  const r = await renderOne(f);
  results.push(r);
  console.error(r.ok ? `  ✓ ${r.slug}` : `  ❌ ${r.slug}: ${r.err}`);
}

const ok = results.filter(r => r.ok);
const fail = results.filter(r => !r.ok);
console.error(`\n성공 ${ok.length}/${results.length}`);
if (fail.length) {
  console.error('실패:');
  for (const r of fail) console.error(`  ❌ ${r.slug}: ${r.err}`);
}
console.log(JSON.stringify(results, null, 2));
