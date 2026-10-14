# EM Project Rules

These rules apply to every task in this repository. Where a generic reference shows a
different pattern, this file wins.

Background: `docs/ems-knowledge/` (read `GOTCHAS.md` before touching money flows).

## System Under Test

| Part | What | Env var |
|---|---|---|
| `em-web` | Vue 3 / PrimeVue back-office portal | `BASE_URL` |
| `em-backend` | Back-office API (Laravel, Passport Bearer token) | `API_BASE_URL` |
| `estate-billing-api` | External partner API, same DB, auth by API key | `PARTNER_API_BASE_URL` |

- Currency MMK (main), USD (secondary). Identity numbers are Myanmar NRC.
- Never run against production. The deployed branches are `develop` → `uat` → `preprod` → `master`.

## Encrypted API Responses

em-backend wraps every response body in an AES-encrypted `payload` field (`ApiEncrypt`
middleware). em-web decrypts it in `src/libs/crypton` with a key shipped in the frontend bundle.

- All back-office API reads go through one helper: `src/api/crypto.ts` → `decryptPayload()`.
- Clients never call `response.json()` directly on em-backend responses.
- The key comes from `API_PAYLOAD_KEY` in `.env`; never commit it.
- Cipher, IV handling and encoding must be copied from `em-web/src/libs/crypton`. Until that
  is confirmed, `decryptPayload()` throws instead of guessing.
- IDs can be big integers (em-web parses them specially). Keep IDs as strings in tests.
- Check whether `estate-billing-api` encrypts responses before reusing the helper there.

## Two API Clients

| Client | Base URL | Auth |
|---|---|---|
| `src/api/clients/*` (back-office) | `API_BASE_URL` | Bearer token from user login, per role |
| `src/api/partner/*` | `PARTNER_API_BASE_URL` | API key → `POST /v2/get_token` (never the `GET /v1/get_token/{key}` form) |

Tokens:

- **Partner API: each token exchange deletes the key's earlier tokens** (`MONEY_FLOWS.md` §8).
  Exchange the key once per run (setup project → file, or a single worker) and share that
  token; tests that exchange the key themselves will invalidate each other in parallel.
- Back-office: get one token per role per worker and reuse it (worker-scoped fixture). Check
  whether em-backend login revokes the user's earlier tokens; if it does, the API login would
  also log out the browser storage state for that user, and roles need separate accounts for
  API and UI.

Create each `APIRequestContext` with its own `baseURL` and `extraHTTPHeaders`
(`Authorization: Bearer <token>`). Do not reuse the browser `request` fixture for the API,
because it points at `BASE_URL`.

## Roles and Authentication (maker–checker)

Roles: `admin`, `management`, `uo-operator`/`uo-manager`, `mo-operator`/`mo-manager`,
`leasing-operator`/`leasing-manager`, `finance-operator`/`finance-manager`,
`cashier-operator`/`cashier-manager`, `credit-control`, `it-operator`.

- Operators create, managers approve. Most money cases need **two roles in one test**.
- One `auth.setup.ts` logs in every role used by the suite and saves
  `playwright/.auth/<role>.json` (git-ignored). The em-web token lives in localStorage, which
  storageState captures.
