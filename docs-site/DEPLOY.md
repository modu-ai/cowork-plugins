# 배포 런북 — `cowork.mo.ai.kr`

이 문서는 `cowork-plugins/docs-site/` Hugo 사이트를 Vercel에 배포하고 `cowork.mo.ai.kr` 도메인에 연결하는 절차입니다. 모든 단계는 사용자(GOOS) 직접 수행이 필요합니다 (외부 서비스 콘솔 작업 포함).

---

## 사전 점검

```bash
cd cowork-plugins/docs-site
hugo mod get -u                # Geekdoc 테마 동기화
hugo --gc --minify             # 로컬 빌드 — 0 warning, public/ 생성 확인
hugo server -D                 # 로컬 미리보기 → http://localhost:1313
```

배포 전 필수:

- [ ] `hugo --gc --minify` 시 WARN/ERROR가 없다
- [ ] `public/sitemap.xml`이 생성된다
- [ ] `public/index.html`에 한국어 메타 태그가 정상 출력된다
- [ ] 모든 내부 링크가 `hugo --printPathWarnings` 통과

---

## 1단계 — Vercel 프로젝트 생성

1. [vercel.com/new](https://vercel.com/new) 접속, GitHub 계정으로 로그인
2. **Import Git Repository** 클릭 → `modu-ai/cowork-plugins` 선택
3. **Configure Project** 화면:
   - **Project Name**: `cowork-docs` (또는 임의)
   - **Framework Preset**: `Hugo` (자동 감지됨)
   - **Root Directory**: `docs-site` ← **반드시 명시**. 저장소 루트가 아닙니다.
   - **Build & Output Settings**: 기본값 유지 — `vercel.json`이 자동 적용됩니다
4. **Environment Variables** 섹션은 비워둡니다 (vercel.json에서 `HUGO_VERSION=0.160.1` 자동 주입)
5. **Deploy** 클릭 → 약 1~2분 대기

배포 완료 시 `<project>.vercel.app` 임시 URL이 발급됩니다. 이 URL로 정상 동작 확인.

## 2단계 — 도메인 연결 (`cowork.mo.ai.kr`)

### 2-1. Vercel에 도메인 추가

1. Vercel 프로젝트 대시보드 → **Settings** → **Domains**
2. **Add** 입력란에 `cowork.mo.ai.kr` 입력 → **Add** 클릭
3. Vercel이 두 가지 검증 방법을 제시합니다:
   - **CNAME 방식 (권장)**: `cname.vercel-dns.com` 가리키기
   - **A 레코드 방식**: `76.76.21.21` 가리키기

서브도메인이므로 **CNAME** 방식을 사용합니다.

### 2-2. DNS 레코드 등록 (mo.ai.kr 관리자)

`mo.ai.kr` 도메인 관리 콘솔(가비아/Cloudflare/AWS Route 53 등)에서 다음 CNAME 레코드를 추가합니다.

| 타입 | 호스트 | 값 | TTL |
|---|---|---|---|
| CNAME | `cowork` | `cname.vercel-dns.com` | 600 |

기존에 `cowork.mo.ai.kr`를 다른 곳으로 라우팅하던 레코드가 있다면 먼저 삭제합니다.

### 2-3. 검증·HTTPS 발급

1. DNS 전파 대기 (보통 5~15분, 최대 48시간)
2. Vercel 도메인 페이지에서 자동으로 **Valid Configuration** 표시되면 성공
3. Let's Encrypt 인증서가 자동 발급됨 — 별도 작업 불필요
4. `https://cowork.mo.ai.kr` 접속 → 사이트 표시 확인

## 3단계 — 정적 자산 점검

배포 후 다음 경로에서 200 응답을 확인합니다.

```
https://cowork.mo.ai.kr/                  # 홈
https://cowork.mo.ai.kr/cowork/intro/     # 소개 페이지
https://cowork.mo.ai.kr/plugins/          # 플러그인 카탈로그
https://cowork.mo.ai.kr/cookbook/         # 쿡북 허브
https://cowork.mo.ai.kr/sitemap.xml       # 사이트맵
https://cowork.mo.ai.kr/robots.txt        # 로봇 정책
https://cowork.mo.ai.kr/search.json       # 검색 인덱스
```

## 4단계 — Auto Deploy 설정

기본적으로 Vercel은 `main` 브랜치 push 시 자동 배포합니다. 변경:

- **Settings → Git → Production Branch**: `main`
- **Settings → Git → Ignored Build Step**: 다음 명령으로 docs-site 외 변경은 빌드 스킵

  ```bash
  git diff HEAD^ HEAD --quiet -- docs-site/
  ```

  이 명령이 0이면(=docs-site 변경 없음) 빌드를 건너뜁니다. 플러그인 코드만 바뀐 푸시는 사이트 재빌드가 불필요합니다.

## 5단계 — Preview Branch (선택)

PR/feature 브랜치 자동 프리뷰가 필요하면:

- **Settings → Git → Preview Deployments**: Enable
- 모든 PR이 `<branch>-cowork-docs.vercel.app` URL에서 미리보기 가능

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 배포 실패 — `hugo: command not found` | HUGO_VERSION 환경변수 누락 | `vercel.json`의 `build.env.HUGO_VERSION` 확인 |
| 배포 실패 — 모듈 다운로드 오류 | go.mod 누락 또는 Geekdoc 버전 불일치 | 로컬에서 `hugo mod get -u` 후 `go.mod`/`go.sum` 함께 커밋 |
| 도메인이 자꾸 `Invalid Configuration` | DNS 전파 대기 중 | `dig cowork.mo.ai.kr`로 CNAME 응답 확인 |
| HTTPS 인증서 발급 실패 | DNS가 아직 전파되지 않음 | 1시간 대기 후 Vercel 도메인 페이지에서 **Refresh** |
| 정적 자산 404 | `Root Directory`가 `docs-site`로 설정되지 않음 | Project Settings → General → Root Directory 수정 |
| 한글이 깨짐 | hugo.toml의 `defaultContentLanguage` 누락 | 이미 `ko`로 설정됨, 확인만 필요 |

---

## 운영 체크리스트 (분기별)

- [ ] Hugo 버전 업데이트 — `vercel.json`의 `HUGO_VERSION` 갱신
- [ ] Geekdoc 테마 업데이트 — `hugo mod get -u`
- [ ] 외부 링크 점검 — `hugo --printPathWarnings`
- [ ] 사이트맵 갱신 확인
- [ ] Vercel Analytics에서 404 트래픽 검토
- [ ] cowork-plugins 신규 플러그인·스킬을 사이트에 반영했는지 점검

---

## 참고 링크

- [Vercel Hugo 공식 가이드](https://vercel.com/guides/deploying-hugo-with-vercel)
- [Hugo Modules 공식 문서](https://gohugo.io/hugo-modules/)
- [Geekdoc 테마](https://github.com/thegeeklab/hugo-geekdoc)
- [vercel.json 스키마](https://vercel.com/docs/projects/project-configuration)
