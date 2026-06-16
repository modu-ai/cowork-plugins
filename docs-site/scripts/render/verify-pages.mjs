// 실제 Hugo 사이트(localhost:1313) 페이지의 mermaid 렌더링 결과 검증
// 각 페이지의 .mermaid 요소가 svg 자식을 가졌는지(렌더링 성공) 확인
import puppeteer from 'puppeteer';

const BASE = 'http://localhost:1313';
const pages = [
  '/',
  '/plugins/',
  '/plugins/moai-tutor/',
  '/getting-started/quick-start/',
  '/cookbook/skill-chaining/',
  '/cookbook/business-plan/',
  '/cookbook/track-marketing/',
  '/claude-design/',
  '/cowork/skills/',
  '/cowork/permissions/',
];

const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
const page = await browser.newPage();
const report = [];

for (const path of pages) {
  const url = BASE + path;
  const errs = [];
  page.on('pageerror', e => errs.push(String(e).slice(0, 120)));
  try {
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 25000 });
    await new Promise(r => setTimeout(r, 2000)); // mermaid 비동기 렌더링 대기
    const status = await page.evaluate(() => {
      const els = [...document.querySelectorAll('.mermaid')];
      return els.map((el, i) => {
        const hasSvg = !!el.querySelector('svg');
        const txt = (el.textContent || '').replace(/\s+/g, ' ').trim();
        const looksErr = /syntax error|parse error|error in/i.test(txt);
        return { i, hasSvg, looksErr, preview: txt.slice(0, 50) };
      });
    });
    const bad = status.filter(s => !s.hasSvg || s.looksErr);
    report.push({ path, total: status.length, bad, pageErrors: errs.slice(0, 3) });
  } catch (e) {
    report.push({ path, error: e.message.split('\n')[0].slice(0, 120) });
  }
  page.removeAllListeners('pageerror');
}
await browser.close();

const totalBad = report.reduce((a, r) => a + (r.bad ? r.bad.length : 0), 0);
console.error(`\n검증 완료: ${report.length}페이지, 렌더링 실패 mermaid ${totalBad}개`);
for (const r of report) {
  const tag = (r.bad && r.bad.length) ? `❌ ${r.bad.length}실패` : '✓';
  console.error(`  ${tag} ${r.path} (mermaid ${r.total || 0})`);
  if (r.bad) for (const b of r.bad) console.error(`     #${b.i} svg=${b.hasSvg} err=${b.looksErr} "${b.preview}"`);
}
console.log(JSON.stringify(report, null, 2));
