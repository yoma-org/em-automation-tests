---
name: playwright-skill
description: >
  Set up, design, implement, review, debug, heal, and report Playwright TypeScript
  automation for the EM (Estate Management) project from the canonical test cases in
  docs/test-cases/. Use when writing or changing specs, Page Objects, fixtures, API
  clients, test data, or Playwright config; when turning a test case ID (AUTH-001,
  INV-017, OB-SOA-007, CONC-003, E2E-01…) into a test; when reviewing or healing tests;
  or when coordinating the playwright-test-planner / generator / healer agents.
---

# Playwright Skill

## Purpose

Implement approved EM test cases with a maintainable Playwright TypeScript framework.

This skill also supports:

- creating the Playwright framework from scratch;
- reviewing an existing Playwright repository;
- targeted Website Discovery;
- planning automation from canonical test cases;
- implementing UI and API automation;
- reviewing, refactoring, debugging, healing, and reporting.

**Always read `references/em-project.md` first.** It holds the EM-specific rules
(roles, encrypted API responses, two APIs, tags, data isolation, safety) that override
the generic examples in the other references.

## Canonical Test Cases

- Source of truth: the case sections in `docs/test-cases/features/**/*.md`. `docs/test-cases/test-catalog.csv`,
  the suites and the summary tables are generated from them by `npm run cases:build`.
- Cross-module flows: `docs/test-cases/suites/e2e-critical-flows.md` (`E2E-01` … `E2E-12`).
- IDs are `<FEATURE>-<nnn>` (e.g. `AUTH-001`, `INV-017`, `OB-SOA-007`). Keep the source ID
  (e.g. `TC_Login_001`) for traceability.
- Business context: `docs/EM_Business_Summary.md` and `docs/ems-knowledge/`.

Status mapping:

| Status | Action |
|---|---|
| `Active` | Implement. |
| `Review` | Implement as the case states it, tag `@review`, annotate the open question (`status_note`). Use `test.fixme()` only when there is no usable expected result. Never invent one. |
| `Obsolete` | Do not implement. |
| Automation `Manual` | Do not implement; list it as manual-only in the report. |

## Preconditions

Before executing a Playwright task, determine:

- requested scope (IDs, feature, suite);
- whether the framework pieces it needs already exist;
- environment and base URLs (web, back-office API, partner API) — never production;
- roles and credentials needed (maker / checker / partner API key);
- test-data strategy (fresh apartment / contact per test or flow);
- permitted and forbidden discovery actions.

Do not claim setup or validation succeeded unless the commands were executed successfully.

## Global Rules

1. Inspect the repository before creating or moving files.
2. For a new setup, follow `references/project-setup-architecture.md`.
3. Preserve valid existing conventions unless restructuring is explicitly requested.
4. Implement only `Active` and `Review` canonical cases, as the Status mapping says; never `Obsolete` or `Manual`.
5. `docs/test-cases/` remains the single source of truth; the Planner never owns a separate case set.
6. Validated gaps are written back to the feature file in `docs/test-cases/` and the catalog rebuilt
   (`npm run cases:build`), not kept only in `specs/`.
7. Use fixtures for dependency injection and lifecycle management.
8. Keep locators and reusable page interactions in Page or Component Objects.
9. Keep scenario-specific business assertions visible in specs.
10. Prefer API setup when it is more reliable than UI setup.
11. Use Playwright web-first assertions and locator auto-waiting.
12. Do not use `page.waitForTimeout()` for synchronization.
13. Do not hide flakiness with retries.
14. Never perform unsafe Website Discovery actions.
15. One merged case with Data variants = one parameterized test, one run per variant.
    The catalog has one `canonical` row per case and one `variant` row per extra variant;
    plan by canonical row, never one test case per catalog row.
16. Every implemented case has its own test in `tests/<feature>/`, whether or not an E2E flow
    also covers it.
17. Before reporting, run `node .claude/skills/playwright-skill/scripts/check-traceability.mjs`
    and fix what it reports.

## Playwright Agents

The repo has `.claude/agents/playwright-test-planner.md`, `-generator.md`, `-healer.md`
and the `playwright-test` MCP server. Use them within this skill's architecture:

- **Planner** explores the app and saves plans to `specs/`. A plan must reference canonical
  IDs; anything new is a `GAP-*` until validated (see `references/planner.md`).
- **Generator** records a working flow and writes a raw spec under `tests/_drafts/`.
  Treat its output as a **draft**: move locators into Page/Component Objects, switch
  imports to `@fixtures`, add tags and the `tc` / `source` annotations, then delete the draft.
- **Healer** fixes failing tests. Its fixes must land in the Page Object, not as inline
  locators in specs, and must follow `references/debugging-healing.md`.
- `tests/seed.spec.ts` is the agents' starting point. Once the framework is set up it
  imports from `@fixtures` and starts authenticated (`templates/seed.spec.ts`); check the
  repo, because until then it is the empty generated file.
- Each agent file starts with an **"EM project rules"** block that points it to this skill.
  `npx playwright init-agents` overwrites the agent files: after running it, restore the
  blocks from `references/agent-overrides.md`.

## Task Routing

### Setup the Framework

Read:

- `references/em-project.md`
- `references/project-setup-architecture.md`
- `references/configuration.md`
- `references/page-objects-components.md`
- `references/fixtures.md`
- `references/authentication.md`
- `references/test-data.md`
- `references/ci-cd.md`

Use templates under `templates/`.

### Review Existing Framework Architecture

Read:

- `references/em-project.md`
- `references/project-setup-architecture.md`
- `references/page-objects-components.md`
- `references/fixtures.md`
- `references/review-refactoring.md`

### Website Discovery

Read:

- `references/em-project.md` (Safety)
- `references/website-discovery.md`
- `references/network-mocking.md`

### Plan Automation

Read:

- `references/em-project.md`
- `references/planner.md`
- `references/fixtures.md`
- `references/test-data.md`
- `references/authentication.md`

### Implement UI Automation

Read:

- `references/em-project.md`
- `references/page-objects-components.md`
- `references/fixtures.md`
- `references/ui-automation.md`
- `references/assertions-waiting.md`
- `references/test-data.md`

### Implement API Automation (including Auto-UI+API money checks)

Read:

- `references/em-project.md`
- `references/api-testing.md`
- `references/fixtures.md`
- `references/test-data.md`

### Review, Refactor, or Heal

Read:

- `references/em-project.md` (money assertions, `@review`, Known Product Bugs)
- `references/review-refactoring.md`
- `references/debugging-healing.md`
- `references/reporting.md`

## Setup Workflow

1. Inspect repository and application technology.
2. Detect package manager.
3. Check whether Playwright already exists (it does: `@playwright/test` is installed).
4. Initialize Playwright only when absent.
5. Create the expected structure.
6. Configure TypeScript, Playwright, linting, formatting, environment, aliases, and npm scripts.
7. Add minimal Page Object, Component, API client, fixtures, and example test.
8. Add role-based authentication setup.
9. Run validation, including `scripts/check-traceability.mjs`.
10. Report files created, commands executed, failures, and remaining manual steps.

## Automation Workflow

```text
Active / Review case IDs (canonical rows; variants come with their case)
→ Planner review (+ optional discovery)
→ Gap classification
→ Canonical artifact update
→ Implementation plan
→ Generator (draft) → refactor into POM / fixtures
→ Reviewer
→ Targeted healing
→ Reporting
```

## Required Completion Summary

Report:

- files created or modified;
- test case IDs implemented (and those tagged `@review`, left as `fixme`, or manual);
- commands executed;
- validation results;
- blockers;
- remaining manual work.
