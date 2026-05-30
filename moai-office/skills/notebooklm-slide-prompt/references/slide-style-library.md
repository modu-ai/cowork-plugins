# NotebookLM 슬라이드 스타일 라이브러리 (49 스타일)

> notebooklm-slide-prompt 스킬이 Phase 3(나노바나나 이미지 프롬프트 생성) 또는 Phase 2의 `[4] 톤 & 스타일` 블록 작성 시 참조하는 시각 스타일 카탈로그.

본 라이브러리는 **49가지 시각 스타일**을 8개 카테고리로 분류해, 강연·발표·세미나 주제에 적합한 톤을 빠르게 매칭할 수 있도록 정리한 자료입니다. 각 스타일에는 (a) 한국어 이름, (b) 핵심 영문 프롬프트 키워드, (c) 추천 사용 상황을 명시했습니다.

## 사용 방법

1. 발표 주제·청중·톤에서 키워드를 추출한다 (예: "스타트업 IR" → 비즈니스 + 미래 + 신뢰)
2. 아래 카테고리에서 후보 2~3개 선정 후 사용자에게 AskUserQuestion 제시
3. 선택된 스타일의 영문 프롬프트 키워드를 Phase 3 산출물의 `Style:` 필드에 그대로 또는 변형해 적용
4. 시리즈 일관성을 위해 한 발표 내 **모든 슬라이드에 동일 Style 키워드**를 강제

## 카테고리 A — 모던 웹·기술 UI (8 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 1 | 벤토 그리드 | `Bento grid UI layout, tech minimalist design` | SaaS 제품 소개·기술 스타트업 발표 |
| 5 | 뉴 모피즘 | `Neumorphic tech schematic, soft UI, drop shadows` | 앱·웹서비스 런칭, 부드러운 톤 |
| 19 | 글래스 모피즘 3D | `3D glassmorphism icons, frosted glass UI elements, soft lighting` | C-레벨 임원 발표·프리미엄 기업 |
| 25 | 그라디언트 모던 커버 | `Abstract gradient background, smooth color transitions, geometric effects` | 보고서 표지·섹션 구분 슬라이드 |
| 27 | SaaS 대시보드 | `SaaS dashboard infographic, clean enterprise UI, cards and charts` | B2B 소프트웨어 제품 소개 |
| 39 | 아이소메트릭 플랫 | `Isometric flat vector infographic, clean technical illustration` | 시스템 아키텍처·기술 워크플로우 |
| 43 | 모던 다크 모드 | `Sleek dark mode UI, subtle glowing gradients, deep black palette` | 개발자 컨퍼런스·기술 스타트업 피칭 |
| 47 | 디지털 태블릿 다이어리 | `Digital planner interface, iPad GoodNotes aesthetic, pastel highlighters` | 개인 생산성·노트테이킹 콘텐츠 |

## 카테고리 B — 비즈니스·코퍼레이트 (10 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 2 | 비즈니스 미니멀 | `Minimalist timeline infographic, simple flat vector art` | 재무·분석 보고서 |
| 18 | 플랫 코퍼레이트 | `Corporate flat illustration, Alegria style, modern tech startup blog art` | HR·다양성 캠페인 |
| 23 | 뉴스레터 에디토리얼 | `Magazine editorial layout, modern business newsletter, elegant serif` | 경제·경영 분석 리포트 |
| 31 | 서류·리서치 데스크 | `Research desk visualization, laptop with documents, analytical workspace` | 컨설팅 보고서 |
| 32 | 데이터 스토리텔링 | `Data storytelling poster, one key metric highlighted, chart-driven` | 실적 발표·KPI 리뷰 |
| 33 | 프리미엄 컨설팅 | `Consulting deck visual, premium business slide aesthetic, corporate palette` | 경영진 브리핑 |
| 34 | 협업툴 메시지형 | `Collaboration app scene, modern team messaging interface, floating windows` | 내부 공지·팀 소식 |
| 37 | 프리미엄 스톡 사진 | `Candid photography of diverse corporate team, authentic expression, shallow DoF` | 기업 소개 자료 |
| 42 | 3D 아이소메트릭 비즈니스 | `3D isometric illustration, modern corporate workflow, clay render style` | 기업 문화 소개 |
| 48 | 스위스 그리드 인포디자인 | `Swiss grid editorial design, ultra-clean modular layout, asymmetric grid` | 학술·공식 보고서 |

