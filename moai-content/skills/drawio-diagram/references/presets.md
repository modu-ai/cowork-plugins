# drawio-diagram 프리셋 SSOT (6종)

`moai-content:drawio-diagram`이 생성하는 `.drawio`(mxGraph XML)의 프리셋별 셰이프·레이아웃·색상 규칙 **단일 진실(SSOT)**. 모든 좌표는 그리드 10px 배수.

---

## 시맨틱 색상 (html-report 팔레트 정렬)

같은 역할은 같은 색을 쓴다. 값은 `moai-content:html-report`의 `references/design-tokens.md`와 동일 팔레트.

| 역할 | fillColor | strokeColor | fontColor | 용도 |
|------|-----------|-------------|-----------|------|
| 기본/프로세스 | `#FFFFFF` | `#D1CFC5` | `#141413` | 일반 노드·박스 |
| 강조/주체 | `#D97757` | `#B85C3E` | `#FFFFFF` | 핵심 컴포넌트·시작점 |
| 데이터/저장소 | `#788C5D` | `#5F6F4A` | `#FFFFFF` | DB·스토어·데이터셋 |
| 외부/경계 | `#E3DACC` | `#C9BCA6` | `#141413` | 외부 시스템·액터·그룹 배경 |
| 판단/분기 | `#FAF9F5` | `#D97757` | `#141413` | 판단 다이아몬드 |

엣지 기본 스타일: `edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#87867F;`

---

## .drawio 파일 골격

모든 산출물은 이 구조를 따른다. `<root>` 안 `id="0"`(루트)·`id="1"`(레이어)은 필수 고정.

```xml
<mxfile host="app.diagrams.net" type="device">
  <diagram name="Page-1" id="diagram-1">
    <mxGraphModel dx="900" dy="640" grid="1" gridSize="10" guides="1" tooltips="1"
        connect="1" arrows="1" fold="1" page="1" pageScale="1"
        pageWidth="850" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 노드·엣지가 여기에 (parent="1") -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

노드 템플릿:
```xml
<mxCell id="n1" value="라벨" vertex="1" parent="1"
    style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#D1CFC5;fontColor=#141413;fontFamily=Helvetica;">
  <mxGeometry x="40" y="40" width="160" height="60" as="geometry" />
</mxCell>
```

엣지 템플릿:
```xml
<mxCell id="e1" edge="1" parent="1" source="n1" target="n2"
    style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#87867F;">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

---

## 1. `erd` — 엔티티-관계

테이블은 `shape=table`(또는 3-구획 박스)로, 행은 PK/FK 표기. 관계는 `1`·`N` 라벨 엣지.

```xml
<mxCell id="t_user" value="User" vertex="1" parent="1"
    style="shape=table;startSize=30;container=1;collapsible=0;fillColor=#FFFFFF;strokeColor=#D1CFC5;fontStyle=1;align=center;">
  <mxGeometry x="40" y="40" width="200" height="120" as="geometry" />
</mxCell>
<mxCell id="t_user_pk" value="🔑 id  : bigint (PK)" vertex="1" parent="t_user"
    style="text;align=left;verticalAlign=middle;spacingLeft=8;html=1;fillColor=#FAF9F5;strokeColor=#D1CFC5;">
  <mxGeometry y="30" width="200" height="30" as="geometry" />
</mxCell>
<mxCell id="t_user_c1" value="email : varchar" vertex="1" parent="t_user"
    style="text;align=left;verticalAlign=middle;spacingLeft=8;html=1;strokeColor=#D1CFC5;">
  <mxGeometry y="60" width="200" height="30" as="geometry" />
</mxCell>
```

- PK 행: 🔑 prefix + `fillColor=#FAF9F5`. FK 행: 🔗 prefix.
- 관계 엣지: `style="edgeStyle=entityRelationEdgeStyle;..." ` + `value="1"`/`value="N"` 종단 라벨.
- 레이아웃: 테이블을 좌→우, 위→아래로 240px 간격 배치.

## 2. `uml-class` — 클래스 다이어그램

`shape=table`로 3 구획(클래스명·속성·메서드). 상속은 빈 삼각 화살표.

- 클래스 박스: 헤더(클래스명, `fontStyle=1`) + 속성 구획 + 메서드 구획(`────` 구분).
- 상속 엣지: `style="endArrow=block;endFill=0;edgeStyle=orthogonalEdgeStyle;"` (빈 삼각형).
- 연관: `endArrow=open`. 합성: `startArrow=diamondThin;startFill=1`.
- 가시성: `+ public`, `- private`, `# protected` prefix.

