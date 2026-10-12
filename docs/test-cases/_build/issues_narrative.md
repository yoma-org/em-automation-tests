## Decisions needed (business / EM team)

| # | Topic | Detail | Affects |
|---|---|---|---|
| D1 | Admin self-approval | EM initial findings: Admin could not approve its own Invoice / DN / UO / EM, or create Setting items. Is this maker–checker by design or a defect? | {{Role&Permission#8}}, {{Role&Permission#12}}, E2E-12 |
| D2 | Cash Transfer approval | No Cash Transfer case mentions approval. The business summary says a JV posts only on approval. | {{Cash Transfer#5}}, E2E-07 |
| D3 | Cash Outflow approval | {{Cash Outflow#5}} expects draft + approver notification. The overdraft case expects immediate "Transaction Added Successfully". | {{Cash Outflow#14}} |
| D4 | Minimum document amount | Invoice min 0.1 vs debit note min 0.01 (GT remark Aug-2025 asks the same). | {{Invoice-Debit Note#23}}, {{Invoice-Debit Note#41}} |
| D5 | Same-month UO import after a manual reading | Onenex: "not included in v4 release, user can't import". Contradicts the UO sheet, which allows it. | {{Uo import#4}}, {{UO#13}} |
| D6 | Editing initial balance after transactions | Allowed, with closing balance recalculated. Confirm with Finance that this is intended (audit risk). | {{Cash and Bank Account#19}} |
| D7 | API error status codes | Invalid ID / params / disabled apartment expect **401** in some rows and **200 + error** in others. 401 is the wrong code for bad input. | {{API#23}}, {{API#35}}, {{API#36}}, {{API#51}} |
| D8 | Error message wording (new EM vs sheet) | New EM: "Insufficient wallet balance" / "Insufficient deposit balance". Sheet: "Insufficient Balance in 'Withdraw From' Account" or "Invalid Amount". Behaviour matches; agree the wording and update the expected results. | {{Wallet - OB & CB#130}}, {{Deposit - OB & CB#46}}, {{Cash Outflow#10}} |
| D9 | Permission model changes (ZL comments) | No separate Dashboard permission. Extra View permissions are needed for Contact, Invoice and Wallet. One "Reports" permission replaces per-report permissions (accepted as a known difference). | {{Role&Permission#3}}, {{Role&Permission#25}}, {{Role&Permission#76}} |

## Known defects referenced in the workbook

| Defect | Source | Cases |
|---|---|---|
| UO unit calculation wrong after meter reset (import) | Onenex, v4 | {{Uo import#5}}, {{UO#19}} |
| Make payment via API does not create the RV in Cash Received | ZL comment | {{API#67}} |
| Report Contact filter does not fully work (EM: keep unchanged in production) | EM team | {{Reports#41}} |
| CLEARED status filter has no effect (status field removed from Make Payment) | EM team | {{Reports#38}} |
| Search: Location matches name only; Zone / Building have no search box; Staff matches email only | ZL comment | {{Setting#75}} |

## Wrong or contradictory expected results (fix in source)

- Copy-paste errors:
  - Deposit-overflow assignment expects a *wallet* update ({{Make Payment#19}}).
  - A cheque payment expects a WP code ({{Make Payment#25}}).
  - A PV expects an RV in the Cash Received list ({{Cash Outflow#6}}).
  - The Cash Outflow report expects "cash received" data ({{Reports#78}}).
  - Expense categories are checked on the invoice form ({{Setting#36}}).
- EM approval expected results say "invoice", but EM produces **debit notes** ({{EM#9}}).
- 1 Inv × 2 RV: a partial payment + full SCLA expects "paid in full" although only 500 / 1,000 is paid ({{1Inv 2RV#30}}).
- Login:
  - An unregistered email is expected to show "Email is not a valid email address" ({{Login#6}}).
  - The password-required error is placed under the email field ({{Login#10}}).
  - The steps contradict the data ({{Login#11}}).
- UO#13 / UO#14 data has a year typo (2024 vs 2025), so the "same month" scenario is not really the same month ({{UO#13}}).
- Concurrency rows keep the expected result in the *Check area* or *Data* column, not *Expected* ({{SOA - OB & CB#314}}, {{Deposit - OB & CB#46}}).
- 96 SOA rows (r72–r167) have the section label "High". The real label is "2 different transaction types at the same time" ({{SOA - OB & CB#72}}).
- Titles swap min/max on wallet amounts (0.1 called "maximum") ({{Wallet#9}}).
- Found in the merge review (11 Oct 2026):
  - A successful delete is described as an "error message" ({{Invoice-Debit Note#24}}, {{Invoice-Debit Note#43}}).
  - The zero-Unit message differs: invoice "The selected Unit is invalid." vs debit note "Unit is required." ({{Invoice-Debit Note#16}}, {{Invoice-Debit Note#34}}).
  - The data note says the latest reading is a bulk upload, which contradicts the title ({{UO#17}}). The title says "same unit", but the expected result fails the record for lower units ({{Uo import#24}}).
  - An overdraft PV expects "Transaction Added Successfully" and an immediate balance update, but every PV is saved as a draft for approval ({{Cash Outflow#14}}; see D3).
  - The Received-In account list filtered by payment method is never asserted, though it is the point of the case ({{Make Payment#7}}).
  - A wallet payment asks for a Received-In account ({{Wallet#29}}). The wallet refund precondition is copied from wallet payment ({{Wallet#41}}). Wallet-transfer steps say "Click Recharge" ({{Wallet#17}}).
  - A $10 Funding receipt goes into an MMK cash account (Cash Received r10, in {{Cash Received#9}}).
  - 1 Inv × 2 RV r14 (WP 1000 then SCLA 1000) expects only the UI message; every other SCLA-second row also expects API "Invalid Amount" ({{1Inv 2RV#4}}). It probably belongs with {{1Inv 2RV#7}}.
  - Where the two partial payments add up to the full invoice (500 + 500), the final invoice status (Paid, nothing due) is never asserted ({{1Inv 2RV#18}}).
  - Contact payments are said to be stored in the *contact's* SOA; only apartments have an SOA ({{Contacts#49}}, {{Contacts#51}}, {{Contacts#54}}, {{Contacts#56}}).
  - Wrong preconditions on the contact summary cases ({{Contacts#37}}, {{Contacts#38}}). The apartment note case says "Contact" ({{Apartments#67}}).
  - The token request uses an "invalid authentication token" instead of invalid client credentials ({{API#5}}). API r29 copies its expected text from the contact-detail row ({{API#9}}).
  - Permission-denied API rows expect **401**. For a logged-in caller without the permission, the usual code is **403** ({{API#8}}, {{API#69}}). Settle this together with D7.
  - The steps edit the user's own account, but the title is about the admin's password ({{Setting#119}}). Cash Outflow report preconditions list RV types instead of PV types ({{Reports#40}}). The Edit permission says "Can View" ({{Role&Permission#75}}).
  - Minimum amount is 0.01 on Cash Received / Outflow / Transfer / Cash & Bank Account, but 0.1 on wallet recharge / transfer / CN / refund and deposit withdraw. Zero-amount and over-balance messages also differ by form. One rule is needed before these are asserted.
  - Login: the message for an unregistered email differs from the one for a wrong password ({{Login#6}}). This lets anyone find out which emails are registered; use one generic message.

## Coverage gaps (no case exists — recommend adding)

| Gap | Asked for by | Suggested home |
|---|---|---|
| **Reject** an Invoice / DN / UO / EM / CN / PV draft → no AR, SOA or numbering effect | Business summary (approval backbone) | 04 Invoice, 05 UO, 07 EM, E2E-03 |
| Login with leading / trailing spaces; first login of a newly created user | GT remarks Aug-2025 | 01 Login |
| USD invoice / DN; payment terms Due-on-receipt / +30 / +45 / +60 / +90; tax 5% / No tax / Incl. 5% / Incl. 3%; decimal paste in unit / discount | GT remarks Aug-2025 | 04 Invoice |
| Bulk SOA in USD | GT remarks Aug-2025 | 03 AR |
| Back-dated Make Payment RV, Wallet Payment and Wallet Transfer in the OB/CB matrices | Matrix review | 19 / 20 balances |
| Account-statement back-dated RV for Wallet recharge, Add deposit, Make payment and SCLA | Matrix review | 22 balances |
| Delete a contact that is linked to an apartment or has invoices | Matrix review | 09 Contacts |
| Multi-record UO import rows lost their second data row in the source | Matrix review | 06 UO import |
| Deposit - OB & CB r15 / r18 duplicate r14 / r17 exactly; probably meant another currency | Matrix review | 21 balances |

### Coverage gaps found in the completeness review (11 Oct 2026)

The catalog covers the happy paths and field validation well. What is missing is mostly **reversal**, **negative permission**, **calculated amounts** and **cross-module reconciliation**: the places where a finance system loses money silently.

| Pri | Gap | Why it matters | Suggested home |
|---|---|---|---|
| P1 | **Void / reverse an approved document** (Invoice, DN, RV, PV, CN, WT, JV), including one dated in an earlier month. Check that invoice status, AR, wallet / deposit, account balance and SOA roll back, and that the OB/CB of **every** later period is recalculated. | No reversal path is tested anywhere; the OB/CB matrices only add transactions. | 04, 10, 11, 13, 19–22 |
| P1 | **Edit after approval is blocked**; edit a **draft** (items, tax, discount, amount, account) and check the approved values. | Inv/DN, PV, CN and DI have no edit case. Approved finance documents must not change. | 04, 13, 16 |
| P1 | **Negative permission tests and maker–checker.** A user without the permission gets no button and is refused on direct URL / API. Can the creator approve their own draft? A permission change applies to an active session. | The Role & Permission suite only tests "can do X". Access leaks are the main risk (see D1). | 24, 04, 05, 07, 13 |
| P1 | **Calculated amounts.** Inv/DN line = unit × price − discount + tax (incl. inclusive tax), rounded to 2 dp, with multi-line totals. UO = consumption × tariff per meter type. EM DN = fee × months, with the auto "to" date (month end, leap year). The same numbers must appear in list, detail, PDF, AR and SOA. | Current cases only assert that a document was issued. | 04, 05, 07 |
| P1 | **Multi-currency rounding.** Pay in another currency (FX to 2 dp, 0.01 residual due, overflow converted to wallet). MMK and USD balances stay separate and do not drift as they carry forward. | Rounding leaves invoices Partial and makes CB ≠ next OB by cents. | 10, 16, 19–22 |
| P1 | **Balance rechecked at approval.** Two refund / withdraw / PV drafts each within the balance but over it together, approved at the same time. One wallet spent on different invoices at the same moment. | Drafts do not reserve money; concurrency cases cover only one invoice. | 13, 16, 17, 20, 21 |
| P1 | **Month boundary and time zone.** Transactions at 23:59:59 and 00:00 Myanmar time (UTC+6:30); a back date 2+ months ago updates every month in between; an unknown RV received in month M and assigned in M+1. | UTC storage commonly moves late-evening entries to the wrong day or month. | 19–22 |
| P1 | **Reconciliation between modules.** Dashboard AR = AR page = sum of the list. SOA closing = apartment outstanding = AR aging = API. Account Statement = Cash & Bank balance = Transactions report. Export rows and totals = screen. | Each sheet checks its own ledger in isolation. | 02, 03, 18, 19–22, E2E |
| P1 | **Make Payment API boundaries and retries.** Partial payment, amount over the balance, zero / negative, more than 2 dp, wrong currency, paying a Paid / Draft invoice. Duplicate submit, and API + UI paying the same invoice at once. | External callers retry; duplicate RVs mean over-collection. | 26 |
| P1 | **Owner / tenant rules.** Overlapping periods, end date not after start date, duplicate current owner. Which contact holds existing unpaid invoices after an owner change. | The rules are written in the data column, but only the positive path is tested. | 08, 09 |
| P1 | **UO price change** with UO drafts already in progress (draft-time vs approval-time rate). | Billing correctness for drafts in flight. | 23, 05 |
| P1 | **Back-dating into a month whose SOA was already issued**, and the audit trail for back-dated or late-approved entries. | Statements already sent to residents could change silently. | 19, 22 |
| P2 | **Aging bucket edges** (day 0/1, 30/31, 180/181) and bucket % adding up to 100 %. | Cards are only checked for being visible. | 02, 03, 08 |
| P2 | **Bulk approve with one invalid draft** (atomic or partial?), and two approvers on the same draft (no double invoice, no gap in numbering). | Bulk approval can create duplicates or skip numbers. | 05, 07 |
| P2 | **Year boundary** (Dec → Jan) and Feb 28/29 for back-dated entries; months with no activity carry OB = CB; an apartment's first SOA month. | The matrices use a generic 1st / mid / last day. | 19–22 |
| P2 | Wallet / deposit movements **do not change** the SOA AR balance. | A cheap negative assertion that catches ledger mix-ups. | 19 |
| P2 | Cheque lifecycle: pending → cleared / bounced; a bounced cheque reopens the invoice and reverses the cash. | {{Cash Received#33}} is vague. | 11 |
| P2 | Invalid targets: transfer to the same account; wallet transfer to the same, a disabled or a different-currency apartment; account currency must match the transaction currency. | Money can be stranded or double counted. | 14, 15, 16 |
| P2 | Disable a currency / payment method / account type / category / apartment that pending drafts or balances still use; edit a contact to an ID or email already taken. | Disable cases only check form visibility. | 08, 09, 23 |
| P2 | Drafts, removed and rejected items are **excluded** from the reports. | Finance reports must show approved postings only. | 18 |
| P2 | Lower date limit for Inv/DN (first day of last month accepted, earlier rejected); meter reset dated on or before the last reading; import with an unknown apartment code or a wrong date / number format. | Only the upper or positive edge is tested. | 04, 05, 06 |
| P2 | Login security: deactivated user, lockout after failures, session timeout, logout + back button. API token expiry and revoked credentials. Global Search does not return entities the user cannot view. | Basic authentication and data-exposure checks. | 01, 25, 26 |
| P2 | Voucher / PDF **content** (number, date, payer, amount, amount in words, currency, approver), not only "can be printed". | Vouchers are audit documents. | 11, 13, 14, 16, 17 |
| P3 | Audit log of role, permission, UO price and ownership changes; duplicate staff email; password policy. | Config changes must be traceable. | 23, 24 |

## Workbook reconciliation

- The "Test Case Count" sheet claims **1,520** cases. Parsing the module sheets gives **1,539** rows with a test intent.
- The difference comes from:
  - matrix header rows without a priority (SOA r22, r28, r32 …);
  - duplicated blank-title rows in Wallet OB/CB;
  - the 2 "approved during import" rows in EM.
- All 1,539 rows are kept and traceable in [`test-catalog.csv`](test-catalog.csv).
- Credentials found in the source (superadmin email / password) are **masked** in these docs (`<ADMIN_EMAIL>`, `<VALID_PASSWORD>`). Supply them from the test environment's secrets, never from the repo.
