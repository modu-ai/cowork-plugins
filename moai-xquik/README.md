# moai-xquik

Xquik 원격 MCP를 Cowork 프로젝트에 연결하는 설정 플러그인입니다. X 데이터 검색, 프로필 조회, 추출, 모니터링, 웹훅, 게시 워크플로우를 다룰 때 사용합니다.

## 스킬

| 스킬 | 설명 | 상태 |
|---|---|---|
| [`xquik-mcp-setup`](./skills/xquik-mcp-setup/SKILL.md) | Xquik MCP 엔드포인트, API 키 보관, 연결 검증, 오류 처리를 안내합니다. | active |

## 연결 정보

| 항목 | 값 |
|---|---|
| MCP URL | `https://xquik.com/mcp` |
| API 키 환경변수 | `XQUIK_API_KEY` |
| 인증 방식 | `Authorization: Bearer ${XQUIK_API_KEY}` |
| 문서 | https://docs.xquik.com/mcp/overview |

## 사용 예시

```text
Xquik MCP 연결해줘. API 키는 클라이언트 비밀값 저장소에 넣을게.
```

```text
X 데이터 모니터링 워크플로우를 만들기 전에 Xquik MCP 연결 상태를 점검해줘.
```

## 보안 원칙

- API 키 원문을 채팅, 문서, 로그에 붙여넣지 않습니다.
- 클라이언트의 비밀값 저장소나 환경변수에만 `XQUIK_API_KEY`를 저장합니다.
- 공개 문서에는 내부 라우팅, 비용 구조, 비공개 구현 세부사항을 적지 않습니다.

## 라이선스

MIT
