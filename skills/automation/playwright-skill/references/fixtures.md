# Fixtures and Dependency Injection

## Purpose

Provide each test with the dependencies it needs while preserving isolation and cleanup.

## Public Import Boundary

Tests should import from:

```ts
import { test, expect } from '@fixtures';
```

`src/fixtures/index.ts`:

```ts
import { test as basePage } from 'src/fixtures/base.fixture';

import { mergeTests } from '@playwright/test';

export const test = mergeTests(basePage);
export { expect } from '@playwright/test';
```

## Base Fixture Example

```ts
import { test as base } from '@playwright/test';
import { ApiClient } from '@api/clients/ApiClient';
import { BasePage } from '@pages/BasePage';

type AppFixtures = {
  basePage: BasePage;
  apiClient: ApiClient;
};

export const test = base.extend<AppFixtures>({
  basePage: async ({ page }, use) => {
      const basePage = new BasePage(page);        
      // Setup
      await basePage.navigateTo();
      await use(basePage);
  },

  apiClient: async ({ request }, use) => {
    await use(new ApiClient(request));
  }
});

export { expect } from '@playwright/test';
```

## Usage

```ts
import { test, expect } from '@fixtures';

test('TC-AUTH-001 user signs in', async ({ loginPage, dashboardPage }) => {
  await loginPage.goto();
  await loginPage.login('user@example.com', 'secret');

  await expect(dashboardPage.heading).toBeVisible();
});
```

## Lifecycle Fixture

```ts
type UserFixtures = {
  createdUser: User;
};

export const test = base.extend<UserFixtures>({
  createdUser: async ({ usersApi }, use) => {
    const user = await usersApi.createUser(buildUser());

    try {
      await use(user);
    } finally {
      await usersApi.deleteUser(user.id);
    }
  }
});
```

## Scope Rules

### Test-scoped

Use for:

- Page Objects
- API clients using test context
- per-test data
- mutable resources

### Worker-scoped

Use only for resources safe to share across tests in one worker:

- isolated worker account
- expensive read-only setup
- worker-specific environment allocation

## Fixture Dependency

Fixtures may depend on other fixtures:

```ts
authenticatedDashboard: async ({ page, authApi }, use) => {
  await authApi.loginAsDefaultUser();
  await page.goto('/dashboard');
  await use(new DashboardPage(page));
}
```

Avoid hiding the entire test scenario inside fixtures.

## Anti-patterns

- one “god fixture” containing every dependency;
- fixture setup with no cleanup;
- static shared data modified by parallel tests;
- business assertions inside fixture setup;
- creating Page Objects manually in every test;
- fixture dependencies that create test-order coupling.