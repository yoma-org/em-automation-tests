# Playwright Planner

## Inputs

- canonical `docs/test-cases.md`;
- business rules;
- automation plan;
- architecture;
- API specification;
- existing automation;
- optional Website Discovery evidence.

## Responsibilities

1. review canonical test cases;
2. inspect existing automation;
3. identify gaps, duplicates, blockers, and non-automatable cases;
4. validate gaps;
5. update canonical artifacts;
6. create implementation plan.

## Planner Output Example

| TC ID | Layer | Files | Fixtures | Data | Mock | Cleanup | Complexity |
|---|---|---|---|---|---|---|---|
| TC-AUTH-001 | UI | LoginPage, login.spec.ts | loginPage | valid user | No | None | Low |
| TC-USER-010 | API/UI | UsersApi, user.spec.ts | usersApi, createdUser | generated | No | API delete | Medium |

Planner never owns a separate test case set.
