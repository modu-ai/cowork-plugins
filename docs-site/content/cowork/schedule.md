---
title: "예약 작업"
weight: 90
description: "반복 업무를 예약 작업으로 등록해 매일·매주·매월 자동 실행시키는 방법과 주의사항입니다."
geekdocBreadcrumb: true
---

# 예약 작업

> 반복되는 업무는 예약 작업(Scheduled Tasks)으로 등록해 Cowork가 일정에 맞춰 자동 실행하게 할 수 있습니다.

## 사용 예

- 매일 아침 8시에 업계 뉴스 브리핑 Word 파일 생성
- 매주 금요일에 Slack 주요 채널 요약
- 매월 1일에 전월 매출 대시보드 갱신

## 등록 절차

1. 해당 작업을 한 번 실행해 원하는 산출물이 나오는지 확인합니다.
2. 대화 상단의 **예약** 메뉴에서 반복 주기를 선택합니다(매일·매주·매월·커스텀 cron).
3. 결과를 받을 경로(로컬 폴더, 이메일, Slack 채널)를 지정합니다.
4. 저장하면 다음 실행 시간이 표시됩니다.

## 주의할 점

- 예약된 작업은 Cowork가 백그라운드에서 실행하므로, 새 파일을 만들 폴더 권한이 유효해야 합니다.
- 외부 API·MCP 연결이 필요한 경우, 인증 토큰이 만료되면 예약이 실패합니다. 정기 점검을 권장합니다.
- 결과물이 항상 같은 품질이라는 보장은 없습니다. 몇 차례 실행 후 출력 품질을 점검하세요.

## 원격 실행과 디스패치

모바일이나 외부 기기에서 "오늘 저녁 6시까지 이 작업 끝내줘"처럼 원격 지시를 보내면, 본인 데스크톱의 Cowork가 일정에 맞춰 처리합니다. [원격 디스패치 가이드](https://support.claude.com/en/articles/13947068)를 참고하세요.

## 다음 단계

- [쿡북 — 주간 보고서 자동화](../../cookbook/report-automation/)
- [컴퓨터 사용](../computer-use/)

---

### Sources

- [Schedule recurring tasks in Claude Cowork](https://support.claude.com/en/articles/13854387)
- [Assign tasks from anywhere in Claude Cowork](https://support.claude.com/en/articles/13947068)
