# job-lifecycle.md — 비용·잡 수명주기·리드백

> `media-higgsfield-core` | 프리플라이트 비용, 비동기 JOB 폴링, 오류 분류, 서버 치환 리드백.

**Evidence tier:** 1차 (라이브 `get_cost` / `job_status` 관측. `mcp-catalog-snapshot.md` §5.1 근거)

---

## 1. 비용 프리플라이트 — `get_cost`

모든 실제 생성 **직전**, 같은 `params`에 `get_cost: true`를 넣어 프리플라이트한다. 이 호출은 **JOB을 제출하지 않고 크레딧을 0 소모**하며, 반환값에 예상 `credits`가 담긴다. 파라미터 검증 오류도 이때 드러난다.

## 2. `credits` vs `credits_exact` — 반드시 `credits`를 보고

프리플라이트 응답은 두 숫자를 줄 수 있다. 예: `soul_2`는 `credits: 1`이지만 `credits_exact: 0.12`를 반환한다 — 반올림/최소 청구 하한(floor)이 있기 때문이다.

**규칙: 스킬은 사용자에게 `credits`(실제 청구되는 값)를 보고한다. `credits_exact`(청구되지 않는 미반올림 값)를 보고하지 않는다.** `credits_exact`를 그대로 노출하면 사용자는 실제보다 싼 값으로 오해한다.

## 3. `adjustments` 리드백 — 서버 치환을 반드시 보고

응답에 `adjustments` 필드가 있으면 서버가 미지정 파라미터에 기본값을 채웠다는 뜻이다. 예(`cinematic_studio_3_0` 프리플라이트, 관측):

```
adjustments:
  params.genre:          requested "(unset)"  used "auto"   reason "default for model"
  params.generate_audio: requested "(unset)"  used  false   reason "default for model"
```

생성 도구 설명은 "apply `adjustments`"를 지시한다. **스킬은 `adjustments`를 리드백해 사용자에게 무엇이 조용히 치환됐는지 보고한다** — 오디오를 요청했는데 `generate_audio`가 `false`로 치환됐다면, 소리 없는 영상을 아무 말 없이 전달하지 않고 그 사실을 알린다.

## 4. 잔액 정지(halt) 규칙 — REQ-023

- 실제 생성 전에 `balance`로 잔액을 확인한다.
- 프리플라이트 `credits` 합이 잔액을 초과하거나, 선택한 조합이 사전 정의된 예산 상한을 넘으면 **제출하지 않고 정지**한다. 사용자에게 비용을 보고하고 더 싼 조합(모델·해상도·길이)을 제안하거나, 명시적 승인을 받는다.
- "일단 제출하고 보자"는 금지. 프리플라이트가 무료이므로 blind 소비의 변명이 없다.

## 5. 비동기 JOB 폴링·오류 분류

Higgsfield는 비동기 처리다. 생성 호출 직후 `job_id`를 받고 `job_status`로 폴링한다.

| 상태 | 의미 | 대응 |
|---|---|---|
| `queued` | 대기 중(잔액 부족 시 길어짐) | 잔액 확인 |
| `in_progress` | 처리 중 | 폴링 지속 |
| `completed` | 완료 — `result`에 결과 URL | 결과 리드백 + `adjustments` 보고 |
| `failed` | 실패(프롬프트·파라미터 문제) | 원인 진단, 파라미터 라이브 재확인 → **값이 바뀌면 재견적·재승인** |
| `nsfw` | 콘텐츠 필터링 | 민감 요소 제거 → **프롬프트가 바뀌었으므로 재견적·재승인 후** 재시도 |

**[HARD] 내용이 바뀐 재시도는 새 요청이다.** 프롬프트·나레이션 문장·모델·입력 미디어·옵션 중 **하나라도 달라지면** 그것은 사용자가 승인한 그 요청이 아니다. 승인 금액 안이라는 사실은 **승인한 콘텐츠라는 뜻이 아니다** — 보지 않은 문장에 돈이 나가는 것을 막는 것이 게이트의 목적이다.

| 재시도 유형 | 재승인 |
|---|---|
| **같은 요청 그대로** 재호출 (타임아웃·일시 오류) | 불필요 — 확인된 실패 뒤에만 |
| 프롬프트·문장·모델·입력·옵션이 **바뀜** | **필요** — 프리플라이트부터 다시 |

`completed` 시 결과 URL과 함께, 반환된 `adjustments`(있으면)를 반드시 사용자에게 함께 보고한다.
