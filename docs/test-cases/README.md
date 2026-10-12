# EM Test Cases — Smoke · E2E · Regression

Consolidated test-case catalog for the **Estate Management System (EM)** rebuild (TED estate, Yoma Land × Zeya Labs). It is the baseline for building the automated **Smoke**, **E2E** and **Regression** suites.

| | |
|---|---|
| **Source** | `ZL_TED EM Test Case for Round Testing (2026)_19082026.xlsx` (SharePoint, last modified 9 Oct 2026). 27 test sheets, prepared by the EM QA team |
| **Consolidated** | 11 Oct 2026 |
| **Business context** | [EM Business Summary](../EM_Business_Summary.md) |

## How to read this

**Priority**

| | Meaning |
|---|---|
| **P1** | Money correctness or a critical business flow: create / approve financial documents, payments and allocation, wallet / deposit / cash balances, AR / SOA / OB-CB, login, approval permissions. Must pass to release. |
| **P2** | Core functional behaviour that does not calculate money: list / view / filter / edit / delete of master data, PDF content, report filters, data-integrity validation, view / create permissions. |
| **P3** | Field-level and UI validation, messages, sorting, cosmetic. |

**★ Critical business flow** — the case directly exercises one of these:

1. Billing: UO → invoice, EM → debit note, manual Inv / DN with approval.
2. Collection: payment → allocation → invoice status → AR.
3. Balance continuity: OB = previous CB.
4. Maker–checker and concurrency protection.
5. Access to money operations.

**Suites** (one case can be in several)

- `Smoke`: a small happy-path set run on every deploy.
- `E2E`: the case is a step in a cross-module flow, composed into flows in [e2e-critical-flows.md](suites/e2e-critical-flows.md).
- `Regression`: every non-obsolete case, run in tiers R1 / R2 / R3.

**Automation**

| Tag | Meaning |
|---|---|
| `Auto-UI` | Browser automation; assert on screen. |
| `Auto-UI+API` | Act in the UI, assert the numbers via API or parsed PDF. Used for most money checks. |
| `Auto-API` | Pure API test, including parallel requests for race conditions. |
| `Manual` | Physical print, visual layout or untestable-as-written. The reason is given on each case. |

**Status:** `Active` · `Review` (expected result or behaviour needs confirmation — see [source-issues.md](source-issues.md)) · `Obsolete`.

**Merged cases.** Duplicates and "same check, different data" rows were combined into one canonical case. The merged rows are listed in that case's **Data variants** table. Automate each such case as **one parameterized / data-driven test** with one row per variant. The full merge list is in [duplicates-merged.md](duplicates-merged.md).

**IDs.** `<FEATURE>-<nnn>`, for example `INV-017` or `OB-SOA-007`. Every case keeps its source sheet, row and original ID (e.g. `TC_Inv_021`) for traceability.


## At a glance

| | |
|---|---|
| Source rows read | 1539 |
| Test cases after merging | **599** (940 rows merged as duplicates / data variants) |
| ★ Critical business flow | 208 |
| Priority P1 / P2 / P3 | 225 / 303 / 71 |
| Smoke / E2E-tagged | 56 / 198 (+ 12 composed [E2E flows](suites/e2e-critical-flows.md)) |
| Automatable / Manual | 590 / 9 |
| Review (open question) / Obsolete | 53 / 0 |

## Suites

| Suite | File | Size | Purpose |
|---|---|---|---|
| Smoke | [suites/smoke.md](suites/smoke.md) | 56 cases | Every deploy — can EM still bill, collect and report? |
| E2E | [suites/e2e-critical-flows.md](suites/e2e-critical-flows.md) | 12 flows | ★ Critical business flows chained across modules |
| Regression | [suites/regression.md](suites/regression.md) | R1 / R2 / R3 tiers | Coverage per feature; manual-only list |

## Features

