# UI Automation

## Spec Structure

```ts
import { test, expect } from '@fixtures';
import users from '../../test-data/users.json';

test.describe('Authentication', () => {
  test('TC-AUTH-001 user signs in with valid credentials', async ({
    loginPage,
    dashboardPage
  }) => {
    await loginPage.goto();
    await loginPage.login(users.valid.email, users.valid.password);

    await expect(dashboardPage.heading).toBeVisible();
    await expect(dashboardPage.header.profileMenu).toBeVisible();
  });
});
```

## Locator Priority

Prefer:

1. `getByRole`
2. `getByLabel`
3. `getByPlaceholder`
4. `getByText`
5. `getByTestId`

Use XPath or CSS only when a semantic locator is not practical.

## Rules

- assert business outcomes;
- keep tests independent;
- use API setup when it reduces UI noise;
- avoid cross-test dependencies;
- include canonical `TC-*` in test title or annotation;
- use tags for suite selection where appropriate.
