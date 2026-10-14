# Playwright Configuration

```ts
import { defineConfig, devices } from '@playwright/test';
import 'dotenv/config';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 4 : undefined,

  reporter: [
    ['list'],
    ['html', { open: 'never' }]
  ],

  use: {
    baseURL: process.env.BASE_URL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },

  projects: [
    {
      name: 'setup',
      testMatch: /auth\.setup\.ts/
    },
    {
      name: 'chromium',
      testIgnore: /.*\.serial\.spec\.ts/,
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/admin.json' },
      dependencies: ['setup']
    },
    {
      name: 'serial-global-totals',
      testMatch: /.*\.serial\.spec\.ts/,
      fullyParallel: false,
      use: { ...devices['Desktop Chrome'], storageState: 'playwright/.auth/admin.json' },
      dependencies: ['setup']
    }
  ]
});
```

Only add the serial project when a case must assert an absolute global total.
`fullyParallel: false` keeps tests in one file in order; also run this project alone with
`--workers=1` (or `--project serial-global-totals --workers=1` as its own CI step) so no
other test changes the totals meanwhile.

## Rules

- Chromium only, unless a case requires another browser.
- Do not hardcode environment values; read them from `.env` / CI variables.
- Retries collect evidence (trace on the retry), not hide flaky tests. A test that passes only
  on retry is reported as flaky and fixed.
- Projects may represent browsers, roles, setup dependencies, or serial groups.
- `webServer` is not used: the app runs on a deployed test environment.
- Back-office API clients do not use `use.baseURL`; they build their own request context from
  `API_BASE_URL` (see `em-project.md`).
