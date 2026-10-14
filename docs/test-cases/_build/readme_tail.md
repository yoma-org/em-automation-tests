## Other files

| File | What it is |
|---|---|
| [test-catalog.csv](test-catalog.csv) | One row per **source row**, with columns:<br>• new ID, canonical / variant<br>• feature and priority<br>• ★, smoke, E2E, regression<br>• automation, status, variant label<br>• source sheet / row / ID<br>Use it to import into a test-management tool or to drive automation tags. |
| [duplicates-merged.md](duplicates-merged.md) | Every merge: canonical case ← merged rows, and why. |
| [source-issues.md](source-issues.md) | Decisions needed, known defects, wrong expected results, coverage gaps, all cases in Review. |
| [_build/](_build/) | The scripts and annotation data that generated these docs (see below). |

## Suggested automation tagging

Tag each automated test from the catalog values, so suites can be selected without separate lists. The case ID goes in the test title (and a `tc` annotation), not in a tag:

```
INV-017 <title>   @P1 @critical @smoke @review
```

| Tag | On |
|---|---|
| `@P1` / `@P2` / `@P3` | every case (priority) |
| `@critical` | ★ cases (always P1) |
| `@smoke` | smoke cases (base row only for data-driven cases) |
| `@review` | cases with status Review |
| `@e2e` | only the 12 composed [E2E flows](suites/e2e-critical-flows.md); single cases marked E2E are listed in the flow, not tagged |

There is no `@regression` tag: every case is in regression.

| When | Run |
|---|---|
| Every deploy (smoke) | `--grep @smoke --grep-invert @review` |
| Every merge / nightly (R1) | `--grep @P1 --grep-invert @review` |
| Release candidate (R2) | `--grep "@P1\|@P2" --grep-invert @review` |
| Before production release (R3) | everything, `@review` included |
| E2E flows | `--grep @e2e` |
| Review cases (non-blocking report) | `--grep @review` |

Blocking gates leave out `@review`: their expected result is still in question, so a red one is checked against [source-issues.md](source-issues.md) instead of failing the build.

The full rules are in the Playwright skill (`.claude/skills/playwright-skill/references/em-project.md`).

## Updating

The feature files, suites and catalog are **generated**; do not hand-edit them, or the next regeneration will lose the changes. Two exceptions:

- [suites/e2e-critical-flows.md](suites/e2e-critical-flows.md) is hand-written.
- `_build/*.md` are hand-written fragments (README, issues).

To change a classification, edit `_build/annotations/*.json` and regenerate:

```bash
# from docs/test-cases/_build, with openpyxl installed
python3 normalize.py "<path to workbook>.xlsx" cases.json
python3 render.py cases.json annotations ..
python3 suites.py ..
```

When the source workbook gains or loses rows, row numbers shift. Re-check `annotations/*.json` keys (`"<Sheet>#<row>"`) before regenerating.
