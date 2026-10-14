# Playwright Planner

## Inputs

- canonical cases: `docs/test-cases/features/**/*.md` and `docs/test-cases/test-catalog.csv`;
- E2E flows: `docs/test-cases/suites/e2e-critical-flows.md`;
- open questions: `docs/test-cases/source-issues.md`;
- business rules: `docs/EM_Business_Summary.md`, `docs/ems-knowledge/`;
- existing automation under `tests/` and `src/`;
- optional Website Discovery evidence (plans in `specs/`).

## Responsibilities

1. review the canonical cases in scope (filter the catalog by feature, suite or priority);
2. inspect existing automation (search `tests/` for the IDs);
3. identify gaps, duplicates, blockers, `Review` cases and manual-only cases;
4. validate gaps;
5. update canonical artifacts;
6. create implementation plan.

## Gaps

- A new scenario found by the planner or the `playwright-test-planner` agent is a `GAP-<n>`
  in the plan under `specs/`.
- It becomes a canonical case only after validation: add it to the feature file and
  `test-catalog.csv` with a new `<FEATURE>-<nnn>` ID. Do not edit generated sections by hand
  if `docs/test-cases/_build/` scripts own them; update the build input instead and say so.

## Planner Output Example

| Case ID | Layer | Roles | Files | Fixtures | Data | Mock | Tags | Complexity |
|---|---|---|---|---|---|---|---|---|
| AUTH-001 | UI | admin | LoginPage, tests/auth/login.spec.ts | loginPage, dashboardPage | env admin user | No | @smoke @P1 @critical | Low |
| UO-007 | UI+API | uo-operator → uo-manager | UoPage, UoApi, tests/uo/uo.spec.ts | asRole, apartment | fresh apartment | No | @smoke @P1 @critical | Medium |
| CONC-001 | API | 2 × cashier-operator | PaymentsApi, tests/payment/concurrency.spec.ts | apiAs, approvedInvoice | fresh invoice, base + variant rows | No | @P1 @critical | High |

Planner never owns a separate test case set. `specs/` holds plans, not cases.
