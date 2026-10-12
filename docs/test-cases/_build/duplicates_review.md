## Review result (11 Oct 2026)

Every merged row was re-read against its canonical case (title, preconditions, data, steps, expected result).

- **The merges hold up.** 939 of 940 stay merged. Only one row tests different behaviour and should be split (see the table below). No canonical mixes rows whose outcome is *accepted* with rows whose outcome is *rejected*; the concurrency cases are split correctly by outcome.
- **107 merges need care when automating (⚠️).** The variant stays in the data-driven test, but it adds or changes an assertion. The main patterns:
  - **Other currency / overflow to wallet or deposit.** Also assert the FX conversion and rounding, which currency the wallet is credited in, and that the overflow stays off the SOA balance.
  - **Same-time payment + payment pairs in the SOA matrix** (OB-SOA-011 … 016). If both payments hit the same open invoice, the second is rejected (see 12 Payment Concurrency). Use separate invoices, or assert the rejection.
  - **UO × UO and EM × EM pairs in {{SOA - OB & CB#248}}.** A second UO or EM for the same apartment and period may be blocked (relates to D5). Confirm before automating; split them out if they are blocked.
  - **Assigning an unknown RV on the account statement** ({{Acc Statement - OB & CB#4}}, {{Acc Statement - OB & CB#14}}). This reclassifies cash already in the bank, so the statement must show **no second inflow**. The generic expected text would let double counting pass.
  - **Over-balance concurrency** ({{Wallet - OB & CB#130}}, {{Acc Statement - OB & CB#228}}). Rows differ in when the balance is checked (draft save vs posting) and in the message. Parameterize the type, stage and message.
- **Every OB/CB matrix shares one expected text** ("closing balance of the previous period = opening balance of the next"). The parameterized test must compute the expected balance change per transaction type (charge adds, payment subtracts; Cash In vs Cash Out). Without that, the "balance calculation" check proves nothing.
- **Two SOA canonicals are very wide:** {{SOA - OB & CB#72}} (59 rows) and {{SOA - OB & CB#170}} (130 rows). Keep them as one rule, but consider sub-groups (charge + charge, charge + payment, payment + payment) so a failure is easier to trace.

## Possible missed duplicates (not merged yet)

These canonical cases look like the same test as each other. They were **not** merged, because merging renumbers IDs. Decide case by case, then set `merge_into` in `annotations/*.json` and regenerate.

| Cases | Why they look like duplicates |
|---|---|
| {{UO#14}}, {{Uo import#8}} | Both: import in same month as last bulk-upload reading is rejected. Cross-sheet duplicate (UO-010 data also has a year typo). |
| {{UO#15}}, {{Uo import#3}} | Import in month after last bulk-upload reading succeeds; Uo import#7 is already merged into UOI-001. Cross-sheet duplicate. |
| {{UO#13}}, {{Uo import#4}} | Same rule (same-month import after manual/meter-reset reading). Cross-sheet duplicate whose expected results conflict; merge once the decision is made. |
| {{UO#21}}, {{Uo import#11}}, {{Uo import#15}} | UO-016 (lower or blank units rejected) is the generic form of UOI-006 (blank) and UOI-009 (lower). Cross-sheet duplicate. |
| {{UO#19}}, {{Uo import#3}} | Both import after meter reset and check that consumption uses MR units (same v4 bug). Merge the calc assertion into one test. |
| {{Accounts Receivable#33}}, {{Accounts Receivable#34}}, {{Accounts Receivable#35}} | AR-013 (open detail, blank expected) is the first step of AR-014/015. Assertion split: one test opens the detail and views/downloads the PDF. |
| {{Uo import#63}}, {{Uo import#68}} | Both download the uploaded CSV from import history; UOI-035 is the same flow run as admin. |
| {{Make Payment#10}}, {{Wallet#30}} | Both pay an apartment invoice in full with Wallet method from Apartment > Invoice > Make Payment; same WP/SOA/wallet/AR assertions. WAL-019 (partial by wallet) is the partial-amount variant. |
| {{Cash and Bank Account#8}}, {{Cash and Bank Account#16}} | Account without payment method excluded from payment/recharge/deposit; CBA-007 only changes type to Other (Bank variant is already merged into CBA-003). |
| {{Cash and Bank Account#5}}, {{Cash and Bank Account#9}}, {{Cash and Bank Account#14}} | Create account with initial balance and see it in list; only account type differs (Cash/Bank/Other). One test parameterized by type, with type-specific fields. |
| {{Make Payment#24}}, {{Cash Received#8}}, {{Cash Outflow#20}}, {{Cash Transfer#19}}, {{Wallet#11}}, {{Wallet#18}}, {{Wallet#28}}, {{Wallet#41}}, {{Deposit#17}}, {{Deposit#30}}, {{Cash and Bank Account#17}} | Same rule 'Enter key does not submit the form'; parameterize one test by form instead of 11 cases. |
| {{Cash Received#15}}, {{Cash Outflow#7}}, {{Cash Transfer#12}}, {{Wallet#10}}, {{Wallet#17}}, {{Wallet#24}}, {{Wallet#38}}, {{Deposit#11}}, {{Deposit#29}} | Same rule and message ('Amount exceeded maximum limit' for 99,999,999,999,999); one test parameterized by form. |
| {{Apartments#66}}, {{Contacts#64}} | Add note: identical flow and expected, only entity differs; source even reuses src_id TC_Apart:N&E_001. Same for edit/other-user/Enter (next entries). |
| {{Apartments#67}}, {{Contacts#65}} | Edit own note: same flow and expected; entity differs (apartment vs contact). |
| {{Apartments#68}}, {{Contacts#66}} | Cannot edit other user's note: same check; entity differs. |
| {{Apartments#8}}, {{Apartments#69}}, {{Contacts#17}}, {{Contacts#67}}, {{Setting#28}} | All 'Enter key does not submit form' checks; SET-011 is already parameterized by entity - add Apartment, Contact and Note forms. |
| {{Apartments#15}}, {{Apartments#16}}, {{Apartments#17}}, {{Apartments#18}} | Assertion split: total unpaid, Current, Total Overdue and bucket cards are on one Summary screen; one test asserts all and that buckets sum to Total Overdue. |
| {{Contacts#27}}, {{Contacts#28}}, {{Contacts#29}}, {{Contacts#30}} | Assertion split: same contact Summary screen cards; one test. Could also parameterize with APT-005..008 by entity. |
| {{Apartments#41}}, {{Contacts#49}} | Full payment: same Make Payment dialog and SOA/AR/unpaid assertions; only entry point (apartment vs contact) differs. |
| {{Apartments#42}}, {{Contacts#51}} | Partial payment: same flow and Partially Paid assertions; entry point differs. |
| {{Apartments#43}}, {{Contacts#54}} | Overpayment to wallet: same flow and expected; entry point differs. |
| {{Apartments#44}}, {{Contacts#56}} | Currency-conversion payment: same flow, data and expected; entry point differs. |
| {{Contacts#18}}, {{Contacts#38}} | Edit contact from list vs from summary: same edit form and expected update. |
| {{Apartments#35}}, {{Apartments#37}} | Assertion split: same apartment Invoices tab shows list and unpaid/wallet totals. |
| {{Contacts#46}}, {{Contacts#48}} | Assertion split: same contact Unpaid Invoices tab list and total. |
| {{Reports#62}}, {{Reports#78}} | Report list with transaction type pre-selected; only report differs (Cash Received vs Cash Outflow) - parameterize like RPT-015..025. |
| {{Reports#11}}, {{Reports#12}} | Account Statement summary export; only format differs (PDF vs Excel). |
| {{Reports#14}}, {{Reports#15}} | Account statement detail export; only format differs (PDF vs Excel). |
| {{Setting#22}}, {{Setting#30}} | Add parent category: same flow; type differs (income vs expense), form-visibility target differs - same as how sort cases were merged. |
| {{Setting#24}}, {{Setting#31}} | Add child category under parent: same flow and expected; only category type differs. |
| {{Setting#29}}, {{Setting#36}} | Disable category hidden in create form; only category type/target form differs. |
| {{Setting#58}}, {{Setting#63}} | Disable account type / bank: both hidden in Cash & Bank Account create form, history kept; data variant by entity. |
| {{API#34}}, {{API#39}}, {{API#44}} | Get SOA/wallet/deposit by apartment+month: same request and 200 list rule; endpoint variant (as API-027 already does for PDFs). |
| {{API#8}}, {{API#69}} | Make payment without Payment create permission is the same 401 Permission Denied rule; add as endpoint row of API-005. |
| {{API#23}}, {{API#68}} | Make payment with invalid invoice/location/method/account is the same invalid-parameter 401 rule; endpoint row of API-011. |
| {{API#36}}, {{API#51}} | Both 'disabled apartment by endpoint'; only expected status code differs (200 vs 401) - one parameterized test with per-endpoint expected code once contract is confirmed. |
| {{Role&Permission#68}}, {{Role&Permission#72}} | Remove own draft with View+Create; only module differs (Cash Outflow vs Cash Transfer). |
| {{Role&Permission#76}}, {{Role&Permission#78}}, {{Role&Permission#79}} | Report view with module dependency; with single Reports permission in new EM these collapse to one parameterized test (Cash Outflow adds type filter). |
| {{Deposit - OB & CB#21}}, {{Deposit - OB & CB#24}}, {{Deposit - OB & CB#26}} | Same 2-same-type-at-same-time deposit matrix split only by date combo; wallet (OB-WAL-009) and account (OB-ACS-007) keep date combo as parameter. Merge for consistency. |
| {{Deposit - OB & CB#30}}, {{Deposit - OB & CB#33}}, {{Deposit - OB & CB#37}} | Same 2-different-type deposit matrix split only by date combo (cur/cur, cur/back, back/back); OB-WAL-010 and OB-ACS-008 treat dates as a parameter. |

