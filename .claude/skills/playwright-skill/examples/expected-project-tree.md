# Expected Project Tree

The canonical tree with folder responsibilities is in
`references/project-setup-architecture.md` ("Default Structure"). Template → destination:

| Template | Destination |
|---|---|
| `templates/tsconfig.json` | `tsconfig.json` |
| `templates/playwright.config.ts` | `playwright.config.ts` |
| `templates/eslint.config.mjs` | `eslint.config.mjs` |
| `templates/env.example` | `.env.example` |
| `templates/Environment.ts` | `src/utils/Environment.ts` |
| `templates/Routes.ts` | `src/constants/Routes.ts` |
| `templates/crypto.ts` | `src/api/crypto.ts` |
| `templates/AuthApi.ts` | `src/api/clients/AuthApi.ts` |
| `templates/LoginPage.ts` | `src/pages/LoginPage.ts` |
| `templates/DashboardPage.ts` | `src/pages/DashboardPage.ts` |
| `templates/Header.ts` | `src/components/Header.ts` |
| `templates/money.ts` | `src/helpers/money.ts` |
| `templates/base.fixture.ts` | `src/fixtures/base.fixture.ts` |
| `templates/role.fixture.ts` | `src/fixtures/role.fixture.ts` |
| `templates/fixtures.index.ts` | `src/fixtures/index.ts` |
| `templates/auth.setup.ts` | `tests/auth.setup.ts` |
| `templates/seed.spec.ts` | `tests/seed.spec.ts` |
| `templates/login.spec.ts` | `tests/auth/login.spec.ts` |

Locators, routes and the login endpoint in the templates are unconfirmed placeholders;
verify them against em-web / em-backend before relying on them.
