# 공공데이터 조회 가이드

## data.go.kr API 호출 패턴

```
GET https://apis.data.go.kr/{기관코드}/{서비스명}?ServiceKey={키}&...
```

응답: JSON 또는 XML

## KOSIS API 호출 패턴

```
GET https://kosis.kr/openapi/Param/statisticsParameterData.do
  ?method=getList
  &apiKey={키}
  &itmId=T10
  &objL1=ALL
  &objL2=ALL
  &format=json
  &jsonVD=Y
  &prdSe=M
  &startPrdDe=202501
  &endPrdDe=202512
  &orgId=101
  &tblId=DT_1B04005N
```

## API 키 로드 함수 (참조)

키는 `${CLAUDE_PLUGIN_DATA}/moai-credentials.env`에서 `KEY=VALUE` 형식으로 로드한다(예: `os.environ` 또는 파일 파싱). 별도 init-protocol 모듈에 의존하지 않는다.
