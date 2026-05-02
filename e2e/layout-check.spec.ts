import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';
const SCREENSHOT_DIR = './e2e/screenshots';

// 주요 페이지 경로
const pages = [
  { path: '/', name: 'home' },
  { path: '/plugins/', name: 'plugins' },
  { path: '/cowork/', name: 'cowork' },
  { path: '/getting-started/', name: 'getting-started' },
  { path: '/cookbook/', name: 'cookbook' },
  { path: '/contributing/', name: 'contributing' },
  { path: '/releases/', name: 'releases' },
];

pages.forEach(({ path, name }) => {
  test(`Layout check: ${name}`, async ({ page }) => {
    await page.goto(BASE_URL + path);

    // 페이지 로딩 대기
    await page.waitForLoadState('networkidle');

    // 전체 페이지 스크린샷 (full page)
    await page.screenshot({
      path: `${SCREENSHOT_DIR}/${name}-full.png`,
      fullPage: true,
    });

    // 뷰포트 스크린샷 (above fold)
    await page.screenshot({
      path: `${SCREENSHOT_DIR}/${name}-viewport.png`,
      fullPage: false,
    });

    // 기본 레이아웃 검증
    const body = page.locator('body');
    await expect(body).toBeVisible();

    // 모바일 뷰포트에서도 확인
    await page.setViewportSize({ width: 375, height: 667 });
    await page.screenshot({
      path: `${SCREENSHOT_DIR}/${name}-mobile.png`,
      fullPage: true,
    });

    // 데스크톱 뷰포트 복원
    await page.setViewportSize({ width: 1280, height: 720 });
  });
});

test('Common layout elements check', async ({ page }) => {
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');

  // 헤더 존재 + role="banner" 확인
  const header = page.locator('header[role="banner"]');
  await expect(header).toBeVisible();

  // 내비게이션 확인 — <nav role="navigation">
  const nav = page.locator('nav[role="navigation"]');
  await expect(nav).toBeVisible();

  // 내비게이션 링크 5개 확인
  const navLinks = page.locator('.cw-header-nav a');
  await expect(navLinks).toHaveCount(5);

  // 푸터 존재 + role="contentinfo" 확인
  const footer = page.locator('footer[role="contentinfo"]');
  await expect(footer).toBeVisible();

  // Skip to main content 링크 확인
  const skipLink = page.locator('#gdoc-to-main');
  await expect(skipLink).toBeAttached();
});

test('Responsive breakpoints', async ({ page }) => {
  const breakpoints = [
    { width: 375, height: 667, name: 'mobile' },
    { width: 768, height: 1024, name: 'tablet' },
    { width: 1280, height: 720, name: 'desktop' },
    { width: 1920, height: 1080, name: 'wide' },
  ];

  for (const bp of breakpoints) {
    await page.setViewportSize({ width: bp.width, height: bp.height });
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');

    await page.screenshot({
      path: `${SCREENSHOT_DIR}/responsive-${bp.name}.png`,
      fullPage: false,
    });

    // 수평 스크롤 없는지 확인
    const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
    const viewportWidth = bp.width;

    expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 10); // 10px 여유
  }
});

test('Dark mode compatibility', async ({ page }) => {
  // 시스템 선호 모드 확인을 위한 에뮬레이션
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto(BASE_URL);
  await page.waitForLoadState('networkidle');

  await page.screenshot({
    path: `${SCREENSHOT_DIR}/dark-mode.png`,
    fullPage: false,
  });

  // HTML 클래스 확인
  const html = page.locator('html');
  const hasColorScheme = await html.getAttribute('class');
  console.log('HTML classes in dark mode:', hasColorScheme);
});
