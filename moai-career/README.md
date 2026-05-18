# moai-career

한국 취준생·재직자를 위한 커리어 풀스택 플러그인 — 자기소개서·이력서·JD 분석·AI 면접·포트폴리오 4종 스킬.

2026년 한국 채용 시장은 **컬처핏을 넘어 팀핏**, 대규모 공채에서 **소규모 핀셋 채용**, 학벌·스펙보다 **즉시 쓰일 스킬**, 그리고 **AI 리터러시 + 진정성 검증**으로 빠르게 이동하고 있습니다. moai-career는 이 흐름에 맞춰 신입 취준생부터 4~7년차 경력 이직자, 헤드헌터 오퍼를 받는 시니어까지 동일한 4 스킬로 커버합니다.

## 누구를 위한 플러그인인가

- **신입 취준생** — 첫 자소서·이력서·포트폴리오·AI 면접 1분 자기소개를 다듬는 사람
- **3~7년차 경력 이직자** — 리멤버·원티드·헤드헌터 오퍼를 받는 시점에서 경력기술서·1page 셀링 시트를 빠르게 만드는 사람
- **재직 중 부캐 준비자** — 퇴근 후 사이드 프로젝트·노션 포트폴리오·링크드인 프로필을 누적해 다음 이직을 준비하는 사람
- **공기업·대기업 공채 준비자** — NCS·블라인드 채용·역량 면접(BEI)·인성 검사를 대비하는 사람

## 스킬 4종

| 스킬 | 설명 | 주 사용자 | 상태 |
|------|------|---|:----:|
| [resume-builder](./skills/resume-builder/) | 자소서(KKK-STAR)·이력서(USP+CAR)·경력기술서·영문 CV·링크드인 — 2026 ATS·AI 검증 회피 가드 | 전체 | ✅ |
| [job-analyzer](./skills/job-analyzer/) | JD 분해·키워드 매칭·기업 리서치(DART+잡플래닛+블라인드+사람인 공고 이력)·헤드헌터 오퍼 검증 | 경력 이직 우선 | ✅ |
| [interview-coach](./skills/interview-coach/) | AI 역량검사·BEI·PT·토론·임원·팀핏 면접 — 모의 면접 루프 + 답변 코칭 + 역질문 15종 | 전체 | ✅ |
| [portfolio-guide](./skills/portfolio-guide/) | 개발(GitHub·기술 블로그)·디자인(Figma·Behance)·마케팅·기획 분야별 포트폴리오 + 검색되는 노션 포트폴리오 | 재직자 누적·신입 첫 구축 | ✅ |

## 한국 채용 환경 특화

- **2026 팀핏 평가 대응** — interview-coach가 조직 전체 컬처핏이 아닌 **함께 일할 팀**의 업무 스타일·갈등 대응 질문을 별도 모드로 처리
- **AI 진정성 검증 회피** — 챗GPT·제미나이 흔적이 남는 표현(추상 형용사·결론 클리셰)을 resume-builder가 자동 감지·재작성
- **블라인드 채용** — 학력·나이·사진·출신 마스킹 옵션 (resume-builder)
- **NCS 기반 직무 매칭** — 공기업 직무기술서 양식 자동 변환 (resume-builder + job-analyzer)
- **수시채용·핀셋 대응** — job-analyzer가 동일 회사 다른 직무·과거 6~12개월 채용 이력을 분석해 회사 현재 우선순위 추출
- **헤드헌터·리멤버 흐름** — 사람인 출신 헤드헌터 오퍼 검증 + 영문/국문 이력서 병행 + 희망 연봉 ±20% 가이드
- **자소서 분량 최적화** — 500/1000/1500자 별 KKK-STAR 비율 자동 적용

## 공유 에이전트

| 에이전트 | 소속 | 용도 |
|---------|------|------|
| quality-evaluator | moai-core | 산출물 품질 PASS/FAIL 판정 |
| korean-tone-reviewer | moai-hr | 직급별 경어·비즈니스 톤 적절성 검토 |

## 빠른 사용 예

```
삼성전자 DX부문 SW 엔지니어 자소서 4문항 써줘. 컴공 전공, AI 사이드 프로젝트 있어.
```

```
헤드헌터가 토스 PM 오퍼 줬어. JD 분석 + 내 경력이랑 매칭 + 임원 면접 예상 질문까지.
```

```
이직 5년차 경력기술서 정리해줘. 마케팅 → PM 직무 변경 케이스.
```

```
원티드 노출되는 1page 노션 포트폴리오 만들어줘. 백엔드 5년차.
```

## 대표 워크플로우 체인

```
신입 취준 풀패키지 (대기업 공채)
  job-analyzer(JD+기업분석) → resume-builder(자소서·이력서) → ai-slop-reviewer
                                  ↓
                            portfolio-guide(스펙·프로젝트)

경력 이직 풀패키지 (수시채용·헤드헌터)
  job-analyzer(JD+DART+잡플래닛) → resume-builder(경력기술서·1page 셀링)
                                       ↓
                                 interview-coach(임원·팀핏)

AI 면접 + 인성검사 대비
  job-analyzer(기업 인재상) → interview-coach(AI 역량검사 모드 + 모의 루프 3회)

재직자 누적 포트폴리오 (검색되는 노션)
  portfolio-guide(노션 구조) → docx-generator(이력서 PDF/Word) → ai-slop-reviewer
```

## 다른 플러그인과의 경계

| 헷갈리는 영역 | 사용해야 할 스킬 |
|---|---|
| 채용 담당자(HR) 관점 JD·면접 설계 | `moai-hr/employment-manager` |
| HR의 NCS 기반 이력서 평가 | `moai-hr/resume-screener` |
| 정부 청년·창업 지원사업 신청서 | `moai-business/kr-gov-grant` |
| B2B 영업 제안서 | `moai-sales/proposal-writer` |
| 링크드인·블로그 등 퍼스널 브랜딩 콘텐츠 누적 | `moai-marketing` + `moai-content` |
| 코딩테스트 알고리즘 풀이 | 본 플러그인 범위 밖 (외부 LeetCode·프로그래머스) |

## 설치

Settings > Plugins > cowork-plugins에서 `moai-career` 선택.

산출물을 PDF/Word/PPT로 떨어뜨리려면 `moai-office`를, 모든 텍스트 산출물 마지막엔 `moai-core:ai-slop-reviewer`를 함께 체인하세요.

## 참고자료

- [원티드 블로그 — 채용 트렌드 2026: 컬처핏을 넘어 팀핏으로](https://blog.wantedlab.com/hr/report/hr-trend-report-2026)
- [한경잡앤조이 — 2026년 채용트렌드: 소규모 질적 채용·AI 잘 활용하는 인재 선호](https://magazine.hankyung.com/job-joy/article/202512290531d)
- [ZDNet Korea — 기업 70% 올해 사람 뽑는다 (사람인 327개사 조사)](https://zdnet.co.kr/view/?no=20260218142701)
- [Anthropic 플러그인 가이드](https://code.claude.com/docs/en/plugins)
- [MoAI 마켓플레이스](https://github.com/modu-ai/cowork-plugins)
