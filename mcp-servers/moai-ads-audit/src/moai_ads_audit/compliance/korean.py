"""
한국 컴플라이언스 5개 규제 검사 — SPEC §3.7.
NOTICE.md §"Korean Market Adaptation" Area 3 (Regulations) 인용.

규제 목록:
    1. 개인정보보호법 (PIPA): em/ph 해시화 검사
    2. 정보통신망법 (ITNA): 영리 광고성 정보 야간 발송 (21시-08시) + 옵트아웃
    3. 전자상거래법: 사업자 정보·청약철회·환불 정책
    4. 표시광고법: 허위·과장·부당 비교·최상급 표현
    5. 식약처 광고 심의: 사전 심의 번호·금지 표현 (질병 치료·예방 효과)

주의:
    - REQ-AUDIT-MCP-021: 단정적 명령 금지 → 시정 옵션 형식으로 반환
    - REQ-AUDIT-MCP-022: 시간 예측 금지. 예외: ITNA 21시-08시는 법률 시간 정의.
    - REQ-AUDIT-MCP-015: 식품·건강기능식품 카테고리 시 식약처 심의 강제 활성화
    - v1: 키워드 매칭 + 시정 가이드 출력까지. 실제 심의 통과는 사용자 책임.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

from moai_ads_audit.scoring.weighted import CheckStatus


class RegulationType(str, Enum):
    """5개 한국 규제 — SPEC §3.7."""
    PIPA = "개인정보보호법"
    ITNA = "정보통신망법"
    ECOMMERCE = "전자상거래법"
    ADVERTISING_ACT = "표시광고법"
    MFDS = "식약처 광고 심의"


@dataclass
class ComplianceCheckResult:
    """단일 규제 check 결과."""
    regulation: RegulationType
    status: CheckStatus
    # 체크 ID·심각도·예상 영향·시정 옵션 4요소 (REQ-AUDIT-MCP-021)
    check_id: str
    severity: str
    description: str
    expected_impact: str
    # 시정 옵션 — 단정적 명령 금지, "검토 권장" 형식
    remediation_option: str
    # 매칭된 위반 키워드 (있다면)
    matched_patterns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "regulation": self.regulation.value,
            "status": self.status.value,
            "check_id": self.check_id,
            "severity": self.severity,
            "description": self.description,
            "expected_impact": self.expected_impact,
            "remediation_option": self.remediation_option,
            "matched_patterns": self.matched_patterns,
        }


# ============================================================
# 표시광고법 금지 패턴 — 허위·과장·부당 비교·최상급 표현
# ============================================================
ADVERTISING_PROHIBITED_PATTERNS: list[tuple[str, str]] = [
    # (정규식 패턴, 설명)
    (r"1위", "순위 표현 (근거 없는 최상급)"),
    (r"최고(?:의|로|급)", "최상급 표현 (근거 없는 최고)"),
    (r"최저(?:가|로)", "최저가 표현 (근거 없음 시)"),
    (r"100%\s*(?:효과|효능|보장)", "효과 100% 표현 (과장 가능)"),
    (r"무조건|반드시\s*효과", "단정적 효과 표현"),
    (r"(?:경쟁사|타사|A사)\s*보다\s*(?:훨씬|월등)", "부당 비교 광고 가능"),
    (r"완전\s*(?:무료|공짜)", "무료 강조 (조건 미명시 시 허위 가능)"),
    (r"사기\s*아님|진짜\s*효과", "신뢰성 어필 (역설적 과장 가능)"),
]

# ============================================================
# 식약처 금지 표현 — 질병 치료·예방 효과 주장
# ============================================================
MFDS_PROHIBITED_PATTERNS: list[tuple[str, str]] = [
    (r"(?:치료|치유|완치)", "질병 치료 효과 주장 (식약처 금지)"),
    (r"(?:예방|방지|억제).*(?:질병|암|당뇨|고혈압|심장)", "질병 예방 효과 주장 (식약처 금지)"),
    (r"(?:혈당|혈압|콜레스테롤)\s*(?:낮춤|개선|정상화)", "의학적 효능 표현 (심의 필요)"),
    (r"(?:항암|항바이러스|항염)", "의약품 수준 효능 표현 (식약처 금지)"),
    (r"FDA\s*승인|미국\s*FDA", "FDA 표현 오용 가능 (국내 심의와 무관)"),
    (r"의사\s*(?:추천|권고|처방)", "의사 추천 사칭 (근거 없는 경우 금지)"),
    (r"임상\s*시험\s*결과", "임상 시험 표현 (식약처 심의 필요)"),
]

# 식약처 심의 번호 형식 패턴 — 번호 존재 여부 확인
MFDS_APPROVAL_NUMBER_PATTERN = re.compile(
    r"(?:식약처|식품의약품안전처)\s*심의\s*(?:번호|No\.?)\s*[\w\-]+"
)

# 전자상거래법 — 사업자 정보 검사 패턴
ECOMMERCE_BIZ_INFO_PATTERNS: list[tuple[str, str]] = [
    (r"사업자\s*등록\s*번호", "사업자 등록 번호 노출 (전자상거래법 의무)"),
    (r"청약\s*철회|환불\s*정책", "청약철회·환불 정책 안내"),
    (r"통신판매업\s*신고", "통신판매업 신고 번호"),
]

# ITNA 야간 발송 제한 시각 (21시-08시는 법률 시간 정의, REQ-AUDIT-MCP-022 예외)
ITNA_NIGHTTIME_START = 21  # 시 (24시간제)
ITNA_NIGHTTIME_END = 8     # 시


# ============================================================
# 규제별 검사 함수
# ============================================================

def _check_pipa(creative_text: str, pixel_context: dict | None = None) -> ComplianceCheckResult:
    """
    PIPA (개인정보보호법) 검사.
    v1: em/ph 해시화 여부 텍스트 패턴 검사 + pixel_context 보조.

    Args:
        creative_text: 광고 소재 텍스트
        pixel_context: Pixel 설정 정보 (선택 — em/ph 해시화 여부)
    """
    # Pixel 컨텍스트가 있으면 해시화 여부 직접 검사
    has_email_hash = False
    has_phone_hash = False
    if pixel_context:
        has_email_hash = bool(pixel_context.get("em_hashed", False))
        has_phone_hash = bool(pixel_context.get("ph_hashed", False))

    # 텍스트에서 개인정보 수집 안내 여부 확인
    text_lower = creative_text.lower()
    has_privacy_notice = any(
        kw in creative_text for kw in ["개인정보", "수집", "동의", "처리방침"]
    )

    if not has_privacy_notice and "개인정보" not in creative_text:
        # 광고 카피에 개인정보 수집 문구가 전혀 없으면 INFO (WARNING 아님)
        status = CheckStatus.WARNING
        desc = "광고 카피에 개인정보 수집·동의 안내가 없습니다 — 랜딩 페이지 동의 배너 확인 권장"
        impact = "PIPA 미준수 시 과태료 및 행정처분 가능성"
        remediation = (
            "광고 랜딩 페이지 개인정보 동의 배너 적절성 검토 권장. "
            "Pixel 이벤트에 SHA-256 hashed email (em) 및 phone (ph) 적용 검토 권장."
        )
        matched = []
    else:
        status = CheckStatus.PASS
        desc = "광고 카피에 개인정보 관련 안내 문구 확인됨"
        impact = ""
        remediation = ""
        matched = []

    return ComplianceCheckResult(
        regulation=RegulationType.PIPA,
        status=status,
        check_id="PIPA-001",
        severity="High",
        description=desc,
        expected_impact=impact,
        remediation_option=remediation,
        matched_patterns=matched,
    )


def _check_itna(creative_text: str) -> ComplianceCheckResult:
    """
    정보통신망법 (ITNA) 검사.
    영리 광고성 정보 야간 발송 제한 + 옵트아웃 링크 검사.
    REQ-AUDIT-MCP-022 예외: 21시-08시는 법률 시간 정의.

    Args:
        creative_text: 광고 소재 텍스트
    """
    # 옵트아웃 링크 여부 확인
    has_optout = any(
        kw in creative_text for kw in ["수신거부", "수신 거부", "수신동의 철회", "광고 수신 동의 철회"]
    )
    # 야간 발송 문구 감지 (정보성 SMS·알림톡 컨텍스트)
    has_nighttime_ref = any(
        kw in creative_text for kw in ["밤 10시", "오후 9시", "저녁 9시", "새벽"]
    )

    if not has_optout:
        status = CheckStatus.WARNING
        desc = "광고 소재에 수신거부(옵트아웃) 안내 문구가 없습니다"
        impact = "정보통신망법 위반 가능 — 영리 광고성 정보 전송 시 옵트아웃 수단 제공 의무"
        remediation = (
            "SMS·알림톡 광고 소재에 '수신거부: [링크 또는 번호]' 문구 추가 검토 권장. "
            f"야간 ({ITNA_NIGHTTIME_START}시-{ITNA_NIGHTTIME_END}시) 발송 여부도 확인 권장."
        )
        matched = ["수신거부_미발견"]
    else:
        status = CheckStatus.PASS
        desc = "옵트아웃 안내 문구 확인됨"
        impact = ""
        remediation = ""
        matched = []

    return ComplianceCheckResult(
        regulation=RegulationType.ITNA,
        status=status,
        check_id="ITNA-001",
        severity="High",
        description=desc,
        expected_impact=impact,
        remediation_option=remediation,
        matched_patterns=matched,
    )


def _check_ecommerce(creative_text: str) -> ComplianceCheckResult:
    """
    전자상거래법 검사.
    사업자 정보·청약철회·환불 정책 노출 여부.

    Args:
        creative_text: 광고 소재 텍스트 (랜딩 페이지 포함 권장)
    """
    matched_info = []
    for pattern, desc in ECOMMERCE_BIZ_INFO_PATTERNS:
        if re.search(pattern, creative_text):
            matched_info.append(desc)

    if matched_info:
        status = CheckStatus.PASS
        desc = f"전자상거래법 필수 정보 확인: {', '.join(matched_info)}"
        impact = ""
        remediation = ""
        matched = matched_info
    else:
        status = CheckStatus.WARNING
        desc = "광고 소재·랜딩 페이지에 전자상거래법 필수 정보가 확인되지 않음"
        impact = "전자상거래법 위반 가능 — 사업자 정보·청약철회·환불 정책 표시 의무"
        remediation = (
            "광고 랜딩 페이지 footer에 사업자 등록 번호·통신판매업 신고 번호·청약철회 정책 표시 검토 권장."
        )
        matched = []

    return ComplianceCheckResult(
        regulation=RegulationType.ECOMMERCE,
        status=status,
        check_id="ECOM-001",
        severity="Medium",
        description=desc,
        expected_impact=impact,
        remediation_option=remediation,
        matched_patterns=matched,
    )


def _check_advertising_act(creative_text: str) -> ComplianceCheckResult:
    """
    표시광고법 검사.
    허위·과장 표현·부당 비교·최상급 표현 키워드 매칭.

    Args:
        creative_text: 광고 소재 텍스트
    """
    matched_violations: list[str] = []
    for pattern, desc in ADVERTISING_PROHIBITED_PATTERNS:
        if re.search(pattern, creative_text):
            matched_violations.append(desc)

    if matched_violations:
        status = CheckStatus.WARNING
        desc = f"표시광고법 주의 표현 감지: {len(matched_violations)}건"
        impact = "표시광고법 위반 가능 — 공정거래위원회 시정 명령·과징금 부과 가능성"
        remediation = (
            "다음 표현에 대해 객관적 근거 확보 또는 표현 수정 검토 권장: "
            + "; ".join(matched_violations)
        )
    else:
        status = CheckStatus.PASS
        desc = "표시광고법 주요 금지 표현 미감지"
        impact = ""
        remediation = ""

    return ComplianceCheckResult(
        regulation=RegulationType.ADVERTISING_ACT,
        status=status,
        check_id="ADV-001",
        severity="High",
        description=desc,
        expected_impact=impact,
        remediation_option=remediation,
        matched_patterns=matched_violations,
    )


def _check_mfds(creative_text: str, force_active: bool = False) -> ComplianceCheckResult:
    """
    식약처 광고 심의 검사.
    사전 심의 번호 형식 검사 + 금지 표현 키워드 매칭.
    REQ-AUDIT-MCP-015: 식품·건강기능식품 카테고리 시 강제 활성화.

    Args:
        creative_text: 광고 소재 텍스트
        force_active: True이면 카테고리 무관 강제 활성 (건강기능식품/의료 카테고리)
    """
    # 금지 표현 매칭
    matched_violations: list[str] = []
    for pattern, desc in MFDS_PROHIBITED_PATTERNS:
        if re.search(pattern, creative_text, re.IGNORECASE):
            matched_violations.append(desc)

    # 심의 번호 존재 여부
    has_approval_number = bool(MFDS_APPROVAL_NUMBER_PATTERN.search(creative_text))

    if matched_violations:
        status = CheckStatus.FAIL
        desc = f"식약처 금지 표현 감지: {len(matched_violations)}건 — 사전 심의 필요"
        impact = "식약처 행정처분·광고 중지 명령 가능성 (식품·건기식·의료기기·의약품 광고)"
        remediation = (
            "다음 표현 삭제 또는 수정 검토 권장: " + "; ".join(matched_violations) +
            ". 광고 집행 전 식약처 사전 심의 번호 취득 검토 권장."
        )
    elif not has_approval_number and force_active:
        status = CheckStatus.WARNING
        desc = "식약처 사전 심의 번호가 확인되지 않음 (건강기능식품/의료 카테고리 강제 활성)"
        impact = "식약처 심의 번호 미표기 시 행정처분 가능성"
        remediation = (
            "식약처 광고 심의 번호 취득 후 광고 소재에 표기 검토 권장. "
            "심의 신청: 한국건강기능식품협회 또는 식품의약품안전처 행정 민원."
        )
    else:
        status = CheckStatus.PASS
        desc = "식약처 금지 표현 미감지" + (" + 심의 번호 확인됨" if has_approval_number else "")
        impact = ""
        remediation = ""

    return ComplianceCheckResult(
        regulation=RegulationType.MFDS,
        status=status,
        check_id="MFDS-001",
        severity="Critical" if matched_violations else "High",
        description=desc,
        expected_impact=impact,
        remediation_option=remediation,
        matched_patterns=matched_violations,
    )


# ============================================================
# 공개 진입점
# ============================================================

MFDS_REQUIRED_CATEGORIES = {
    "건강기능식품/의료", "건강기능식품", "의료", "의료기기", "의약품",
    "HEALTH_MEDICAL",
}


def check_korean_compliance(
    creative_text: str,
    product_category: str,
) -> list[ComplianceCheckResult]:
    """
    5개 한국 규제 검사 실행 + 결과 리스트 반환.

    REQ-AUDIT-MCP-015: 5개 규제 모두 검사.
    식품·건강기능식품 카테고리 시 식약처 심의 강제 활성화.

    Args:
        creative_text: 광고 소재 텍스트 (카피·헤드라인·설명 통합)
        product_category: 제품 카테고리 이름

    Returns:
        5개 ComplianceCheckResult 리스트
    """
    # 식약처 심의 강제 활성 판단 (REQ-AUDIT-MCP-015)
    mfds_force = any(
        cat in product_category for cat in MFDS_REQUIRED_CATEGORIES
    ) or product_category in MFDS_REQUIRED_CATEGORIES

    results = [
        _check_pipa(creative_text),
        _check_itna(creative_text),
        _check_ecommerce(creative_text),
        _check_advertising_act(creative_text),
        _check_mfds(creative_text, force_active=mfds_force),
    ]

    return results
