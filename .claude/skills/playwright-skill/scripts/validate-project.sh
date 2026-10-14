#!/usr/bin/env bash
# Run from the repository root.
set -euo pipefail

npm ci
npx playwright install chromium
npm run typecheck
npm run lint
node .claude/skills/playwright-skill/scripts/check-traceability.mjs
