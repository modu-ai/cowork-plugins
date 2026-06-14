// 법원경매 매각공고 조회 예시 (Node.js)
// 출처: NomaDamas/k-skill (MIT) — court-auction-notice-search
// 사용 전 npm i court-auction-notice-search

const {
  searchSaleNotices,
  getSaleNoticeDetail,
  getCaseByCaseNumber,
  getCourtCodes,
} = require("court-auction-notice-search");

async function main() {
  // 1. 법원사무소 코드표 로드
  const courts = await getCourtCodes();
  console.log(`법원사무소 ${courts.count}개 로드됨`);

  // 2. 특정일·법원·입찰구분 매각공고 검색
  const notices = await searchSaleNotices({
    date: "2026-04-27",
    courtCode: "B000210", // 서울중앙지방법원
    bidType: "date",       // 기일입찰
  });
  console.log(`서울중앙지방법원 매각공고 ${notices.count}건`);

  // 3. 첫 카드 펼치기 → 사건/물건 상세
  if (notices.items.length > 0) {
    const detail = await getSaleNoticeDetail(notices.items[0]);
    for (const item of detail.items) {
      console.log(
        `${item.caseNumber} (${item.usage}) — 감정 ${item.appraisedPrice}원 / 최저 ${item.minimumSalePrice}원`,
      );
      console.log(`  주소: ${item.address}`);
    }
  }

  // 4. 사건번호 단건 조회
  const caseInfo = await getCaseByCaseNumber({
    courtCode: "B000210",
    caseNumber: "2024타경100001",
  });
  if (caseInfo.found) {
    console.log(`사건명: ${caseInfo.caseInfo.caseName}`);
    console.log(`매각기일 횟수: ${caseInfo.schedule.length}`);
  }
}

main().catch((error) => {
  if (error.code === "BLOCKED") {
    console.error(
      "[BLOCKED] 사이트가 1시간 차단했습니다. 다른 IP에서 재시도하거나 1시간 후 재시도하세요.",
    );
  } else {
    console.error(error);
  }
  process.exitCode = 1;
});
