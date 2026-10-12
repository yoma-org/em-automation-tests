#!/usr/bin/env bash
set -euo pipefail

npm install
npx playwright install
npm run typecheck
npm run lint
npx playwright test --list
