export const meta = {
  name: 'hns-www-docs-run',
  description: 'www 온라인 문서 작성 하네스 Runner — manifest 기반 specialist dispatch (Pipeline + Producer-Reviewer)',
  phases: [
    { title: 'Classify', detail: '요청 분류: 작성/동기화/감사' },
    { title: 'Write', detail: '본문 + 멀티모달(mermaid 직접·SVG 직접·Higgsfield 위임)' },
    { title: 'Polish', detail: '한국어 윤문 (slop-reviewer → humanize-korean)' },
    { title: 'Audit', detail: 'DS·WCAG·빌드·한국어 비평적 감사' },
    { title: 'Sync', detail: '플러그인/스킬 변경 → www 전파 (조건부)' },
  ],
}

// manifest SSOT — hns-www-docs-{writer,polish,audit,sync}-specialist 의 dispatch 정의가 여기 있다.
const MANIFEST_PATH = '.claude/commands/harness/www-docs/manifest.json'
const req = (typeof globalThis !== 'undefined' && globalThis.args && globalThis.args.request) || '(요청 없음)'

// Phase 0: 요청 분류 — 어느 흐름으로 갈지 (write 파이프라인 / sync 단독 / audit 단독)
phase('Classify')
const intent = await agent(
  `다음 www 문서 요청을 분류하라.\n요청: ${req}\n\n` +
    '분류 기준:\n' +
    '- "write": 새 문서 작성 또는 기존 문서 본문 작성/수정 (가이드·쿡북·릴리스 노트)\n' +
    '- "sync": 플러그인/스킬/에이전트의 추가·업데이트·삭제를 www 문서에 전파\n' +
    '- "audit": 기존 문서의 DS 규칙·대비·빌드 품질 감사 (본문 작성 아님)\n',
  {
    phase: 'Classify',
    effort: 'low',
    schema: {
      type: 'object',
      properties: {
        kind: { enum: ['write', 'sync', 'audit'] },
        target: { type: 'string', description: '대상 문서/경로/변경 대상' },
        notes: { type: 'string', description: '추가 맥락' },
      },
      required: ['kind', 'target'],
    },
  }
)

// ── sync 흐름: 단독 (코드 변경 → www 전파). write 파이프라인과 분리.
if (intent.kind === 'sync') {
  phase('Sync')
  const syncResult = await agent(
    `플러그인/스킬/에이전트 변경을 www 온라인 문서에 전파하라.\n` +
      `대상 변경: ${intent.target}\n추가 맥락: ${intent.notes || '(없음)'}\n\n` +
      `hns-www-docs-sync-specialist 역할을 수행하라. manifest: ${MANIFEST_PATH}.\n` +
      `1) gen-agent-teams.py 재실행으로 data/agent_teams.json 재생성(marketplace SSOT 기반)\n` +
      `2) 영향 받는 에이전트 페이지(www/content/moai-agents/)·플러그인 페이지(www/content/plugins/) 갱신\n` +
      `3) menu/main.yaml 동기화(필요 시) 4) README·릴리스 노트 반영(필요 시)\n` +
      `design-logo 추가 시처럼 — 스킬 추가가 www 4~5곳에 전파되던 손작업을 자동화한다.`,
    { phase: 'Sync', agentType: 'hns-www-docs-sync-specialist' }
  )
  return { kind: 'sync', target: intent.target, result: syncResult }
}

// ── write 파이프라인: writer → polish → audit (Pipeline + Producer-Reviewer)
phase('Write')
const written = await agent(
  `www 온라인 문서(Hugo/Geekdoc)를 작성하라.\n대상: ${intent.target}\n추가 맥락: ${intent.notes || '(없음)'}\n\n` +
    `hns-www-docs-writer-specialist 역할을 수행하라. manifest: ${MANIFEST_PATH}.\n` +
    `필수: 한국어 경어체, 전문용어 한국어(영문) 병기(스킬·플러그인), 슬러그 영문 케밥, ` +
    `페이지 하단 Sources 섹션, per-page mermaid 최소 1개(REQ-IA-019).\n` +
    `멀티모달: 구조/플로우 다이어그램은 mermaid 코드블록 직접 삽입(foot.html이 DS 팔레트 자동 적용), ` +
    `정확한 숫자/라벨 인포그래픽은 인라인 SVG 직접 저작(inline-svg-infographics 패턴), ` +
    `히어로/장식/로고는 Skill()로 위임(design-logo·design-brand-visual·media-higgsfield-image).`,
  { phase: 'Write', agentType: 'hns-www-docs-writer-specialist' }
)

phase('Polish')
const polished = await agent(
  `다음 www 문서 원고를 한국어 윤문하라 — AI 번역체(AI tell)를 제거하되 의미·사실·고유명사는 불변.\n` +
    `hns-www-docs-polish-specialist 역할. 2단계 체인:\n` +
    `  1) Skill("general-ai-slop-reviewer") — 범용 AI 슬롯 1차 제거\n` +
    `  2) Skill("general-humanize-korean") — 한국어 정밀 윤문 2차\n` +
    `과교정 가드레일: prose 변경률 30% WARN / 50% HALT. mermaid 코드블록은 건드리지 말 것(라벨 자연어는 본문 일부로 다듬기).\n\n원고:\n${written}`,
  { phase: 'Polish', agentType: 'hns-www-docs-polish-specialist' }
)

phase('Audit')
const verdict = await agent(
  `다음 www 문서를 비평적 감사하라(Producer-Reviewer — 관대성 금지, 의심 우선).\n` +
    `hns-www-docs-audit-specialist 역할. manifest: ${MANIFEST_PATH}.\n` +
    `검사 차원:\n` +
    `  - DS 규칙(이모지 금지·Lucide 아이콘·금지 폰트·CSS 구조) — must-pass\n` +
    `  - WCAG AA 대비 4.5:1 (cd www && python3 scripts/check-contrast.py) — must-pass\n` +
    `  - 빌드 (cd www && hugo --logLevel error) — must-pass\n` +
    `  - 내부 링크 (node scripts/check-links.mjs) — must-pass\n` +
    `  - 한국어 번역체 잔존 (S1/S2/S3) — threshold 0.9\n` +
    `  - per-page mermaid (REQ-IA-019) — must-pass\n` +
    `하나라도 must-pass 어긋나면 FAIL + 구체적 조치 제안. 근사치 PASS 금지.\n\n문서:\n${polished}`,
  {
    phase: 'Audit',
    agentType: 'hns-www-docs-audit-specialist',
    effort: 'high',
    schema: {
      type: 'object',
      properties: {
        verdict: { enum: ['PASS', 'FAIL'] },
        findings: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              dimension: { type: 'string' },
              severity: { enum: ['critical', 'major', 'minor'] },
              fix: { type: 'string' },
            },
          },
        },
      },
      required: ['verdict'],
    },
  }
)

return { kind: intent.kind, target: intent.target, written, polished, audit: verdict }
