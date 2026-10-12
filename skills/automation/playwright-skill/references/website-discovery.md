# Website Discovery

## Purpose

Allow the Planner to use Playwright to understand a released website before automation planning.

## Required Preconditions

- environment name;
- base URL;
- target module;
- allowed roles;
- credentials mechanism;
- test data;
- cleanup strategy;
- permitted actions;
- forbidden actions;
- feature flags, tenant, region, and locale;
- handling rules for CAPTCHA, MFA, email, SMS, payment, upload, and third parties.

If required preconditions are missing, do not interact with the application.

## Discovery Scope

Planner may inspect:

- navigation;
- visible modules and features;
- forms and validation;
- tables, search, filter, sort, pagination;
- dialogs and notifications;
- role-based visibility;
- URL transitions;
- network requests and responses;
- cookies and storage when permitted;
- feature flags exposed to the client.

## Safety Boundaries

Do not:

- make real payments;
- send real email or SMS;
- approve, reject, refund, publish, or delete production data;
- bypass CAPTCHA or MFA;
- crawl without a target boundary;
- perform load or security testing.

## Output

Update `docs/feature-map.md`.

Potential coverage findings use temporary `GAP-*`.
They become `TC-*` only after validation.
