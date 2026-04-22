---
title: "Team·Enterprise 관리"
weight: 110
description: "조직에서 Cowork를 도입할 때 관리자가 챙겨야 할 거버넌스, 모니터링, 데이터 흐름 정리."
geekdocBreadcrumb: true
---

# Team·Enterprise 관리

> 조직에서 Cowork를 도입할 때 관리자가 챙겨야 할 요소들을 정리합니다.

## 요금제 특징

- **Team**: 팀 단위 플러그인 관리, 공유 프로젝트
- **Enterprise**: SSO·감사 로그·OpenTelemetry 모니터링·도메인 정책·DLP 연동

## 플러그인 거버넌스

- 관리자가 승인된 플러그인 목록을 지정해 구성원이 사용할 수 있는 범위를 제한합니다.
- `modu-ai/cowork-plugins` 같은 커뮤니티 마켓플레이스도 조직 정책에 맞춰 선별 등록할 수 있습니다.
- 각 플러그인이 요구하는 API 키·MCP 권한은 조직 공용 자격 증명으로 관리하도록 합니다.

## 모니터링 (OpenTelemetry)

- Cowork의 프롬프트·도구 사용·API 호출·오류를 OTel 이벤트로 내보낼 수 있습니다.
- Splunk, Cribl, Datadog 같은 SIEM/관찰 도구로 수집·분석 가능합니다.
- 규제 업무에서는 감사 추적을 위해 모니터링 연결을 의무화하는 것이 권장됩니다.

설정 방법은 [공식 가이드](https://claude.com/docs/cowork/monitoring)와 [Support 문서](https://support.claude.com/en/articles/14477985)를 참고하세요.

## 데이터 흐름과 프라이버시

- 기본 정책: 사용자·조직 데이터는 학습에 사용되지 않습니다(Enterprise 플랜 기준). 세부는 최신 약관을 확인하세요.
- 로컬 폴더 내용은 Cowork 세션 처리를 위해 Anthropic 인프라를 거쳐 전송됩니다. 민감 데이터는 마스킹 후 입력을 권장합니다.
- 컴퓨터 사용(computer use)은 별도 승인 없이는 화면 캡처·클릭을 수행하지 않습니다.

## 배포 체크리스트

- 사용자 권한 정책(플러그인·커넥터) 초안 확정
- OpenTelemetry 수집 파이프라인 구축
- 안전 사용 가이드와 [규제 워크로드 금지 영역](../safety/)을 사내 공지
- 1차 파일럿 팀 선정 후 피드백 루프 운영

## 다음 단계

- [안전하게 사용하기](../safety/)

---

### Sources

- [Monitoring (docs.claude.com)](https://claude.com/docs/cowork/monitoring)
- [Monitor Claude Cowork activity with OpenTelemetry](https://support.claude.com/en/articles/14477985)
- [Use Cowork on Team and Enterprise plans](https://support.claude.com/en/articles/13455879)
- [Manage Cowork plugins for your organization](https://support.claude.com/en/articles/13837433)
- [Deploying Cowork across the enterprise with PayPal (Webinar)](https://www.anthropic.com/webinars/deploying-cowork-across-the-enterprise-with-paypal)
