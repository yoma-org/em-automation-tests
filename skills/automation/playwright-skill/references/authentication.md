# Authentication Strategy

## Choose a Strategy

### Shared storage state

Use when:

- tests can safely share one account;
- server-side state is not mutated incompatibly;
- parallel execution remains isolated.

### One account per worker

Use when:

- tests modify shared server-side state;
- parallel workers need independent users.

### Role-specific fixtures

Use when:

- scenarios validate multiple permissions;
- admin, user, supporter, or partner roles differ.

### API login

Prefer when:

- authentication API is stable;
- UI login is not the subject under test.

## Setup Project Example

```ts
// tests/auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('authenticate user', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Username').fill(process.env.USER_NAME!);
  await page.getByLabel('Password').fill(process.env.USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).toHaveURL(/dashboard/);

  await page.context().storageState({
    path: 'playwright/.auth/user.json'
  });
});
```

Project dependency:

```ts
projects: [
  {
    name: 'setup',
    testMatch: /.*\.setup\.ts/
  },
  {
    name: 'chromium',
    use: {
      ...devices['Desktop Chrome'],
      storageState: 'playwright/.auth/user.json'
    },
    dependencies: ['setup']
  }
]
```

## Security Rules

- never commit authentication state;
- never hardcode secrets;
- use environment variables or approved secret stores;
- refresh expired state safely;
- do not reuse production accounts for destructive testing.
