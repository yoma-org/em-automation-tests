"""Render EM test-case docs from normalized cases + annotations.
usage: python -I render.py <cases.json> <ann_dir> <out_dir>
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict

cases_path, ann_dir, OUT = sys.argv[1:4]
cases = json.load(open(cases_path))
ann = {}
for g in "ABCDEFG":
    for a in json.load(open(os.path.join(ann_dir, f"{g}.json"))):
        ann[a["key"]] = a
missing = [c["key"] for c in cases if c["key"] not in ann]
assert not missing, f"missing annotations: {missing[:10]} ({len(missing)})"

# feature order: code -> (file no, slug, display name, folder)
FEATURES = [
    ("AUTH", "login", "Login & Authentication", "features"),
    ("DASH", "dashboard", "Dashboard", "features"),
    ("AR", "accounts-receivable", "Accounts Receivable", "features"),
    ("INV", "invoice-debit-note", "Invoice & Debit Note", "features"),
    ("UO", "utility-operations-uo", "Utility Operations (UO) — manual entry", "features"),
    ("UOI", "uo-import", "UO Import (bulk meter readings)", "features"),
    ("EMF", "estate-management-fee", "Estate Management Fee (EM)", "features"),
    ("APT", "apartments", "Apartments", "features"),
    ("CON", "contacts", "Contacts", "features"),
    ("PAY", "make-payment", "Make Payment", "features"),
    ("CR", "cash-received", "Cash Received (RV / Unknown / Funding)", "features"),
    ("CONC", "payment-concurrency", "Payment Concurrency (1 Inv × 2 RV, 1 RV × 2 Inv)", "features"),
    ("CO", "cash-outflow", "Cash Outflow (PV)", "features"),
    ("CT", "cash-transfer", "Cash Transfer (JV)", "features"),
    ("CBA", "cash-bank-account", "Cash & Bank Account", "features"),
    ("WAL", "wallet", "Wallet", "features"),
    ("DEP", "deposit", "Deposit", "features"),
    ("RPT", "reports", "Reports", "features"),
    ("OBCB-SOA", "soa-ob-cb", "SOA — Opening / Closing Balance", "features/balances"),
    ("OBCB-WAL", "wallet-ob-cb", "Wallet — Opening / Closing Balance", "features/balances"),
    ("OBCB-DEP", "deposit-ob-cb", "Deposit — Opening / Closing Balance", "features/balances"),
    ("OBCB-ACS", "account-statement-ob-cb", "Account Statement — Opening / Closing Balance", "features/balances"),
    ("SET", "settings", "Settings (master data & configuration)", "features"),
    ("RBAC", "role-permission", "Role & Permission", "features"),
    ("SRCH", "global-search", "Global Search", "features"),
    ("API", "api", "External API", "features"),
]
FMETA = {}
for i, (code, slug, name, folder) in enumerate(FEATURES, 1):
    FMETA[code] = dict(no=i, slug=slug, name=name, folder=folder,
                       path=f"{folder}/{i:02d}-{slug}.md")

def idcode(code):
    return code.replace("OBCB-", "OB-")

# Real credentials in the source workbook are masked. They are read from the workbook itself at render time
# (TC_Login_001 test data), so no copy of them - plain or hashed - lives in the repo.
SECRETS = {}
for c in cases:
    if c["sheet"] != "Login":
        continue
    for pw in re.findall(r'Password\s*=\s*"([^"]+)"', c["data"]):
        if c["src_id"] == "TC_Login_001":
            SECRETS[pw] = "<VALID_PASSWORD>"
        elif len(pw) >= 6:
            SECRETS.setdefault(pw, "<INVALID_PASSWORD>")
    if c["src_id"] == "TC_Login_001":
        for em in re.findall(r'Email\s*=\s*"([^"]+)"', c["data"]):
            SECRETS[em] = "<ADMIN_EMAIL>"

def scrub(s):
    for raw in sorted(SECRETS, key=len, reverse=True):
        s = s.replace(raw, SECRETS[raw])
    return s

def cell(s):
    return scrub(s or "").replace("|", "\\|").replace("\n", " ").strip()

def block(s):
    """multi-line source text -> markdown lines"""
    s = scrub(s or "").strip()
    if not s:
        return ""
    out = []
    for ln in s.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        if re.match(r"^\d+[.)]\s*", ln):
            ln = re.sub(r"^(\d+)[.)]\s*", r"\1. ", ln)
            out.append(ln)
        elif re.match(r"^[-•*]\s*", ln):
            out.append("   - " + re.sub(r"^[-•*]\s*", "", ln) if out and re.match(r"^\d+\. ", out[-1]) else "- " + re.sub(r"^[-•*]\s*", "", ln))
        else:
            out.append(("   " if out and re.match(r"^(\d+\. |   )", out[-1]) else "") + ln + ("  " if not out or not re.match(r"^\d", out[-1]) else ""))
    return "\n".join(out)

# ---- assign new IDs to canonicals in source order per feature
by_feat = defaultdict(list)
for c in cases:
    by_feat[c["feature"]].append(c)
newid, canon_of = {}, {}
for code in FMETA:
    n = 0
    for c in by_feat[code]:
        a = ann[c["key"]]
        if not a.get("merge_into"):
            n += 1
            newid[c["key"]] = f"{idcode(code)}-{n:03d}"
# resolve merge chains / bad targets
def root(k, depth=0):
    m = ann[k].get("merge_into")
    if not m or depth > 10 or m not in ann or m == k:
        return k
    return root(m, depth + 1)
for c in cases:
    r = root(c["key"])
    if r != c["key"] and r not in newid:  # target was itself merged incorrectly -> should not happen
        r = c["key"]
    if r == c["key"] and c["key"] not in newid:
        # merge target invalid: promote to canonical
        code = c["feature"]; n = sum(1 for v in newid if v.startswith(c["sheet"]))
        newid[c["key"]] = f"{idcode(code)}-X{len(newid):03d}"
    canon_of[c["key"]] = r
variants = defaultdict(list)
for c in cases:
    if canon_of[c["key"]] != c["key"]:
        variants[canon_of[c["key"]]].append(c)

def src_ref(c):
    sid = c["src_id"] if c["src_id"] and not re.match(r"^[A-Z0-9]+-R\d+$", c["src_id"]) else ""
    return f'{c["sheet"]} r{c["row"]}' + (f" ({sid})" if sid else "")

def suites(a):
    s = []
    if a["smoke"]: s.append("Smoke")
    if a["e2e"]: s.append("E2E")
    if a["status"] != "Obsolete": s.append("Regression")
    return " · ".join(s) or "—"

def star(a):
    return "★ " if a["critical"] else ""

def rel(frm, to):
    return os.path.relpath(os.path.join(OUT, to), os.path.dirname(os.path.join(OUT, frm))).replace(os.sep, "/")

def anchor(cid, title, a):
    t = f"{star(a)}{cid} · {title}".lower()
    t = re.sub(r"[^\w\- ]", "", t).replace(" ", "-")
    return t

# ---- feature files
stats = {}
for code, m in FMETA.items():
    items = by_feat[code]
    canon = [c for c in items if canon_of[c["key"]] == c["key"]]
    ac = [ann[c["key"]] for c in canon]
    st = dict(src=len(items), canon=len(canon), merged=len(items) - len(canon),
              P1=sum(a["priority"] == "P1" for a in ac), P2=sum(a["priority"] == "P2" for a in ac),
              P3=sum(a["priority"] == "P3" for a in ac), crit=sum(a["critical"] for a in ac),
              smoke=sum(a["smoke"] for a in ac), e2e=sum(a["e2e"] for a in ac),
              auto=sum(a["automation"] != "Manual" for a in ac), manual=sum(a["automation"] == "Manual" for a in ac),
              obsolete=sum(a["status"] == "Obsolete" for a in ac), review=sum(a["status"] == "Review" for a in ac),
              sheets=sorted(set(c["sheet"] for c in items), key=lambda s: items.index(next(x for x in items if x["sheet"] == s))))
    stats[code] = st
    L = []
    L.append(f'# {m["no"]:02d} · {m["name"]}\n')
    L.append(f'[← Test case index]({rel(m["path"], "README.md")})\n')
    L.append(f'**Source sheet(s):** {", ".join(st["sheets"])} · **Source rows:** {st["src"]} → **{st["canon"]} test cases** after merging {st["merged"]} duplicates / data variants.  ')
    L.append(f'**Priority:** P1 {st["P1"]} · P2 {st["P2"]} · P3 {st["P3"]} · **★ Critical:** {st["crit"]} · **Smoke:** {st["smoke"]} · **E2E:** {st["e2e"]} · **Auto:** {st["auto"]} · **Manual:** {st["manual"]}'
             + (f' · **Review:** {st["review"]}' if st["review"] else "") + (f' · **Obsolete:** {st["obsolete"]}' if st["obsolete"] else "") + "\n")
    # summary table grouped by sub_feature
    L.append("## Summary\n")
    L.append("| ID | Test case | Sub-feature | Pri | Suites | Automation | Status | Variants |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c in canon:
        a = ann[c["key"]]; cid = newid[c["key"]]
        L.append(f'| [{cid}](#{anchor(cid, a["title"], a)}) | {star(a)}{cell(a["title"])} | {cell(a["sub_feature"])} | {a["priority"]} | {suites(a)} | {a["automation"]} | {a["status"]} | {len(variants[c["key"]]) + 1 if variants[c["key"]] else ""} |')
    L.append("")
    L.append("## Test cases\n")
    cur_sub = None
    for c in canon:
        a = ann[c["key"]]; cid = newid[c["key"]]
        if a["sub_feature"] != cur_sub:
            cur_sub = a["sub_feature"]
            L.append(f"### {cur_sub}\n")
        L.append(f'#### {star(a)}{cid} · {a["title"]}\n')
        L.append("| Priority | Suites | Automation | Status | Source |")
        L.append("|---|---|---|---|---|")
        auto = a["automation"] + (f' — {cell(a["manual_reason"])}' if a["automation"] == "Manual" and a.get("manual_reason") else "")
        status = a["status"] + (f' — {cell(a["status_note"])}' if a.get("status_note") else "")
        L.append(f'| {a["priority"]} | {suites(a)} | {auto} | {status} | {cell(src_ref(c))} |\n')
        if c.get("section"):
            L.append(f'**Scenario group:** {cell(c["section"])}\n')
        if c["sheet"] == "Role&Permission":
            parts = [("Feature", c["area"]), ("Permission required", c["data"]), ("Permission dependency", c["steps"]),
                     ("Precondition", c["pre"]), ("Expected result", c["expected"])]
        else:
            parts = [("Preconditions", c["pre"]), ("Test data", c["data"]), ("Steps", c["steps"]),
                     ("Check point", c.get("check_point", "")), ("Expected result", c["expected"]), ("Check areas", c["area"])]
            if c["sheet"] in ("Uo import",):
                parts = [("Pre-existing system data", c["pre"]), ("Import data", c["data"]), ("Expected result", c["expected"])]
            if c["sheet"].endswith("OB & CB"):
                parts = [("Test way", c["data"]), ("Check point", c.get("check_point", "")), ("Check areas", c["area"]), ("Expected result", c["expected"])]
            if c["sheet"] in ("1Inv 2RV", "1RV 2Inv"):
                parts = [("Scenario", c["section"]), ("Type", c["title"]), ("Concurrent actions", c["data"]), ("Expected result", c["expected"])]
        for label, val in parts:
            b = block(val)
            if b:
                L.append(f"**{label}:**\n\n{b}\n")
        if c.get("comments"):
            L.append(f'> **Source comments:** {cell(c["comments"])}\n')
        vs = variants[c["key"]]
        if vs:
            L.append(f"**Data variants ({len(vs) + 1} incl. base) — run as one data-driven test:**\n")
            L.append("| # | Variant | Source | Note |")
            L.append("|---|---|---|---|")
            L.append(f'| 1 | (base) {cell(c["title"]) or "—"} | {cell(src_ref(c))} | |')
            for j, v in enumerate(vs, 2):
                va = ann[v["key"]]
                note = "; ".join(x for x in (va["status"] if va["status"] != "Active" else "", va.get("status_note", "")) if x)
                L.append(f'| {j} | {cell(va.get("variant") or va["title"])} | {cell(src_ref(v))} | {cell(note)} |')
            L.append("")
        L.append("---\n")
    p = os.path.join(OUT, m["path"])
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write("\n".join(L))

# ---- catalog CSV (every source row)
with open(os.path.join(OUT, "test-catalog.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["test_id", "row_type", "feature", "sub_feature", "title", "priority", "critical", "smoke", "e2e",
                "regression", "automation", "manual_reason", "status", "status_note", "variant",
                "source_sheet", "source_row", "source_id", "source_priority", "doc"])
    for c in cases:
        a = ann[c["key"]]; r = canon_of[c["key"]]; ca = ann[r]
        is_c = r == c["key"]
        w.writerow([newid[r], "canonical" if is_c else "variant", FMETA[c["feature"]]["name"], ca["sub_feature"],
                    scrub(ca["title"] if is_c else ca["title"]), ca["priority"], "Y" if ca["critical"] else "",
                    "Y" if ca["smoke"] and is_c else "", "Y" if ca["e2e"] else "", "Y" if a["status"] != "Obsolete" else "",
                    ca["automation"], ca.get("manual_reason", ""), a["status"], a.get("status_note", ""),
                    "" if is_c else a.get("variant", ""), c["sheet"], c["row"],
                    c["src_id"] if not re.match(r"^[A-Z0-9]+-R\d+$", c["src_id"] or "") else "", c["priority"],
                    FMETA[c["feature"]]["path"]])

# ---- merged / duplicates report
MERGE_TYPES = [
    ("Exact duplicate", "Same sheet, same intent, steps and expected result. Adds nothing."),
    ("Cross-sheet duplicate", "The same check repeated in another sheet."),
    ("Data variant", "Same steps and expected rule; only the input data differs (currency, category, date, field, bucket, role …)."),
    ("Matrix combination", "One cell of a combination matrix (e.g. transaction type × date × currency), checked by the same rule."),
    ("Assertion split", "Same screen or flow; the source split the check points into separate rows. One test asserts them all."),
    ("Header row", "Matrix / section header row with no test of its own."),
]
VERDICT = {"OK": "✅ OK", "QUESTIONABLE": "⚠️ Check", "SPLIT": "✂️ Split"}

def case_link(k, frm="duplicates-merged.md"):
    r = canon_of[k]; a = ann[r]; cid = newid[r]; m = FMETA[C_BY_KEY[r]["feature"]]
    return f'[{cid}]({rel(frm, m["path"])}#{anchor(cid, a["title"], a)})'

def src_id(c):
    return c["src_id"] if c["src_id"] and not re.match(r"^[A-Z0-9]+-R\d+$", c["src_id"]) else ""

def src_tc(c):
    """row reference: original TC ID (if the sheet has one) + sheet and row"""
    return (f'`{src_id(c)}` · ' if src_id(c) else "") + f'{cell(c["sheet"])} r{c["row"]}'

C_BY_KEY = {c["key"]: c for c in cases}
merged = [c for c in cases if canon_of[c["key"]] != c["key"]]
with_v = [k for k, v in variants.items() if v]
type_n = Counter(ann[c["key"]].get("merge_type", "") for c in merged)
verd_n = Counter(ann[c["key"]].get("merge_verdict", "") for c in merged)

L = ["# Duplicates & data variants merged\n", "[← Test case index](README.md)\n",
     "Each section lists, per canonical test case, every source test case that was merged into it, the merge type and the reason. "
     "A merged row is either a true duplicate or the same check with different data, which automation should run as **one data-driven (parameterized) test** with one row per variant.\n",
     f"**{len(merged)} source rows merged into {len(with_v)} canonical cases** (of {len(newid)} canonical cases in total).\n",
     "## Merge types\n", "| Type | Meaning | Rows |", "|---|---|---|"]
for t, d in MERGE_TYPES:
    L.append(f"| {t} | {d} | {type_n.get(t, 0)} |")
L += ["", "**Verdict** (merge review, 11 Oct 2026): "
      + " · ".join(f'{VERDICT[v]} {verd_n.get(v, 0)}' for v in VERDICT)
      + ". ✅ the merge is sound. ⚠️ the merge stands, but the variant has an extra or different expected result that the parameterized test must assert. "
      "✂️ the row tests different behaviour and should become its own case.\n"]

frag = os.path.join(OUT, "_build", "duplicates_review.md")
if os.path.exists(frag):
    L.append(re.sub(r"\{\{(.+?)\}\}", lambda mm: case_link(mm.group(1)), open(frag).read()))

flagged = [c for c in merged if ann[c["key"]].get("merge_verdict") in ("SPLIT", "QUESTIONABLE")]
if flagged:
    L += [f"## Merges to split or check ({len(flagged)})\n",
          "| Verdict | Canonical | Merged TC | Reason |", "|---|---|---|---|"]
    for c in sorted(flagged, key=lambda c: ann[c["key"]]["merge_verdict"] != "SPLIT"):
        va = ann[c["key"]]
        L.append(f'| {VERDICT[va["merge_verdict"]]} | {case_link(c["key"])} | {src_tc(c)} | {cell(va.get("merge_reason", ""))} |')
    L.append("")

for code, m in FMETA.items():
    blocks = [c for c in by_feat[code] if variants[c["key"]]]
    if not blocks:
        continue
    n = sum(len(variants[c["key"]]) for c in blocks)
    L.append(f'## {m["name"]}\n')
    L.append(f'{n} rows merged into {len(blocks)} canonical cases.\n')
    L.append("| Canonical (base TC) | Merged TC | Variant | Type | Reason | Verdict |")
    L.append("|---|---|---|---|---|---|")
    for c in blocks:
        cid = newid[c["key"]]; a = ann[c["key"]]
        head = f'[{cid}]({m["path"]}#{anchor(cid, a["title"], a)}) {cell(a["title"])}<br>base: {src_tc(c)}'
        for j, v in enumerate(variants[c["key"]]):
            va = ann[v["key"]]
            L.append(f'| {head if j == 0 else "〃"} | {src_tc(v)} | {cell(va.get("variant") or va["title"])} '
                     f'| {va.get("merge_type", "")} | {cell(va.get("merge_reason", ""))} | {VERDICT.get(va.get("merge_verdict"), "")} |')
    L.append("")
open(os.path.join(OUT, "duplicates-merged.md"), "w").write("\n".join(L))

json.dump(dict(stats=stats, newid=newid, canon_of=canon_of, fmeta=FMETA),
          open(os.path.join(OUT, "_build", "render_meta.json"), "w"), ensure_ascii=False, indent=1)
tot = Counter()
for s in stats.values():
    for k, v in s.items():
        if isinstance(v, int): tot[k] += v
print(dict(tot))
