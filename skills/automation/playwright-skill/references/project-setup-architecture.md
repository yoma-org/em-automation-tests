# Project Setup and Framework Architecture

## Purpose

Define how to create a new Playwright TypeScript repository and how to assess
an existing repository without imposing unnecessary restructuring.

## Project Initialization

For a new project:

```bash
npm init playwright@latest
```

Select:

- TypeScript
- a suitable test directory
- GitHub Actions only when requested
- required browsers only

Do not initialize Playwright again when it already exists.

## Mandatory Default Structure for New Projects

```text
my-playwright-project/
├── src/
│   ├── pages/
│   │   ├── BasePage.ts
│   │   └── LoginPage.ts
│   ├── components/
│   │   ├── Header.ts
│   │   └── NotificationModal.ts
│   ├── api/
│   │   ├── clients/
│   │   │   └── AuthApi.ts
│   │   └── models/
│   │       └── auth.ts
│   ├── fixtures/
│   │   ├── base.fixture.ts
│   │   ├── auth.fixture.ts
│   │   └── index.ts
│   ├── data/
│   │   ├── factories/
│   │   │   └── user.factory.ts
│   │   └── static/
│   ├── utils/
│   │   ├── Environment.ts
│   │   └── DataGenerator.ts
│   ├── constants/
│   │   ├── Routes.ts
│   │   └── Timeouts.ts
│   ├── helpers/
│   └── types/
│       ├── api.ts
│       └── ui.ts
├── tests/
│   ├── smoke/
│   │   └── login.spec.ts
│   ├── regression/
│   ├── api/
│   ├── e2e/
│   └── ui/
├── test-data/
│   └── users.json
├── playwright/
│   └── .auth/
│       └── .gitkeep
├── scripts/
│   └── validate-project.sh
├── docs/
│   ├── architecture.md
│   └── coding-standard.md
├── AI-Toolkit/
├── playwright.config.ts
├── tsconfig.json
├── eslint.config.js
├── prettier.config.js
├── .env.example
├── .gitignore
├── package.json
└── README.md
```

Use `.gitkeep` only for empty directories that must be committed.

## Existing Repository Rule

For Brownfield projects:

1. inspect the existing structure;
2. reuse valid conventions;
3. map toolkit responsibilities to existing folders;
4. do not move files merely to match the default tree;
5. propose restructuring separately when necessary.

## Folder Responsibilities

| Folder | Responsibility |
|---|---|
| `src/pages` | Page-level UI behavior |
| `src/components` | Reusable UI regions |
| `src/api/clients` | Reusable API operations |
| `src/api/models` | Request and response types |
| `src/fixtures` | Dependency injection and lifecycle |
| `src/data/factories` | Generated test data |
| `src/data/static` | Stable static data |
| `src/utils` | Generic utilities |
| `src/constants` | Stable constants |
| `tests/smoke` | Release-blocking checks |
| `tests/regression` | Broad functional coverage |
| `tests/api` | Direct service tests |
| `tests/e2e` | Cross-system workflows |
| `tests/ui` | Focused UI-level behavior |

## TypeScript Configuration

Recommended `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noEmit": true,
    "resolveJsonModule": true,
    "esModuleInterop": true,
    "types": ["node", "@playwright/test"],
    "baseUrl": ".",
    "paths": {
      "@pages/*": ["src/pages/*"],
      "@components/*": ["src/components/*"],
      "@api/*": ["src/api/*"],
      "@fixtures": ["src/fixtures/index.ts"],
      "@fixtures/*": ["src/fixtures/*"],
      "@data/*": ["src/data/*"],
      "@utils/*": ["src/utils/*"],
      "@constants/*": ["src/constants/*"],
      "@helpers/*": ["src/helpers/*"],
      "@types/*": ["src/types/*"]
    }
  },
  "include": ["src", "tests", "playwright.config.ts"]
}
```

## Package Scripts

Recommended:

```json
{
  "scripts": {
    "test": "playwright test",
    "test:smoke": "playwright test tests/smoke",
    "test:api": "playwright test tests/api",
    "test:headed": "playwright test --headed",
    "test:debug": "playwright test --debug",
    "test:ui": "playwright test --ui",
    "test:report": "playwright show-report",
    "typecheck": "tsc --noEmit",
    "lint": "eslint .",
    "format": "prettier --write .",
    "validate": "npm run typecheck && npm run lint && playwright test --list"
  }
}
```

## Validation

Run:

```bash
npm install
npx playwright install
npm run typecheck
npm run lint
npx playwright test --list
```

Do not report success without successful command output.