- Credentials come from env: `<ROLE>_EMAIL` / `<ROLE>_PASSWORD` (e.g. `UO_OPERATOR_EMAIL`).
- Fixtures expose `asRole(role)` (a page in its own browser context) and `apiAs(role)` (an
  API context with that role's token). See `templates/role.fixture.ts`.
- Never use the seeded `superadmin` / `password` account.

## Test Case → Test

- Title: `<ID> <case title>`, e.g. `AUTH-001 login with valid credentials lands on dashboard`.
- Annotation: `{ type: 'tc', description: 'AUTH-001' }` and `{ type: 'source', description: 'TC_Login_001' }`.
- Tags from the catalog columns:

| Catalog column | Tag |
|---|---|
| `smoke = Y` | `@smoke` |
| priority | `@P1` / `@P2` / `@P3` |
| `critical = Y` | `@critical` (★ critical business flow; always a subset of P1, used to run only the ★ flows) |
| `status = Review` | `@review` |

- No `@regression` tag: the catalog marks every case `regression = Y`, so regression is
  simply "all tests".
- `@e2e` is only on the 12 composed flows (`E2E-01` … `E2E-12` in `tests/e2e/`), so
  `--grep @e2e` runs exactly the E2E suite. Single cases with `e2e = Y` in the catalog are
  **not** tagged `@e2e`, but they **still get their own test** in `tests/<feature>/`; the flow
  is extra coverage, not a replacement. Each flow lists the case IDs it covers as `tc`
  annotations. Every flow is tagged `@e2e @P1 @critical` (`e2e-critical-flows.md`: "All flows
  are P1 ★"); flows are not in the catalog, so there is no other tag source.

```ts
test('E2E-01 utility billing to collection', {
  tag: ['@e2e', '@P1', '@critical'],
  annotation: ['SET-003', 'APT-001', 'UO-001', 'UO-007', 'AR-003', 'PAY-001', 'APT-021', 'RPT-006' /* … every case in the flow table */]
    .map(id => ({ type: 'tc', description: id }))
}, async () => { /* one test.step() per flow step */ });
```

  E2E flows chain several roles and approvals: give them their own timeout
  (`test.setTimeout()`) instead of raising the global default.

- Folders are **by feature**, not by suite, because one case can be in several suites:
  `tests/<feature>/<feature>.spec.ts` (e.g. `tests/invoice/`, `tests/payment/`,
  `tests/balances/`), `tests/e2e/E2E-01-utility-billing.spec.ts`, `tests/api/partner/`.
- Which tests to run is chosen by tag, no extra tier tags. Gates that block a merge or a
  deploy exclude `@review` (their expected result is in question, so a red one is not a
  regression); a separate non-blocking job runs `--grep @review` and reports its failures
  against `source-issues.md`:

```bash
# every deploy (blocking)
npx playwright test --grep @smoke --grep-invert @review
# every merge / nightly (blocking)
npx playwright test --grep @P1 --grep-invert @review
# release candidate (blocking)
npx playwright test --grep "@P1|@P2" --grep-invert @review
# before production release: everything, @review included
npx playwright test
# review cases (non-blocking report)
npx playwright test --grep @review
```

- `Review` cases stay in the suite, tagged `@review`, with the open question as an annotation
  (`{ type: 'review', description: '<status_note>' }`). Implement the expected result as the
  case states it; a failure is first checked against `docs/test-cases/source-issues.md`.
  Use `test.fixme()` only when the case gives no usable expected result, and keep the
  `review` annotation and `@review` tag on it.
- Merged cases with a **Data variants** table: one data array, one generated test per row,
  variant label in the title: `<ID> [<variant>] <title>`. The label is the catalog `variant`
  column for `variant` rows and the literal `base` for the canonical row (its `variant`
  column is empty), e.g. `AUTH-003 [base] …`, `AUTH-003 [Email=invalid; Password=invalid] …`.
  Each generated test carries `tc` = the case ID and `source` = **that row's** `source_id`
  (variants have their own, e.g. `TC_Login_004`; omit `source` when it is empty).
  Only the base row carries `@smoke`; the variant rows run in regression
  (`docs/test-cases/suites/smoke.md`).
  Variant rows labelled as a duplicate ("Duplicate of TC_…", "Exact duplicate row") or as
  source noise ("header row", "Blank row in source") are not separate data: they need no run
  of their own (`check-traceability.mjs` skips them).

## Automation Types

| Catalog value | Pattern |
|---|---|
| `Auto-UI` | Act and assert in the browser. |
| `Auto-UI+API` | Act in the UI; assert the numbers on screen **and** via API (and via parsed PDF when the case says PDF). |
| `Auto-API` | API only. Concurrency cases fire requests with `Promise.all`. |
| `Manual` | Not automated; report as manual-only. |

Money assertions:

- Compare amounts as exact decimals (strings or integer minor units), never floating point.
- Read the screen value, the API value and the PDF value through helpers in `src/helpers/money.ts`
  so formatting (thousands separators, `MMK`) is parsed in one place.
- PDFs: capture with `page.waitForEvent('download')`, parse text with a PDF library, assert
  the numbers. Do not assert visual layout (that is `Manual`).

## Data Isolation

- Each test or E2E flow creates its own apartment and contact through the API
  (name pattern `AT-<yyyymmdd>-<workerIndex>-<random>`), so balances start from zero.
  This includes smoke: the stages in `suites/smoke.md` are a reading order, not shared data.
- Global totals (Dashboard, AR summary, cash account balances) are shared by every test.
  Assert **deltas** captured before/after, scoped to your own documents where possible; if a
  case can only assert an absolute global total, put it in a `*.serial.spec.ts` file, which
  runs in the `serial-global-totals` project with one worker (see `configuration.md`).
- Approved financial documents cannot be deleted. "Cleanup" means unique data per run on a
  dedicated test environment, not deletion. Draft documents may be deleted when the API allows.
- Back-dated and month-end cases (OB/CB, E2E-10): pass explicit dates; use `page.clock` only for
  UI date defaults. Never depend on today's date being mid-month.

## Concurrency Cases (CONC-*, E2E-09)

- Use separate API contexts (or browser contexts) per simulated user.
- Fire the conflicting requests together with `Promise.all`, then assert the outcome the case
  states: one accepted and one rejected for full / exceeding payments (CONC-001, -002, -004…),
  **both accepted** for partials within the balance (CONC-003). Always also assert the final
  invoice due amount and status.
- Repeat each concurrency test several times (`--repeat-each`) before trusting a pass.

## Known Product Bugs

`docs/ems-knowledge/GOTCHAS.md` lists defects found in code (e.g. the partner API marks
partial payments as PAID). When a case hits one **and the defect is confirmed on the test
environment** (GOTCHAS was written from code reading), keep the correct expected result and
mark the test `test.fail()` with the GOTCHAS reference, so the test alerts when the bug is fixed.
`test.fail()` passes on *any* failure, including a broken locator, so make the steps before the
buggy assertion pass first (assert them explicitly) and re-check these tests whenever the
page they touch changes.

## Safety

- Only test environments listed in `.env` / CI variables. Abort if `BASE_URL` looks like production.
- Never run `php artisan ems:run` or any DB reset from tests.
- Partner API tests use a dedicated test API key; payments created there are real records
  in the shared DB.
- Do not upload real resident data; generate NRC / phone / names.
