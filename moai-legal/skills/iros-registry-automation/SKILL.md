---
name: iros-registry-automation
description: |
  대법원 인터넷등기소(IROS, iros.go.kr)에서 법인·부동산 등기부등본(등기사항증명서)을
  여러 건 일괄 발급할 때 안전한 작업 순서와 로컬 자동화 방법을 안내합니다.
  로그인·인증·결제는 사용자가 브라우저에서 직접 처리하고, 본 스킬은 장바구니 담기·
  결제 후 열람·저장·종합 리포트 생성을 보조합니다.

  다음과 같은 요청 시 반드시 이 스킬을 사용하세요:
  - "법인등기부등본 100개 한번에 떼야 해", "회사 100개 등기부 정리해줘"
  - "고객사 등기부등본 일괄 발급", "실사 대상 법인 등기 묶음 처리"
  - "인터넷등기소 자동화", "iros.go.kr 일괄 발급", "법인등록번호로 등기 받기"
  - "부동산 등기부등본 100건", "주소 목록으로 부동산 등기 한꺼번에"
  - "TouchEn nxKey", "공동인증서 등기 발급", "법인 결제 페이지당 10건"
  - 사업자등록번호 → 법인등기 매핑, 다운로드한 등기 PDF로 종합 리포트 만들기
user-invocable: true
version: 2.0.0
---

# 인터넷등기소 등기부등본 자동화

대법원 인터넷등기소(IROS)에서 **법인·부동산 등기부등본**을 묶음 단위로 발급해야 할 때, 사용자가 직접 로그인·결제하는 흐름 안에서 장바구니·열람·저장을 안전하게 보조합니다. 실사·법무 검토·법인 일괄 관리에 사용합니다.