## 3. `sequence` — 시퀀스 다이어그램

라이프라인(상단 액터 박스 + 점선 수직선) + 활성 막대 + 메시지 엣지.

```xml
<mxCell id="lifeline_a" value="Client" vertex="1" parent="1"
    style="shape=umlActor;verticalLabelPosition=bottom;... " >
  <mxGeometry x="60" y="40" width="30" height="60" as="geometry" />
</mxCell>
<!-- 점선 라이프라인: style="endArrow=none;dashed=1;..." -->
<!-- 동기 메시지: style="html=1;endArrow=block;" / 응답: dashed=1;endArrow=open -->
```

- 액터/객체: 상단 정렬, 동일 y. 라이프라인은 아래로 점선.
- 메시지: 좌→우 수평 엣지 + 호출 라벨. 응답은 점선(`dashed=1`).
- 활성 막대: 가는 사각형(`fillColor=#E3DACC`)을 라이프라인 위에 겹침.

## 4. `architecture` — 시스템·클라우드 아키텍처

그룹 컨테이너(외부/경계 색) + 내부 컴포넌트(기본/강조 색) + 관계.

```xml
<mxCell id="grp_aws" value="AWS VPC" vertex="1" parent="1"
    style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3DACC;strokeColor=#C9BCA6;verticalAlign=top;fontStyle=1;dashed=1;">
  <mxGeometry x="40" y="40" width="360" height="240" as="geometry" />
</mxCell>
<!-- 그룹 내부 컴포넌트는 parent="grp_aws" + 상대 좌표 -->
```

- 클라우드 셰이프: mxGraph 내장 라이브러리만 사용. 예: `shape=mxgraph.aws4.lambda`, `shape=mxgraph.aws4.rds`, `mxgraph.azure.*`, `mxgraph.gcp2.*`, `mxgraph.kubernetes.*`.
- **불확실한 스텐실 이름 추측 금지** — 미확인 셰이프는 라벨 달린 표준 사각형으로 폴백(빈 박스 방지).
- 흐름은 강조색(`#D97757`) 엣지로 방향 표시. 데이터 저장소는 데이터/저장소 색.

## 5. `ml-pipeline` — ML/딥러닝 파이프라인

좌→우 스테이지 흐름: 데이터 → 전처리 → 모델 → 학습/평가 → 배포.

- 스테이지: 둥근 사각형, 단계별 200px 간격. 데이터셋은 데이터/저장소 색(`#788C5D`), 모델은 강조색.
- 흐름 엣지: 굵은 화살표(`strokeWidth=2;`). 피드백 루프는 점선 곡선.
- 분기(검증/평가): 판단 다이아몬드.

## 6. `flowchart` — 프로세스 플로우차트

표준 플로우차트 셰이프, 위→아래 흐름.

| 요소 | 셰이프 스타일 |
|------|---------------|
| 시작/끝 | `rounded=1;arcSize=50;` (스타디움), 강조색 |
| 처리 | `rounded=1;` 사각형, 기본색 |
| 판단 | `rhombus;` 다이아몬드, 판단/분기 색 |
| 입출력 | `shape=parallelogram;` |
| 분기 라벨 | 엣지에 `value="예"`/`value="아니오"` |

- 흐름: 위→아래 80px 간격. 판단에서 분기는 좌(아니오)·우(예) 또는 아래(예)·우(아니오).
- 루프백은 좌측 우회 엣지.

---

## 레이아웃 공통 규칙

1. **그리드 정렬** — 모든 좌표·크기 10px 배수.
2. **방향 일관성** — 흐름형(sequence·ml·flowchart)은 한 방향 고정. 구조형(erd·class·architecture)은 격자 배치.
3. **여백** — 노드 간 최소 40px, 그룹 내부 패딩 20px.
4. **라벨 폭** — `whiteSpace=wrap;html=1;`로 줄바꿈. 라벨이 길면 width 확대(폭<라벨 방지).
5. **색상 일관성** — 같은 역할 = 같은 시맨틱 색.

---

## 출처

프리셋 6종 구성(ERD·UML·시퀀스·아키텍처·ML·플로우차트)은 [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill)(MIT, © 2026)의 프리셋 분류에서 영감을 받아, mxGraph 표준 XML과 html-report 시맨틱 팔레트로 MoAI-Cowork에 맞게 재작성했다. mxGraph 셰이프·스타일 문법은 draw.io/mxGraph(Apache-2.0) 공식 규격을 따른다.
