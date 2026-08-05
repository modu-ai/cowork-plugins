# OWPML (Open Word-Processor Markup Language) Quick Reference

HWPX 파일 편집 시 참고하는 OWPML XML 구조 요약입니다.

## 1. 네임스페이스

| Prefix | URI | 용도 |
|--------|-----|------|
| `hp` | `http://www.hancom.co.kr/hwpml/2011/paragraph` | 단락, 텍스트 런, 텍스트 |
| `hs` | `http://www.hancom.co.kr/hwpml/2011/section` | 섹션 (본문 영역) |
| `hh` | `http://www.hancom.co.kr/hwpml/2011/head` | 헤더 (글꼴, 스타일 정의) |
| `hc` | `http://www.hancom.co.kr/hwpml/2011/core` | 패키지 매니페스트 |
| `hv` | `urn:hancom:office:hwpml:version` | 버전 정보 |
| `odf` | `urn:oasis:names:tc:opendocument:xmlns:manifest:1.0` | ODF 매니페스트 |

## 2. 섹션 파일 구조 (sectionN.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hs:sec xmlns:hs="http://www.hancom.co.kr/hwpml/2011/section"
         xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph">

  <!-- 단락 -->
  <hp:p paraPrIDRef="0" styleIDRef="0">
    <!-- 텍스트 런 -->
    <hp:run charPrIDRef="0">
      <!-- 런 속성 (선택) -->
      <hp:rPr>
        <hp:charPr fontRef="0" sz="1000" bold="false" italic="false"/>
      </hp:rPr>
      <!-- 텍스트 -->
      <hp:t>여기에 텍스트</hp:t>
    </hp:run>
  </hp:p>

  <!-- 빈 단락 (줄바꿈) -->
  <hp:p>
    <hp:run>
      <hp:t></hp:t>
    </hp:run>
  </hp:p>

</hs:sec>
```

## 3. 주요 요소

### 3.1 단락 `<hp:p>`
- 문서의 기본 블록 단위
- 속성: `paraPrIDRef` (단락 스타일 참조), `styleIDRef` (스타일 ID)

### 3.2 텍스트 런 `<hp:run>`
- 동일한 서식이 적용된 텍스트 단위
- 하나의 단락에 여러 런이 올 수 있음
- 속성: `charPrIDRef` (문자 속성 참조)

### 3.3 텍스트 `<hp:t>`
- 실제 텍스트 내용
- 항상 `<hp:run>` 내부에 위치

### 3.4 런 속성 `<hp:rPr>`
- `<hp:charPr>`: 글꼴 참조, 크기, 굵게, 기울임
- `<hp:color>`: 텍스트 색상

## 4. 헤더 파일 구조 (header.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hh:head xmlns:hh="http://www.hancom.co.kr/hwpml/2011/head"
          xmlns:hp="http://www.hancom.co.kr/hwpml/2011/paragraph">

  <!-- 글꼴 정의 -->
  <hh:fontfaces>
    <hh:fontface lang="HANGUL">
      <hp:font id="0" face="함초롬돋움" type="TTF"/>
      <hp:font id="1" face="함초롬바탕" type="TTF"/>
    </hh:fontface>
    <hh:fontface lang="LATIN">
      <hp:font id="0" face="함초롬돋움" type="TTF"/>
    </hh:fontface>
  </hh:fontfaces>

  <!-- 문자 속성 정의 -->
  <hh:charProperties>
    <hh:charPr id="0">
      <hp:fontRef hangul="0" latin="0"/>
      <hp:fontSize hangul="1000" latin="1000"/>
    </hh:charPr>
    <hh:charPr id="1">
      <hp:fontRef hangul="1" latin="0"/>
      <hp:fontSize hangul="1600" latin="1600"/>
      <hp:bold/>
    </hh:charPr>
  </hh:charProperties>

  <!-- 단락 속성 정의 -->
  <hh:paraProperties>
    <hh:paraPr id="0">
      <hp:align horizontal="JUSTIFY"/>
      <hp:heading level="0"/>
    </hh:paraPr>
  </hh:paraProperties>

</hh:head>
```

## 5. 콘텐츠 매니페스트 (content.hpf)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<hc:package xmlns:hc="http://www.hancom.co.kr/hwpml/2011/core">
  <hc:head href="Contents/header.xml"/>
  <hc:body>
    <hc:section href="Contents/section0.xml"/>
    <hc:section href="Contents/section1.xml"/>
  </hc:body>
</hc:package>
```

## 6. 글꼴 크기 단위

HWPX에서 글꼴 크기는 **1/100 포인트** 단위입니다:

| 표시 크기 | HWPX 값 |
|-----------|---------|
| 9pt | 900 |
| 10pt | 1000 |
| 11pt | 1100 |
| 12pt | 1200 |
| 14pt | 1400 |
| 16pt | 1600 |
| 18pt | 1800 |
| 20pt | 2000 |
| 24pt | 2400 |

## 7. 일반적인 편집 패턴

### 텍스트 찾기/바꾸기
```python
for t_elem in root.iter(f'{{{HP_NS}}}t'):
    if t_elem.text and '찾을 텍스트' in t_elem.text:
        t_elem.text = t_elem.text.replace('찾을 텍스트', '바꿀 텍스트')
```

### 단락 끝에 새 단락 추가
```python
sec = root.find(f'.//{{{HS_NS}}}sec') or root
new_p = ET.SubElement(sec, f'{{{HP_NS}}}p')
new_run = ET.SubElement(new_p, f'{{{HP_NS}}}run')
new_t = ET.SubElement(new_run, f'{{{HP_NS}}}t')
new_t.text = '새로운 단락 텍스트'
```

### 특정 단락 삭제
```python
paragraphs = list(sec.iter(f'{{{HP_NS}}}p'))
for p in paragraphs:
    texts = [t.text for t in p.iter(f'{{{HP_NS}}}t') if t.text]
    full_text = ''.join(texts)
    if '삭제할 내용' in full_text:
        p.getparent().remove(p)  # lxml 사용 시
        # 또는 sec.remove(p)     # ElementTree 사용 시
```

### 모든 텍스트를 목록으로 추출
```python
all_text = []
for p_elem in root.iter(f'{{{HP_NS}}}p'):
    para_texts = []
    for t_elem in p_elem.iter(f'{{{HP_NS}}}t'):
        if t_elem.text:
            para_texts.append(t_elem.text)
    if para_texts:
        all_text.append(''.join(para_texts))
```

## 8. 주의사항

1. XML 네임스페이스를 항상 포함해야 합니다 (중괄호 표기법 사용)
2. `hp:t` 요소의 텍스트에 XML 특수문자(`<`, `>`, `&`)가 있으면 이스케이프 처리 필요
3. 빈 단락도 `<hp:run><hp:t></hp:t></hp:run>` 구조를 유지하는 것이 안전합니다
4. `mimetype` 파일은 ZIP 아카이브에서 반드시 첫 번째, 비압축으로 저장
5. UTF-8 인코딩을 항상 사용
