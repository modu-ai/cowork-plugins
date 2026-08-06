#!/usr/bin/env python3
"""Generate www/data/agent_teams.json from the marketplace SSOT.

Reads .claude-plugin/marketplace.json + plugins/*/skills/*/SKILL.md frontmatter
+ plugins/*/agents/*.md frontmatter + plugins/*/.mcp.json, and emits the
site-facing employee/agent/skill catalog. Manual skill tables in content are
prohibited — this file is the only source (drift prevention).
"""
import glob
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'www', 'data', 'agent_teams.json')

def fm(path):
    try:
        s = open(path, encoding='utf-8').read()
    except OSError:
        return {}
    m = re.match(r'^---\n(.*?)\n---', s, re.S)
    if not m:
        return {}
    d = {}
    key = None
    for line in m.group(1).split('\n'):
        km = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
        if km:
            key = km.group(1)
            val = km.group(2).strip().strip('"').strip("'")
            # YAML block scalar indicator(> 또는 |)는 값이 아니라 형식 표시이므로 무시
            if val in ('>', '|', '>-', '|-', '>+', '|+'):
                val = ''
            d[key] = val
        elif key and line.startswith((' ', '\t')) and isinstance(d.get(key), str):
            d[key] = (d[key] + ' ' + line.strip()).strip()
    return d

mp = json.load(open(os.path.join(ROOT, '.claude-plugin', 'marketplace.json'), encoding='utf-8'))
employees = []
for p in mp['plugins']:
    pdir = os.path.join(ROOT, p['source'].lstrip('./'))
    skills = []
    deprecated = []
    for sk in sorted(glob.glob(os.path.join(pdir, 'skills', '*', 'SKILL.md'))):
        f = fm(sk)
        desc = ' '.join((f.get('description') or '').split())
        entry = {
            'name': f.get('name') or os.path.basename(os.path.dirname(sk)),
            'summary': desc[:180],
        }
        # 구명칭 호환 스텁 / 폐지된 스킬은 사이트 카탈로그에서 제외한다.
        # 사용자가 호출할 수 없는 리디렉트 전용 항목이라 노출하면 카운트만 부풀린다.
        if str(f.get('user-invocable', '')).lower() == 'false' and any(
                k in desc for k in ('구명칭 호환 스텁', '폐지', '이름 변경됨', '이전됨', '분리됨')):
            deprecated.append(entry['name'])
            continue
        skills.append(entry)
    agents = []
    for ag in sorted(glob.glob(os.path.join(pdir, 'agents', '*.md'))):
        f = fm(ag)
        tools = [t.strip() for t in (f.get('tools') or '').split(',') if t.strip()]
        agents.append({
            'name': f.get('name') or os.path.splitext(os.path.basename(ag))[0],
            'description': ' '.join((f.get('description') or '').split())[:200],
            'tools': tools,
            'readonly': not any(t in tools for t in ('Write', 'Edit', 'Bash')),
        })
    mcp = []
    mcp_path = os.path.join(pdir, '.mcp.json')
    if os.path.exists(mcp_path):
        try:
            mcp = sorted(json.load(open(mcp_path, encoding='utf-8')).get('mcpServers', {}).keys())
        except Exception:
            pass
    employees.append({
        'id': p['name'],
        'displayName': p.get('displayName', p['name']),
        'category': p.get('category', ''),
        'version': p.get('version', ''),
        'description': p.get('description', ''),
        'skill_count': len(skills),
        'skills': skills,
        'deprecated_skills': deprecated,
        'agents': agents,
        'mcp_servers': mcp,
    })

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump({'marketplace_version': mp['metadata']['version'],
           'generated_from': 'marketplace.json + plugin frontmatter (SSOT)',
           'employees': employees},
          open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"wrote {OUT}: {len(employees)} employees, "
      f"{sum(e['skill_count'] for e in employees)} skills, "
      f"{sum(len(e['agents']) for e in employees)} agents")
