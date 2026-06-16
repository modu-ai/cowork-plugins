// mermaid 블록 전수 lint — content/ 원본을 mermaid 11.14.0 으로 렌더링 검증
// 사용: node lint-mermaid.mjs   (실패 블록만 JSON 출력)
import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const CONTENT_DIR = '/Users/goos/MoAI/MoAI-Cowork-Plugins/docs-site/content';
const MERMAID_CDN = 'https://cdn.jsdelivr.net/npm/mermaid@11.14.0/dist/mermaid.min.js';

function extract(dir, blocks = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (e.name !== 'releases') extract(p, blocks);
    } else if (e.name.endsWith('.md')) {
      const lines = fs.readFileSync(p, 'utf8').split('\n');
      let i = 0;
      while (i < lines.length) {
        if (lines[i].trim() === '```mermaid') {
          const start = i + 1;
          const c = [];
          i++;
          while (i < lines.length && lines[i].trim() !== '```') { c.push(lines[i]); i++; }
          blocks.push({ file: path.relative(CONTENT_DIR, p), line: start, content: c.join('\n') });
        }
        i++;
      }
    }
  }
  return blocks;
}

const blocks = extract(CONTENT_DIR);
console.error(`mermaid 블록 ${blocks.length}개 추출 — 검증 시작`);

const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage();
const pageErrors = [];
page.on('pageerror', e => pageErrors.push(String(e).slice(0, 200)));

const bootstrap = `<!doctype html><html><head><meta charset="utf-8">
<script src="${MERMAID_CDN}"></script></head><body></html>`;
await page.setContent(bootstrap, { waitUntil: 'networkidle0', timeout: 30000 });
await page.waitForFunction(() => typeof mermaid !== 'undefined' && mermaid.initialize, { timeout: 15000 });
await page.evaluate(() => mermaid.initialize({ startOnLoad: false, suppressErrorRendering: true }));

const failures = [];
let checked = 0;
for (const b of blocks) {
  const result = await page.evaluate(async (c) => {
    try {
      const id = 'm' + Math.random().toString(36).slice(2);
      await mermaid.render(id, c);
      return { ok: true };
    } catch (e) {
      const msg = String((e && e.message) || e);
      return { ok: false, err: msg.split('\n').slice(0, 3).join(' | ').slice(0, 300) };
    }
  }, b.content);
  checked++;
  if (!result.ok) {
    failures.push({
      file: b.file,
      line: b.line,
      err: result.err,
      preview: b.content.split('\n').slice(0, 6).join('\n')
    });
    console.error(`❌ ${b.file}:${b.line} — ${result.err.slice(0, 80)}`);
  }
  if (checked % 50 === 0) console.error(`  ... ${checked}/${blocks.length}`);
}

await browser.close();
console.error(`\n검증 완료: ${checked}개 중 ${failures.length}개 실패`);
console.log(JSON.stringify({ total: checked, failed: failures.length, failures }, null, 2));
