import { test as base } from '@playwright/test';
import { LoginPage } from '@pages/LoginPage';
import { AuthApi } from '@api/clients/AuthApi';

type AppFixtures = {
  loginPage: LoginPage;
  authApi: AuthApi;
};

export const test = base.extend<AppFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },

  authApi: async ({ request }, use) => {
    await use(new AuthApi(request));
  }
});

export { expect } from '@playwright/test';