## 카테고리 C — 교육·학습·매뉴얼 (7 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 3 | 칠판 스타일 | `Chalkboard sketch, educational diagram, white chalk on dark green board` | 온라인 강좌·강의 슬라이드 |
| 4 | 일본 만화 튜토리얼 | `Manga instructional comic panel, clean line art, monochrome` | 사용 설명서·가이드북 |
| 24 | 스케치노트 | `Sketchnote visual summary, hand-drawn icons, black ink highlights` | 컨퍼런스 노트·학습 요약 |
| 29 | 화이트보드 전략 | `Whiteboard strategy meeting illustration, office team planning` | 전략 수립 워크숍 |
| 35 | 포스트잇 문제 해결맵 | `Sticky note problem solving map, colorful structured clusters` | 디자인 씽킹 워크숍 |
| 36 | 미니멀 라인 아트 | `Minimalist line art diagram, simple continuous lines, step-by-step` | 절차·프로세스 설명 |
| 41 | 스텝 바이 스텝 매뉴얼 | `Step-by-step instruction manual, IKEA assembly guide aesthetic, numbered` | 제품 설치·사용 가이드 |

## 카테고리 D — 레트로·복고·팝아트 (7 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 8 | DOS 터미널 | `Retro CRT monitor screen, Matrix green text on black background` | 개발 학습 자료·해커 콘셉트 |
| 9 | 복셀(3D 픽셀) 아트 | `Isometric voxel art, gamified office environment, bright lighting` | 게임 기획안·게이미피케이션 |
| 13 | 레트로 팝 아트 | `Retro pop art, 1980s Memphis design, bold outlines, vibrant colors` | 소비재 브랜드 런칭 |
| 14 | 빈티지 액션 코믹스 | `Vintage action comic panel, 1960s comic book style, halftone dots` | 전쟁·역사·역동적 스토리 |
| 15 | 레트로 코믹 블루프린트 | `Retro-comic action blueprint, technical schematic with vintage art` | 기술 역사 강의 |
| 26 | 도트 픽셀 아트 | `16-bit retro pixel art, 2D side-scrolling game scene, bright colors` | 레트로 게임 프로모션 |
| 38 | 핸드드로잉 노트북 | `Hand-drawn notebook journal page, ballpoint pen sketches, margin doodles` | 블로거·크리에이터 콘텐츠 |

## 카테고리 E — 시네마틱·SF·다이내믹 (4 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 7 | 네온·사이버펑크 | `Neon noir technological scene, cyberpunk aesthetic, glowing accents` | 미래 비전·AI 발표 |
| 16 | 역동 애니메이션 | `High-octane anime style, intense dynamic action, speed lines` | 스포츠·게임 발표 |
| 22 | 시네마틱 우주 SF | `Cinematic 3D render of space station, hard sci-fi aesthetic, 8k` | 우주탐사·혁신 프로젝트 |
| 45 | 볼드 타이포그래피 | `Bold typography poster design, Swiss style layout, high contrast` | 슬로건·캠페인 표지 |

## 카테고리 F — 일러스트·예술·핸드메이드 (8 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 6 | 바우하우스 | `Bauhaus aesthetic, geometric abstraction, primary colors` | 건축·디자인 포트폴리오 |
| 11 | 식물학·과학 일러스트 | `Botanical scientific illustration, vintage field guide style` | 의료·생물학 자료 |
| 17 | 로코코(낭만적) | `Elegant Rococo style, romantic ornate aesthetic, soft pastel oil painting` | 럭셔리 브랜드·예술 행사 |
| 20 | 페이퍼 컷아웃 | `Layered paper cutout art, conceptual office desk, soft shadows` | 기업 문화·가치관 |
| 30 | 카드 뉴스형 정보 | `Card news style explainer, modular info blocks, social media aesthetic` | SNS 마케팅 자료 |
| 44 | 디지털 마인드맵 | `Abstract digital node network, glowing connecting lines, mind map aesthetic` | 에코시스템·관계도 설명 |
| 46 | 폴라로이드 무드보드 | `Polaroid scrapbook layout, aesthetic moodboard, sticky notes, wooden desk` | 브랜드 스토리·감성 콘텐츠 |
| 21 | 플랫 벡터 모션그래픽 | `Flat vector illustration, science channel aesthetic, vibrant colors` | 과학 다큐멘터리·교양 |

