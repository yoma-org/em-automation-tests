# CI/CD

Recommended steps:

```yaml
- run: npm ci
- run: npx playwright install --with-deps
- run: npm run typecheck
- run: npm run lint
- run: npx playwright test
```

Publish:

- HTML report;
- traces for failures;
- screenshots and videos when retained;
- test results required by the CI platform.

Use sharding only when test isolation and data strategy support it.
