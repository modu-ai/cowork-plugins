// harness-builder-run.js — Runner for /harness:builder
// Reads manifest.json (SSOT) and dispatches 5 specialists across the 7-Phase pipeline.
// Patterns: Pipeline (stage N feeds N+1) + Producer-Reviewer (curator evaluates).
//
// This is the generated dynamic-workflow Runner that executes INSIDE /harness:builder.
// The Builder (creation) was orchestrator-direct; execution runs here.

export const meta = {
  name: 'harness-builder-run',
  description: 'Runner for /harness:builder — 7-Phase desktop plugin (cowork/code) skill generator with 3-Layer research + audit',
  phases: [
    { title: 'Discovery', detail: 'intent-parser: natural-language → plugin + topic + intent' },
    { title: '3-Layer Research', detail: 'research-collector: qmd vault → Claude docs → web' },
    { title: 'Curation', detail: 'plugin-curator: 4-dimension rubric, top-5' },
    { title: 'Selection', detail: 'orchestrator AskUserQuestion gate' },
    { title: 'Build', detail: 'skill-builder: plugin skill under category constraints' },
    { title: 'Audit', detail: 'auditor: Claude official doc criteria gate (PASS/violations)' },
    { title: 'Report', detail: 'final summary with audit verdict' },
  ],
}

const INTENT_SCHEMA = {
  type: 'object',
  properties: {
    target_plugin: { type: 'string', enum: ['cowork', 'code'] },
    skill_topic: { type: 'string' },
    intent: { type: 'string' },
    keywords: { type: 'array', items: { type: 'string' } },
    constraints: { type: 'array', items: { type: 'string' } },
  },
  required: ['target_plugin', 'skill_topic', 'keywords'],
}

const CURATION_SCHEMA = {
  type: 'object',
  properties: {
    top5: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          source: { type: 'string' },
          layer: { type: 'string', enum: ['qmd', 'docs', 'web'] },
          scores: {
            type: 'object',
            properties: {
              relevance: { type: 'number' },
              specificity: { type: 'number' },
              practicality: { type: 'number' },
              reusability: { type: 'number' },
            },
          },
          excerpt: { type: 'string' },
          value: { type: 'string' },
        },
      },
    },
  },
}

const AUDIT_SCHEMA = {
  type: 'object',
  properties: {
    pass: { type: 'boolean' },
    violations: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          criterion: { type: 'string' },
          file: { type: 'string' },
          detail: { type: 'string' },
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
        },
      },
    },
  },
  required: ['pass'],
}

// Phase 1 — Discovery
phase('Discovery')
const intent = await agent(
  [
    'You are the intent-parser specialist for /harness:builder.',
    'Parse the natural-language directive into a structured intent: target plugin (cowork or code), skill topic, intent, research keywords, and any constraints.',
    'The directive is NOT positional — it is free-form natural language. Infer target_plugin from domain cues (cowork = copy/content/business/non-dev; code = coding/dev/agentic).',
    'Return the structured object only.',
  ].join(' '),
  { label: 'intent-parser', phase: 'Discovery', schema: INTENT_SCHEMA, effort: 'medium' }
)
if (!intent) throw new Error('intent-parser returned no result')
log(`target=${intent.target_plugin} topic="${intent.skill_topic}"`)

