# Network and Mocking

Use `page.route()` for controlled UI scenarios:

```ts
await page.route('**/api/products', async route => {
  await route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Product' }])
  });
});
```

Mock when:

- dependency is external;
- scenario is difficult to reproduce;
- deterministic failure behavior is required.

Do not mock the behavior being validated.
