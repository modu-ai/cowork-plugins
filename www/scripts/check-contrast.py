#!/usr/bin/env python3
"""배경색 · 글자색 대비 감사 — "안 보이는 글씨" 회귀 방지.

실행:  cd www && python3 scripts/check-contrast.py
종료코드: 대비 미달(WCAG AA 4.5:1)이 하나라도 있으면 1

왜 필요한가
  스타일이 여러 레이어(tokens → base → moai-ds → docs → v2)에 흩어져 있어서,
  배경은 한 레이어가 정하고 글자색은 다른 레이어가 정하는 일이 생긴다.
  거기에 moai-ds.css 의 레거시 !important 가 끼면 최종 결과가 뒤집힌다.
  실제 사고 두 건:
    · 코드블록  배경 #09110f(v2) + 글자 #060606(레거시 !important) → 1.05:1, 안 보임
    · 히어로 버튼 배경 #fff(docs) + 글자 #ffffff(!important)      → 1.00:1, 안 보임
  이 스크립트는 !important 와 CSS 변수를 실제 캐스케이드대로 풀어서 대비를 계산한다.

표면을 추가하려면 아래 PAIRS 에 (이름, 배경 셀렉터들, 글자 셀렉터들) 한 줄을 더한다.
반투명 배경(rgba alpha<0.6)은 판정을 보류한다 — 합성색은 부모에 따라 달라지므로
필요하면 손으로 계산할 것.
"""
import re
import pathlib
import sys
ORDER=["moai-ds-tokens.css","moai-ds-base.css","moai-ds.css","moai-ds-docs.css","moai-ds-mascot.css","moai-ds-v2.css"]
def spec(s): return (len(re.findall(r"#[\w-]+",s)),len(re.findall(r"[.:\[][\w-]+",s)),len(re.findall(r"(?:^|[\s>+~])([a-z][\w-]*)",s)))

rules=[]; tokens={}
for i,f in enumerate(ORDER):
    css=re.sub(r"/\*.*?\*/","",pathlib.Path("static/"+f).read_text(encoding="utf-8"),flags=re.S)
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        sels=[" ".join(s.split()) for s in m.group(1).split(",") if s.strip()]
        body=m.group(2)
        if any(s.strip()==":root" for s in sels):
            for dm in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+)", body):
                tokens[dm.group(1)]=dm.group(2).strip()
        for prop in ("color","background-color","background"):
            for dm in re.finditer(rf"(?<![-\w]){prop}\s*:\s*([^;]+)", body):
                val=dm.group(1).strip(); imp="!important" in val
                val=val.replace("!important","").strip()
                for s in sels:
                    rules.append((i,f,s,spec(s),prop,val,imp))

def resolve(v,depth=0):
    if depth>10 or not v: return None
    v=v.strip()
    m=re.fullmatch(r"var\((--[\w-]+)(?:,([^)]*))?\)",v)
    if m:
        t=tokens.get(m.group(1))
        return resolve(t if t else (m.group(2) or ""),depth+1)
    if v.startswith("#"): return v
    if v.startswith("rgba("):
        n=[x.strip() for x in v[5:-1].split(",")]
        if len(n)==4 and float(n[3])<0.6: return None   # 반투명은 판정 보류
        return "#%02x%02x%02x"%tuple(int(float(x)) for x in n[:3])
    if v.startswith("rgb("):
        n=[int(float(x)) for x in v[4:-1].split(",")]
        return "#%02x%02x%02x"%tuple(n)
    if v in ("transparent","none","inherit","currentColor","initial","unset"): return None
    named={"white":"#ffffff","black":"#000000","#fff":"#ffffff","#000":"#000000"}
    return named.get(v.lower())

def hexpand(h):
    h=h.lstrip("#")
    if len(h)==3: h="".join(c*2 for c in h)
    return tuple(int(h[i:i+2],16) for i in (0,2,4)) if len(h)>=6 else None

def lum(h):
    rgb=hexpand(h)
    if not rgb: return None
    def c(v):
        v/=255
        return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    r,g,b=[c(x) for x in rgb]
    return 0.2126*r+0.7152*g+0.0722*b

def ratio(a,b):
    la,lb=lum(a),lum(b)
    if la is None or lb is None: return None
    hi,lo=max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)

def win(sels,prop):
    ms=[r for r in rules if r[2] in sels and r[4]==prop]
    if not ms: return None,None
    imp=[r for r in ms if r[6]]
    pool=imp if imp else ms
    w=sorted(pool,key=lambda r:(r[3],r[0]))[-1]   # cascade: 같은 특이도·같은 파일이면 문서 순 마지막이 승자
    return resolve(w[5]), f"{w[1]}{' !important' if w[6] else ''}"

PAIRS=[
 ("코드블록 본문",      {".gdoc-markdown .highlight"}, {".gdoc-markdown .highlight pre",".chroma"}),
 ("Cowork 지시블록",   {".gdoc-markdown .highlight.cw-instruction"}, {".gdoc-markdown .highlight pre",".chroma"}),
 ("페이지 배경/본문",    {"body",".wrapper"}, {".gdoc-markdown p"}),
 ("사이드바",          {".gdoc-nav"}, {".cw-side-link",".cw-side-head"}),
 ("표 헤더",           {".gdoc-markdown table:not(.lntable):not(.highlight) thead th"}, {".gdoc-markdown table:not(.lntable):not(.highlight) thead th"}),
 ("힌트 warning",      {".gdoc-hint.warning",".gdoc-hint.danger",".gdoc-hint.important"}, {".gdoc-hint.warning .gdoc-hint__title"}),
 ("인라인 코드",        {".gdoc-markdown code"}, {".gdoc-markdown code"}),
 ("primary 버튼",      {".btn--primary"}, {".btn--primary"}),
 ("히어로",            {".cw-hero"}, {".cw-hero h1"}),
 ("헤더",             {".gnav"}, {".gnav-link"}),
 ("푸터",             {".ds-footer"}, {".ds-footer-links"}),
]
print(f"{'표면':<20}{'배경':<10}{'글자':<10}{'대비':>7}  판정")
print("-"*72)
bad=[]
for label,bgsel,fgsel in PAIRS:
    bg,bgsrc=win(bgsel,"background-color")
    if not bg: bg,bgsrc=win(bgsel,"background")
    fg,fgsrc=win(fgsel,"color")
    if not (bg and fg):
        print(f"{label:<20}{str(bg or '-'):<10}{str(fg or '-'):<10}{'—':>7}  (판정 보류)"); continue
    r=ratio(bg,fg)
    verdict = "OK" if r>=4.5 else ("경고 (큰 글자만 가능)" if r>=3 else "★ 실패 — 안 보임")
    if r<4.5: bad.append((label,bg,fg,r,bgsrc,fgsrc))
    print(f"{label:<20}{bg:<10}{fg:<10}{r:>6.2f}:1  {verdict}")
if bad:
    print("\n문제 표면 상세")
    for label,bg,fg,r,bgsrc,fgsrc in bad:
        print(f"  {label}: 배경 {bg} [{bgsrc}] / 글자 {fg} [{fgsrc}] → {r:.2f}:1")

sys.exit(1 if bad else 0)