> 본 스킬은 [`challengekim/iros-registry-automation`](https://github.com/challengekim/iros-registry-automation) (MIT) 참고 구현 위에 cowork 컨벤션을 입혀 정리한 가이드입니다. 원 저작자 어트리뷰션은 `.claude/rules/moai/NOTICE.md`에 기록됩니다.

## Hard Limits — 사용자가 반드시 직접 수행

- **로그인은 사용자가 브라우저에서 직접 한다.** ID/PW, 공동인증서 비밀번호, 간편인증, OTP, 보안카드, 카드번호를 에이전트가 입력·저장하지 않습니다.
- **결제는 사용자가 직접 한다.** 카드 승인, 결제 확인, 결제 실패 대응은 사람이 브라우저에서 처리합니다.
- 법률 자문, 권리관계 해석, 발급 결과의 법적 유효성 보장은 하지 않습니다 — 참고용 자동화 가이드입니다.
- IROS 보안 프로그램(TouchEn nxKey 등)이 요구되면 먼저 설치하고 브라우저/PC 재시작 후 다시 시작합니다.
- **법인 결제는 페이지당 10건 단위 제약**이 있습니다. 그 이상은 10건 단위로 반복 결제합니다.
- 부동산은 IROS가 로그인 상태에서 10만원 미만 일괄 결제와 일괄열람출력/일괄저장 UI를 제공하므로, v1에서는 **장바구니 반복 작업만 자동화**합니다.

## When to use / When not to use

**사용**: 법인 30건 이상 일괄 등기 발급, 고객사 실사·KYC, 부동산 100건 단위 등기 정리, 사업자번호 기반 법인정보 매핑, 다운로드 PDF로 종합 리포트 작성.

**사용 금지**: 단건 등기(브라우저에서 직접 발급), 권리관계 분석·법률 의견, 등기 위조·변조, 발급 결과를 법적 효력으로 단정.

## Prerequisites

- Chrome/Chromium 실행 가능 환경, Python 3.10+, Playwright/Chromium 설치
- IROS 로그인 수단 (아이디·공동인증서·간편인증 중 하나)
- 결제 카드, TouchEn nxKey 사전 설치
- upstream 참고 구현 clone 후 reviewed SHA로 고정

```bash
git clone https://github.com/challengekim/iros-registry-automation.git
cd iros-registry-automation
git checkout 7c6924b2ff88d693a12556659188cb91041e5097
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp config.json.example config.json
```

업스트림 핀(SHA)을 변경할 때는 신뢰 경계가 바뀌므로 새 upstream diff를 검토하고 같은 PR에서 갱신합니다.

## Workflow

### 1. 입력 파일을 저장소 밖 안전 폴더에 둔다

법인등록번호·상호명·주소·동호수 등 민감 정보는 공개 저장소·PR·테스트 로그에 절대 넣지 않습니다.

```bash
workdir="$(mktemp -d "${TMPDIR:-/tmp}/iros-registry.XXXXXX")"
chmod 700 "$workdir"
mkdir -p "$workdir/downloads" "$workdir/logs" "$workdir/output" "$workdir/tmp-downloads"
```

법인 입력 예시 (`$workdir/corp-input.json`):

```json
{
  "1101111234567": "예시 주식회사",
  "1101117654321": "샘플 주식회사"
}
```

`config.json`은 저장소에 커밋하지 않는 로컬 파일로 두고, 모든 민감 입력·로그·산출물 경로를 `$workdir` 아래로 돌립니다 (`corpnum_list`, `companies_list`, `realty_list`, `excel_path`, `save_dir`, `pdf_dir`, `report_output`, `cart_log`, `download_log` 등).

### 2. TouchEn nxKey와 로그인 수단 확인

1. 브라우저로 IROS 로그인 페이지를 직접 엽니다.
2. TouchEn nxKey 설치 안내가 나오면 설치 후 브라우저/PC를 재시작합니다.
3. 사용자가 선택한 방식(공동인증서/간편인증/아이디)으로 직접 로그인합니다.
4. 카드 결제 가능 여부를 확인합니다.

### 3. 법인 등기부등본 장바구니 담기

법인등록번호가 있으면 정확도가 높은 `iros_cart_by_corpnum.py`를 우선합니다. 상호명만 있으면 `iros_cart.py`를 사용하되 사명변경·특수문자 실패분은 법인등록번호로 재시도합니다.

```bash
python iros_cart_by_corpnum.py
# 또는 상호명 기반
python iros_cart.py
```

브라우저에서 결제대상목록 → 페이지당 10건 단위로 직접 결제 → 결제 완료 후 터미널에 Enter.

### 4. 법인 결제 후 열람·저장

```bash
python iros_download.py
```

저장 경로는 `config.json`의 `save_dir = $workdir/downloads`. 결제 전 `companies_list`가 `$workdir/companies-input.json`을 가리키는지 확인하면 `FileNotFoundError`를 예방합니다.

### 5. 부동산 등기부등본 장바구니 담기

```bash
python iros_cart_realty.py
```

결제·열람·다운로드는 IROS 웹 UI의 일괄 결제·일괄열람출력·일괄저장이 보통 더 빠르고 안전합니다. 필요할 때만 `iros_download_realty.py`를 검토합니다.

### 6. 마법사 메뉴 (초보자 권장)

```bash
python iros_wizard.py
```

메뉴: 법인 장바구니, 법인 결제 후 열람·저장, 부동산 장바구니, 부동산 결제 후 열람·저장, 사업자번호 → 법인정보 조회, PDF → 종합 리포트 엑셀 생성.

## Response policy

- 첫 응답에서 **"로그인과 결제는 사용자가 직접"**이라고 명시합니다.
- 법인과 부동산 자동화 범위를 구분 설명합니다.
- TouchEn nxKey 사전 설치와 브라우저 재시작 가능성을 안내합니다.
- 발급 대상 목록·PDF·Excel·보고서에는 개인정보·민감정보가 있을 수 있으므로 **저장소 밖 비공개 폴더**를 사용하게 합니다.
- 법률 자문·권리관계 해석으로 보일 수 있는 표현을 피하고, 발급 보조와 파일 정리까지만 돕습니다.
- 원 저작자 링크를 답변에 남깁니다: `https://github.com/challengekim/iros-registry-automation`

## 관련 스킬 체이닝

- **before**: `moai-business:consulting-brief` — 실사 대상 법인 목록 정리
- **after**: `moai-legal:legal-risk` — 발급된 등기부등본 기반 법적 리스크 분석
- **after**: `moai-office:xlsx-creator` — 종합 리포트 Excel화
- **alternative**: 단건이면 IROS 웹에서 직접 발급

## Done when

- 법인/부동산 대상 유형과 입력 형식을 구분했다.
- 로그인·인증·결제를 사람이 직접 처리한다는 안내가 명확하다.
- TouchEn nxKey와 페이지당 10건 결제 제약을 안내했다.
- 산출물 경로와 개인정보를 저장소 밖에 두도록 안내했다.
- 원 저작자 `challengekim`과 참고 구현 링크를 포함했다.