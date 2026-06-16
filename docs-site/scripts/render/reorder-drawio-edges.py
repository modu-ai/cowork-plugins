#!/usr/bin/env python3
# .drawio 에서 edge(mxCell edge="1")를 node 보다 앞으로 재배치 → SVG export 시 edge가 node 뒤(정상 z-order)로 렌더.
# 사용: python3 reorder-drawio-edges.py
import glob
from lxml import etree

DIAGRAMS = '/Users/goos/MoAI/MoAI-Cowork-Plugins/docs-site/static/diagrams/*.drawio'
fixed = 0
for p in sorted(glob.glob(DIAGRAMS)):
    tree = etree.parse(p)
    roots = tree.xpath('//mxGraphModel/root')
    if not roots:
        continue
    changed = False
    for model_root in roots:
        cells = list(model_root)
        ones = [c for c in cells if c.get('parent') == '1']
        non_ones = [c for c in cells if c.get('parent') != '1']  # id 0, 1 계층
        edges = [c for c in ones if c.get('edge') == '1']
        nodes = [c for c in ones if c.get('edge') != '1']
        if not edges or not nodes:
            continue
        # 이미 edge가 node 앞이면 스킵
        first_node_idx = min(i for i, c in enumerate(cells) if c.get('parent') == '1' and c.get('edge') != '1')
        last_edge_idx = max(i for i, c in enumerate(cells) if c.get('parent') == '1' and c.get('edge') == '1')
        if last_edge_idx < first_node_idx:
            continue  # 이미 edge가 앞
        for c in cells:
            model_root.remove(c)
        for c in non_ones + edges + nodes:
            model_root.append(c)
        changed = True
    if changed:
        tree.write(p, xml_declaration=True, encoding='UTF-8')
        print(f'  ✓ reordered: {p.split("/")[-1]}')
        fixed += 1
print(f'\n재배치 완료: {fixed}개 .drawio')
