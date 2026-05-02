import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: '.',  // 현재 디렉토리 (e2e/)
  fullyParallel: false, // 순차 실행으로 리소스 절약
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1, // 단일 워커로 포트 충돌 방지
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
