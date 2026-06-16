# 코드베이스 시각화 (opt-in)

`moai-content:drawio-diagram`의 **선택 기능**. 소스 코드를 분석해 모듈·클래스 구조를 자동으로 `.drawio` 다이어그램으로 만든다. 학습용 "이 프로젝트 구조도"·아키텍처 역설계에 유용하다.

> **opt-in — 기본 비활성**: 이 기능은 **Python 3 + Graphviz 로컬 설치**가 필요하다. Cowork 관리 환경엔 미설치일 수 있으므로, 사용자가 명시적으로 "코드베이스 구조도 그려줘"라고 요청하고 도구가 설치돼 있을 때만 사용한다. 핵심 6 프리셋(`SKILL.md`)은 이 의존성 없이 동작한다.

---

## 의존성 확인 (먼저)

```bash
python3 --version        # Python 3.x 필요
dot -V                   # Graphviz(dot) 필요 — 자동 레이아웃용
```

미설치 시 안내:
- macOS: `brew install graphviz`
- Debian/Ubuntu: `sudo apt install graphviz`
- 미설치 환경이면 코드베이스 시각화를 건너뛰고, 사용자가 구조를 설명하면 `architecture` 프리셋으로 수동 작도한다.

---

## 2단계 파이프라인

원본 [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill)의 `pyimports.py` → `autolayout.py` 흐름을 따른다.

1. **추출** — 소스에서 모듈·클래스·임포트 관계를 그래프(JSON)로 추출.
2. **레이아웃** — 그래프를 Graphviz로 자동 배치해 `.drawio` XML로 변환.

```bash
# 1) import/구조 그래프 추출 (Python/JS-TS/Go/Rust)
python3 scripts/pyimports.py <project_dir> --group -o graph.json

# 2) 그래프 → .drawio (Graphviz 자동 레이아웃)
python3 scripts/autolayout.py graph.json -o codebase.drawio
```

산출된 `codebase.drawio`는 `references/cdn-viewer.md`의 단일 HTML 래퍼로 렌더한다.

> **스크립트 번들 상태**: 위 `scripts/`는 원본 저장소(MIT)의 도구다. 본 스킬은 기본적으로 스크립트를 번들하지 않고 **opt-in 절차만 문서화**한다. 실제 번들이 필요하면 원본에서 가져오되 MIT 라이선스 헤더를 보존하고, Graphviz 의존성을 사용자에게 사전 고지한다.

---

## 폴백 (도구 없이)

Graphviz·Python이 없으면 자동 추출 대신:
1. 사용자에게 핵심 모듈·관계를 묻거나 디렉터리 트리(`tree`/`ls -R`)를 받는다.
2. `architecture` 프리셋(`references/presets.md`)으로 수동 작도한다.
3. 노드 수가 많으면 계층(레이어)별로 그룹 컨테이너로 묶는다.

---

## 출처·라이선스

코드베이스 시각화 개념·`pyimports.py`/`autolayout.py` 2단계 파이프라인은 [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) — **MIT License, © 2026 Agents365-ai**에서 가져왔다. 원본 스크립트를 번들·재배포할 경우 MIT 라이선스 고지(저작권 + 허가문)를 반드시 보존한다. Graphviz는 EPL/CPL, Python 표준 라이브러리는 PSF 라이선스로 런타임 사용에 제약이 없다.
