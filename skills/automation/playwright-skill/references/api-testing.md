# API Testing

## API Client

```ts
import { type APIRequestContext, expect } from '@playwright/test';

export class AuthApi {
  constructor(private readonly request: APIRequestContext) {}

  async login(email: string, password: string): Promise<string> {
    const response = await this.request.post('/api/auth/login', {
      data: { email, password }
    });

    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    return body.token;
  }
}
```

## API Test

```ts
import { test, expect } from '@fixtures';

test('TC-API-AUTH-001 valid credentials return token', async ({ authApi }) => {
  const token = await authApi.login('user@example.com', 'secret');
  expect(token).toBeTruthy();
});
```

Validate:

- status;
- headers;
- body;
- schema or contract;
- permissions;
- error handling;
- business rules;
- data consistency.
