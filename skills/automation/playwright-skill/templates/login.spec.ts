import { test, expect } from '@fixtures';

test('TC-AUTH-001 user signs in with valid credentials', async ({ loginPage }) => {
  await loginPage.goto();
  await loginPage.login(
    process.env.USER_NAME!,
    process.env.USER_PASSWORD!
  );

  await expect(loginPage.errorAlert).toBeHidden();
});
