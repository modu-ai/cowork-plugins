#!/usr/bin/env node
// docs-site health gate — 릴리스 게이트용 자동 검증
// (1) 카운트 실측 정합 (2) 구버전 카운트 잔재 (3) 본문 버전 마커 누적 (4) Nano Banana/fal.ai 잔재
// 사용: node check-docs-health.mjs   (exit 0 = PASS, exit 1 = 위반 존재)
// 추가: CLAUDE.local.md §4-2 게이트 2·6, §10-4, feedback_fal_ai_deprecated 준거
import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const CONTENT = path.join(ROOT, 'docs-site/content');

const skillCount = parseInt(execSync(`find ${ROOT}/moai-*/skills -name SKILL.md | wc -l`, { encoding: 'utf8' }).trim(), 10);
const pluginCount = parseInt(execSync(`ls -d ${ROOT}/moai-*/ | wc -l`, { encoding: 'utf8' }).trim(), 10);

const mdFiles = execSync(`find ${CONTENT} -name '*.md'`, { encoding: 'utf8' }).trim().split('\n')
  .filter(f => f && !f.includes('/releases/') && !f.includes('/.moai/'));

const findings = [];
for (const f of mdFiles) {
  let txt;
  try { txt = fs.readFileSync(f, 'utf8'); } catch { continue; }
  const rel = path.relative(CONTENT, f);
  // 구버전 스킬 카운트 (현재 178이 아닌 구값) — releases/ 제외했으므로 본문에 남으면 위반
  const staleSkill = txt.match(/\b(21|129|144|73|35)\s*(개)?\s*(스킬|skills?)\b/gi) || [];
  if (staleSkill.length) findings.push({ file: rel, type: 'stale-skill-count', matches: staleSkill });
  // 구버전 플러그인 카운트 (현재 28이 아닌 구값)
  const stalePlugin = txt.match(/\b(17|21)\s*(개)?\s*(플러그인|plugins?)\b/gi) || [];
  if (stalePlugin.length) findings.push({ file: rel, type: 'stale-plugin-count', matches: stalePlugin });
  // 본문 버전 마커 — plugins/_index 카탈로그 "v2.X 신규"는 스킬 도입 메타데이터로 보존(사용자 결정). Wave/출시예정만 경고.
  const markers = txt.match(/Wave\s*\d+|출시\s*예정/gi) || [];
  if (markers.length) findings.push({ file: rel, type: 'version-marker', matches: markers });
  // fal.ai 서비스 잔재 (feedback_fal_ai_deprecated). Nano Banana는 Higgsfield MCP 공식 모델명이므로 제외.
  const fal = txt.match(/(fal\.ai|fal-ai|FAL_KEY|fal-gateway)/gi) || [];
  if (fal.length) findings.push({ file: rel, type: 'fal-residue', matches: fal });
}

const result = {
  measured: { skills: skillCount, plugins: pluginCount, expected: { skills: 178, plugins: 28 } },
  countMatch: skillCount === 178 && pluginCount === 28,
  findings,
  findingCount: findings.length,
  verdict: findings.length === 0 && skillCount === 178 && pluginCount === 28 ? 'PASS' : 'FAIL',
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.verdict === 'PASS' ? 0 : 1);
