# CI/CD

Recommended steps:

```yaml
- run: npm ci
- run: npx playwright install --with-deps chromium
- run: npm run typecheck
- run: npm run lint
- run: node .claude/skills/playwright-skill/scripts/check-traceability.mjs
- run: npx playwright test --grep @smoke --grep-invert @review   # every deploy (blocking)
- run: npx playwright test --grep @P1 --grep-invert @review      # every merge / nightly (blocking)
- run: npx playwright test --grep @review                        # non-blocking report (continue-on-error)
- run: npx playwright test                                       # before production release
```

Environment values and credentials come from CI secret variables, never from the repo.

Publish:

- HTML report;
- traces for failures;
- screenshots and videos when retained;
- test results required by the CI platform (JUnit if needed).

Use sharding only when test isolation and data strategy support it. Tests in the serial
global-totals project must not be sharded.