// Phase 2 — 3-Layer Research
phase('3-Layer Research')
const research = await parallel([
  () => agent(
    [
      'You are the research-collector (Layer 1: qmd vault).',
      `Run: bash .claude/skills/harness-builder/scripts/qmd-search.sh "${intent.keywords.join(' ')}" 10`,
      'Return the raw qmd output (markdown matches). If qmd is unavailable the script falls back to ripgrep automatically.',
    ].join(' '),
    { label: 'research:qmd', phase: '3-Layer Research', effort: 'medium' }
  ),
  () => agent(
    [
      'You are the research-collector (Layer 2: Claude official docs + best practices).',
      `Fetch code.claude.com/docs and docs.claude.com for content relevant to: ${intent.skill_topic} (${intent.target_plugin} plugin context).`,
      'Return structured excerpts with source URLs.',
    ].join(' '),
    { label: 'research:docs', phase: '3-Layer Research', effort: 'medium' }
  ),
  () => agent(
    [
      'You are the research-collector (Layer 3: web search, supplementary).',
      `Search the web for supplementary best practices on: ${intent.skill_topic}.`,
      'Return top results with URLs and one-line relevance.',
    ].join(' '),
    { label: 'research:web', phase: '3-Layer Research', effort: 'low' }
  ),
])
const layerResults = research.filter(Boolean)

// Phase 3 — Curation
phase('Curation')
const curation = await agent(
  [
    'You are the plugin-curator specialist (Producer-Reviewer evaluator).',
    'Score the collected research (3 layers) on 4 dimensions (Relevance / Specificity / Practicality / Reusability, 0–5 each).',
    'Weighted average = (R + S + P + U) / 4. Select top-5 by weighted average.',
    `Target plugin: ${intent.target_plugin}. Skill topic: ${intent.skill_topic}.`,
    'Return the top-5 structured object with scores + excerpts + one-paragraph value each.',
  ].join(' '),
  { label: 'plugin-curator', phase: 'Curation', schema: CURATION_SCHEMA, effort: 'medium' }
)

// Phase 4 — Selection (orchestrator-side AskUserQuestion gate; Runner emits the candidate list)
phase('Selection')
log(`top-5 curated for ${intent.target_plugin}/${intent.skill_topic} — orchestrator surfaces AskUserQuestion`)

// Phase 5 — Build
phase('Build')
const constraints = intent.target_plugin === 'code'
  ? 'ALLOWED categories: commands/, skills/, agents/. FORBIDDEN: hooks/, output-styles/, rules/, mcp-servers/.'
  : 'ALLOWED category: skills/ ONLY. FORBIDDEN: commands/, agents/, hooks/, output-styles/, rules/, mcp-servers/.'
const skill = await agent(
  [
    'You are the skill-builder specialist (opus/high).',
    `Build a ${intent.target_plugin} plugin skill for: ${intent.skill_topic}.`,
    `Category constraints — ${constraints}`,
    'Use the curated top-5 research as source material. Emit SKILL.md (+ references/ + allowed category dirs) under the target plugin path.',
    'Return the file paths created.',
  ].join(' '),
  { label: 'skill-builder', phase: 'Build', effort: 'high', model: 'opus' }
)

// Phase 6 — Audit (Claude 공식 문서 기준 감사)
phase('Audit')
const audit = await agent(
  [
    'You are the harness-builder auditor specialist.',
    'Audit the skill-builder output against Claude official doc criteria:',
    '1. SKILL.md frontmatter (name kebab ≤64, description ≤1536 folded scalar, metadata)',
    '2. Category constraint (cowork=skills/ only; code=commands+skills+agents only) — critical severity',
    '3. Claude official doc fidelity (prompting best practices, literal scope, source URLs)',
    '4. No duplication with existing plugin skills (Glob check)',
    `Skill target: ${intent.target_plugin}. Skill paths: ${JSON.stringify(skill)}.`,
    'Return AUDIT_SCHEMA: pass boolean + violations array (empty if pass).',
  ].join(' '),
  { label: 'auditor', phase: 'Audit', schema: AUDIT_SCHEMA, effort: 'medium' }
)
if (audit && !audit.pass) {
  log(`audit FAIL — ${audit.violations?.length || 0} violations; orchestrator re-delegates skill-builder with violations`)
}

// Phase 7 — Report
phase('Report')
return {
  intent,
  layers_collected: layerResults.length,
  top5: curation?.top5?.length || 0,
  skill_built: skill,
  audit_pass: audit?.pass ?? false,
  audit_violations: audit?.violations ?? [],
}
