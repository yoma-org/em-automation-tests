# Website Discovery

## Purpose

Allow the Planner (or the `playwright-test-planner` agent) to use Playwright to understand
em-web before automation planning.

## Required Preconditions

- environment name and `BASE_URL` (a test environment, never production);
- target module;
- allowed roles and their credentials from `.env`;
- test data to use (a dedicated discovery apartment / contact);
- permitted actions;
- forbidden actions;
- handling rules for uploads (UO import files), PDFs, notifications and the partner API.

If required preconditions are missing, do not interact with the application.

## Discovery Scope

Planner may inspect:

- navigation and menus per role (CASL hides items the role cannot use);
- visible modules and features;
- forms and validation;
- PrimeVue tables: search, filter, sort, pagination;
- dialogs, confirmations and toasts;
- role-based visibility;
- URL transitions;
- network requests (endpoints and status codes; bodies are encrypted `payload`);
- local storage keys (values are encrypted).

## Safety Boundaries

Do not:

- **approve** any financial document (UO, EM, invoice, debit note, RV, PV, JV, wallet,
  deposit) — approval writes ledger rows that cannot be deleted;
- make payments, transfers, refunds or withdrawals;
- run UO / EM imports with real data;
- change Settings (categories, prices, payment terms) — EM approval depends on them;
- create or edit roles and permissions;
- delete any record you did not create in this session;
- crawl without a target boundary;
- perform load or security testing.

Creating drafts on the dedicated discovery apartment is allowed when the precondition lists it.

## Output

The plan goes to `specs/<module>.md` (the agent's `planner_save_plan`). Map every scenario
to an existing case ID.

Potential coverage findings use temporary `GAP-*`.
They become canonical cases only after validation (see `references/planner.md`).
