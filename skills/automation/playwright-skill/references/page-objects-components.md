# Page Objects and Component Objects

## Purpose

Define how UI behavior is modeled without hiding the business intent of tests.

## Page Object Responsibilities

A Page Object should:

- represent one page or a stable page-level domain area;
- own its locators;
- expose business-level actions;
- expose important observable elements;
- optionally provide navigation;
- avoid scenario orchestration.

## Example Page Object

```ts
import { type Locator, type Page } from '@playwright/test';
import { Routes } from '@constants/Routes';

export class LoginPage {
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly signInButton: Locator;
  readonly errorAlert: Locator;

  constructor(private readonly page: Page) {
    this.usernameInput = page.getByLabel('Username');
    this.passwordInput = page.getByLabel('Password');
    this.signInButton = page.getByRole('button', { name: 'Sign in' });
    this.errorAlert = page.getByRole('alert');
  }

  async goto(): Promise<void> {
    await this.page.goto(Routes.login);
  }

  async login(username: string, password: string): Promise<void> {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }
}
```

## Good Method Names

```ts
login()
submitRegistration()
approveApplication()
selectSubscriptionPlan()
openOrderDetails()
```

## Avoid Low-Level Wrappers

Avoid:

```ts
clickButton()
fillInput()
waitForPage()
```

These only rename Playwright APIs and hide intent.

## Component Objects

Use a Component Object when a reusable UI region:

- appears across pages;
- has multiple related locators;
- has behavior or state of its own.

Example:

```ts
import { type Locator, type Page } from '@playwright/test';

export class Header {
  readonly profileMenu: Locator;
  readonly logoutButton: Locator;

  constructor(private readonly page: Page) {
    this.profileMenu = page.getByRole('button', { name: 'Profile' });
    this.logoutButton = page.getByRole('menuitem', { name: 'Log out' });
  }

  async logout(): Promise<void> {
    await this.profileMenu.click();
    await this.logoutButton.click();
  }
}
```

## Composition

```ts
export class DashboardPage {
  readonly header: Header;

  constructor(private readonly page: Page) {
    this.header = new Header(page);
  }
}
```

Prefer composition over inheritance.

## BasePage

`BasePage` is optional.

Use it only for meaningful shared application behavior, such as:

```ts
waitForApplicationReady()
expectToastMessage()
openFromMainNavigation()
```

Do not create generic wrappers for every Playwright method.

## Assertions

Keep scenario-specific assertions in the spec:

```ts
await expect(dashboardPage.heading).toBeVisible();
```

A Page Object may expose reusable invariant checks only when they are truly part of the page contract.
