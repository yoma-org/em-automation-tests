# Test Data

## Static Data

Use `test-data/` for stable JSON or CSV inputs.

## Generated Data

```ts
import { faker } from '@faker-js/faker';

export function buildUser(overrides: Partial<User> = {}): User {
  return {
    email: faker.internet.email(),
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    ...overrides
  };
}
```

## Rules

- generated data must be reproducible when debugging;
- sensitive data must not be committed;
- cleanup must be defined;
- tests must not depend on pre-existing mutable records;
- data should match the business partition being tested.
