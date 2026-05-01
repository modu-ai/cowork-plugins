# Bundled Fonts — Noto Sans CJK KR

이 디렉토리는 `pdf-writer` 스킬의 한·중·일·영 PDF 렌더링용 폰트를 보관합니다.

## 폰트 바이너리는 저장소에 포함되지 않습니다

용량 절감을 위해 `*.otf` 파일은 `.gitignore` 로 제외되며, 스킬 **최초 실행 시 자동 다운로드**됩니다.

## 자동 다운로드 스크립트

```bash
# 누락된 weight만 다운로드 (기본)
python3 ../../scripts/download_fonts.py

# 상태만 확인 (다운로드 없음)
python3 ../../scripts/download_fonts.py --check

# 전체 강제 재다운로드 (무결성 의심 시)
python3 ../../scripts/download_fonts.py --force
```

스크립트는 표준 라이브러리(`urllib.request`)만 사용하므로 추가 의존성이 없습니다. 종료 코드 0=성공, 1=실패.

## 파일 구성 (다운로드 후)

| 파일 | 굵기 | 크기 | 용도 |
|------|------|------|------|
| `NotoSansCJK-Light.otf` | 300 | ~16MB | 본문 보조, 캡션 |
| `NotoSansCJK-Regular.otf` | 400 | ~16MB | 본문 기본 |
| `NotoSansCJK-Medium.otf` | 500 | ~16MB | 강조, 부제목 |
| `NotoSansCJK-Bold.otf` | 700 | ~16MB | 제목, 강조 |
| `LICENSE.txt` | — | 4.2KB | SIL Open Font License 1.1 (저장소 포함) |

다운로드 후 총 용량: 약 **64MB**

## 출처

- **저장소**: https://github.com/notofonts/noto-cjk
- **변형**: Korean (`NotoSansCJKkr-*`) — 한·중·일·영 전체 글리프 커버, 한국어 디자인 우선
- **다운로드 URL**: `https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Korean/NotoSansCJKkr-{Weight}.otf`
- **저장 시 파일명**: 언어 suffix(`kr`) 제거하여 `NotoSansCJK-{Weight}.otf` 로 통일

## 라이선스

**SIL Open Font License, Version 1.1**

상업적 이용·수정·재배포·번들 모두 허용되나, 다음 조건을 따라야 합니다:

1. 원본 폰트 파일과 함께 라이선스(`LICENSE.txt`)를 반드시 포함
2. 폰트를 단독으로 판매하지 않음 (소프트웨어와 함께 배포는 허용)
3. "Noto Sans CJK" 이름 자체를 변형 폰트의 이름으로 사용하지 않음

라이선스 전문은 `LICENSE.txt` 또는 https://openfontlicense.org/open-font-license-official-text/ 참조.

## 폰트 갱신

Noto Sans CJK는 정기적으로 업데이트됩니다. 갱신 시:

```bash
python3 ../../scripts/download_fonts.py --force
```

`LICENSE.txt`는 저장소에 포함되어 있으므로 업스트림 라이선스 변경 시에만 수동으로 재취득하세요:

```bash
curl -sSL -o LICENSE.txt https://github.com/notofonts/noto-cjk/raw/main/Sans/LICENSE
```