| # | Feature | Cases | ★ | P1 | Smoke | Auto | Manual | Source sheet(s) |
|---|---|---|---|---|---|---|---|---|
| | **Billing** | | | | | | | |
| 04 | [Invoice & Debit Note](features/04-invoice-debit-note.md) | 37 | 7 | 7 | 4 | 35 | 2 | Invoice-Debit Note |
| 05 | [Utility Operations (UO) — manual entry](features/05-utility-operations-uo.md) | 28 | 8 | 8 | 2 | 28 | 0 | UO |
| 06 | [UO Import (bulk meter readings)](features/06-uo-import.md) | 38 | 11 | 11 | 1 | 37 | 1 | Uo import |
| 07 | [Estate Management Fee (EM)](features/07-estate-management-fee.md) | 17 | 6 | 6 | 3 | 17 | 0 | EM |
| | **Collection & cash** | | | | | | | |
| 10 | [Make Payment](features/10-make-payment.md) | 14 | 13 | 13 | 4 | 14 | 0 | Make Payment |
| 11 | [Cash Received (RV / Unknown / Funding)](features/11-cash-received.md) | 13 | 3 | 3 | 2 | 11 | 2 | Cash Received |
| 12 | [Payment Concurrency (1 Inv × 2 RV, 1 RV × 2 Inv)](features/12-payment-concurrency.md) | 7 | 7 | 7 | 0 | 7 | 0 | 1Inv 2RV, 1RV 2Inv |
| 13 | [Cash Outflow (PV)](features/13-cash-outflow.md) | 13 | 4 | 4 | 2 | 11 | 2 | Cash Outflow |
| 14 | [Cash Transfer (JV)](features/14-cash-transfer.md) | 12 | 4 | 4 | 1 | 10 | 2 | Cash Transfer |
| 15 | [Cash & Bank Account](features/15-cash-bank-account.md) | 20 | 2 | 4 | 1 | 20 | 0 | Cash and Bank Account |
| | **Apartment ledgers** | | | | | | | |
| 08 | [Apartments](features/08-apartments.md) | 33 | 9 | 15 | 3 | 33 | 0 | Apartments |
| 09 | [Contacts](features/09-contacts.md) | 32 | 8 | 13 | 1 | 32 | 0 | Contacts |
| 16 | [Wallet](features/16-wallet.md) | 32 | 9 | 9 | 5 | 32 | 0 | Wallet |
| 17 | [Deposit](features/17-deposit.md) | 25 | 6 | 6 | 3 | 25 | 0 | Deposit |
| | **Balances (OB / CB)** | | | | | | | |
| 19 | [SOA — Opening / Closing Balance](features/balances/19-soa-ob-cb.md) | 20 | 20 | 20 | 2 | 20 | 0 | SOA - OB & CB |
| 20 | [Wallet — Opening / Closing Balance](features/balances/20-wallet-ob-cb.md) | 13 | 13 | 13 | 1 | 13 | 0 | Wallet - OB & CB |
| 21 | [Deposit — Opening / Closing Balance](features/balances/21-deposit-ob-cb.md) | 13 | 13 | 13 | 1 | 13 | 0 | Deposit - OB & CB |
| 22 | [Account Statement — Opening / Closing Balance](features/balances/22-account-statement-ob-cb.md) | 11 | 11 | 11 | 2 | 11 | 0 | Acc Statement - OB & CB |
| | **Receivables & reporting** | | | | | | | |
| 02 | [Dashboard](features/02-dashboard.md) | 8 | 4 | 6 | 3 | 8 | 0 | Dashboard |
| 03 | [Accounts Receivable](features/03-accounts-receivable.md) | 18 | 2 | 4 | 2 | 18 | 0 | Accounts Receivable |
| 18 | [Reports](features/18-reports.md) | 35 | 4 | 4 | 2 | 35 | 0 | Reports |
| 25 | [Global Search](features/25-global-search.md) | 1 | 0 | 0 | 0 | 1 | 0 | Global Search |
| | **Platform** | | | | | | | |
| 01 | [Login & Authentication](features/01-login.md) | 6 | 1 | 1 | 1 | 6 | 0 | Login |
| 23 | [Settings (master data & configuration)](features/23-settings.md) | 50 | 3 | 3 | 1 | 50 | 0 | Setting |
| 24 | [Role & Permission](features/24-role-permission.md) | 76 | 29 | 29 | 5 | 76 | 0 | Role&Permission |
| 26 | [External API](features/26-api.md) | 27 | 11 | 11 | 4 | 27 | 0 | API |

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
