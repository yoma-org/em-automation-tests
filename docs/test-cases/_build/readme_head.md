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

