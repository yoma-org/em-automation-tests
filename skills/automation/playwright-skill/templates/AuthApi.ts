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
