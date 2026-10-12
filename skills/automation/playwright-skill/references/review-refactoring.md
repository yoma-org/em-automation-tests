# Review and Refactoring

Review:

- architecture;
- locator quality;
- Page Object responsibilities;
- fixture scope;
- setup and cleanup;
- data isolation;
- assertions;
- hardcoded waits;
- duplicated workflows;
- parallel safety;
- traceability.

Refactor only after preserving behavior.

Avoid moving all common methods into `BasePage`.
Prefer composition and domain-specific helpers.
