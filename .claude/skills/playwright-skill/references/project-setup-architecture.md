# Project Setup and Framework Architecture

## Purpose

Define how to set up the EM Playwright TypeScript framework and how to assess the existing
repository without imposing unnecessary restructuring.

## Current State

`@playwright/test` and `@types/node` are installed and `playwright.config.ts` exists
(generated defaults). Do **not** run `npm init playwright` again. Missing pieces are added
on top.

## Dependencies

```bash
npm i -D typescript dotenv @faker-js/faker eslint typescript-eslint eslint-plugin-playwright prettier pdf-parse
```

Add only what the task needs, but `typescript` is required for `npm run typecheck`, and
`eslint` / `prettier` for `lint` / `format`.

## Default Structure

```text
em-automation-tests/
├── src/
│   ├── pages/                 # one class per em-web screen (LoginPage, InvoiceListPage, …)
│   ├── components/            # PrimeVue regions reused across pages (DataTable, Toast, ConfirmDialog, Sidebar)
│   ├── api/
│   │   ├── crypto.ts          # decryptPayload() for em-backend responses
│   │   ├── clients/           # back-office API clients (AuthApi, InvoicesApi, ApartmentsApi, …)
│   │   ├── partner/           # estate-billing-api clients
│   │   └── models/            # request / response types
│   ├── fixtures/
│   │   ├── base.fixture.ts    # page objects
│   │   ├── role.fixture.ts    # asRole(), per-role API clients
│   │   ├── data.fixture.ts    # apartment, contact, … created per test
│   │   └── index.ts           # mergeTests → `@fixtures`
│   ├── data/
│   │   ├── factories/         # buildApartment(), buildContact(), buildNrc() …
│   │   └── static/
│   ├── helpers/               # money.ts (parse/compare amounts), pdf.ts
│   ├── utils/                 # Environment.ts (env vars, roles, auth file paths)
│   ├── constants/             # Routes.ts
│   └── types/
├── tests/
│   ├── auth.setup.ts          # logs in every role → playwright/.auth/<role>.json
│   ├── seed.spec.ts           # starting point for the Playwright agents
│   ├── auth/                  # AUTH-*
│   ├── invoice/               # INV-*
│   ├── payment/               # PAY-*, CONC-* (UI part)
│   ├── balances/              # OB-SOA-*, OB-WAL-*, …
│   ├── …                      # one folder per feature in docs/test-cases/features
│   ├── e2e/                   # E2E-01 … E2E-12
│   └── api/
│       └── partner/           # estate-billing-api cases
├── playwright/.auth/          # git-ignored
├── specs/                     # Planner plans (not test cases)
├── docs/                      # canonical test cases and knowledge base
├── playwright.config.ts
├── tsconfig.json
├── eslint.config.mjs        # templates/eslint.config.mjs
├── .env.example
└── package.json
```

Suites (smoke, priority, E2E) are **tags**, not folders. See `em-project.md`.

## Existing Repository Rule

1. inspect the existing structure;
2. reuse valid conventions;
3. map skill responsibilities to existing folders;
4. do not move files merely to match the default tree;
5. propose restructuring separately when necessary.

## Folder Responsibilities

| Folder | Responsibility |
|---|---|
| `src/pages` | Page-level UI behavior |
| `src/components` | Reusable UI regions |
| `src/api/clients` | Back-office API operations (decrypted) |
| `src/api/partner` | Partner API operations |
| `src/api/models` | Request and response types |
| `src/fixtures` | Dependency injection and lifecycle |
| `src/data/factories` | Generated test data |
| `src/helpers` | Domain helpers: money, PDF |
| `src/utils` | Environment and generic utilities |
| `src/constants` | Routes and stable constants |
| `tests/<feature>` | Specs per feature, tagged by suite |
| `tests/e2e` | Cross-module flows E2E-01 … E2E-12 |
| `tests/api/partner` | Partner API tests |

## TypeScript Configuration

`tsconfig.json` (see `templates/tsconfig.json`):

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "noEmit": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "types": ["node"],
    "paths": {
      "@pages/*": ["./src/pages/*"],
      "@components/*": ["./src/components/*"],
      "@api/*": ["./src/api/*"],
      "@fixtures": ["./src/fixtures/index.ts"],
      "@fixtures/*": ["./src/fixtures/*"],
      "@data/*": ["./src/data/*"],
      "@helpers/*": ["./src/helpers/*"],
      "@utils/*": ["./src/utils/*"],
      "@constants/*": ["./src/constants/*"],
      "@app-types/*": ["./src/types/*"]
    }
  },
  "include": ["src", "tests", "playwright.config.ts"]
}
```

- `paths` are relative to the tsconfig, so `baseUrl` is not needed.
- Use `@app-types/*`, not `@types/*`, which is the npm type-package scope.
- Playwright reads `paths` from `tsconfig.json` itself; no extra bundler setup is needed.

## Package Scripts

```json
{
  "scripts": {
    "test": "playwright test",
    "test:smoke": "playwright test --grep @smoke --grep-invert @review",
    "test:p1": "playwright test --grep @P1 --grep-invert @review",
    "test:review": "playwright test --grep @review",
    "test:e2e": "playwright test --grep @e2e",
    "test:api": "playwright test tests/api",
    "test:headed": "playwright test --headed",
    "test:debug": "playwright test --debug",
    "test:ui": "playwright test --ui",
    "test:report": "playwright show-report",
    "typecheck": "tsc --noEmit",
    "lint": "eslint .",
    "format": "prettier --write .",
    "traceability": "node .claude/skills/playwright-skill/scripts/check-traceability.mjs",
    "validate": "npm run typecheck && npm run lint && npm run traceability"
  }
}
```

## Environment

`.env.example` (committed, no real values). Add `.env` to `.gitignore` (the generated
Playwright `.gitignore` does not include it):

```dotenv
BASE_URL=
API_BASE_URL=
PARTNER_API_BASE_URL=
API_PAYLOAD_KEY=
PARTNER_API_KEY=

ADMIN_EMAIL=
ADMIN_PASSWORD=
UO_OPERATOR_EMAIL=
UO_OPERATOR_PASSWORD=
UO_MANAGER_EMAIL=
UO_MANAGER_PASSWORD=
# … one pair per role used by the suite
```

## Validation

Run (or `scripts/validate-project.sh`):

```bash
npm ci
npx playwright install chromium
npm run typecheck
npm run lint
node .claude/skills/playwright-skill/scripts/check-traceability.mjs   # also runs `playwright test --list`
```

The traceability check compares every test with `test-catalog.csv` (title, `tc` / `source`
annotations, tags, variants, Review / Manual status, leftover drafts) and exits 1 on any
mismatch. `--coverage` also lists the cases that have no test yet.

Do not report success without successful command output.
