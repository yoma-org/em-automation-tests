## Other files

| File | What it is |
|---|---|
| [test-catalog.csv](test-catalog.csv) | One row per **source row**, with columns:<br>• new ID, canonical / variant<br>• feature and priority<br>• ★, smoke, E2E, regression<br>• automation, status, variant label<br>• source sheet / row / ID<br>Use it to import into a test-management tool or to drive automation tags. |
| [duplicates-merged.md](duplicates-merged.md) | Every merge: canonical case ← merged rows, and why. |
| [source-issues.md](source-issues.md) | Decisions needed, known defects, wrong expected results, coverage gaps, all cases in Review. |
| [_build/](_build/) | The scripts and annotation data that generated these docs (see below). |

## Suggested automation tagging

Tag each automated test with the catalog values, so suites can be selected without separate lists:

```
@INV-017 @P1 @critical @smoke @e2e @regression   (Playwright: test.describe / grep tags)
```

- Smoke run: `--grep @smoke`
- R1 nightly: `--grep "@P1|@critical"`
- R2 release candidate: `--grep "@P1|@P2|@critical"`
- R3 full: everything.

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
