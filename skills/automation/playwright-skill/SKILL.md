---
name: playwright-skill
description: >
  Set up, design, implement, review, debug, heal, and report production-grade
  Playwright TypeScript automation using canonical test cases and project-aware architecture.
---

# Playwright Skill

## Purpose

Implement approved `TC-*` test cases with a maintainable Playwright TypeScript framework.

This skill also supports:

- creating a Playwright repository from scratch;
- reviewing an existing Playwright repository;
- targeted Website Discovery for Brownfield projects;
- planning automation from canonical test cases;
- implementing UI and API automation;
- reviewing, refactoring, debugging, healing, and reporting.

## Preconditions

Before executing a Playwright task, determine:

- project mode;
- requested scope;
- whether Playwright already exists;
- repository conventions;
- approved `TC-*`;
- environment and base URL;
- credentials and roles;
- test-data strategy;
- cleanup strategy;
- permitted and forbidden discovery actions;
- required browsers and CI environment.

Do not claim setup or validation succeeded unless the commands were executed successfully.

## Global Rules

1. Inspect the repository before creating or moving files.
2. For a new repository, follow `references/project-setup-architecture.md`.
3. For an existing repository, preserve valid conventions unless restructuring is explicitly requested.
4. Implement only approved canonical `TC-*`.
5. `docs/test-cases.md` remains the single source of truth.
6. Planner may identify gaps, but validated gaps must be written back to canonical artifacts.
7. Use fixtures for dependency injection and lifecycle management.
8. Keep locators and reusable page interactions in Page or Component Objects.
9. Keep scenario-specific business assertions visible in specs.
10. Prefer API setup and cleanup when it is more reliable than UI setup.
11. Use Playwright web-first assertions and locator auto-waiting.
12. Do not use `page.waitForTimeout()` for synchronization.
13. Do not hide flakiness with retries.
14. Never perform unsafe Website Discovery actions.

## Task Routing

### Setup a New Repository

Read:

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

- `references/project-setup-architecture.md`
- `references/page-objects-components.md`
- `references/fixtures.md`
- `references/review-refactoring.md`

### Website Discovery

Read:

- `references/website-discovery.md`
- `references/network-mocking.md`

### Plan Automation

Read:

- `references/planner.md`
- `references/fixtures.md`
- `references/test-data.md`
- `references/authentication.md`

### Implement UI Automation

Read:

- `references/page-objects-components.md`
- `references/fixtures.md`
- `references/ui-automation.md`
- `references/assertions-waiting.md`
- `references/test-data.md`

### Implement API Automation

Read:

- `references/api-testing.md`
- `references/fixtures.md`
- `references/test-data.md`

### Review, Refactor, or Heal

Read:

- `references/review-refactoring.md`
- `references/debugging-healing.md`
- `references/reporting.md`

## Setup Workflow

1. Inspect repository and application technology.
2. Detect package manager.
3. Check whether Playwright already exists.
4. Initialize Playwright only when absent.
5. Create the expected structure for a new project.
6. Configure TypeScript, Playwright, linting, formatting, environment, aliases, and npm scripts.
7. Add minimal Page Object, Component, API client, fixtures, and example test.
8. Add authentication only when required.
9. Run validation.
10. Report files created, commands executed, failures, and remaining manual steps.

## Automation Workflow

```text
Approved TC-*
→ Planner review
→ Gap classification
→ Canonical artifact update
→ Implementation plan
→ Generator
→ Reviewer
→ Targeted healing
→ Reporting
```

## Required Completion Summary

Report:

- files created or modified;
- test cases implemented;
- commands executed;
- validation results;
- blockers;
- remaining manual work.
