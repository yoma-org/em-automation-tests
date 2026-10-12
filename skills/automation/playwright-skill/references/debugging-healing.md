# Debugging and Healing

Use:

```bash
npx playwright test --debug
npx playwright test --ui
npx playwright show-trace <trace.zip>
```

Healing workflow:

1. reproduce failure;
2. inspect trace, screenshot, logs, and network;
3. classify application, automation, environment, data, or requirement issue;
4. apply the smallest safe fix;
5. rerun targeted test;
6. rerun affected suite;
7. report evidence.

Do not blindly replace locators or increase timeouts.