## 카테고리 G — 라이프스타일·캐주얼 (4 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 10 | 클레이 애니메이션 | `Claymation style, tactile 3D illustration, cute office worker figurine` | 신입사원 교육·친근한 비즈니스 |
| 12 | 카와이·파스텔 톤 | `Kawaii illustration, girly pastel colors, soft aesthetic` | 뷰티·패션·여성 라이프스타일 |
| 28 | Before·After 비교 | `Before and after comparison card layout, split screen infographic` | 개선안·솔루션 제안 |
| 40 | 듀오톤 그래픽 | `Duotone graphic design, two-tone overlay on photography, bold contrast` | 음악·문화 이벤트 |

## 카테고리 H — 한국형 편집 디자인 (1 스타일)

| # | 이름 | 영문 프롬프트 핵심 | 추천 상황 |
|---|-----|-------------------|----------|
| 49 | 포털형 카드 매거진 | `Portal-style card magazine layout, modular content cards, bold headlines` | 한국 뉴스레터·포털 서비스 |

## 스타일 매칭 가이드 (자동 추천 규칙)

발표 키워드 → 권장 카테고리 자동 매칭:

| 발표 키워드 | 1순위 카테고리 | 1순위 스타일 후보 |
|------------|--------------|------------------|
| 스타트업·SaaS·IR | A 모던 웹·기술 UI | 1·19·27·43 |
| 분기 실적·KPI·재무 | B 비즈니스 | 2·32·33·48 |
| 강의·강좌·교육 | C 교육·학습 | 3·24·36·41 |
| 회고·문화·HR | F 일러스트 또는 G 라이프스타일 | 20·30·10 |
| AI·미래·혁신 | E 시네마틱·SF | 7·22·43 |
| 워크숍·디자인 씽킹 | C 교육 + 라이프스타일 | 29·35·10 |
| 게임·엔터테인먼트 | D 레트로 + E 시네마틱 | 9·26·16 |
| 마케팅·캠페인 | F 일러스트 또는 D 팝아트 | 13·30·45 |
| 컨설팅·전문성 | B 비즈니스 | 23·31·33·48 |
| 한국형 콘텐츠 | H + B 혼합 | 49·23 |

## 시리즈 일관성 권장 (HARD 가이드)

한 발표(같은 NotebookLM 노트북 산출물)의 **모든 슬라이드 이미지**는 다음을 통일해야 합니다:

1. **Style 키워드**: 위 표의 영문 프롬프트 핵심 문구를 그대로 유지
2. **Palette**: 카테고리 첫 스타일 기준 색 톤 고정 (예: 다크 = `dark teal + amber accent`, 라이트 = `cream + sage green`)
3. **Lighting**: `soft volumetric`, `flat even`, `cinematic key + rim` 중 한 가지 유지
4. **Consistency tag**: `series="<발표명-slug>", palette="<팔레트>", lighting="<조명>"` 형식으로 모든 슬라이드 프롬프트 끝에 부착

표지·섹션 구분 슬라이드만 **wide cinematic** composition 허용. 본문 슬라이드는 **16:9 + center-weighted**.

## 안티패턴 (자주 발생하는 실수)

- ❌ 표지는 시네마틱 우주(22), 본문은 칠판(3) — 시리즈 일관성 파괴
- ❌ 영문 프롬프트 키워드 한국어로 번역해서 사용 — 모델 인식률 저하
- ❌ 한 슬라이드에 두 카테고리 키워드 동시 적용(`Bauhaus + cyberpunk`) — 결과 불안정
- ❌ Composition 누락 — 16:9 슬라이드 비율과 불일치한 결과 발생
- ❌ Palette 없이 Style만 지정 — 슬라이드마다 색이 다르게 나옴

## 출처 및 참고

본 라이브러리는 공개된 옵시디언 publish 자료(이커머스 클래스 · 노트북 LM 슬라이드 가이드북)에서 49개 시각 스타일 분류를 참고해, MoAI cowork-plugins에서 사용하기 위해 카테고리·매칭 규칙·일관성 가드를 재구성한 자료입니다. 영문 프롬프트는 Nano Banana(Gemini 3 Pro Image) 모델 직접 인식을 위해 의도적으로 짧은 키워드 조합 형태를 유지했습니다.

- 원 자료(공개): <https://publish.obsidian.md/datawave/이커머스+클래스/노트북+LM+슬라이드+가이드북>
- 본 라이브러리: 49개 스타일 → 8개 카테고리 분류, 시리즈 일관성 가드, 발표 키워드 → 스타일 자동 매칭 규칙 신규 추가
