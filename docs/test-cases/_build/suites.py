"""Generate README, smoke, regression and source-issues docs from test-catalog.csv.
usage: python -I suites.py <out_dir>
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict

OUT = sys.argv[1]
meta = json.load(open(os.path.join(OUT, "_build", "render_meta.json")))
FMETA, stats = meta["fmeta"], meta["stats"]
rows = list(csv.DictReader(open(os.path.join(OUT, "test-catalog.csv"))))
canon = [r for r in rows if r["row_type"] == "canonical"]
code_of = {v["name"]: k for k, v in FMETA.items()}

def anchor(r):
    t = f'{"★ " if r["critical"] else ""}{r["test_id"]} · {r["title"]}'.lower()
    return re.sub(r"[^\w\- ]", "", t).replace(" ", "-")

def link(r, frm):
    p = os.path.relpath(os.path.join(OUT, r["doc"]), os.path.dirname(os.path.join(OUT, frm))).replace(os.sep, "/")
    return f'[{r["test_id"]}]({p}#{anchor(r)})'

def flink(code, frm):
    m = FMETA[code]
    p = os.path.relpath(os.path.join(OUT, m["path"]), os.path.dirname(os.path.join(OUT, frm))).replace(os.sep, "/")
    return f'[{m["name"]}]({p})'

def cell(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")

by_src = {(r["source_sheet"], r["source_row"]): r for r in rows}
def resolve(text, frm):
    def rep(m):
        sheet, row = m.group(1).rsplit("#", 1)
        r = by_src[(sheet, row)]
        c = next(x for x in canon if x["test_id"] == r["test_id"])
        return link(c, frm)
    return re.sub(r"\{\{(.+?)\}\}", rep, text)

# ------------------------------------------------------------------ smoke
STAGE = [
    ("1 · Access", ["AUTH", "API"], lambda r: r["test_id"] in ("API-001", "API-002") or r["test_id"].startswith("AUTH")),
    ("2 · Setup & master data", ["SET", "CBA", "APT", "CON"], lambda r: r["test_id"] in ("SET-003", "CBA-001", "APT-001", "CON-001")),
    ("3 · Billing", ["UO", "UOI", "EMF", "INV"], None),
    ("4 · Collection", ["PAY", "CR", "APT", "CON"], None),
    ("5 · Wallet & deposit", ["WAL", "DEP"], None),
    ("6 · Cash management", ["CO", "CT", "CBA"], None),
    ("7 · Balances & reporting", ["DASH", "AR", "APT", "RPT", "OBCB-SOA", "OBCB-WAL", "OBCB-DEP", "OBCB-ACS", "API"], None),
    ("8 · Access control", ["RBAC"], None),
]
smoke = [r for r in canon if r["smoke"]]
placed, staged = set(), []
for name, codes, pred in STAGE:
    items = []
    for code in codes:
        for r in smoke:
            if r["test_id"] in placed or code_of[r["feature"]] != code:
                continue
            if pred and not pred(r):
                continue
            if name.startswith("4") and code == "APT" and r["test_id"] not in ("APT-016",):
                continue
            items.append(r); placed.add(r["test_id"])
    staged.append((name, items))
left = [r for r in smoke if r["test_id"] not in placed]
if left:
    staged.append(("9 · Other", left))

F = "suites/smoke.md"
L = ["# Smoke Suite\n", "[← Test case index](../README.md)\n",
     f"**{len(smoke)} test cases.** Run on every deployment, before any other suite. The smoke suite answers one question: *can EM still bill, collect and report money?* Every case is P1, Active and automatable, with a happy path. Run them in stage order: later stages reuse data created by earlier ones (apartment, contact, accounts).\n",
     "**Exit rule:** any failure stops the pipeline. Fix it, or roll back the build, before running E2E or regression.\n",
     "Data-driven cases (with variants) run **only the base row** in smoke. The full variant set runs in regression.\n"]
for name, items in staged:
    if not items:
        continue
    L.append(f"## {name}\n")
    L.append("| # | ID | Test case | Feature | Automation |")
    L.append("|---|---|---|---|---|")
    for i, r in enumerate(items, 1):
        L.append(f'| {i} | {link(r, F)} | {"★ " if r["critical"] else ""}{cell(r["title"])} | {r["feature"]} | {r["automation"]} |')
    L.append("")
os.makedirs(os.path.join(OUT, "suites"), exist_ok=True)
open(os.path.join(OUT, F), "w").write("\n".join(L))

# ------------------------------------------------------------------ regression
F = "suites/regression.md"
active = [r for r in canon if r["status"] != "Obsolete"]
L = ["# Regression Suite\n", "[← Test case index](../README.md)\n",
     "Regression = every non-obsolete test case, in three tiers. Pick the tier by how much changed.\n",
     "| Tier | Content | When to run | Test cases |",
     "|---|---|---|---|",
     f'| **R1 — Critical** | All ★ critical + all P1 | Every merge to main / nightly | {sum(1 for r in active if r["priority"]=="P1" or r["critical"])} |',
     f'| **R2 — Core** | R1 + all P2 | Before each release candidate | {sum(1 for r in active if r["priority"] in ("P1","P2") or r["critical"])} |',
     f'| **R3 — Full** | Everything (incl. P3 field / UI validation) + all data variants | Before production release / major refactor | {len(active)} cases ({sum(1 for r in rows if r["status"]!="Obsolete")} incl. variants) |',
     "",
     "Data-driven cases run **all their variants** in regression; see the *Data variants* table under each case.\n",
     "Cases with status **Review** stay in the suite but are tagged; a failure there must first be checked against the open question in [source-issues.md](../source-issues.md).\n",
     "## Coverage by feature\n",
     "| # | Feature | Cases | ★ | P1 | P2 | P3 | Auto | Manual | Review | Source rows |",
     "|---|---|---|---|---|---|---|---|---|---|---|"]
for code, m in FMETA.items():
    s = stats[code]
    L.append(f'| {m["no"]:02d} | {flink(code, F)} | {s["canon"]} | {s["crit"]} | {s["P1"]} | {s["P2"]} | {s["P3"]} | {s["auto"]} | {s["manual"]} | {s["review"]} | {s["src"]} |')
tot = Counter()
for s in stats.values():
    for k, v in s.items():
        if isinstance(v, int): tot[k] += v
L.append(f'| | **Total** | **{tot["canon"]}** | **{tot["crit"]}** | **{tot["P1"]}** | **{tot["P2"]}** | **{tot["P3"]}** | **{tot["auto"]}** | **{tot["manual"]}** | **{tot["review"]}** | **{tot["src"]}** |')
L.append("")
manual = [r for r in canon if r["automation"] == "Manual"]
L.append(f"## Manual-only cases ({len(manual)})\n")
L.append("These stay in the manual regression checklist. Everything else is planned for automation.\n")
L.append("| ID | Test case | Reason |")
L.append("|---|---|---|")
for r in manual:
    L.append(f'| {link(r, F)} | {cell(r["title"])} | {cell(r["manual_reason"])} |')
L.append("")
L.append("## Automation layer split\n")
L.append("| Layer | Cases | Meaning |")
L.append("|---|---|---|")
au = Counter(r["automation"] for r in canon)
desc = {"Auto-UI": "Browser test; assert on screen", "Auto-UI+API": "Act in UI (or API), assert numbers via API / parsed PDF",
        "Auto-API": "Pure API test (incl. parallel calls for concurrency)", "Manual": "Not automated (see list above)"}
for k in ("Auto-UI", "Auto-UI+API", "Auto-API", "Manual"):
    L.append(f"| {k} | {au.get(k,0)} | {desc[k]} |")
L.append("")
open(os.path.join(OUT, F), "w").write("\n".join(L))

# ------------------------------------------------------------------ source issues
F = "source-issues.md"
review = [r for r in rows if r["status"] == "Review"]
L = ["# Source Issues, Open Questions & Coverage Gaps\n", "[← Test case index](README.md)\n",
     "Found while consolidating the manual workbook. Each item needs an owner (QA lead / EM team / Zeya Labs) before the affected cases are automated.\n",
     resolve(open(os.path.join(OUT, "_build", "issues_narrative.md")).read(), F),
     f"\n## Cases in Review status ({len(review)} source rows)\n",
     "Kept in the suites, but the expected result must be confirmed before an automated assertion is trusted.\n",
     "| ID | Row | Test case | Why |", "|---|---|---|---|"]
for r in review:
    rr = next(c for c in canon if c["test_id"] == r["test_id"])
    L.append(f'| {link(rr, F)} | {"base" if r["row_type"]=="canonical" else "variant"} · {cell(r["source_sheet"])} r{r["source_row"]} | {cell(rr["title"])} | {cell(r["status_note"])} |')
L.append("")
open(os.path.join(OUT, F), "w").write("\n".join(L))

# ------------------------------------------------------------------ README
F = "README.md"
smoke_n = len(smoke)
L = [open(os.path.join(OUT, "_build", "readme_head.md")).read()]
L.append("## At a glance\n")
L.append("| | |")
L.append("|---|---|")
L.append(f'| Source rows read | {tot["src"]} |')
L.append(f'| Test cases after merging | **{tot["canon"]}** ({tot["merged"]} rows merged as duplicates / data variants) |')
L.append(f'| ★ Critical business flow | {tot["crit"]} |')
L.append(f'| Priority P1 / P2 / P3 | {tot["P1"]} / {tot["P2"]} / {tot["P3"]} |')
L.append(f'| Smoke / E2E-tagged | {smoke_n} / {tot["e2e"]} (+ 12 composed [E2E flows](suites/e2e-critical-flows.md)) |')
L.append(f'| Automatable / Manual | {tot["auto"]} / {tot["manual"]} |')
L.append(f'| Review (open question) / Obsolete | {tot["review"]} / {tot["obsolete"]} |')
L.append("")
L.append("## Suites\n")
L.append("| Suite | File | Size | Purpose |")
L.append("|---|---|---|---|")
L.append(f"| Smoke | [suites/smoke.md](suites/smoke.md) | {smoke_n} cases | Every deploy — can EM still bill, collect and report? |")
L.append("| E2E | [suites/e2e-critical-flows.md](suites/e2e-critical-flows.md) | 12 flows | ★ Critical business flows chained across modules |")
L.append(f'| Regression | [suites/regression.md](suites/regression.md) | R1 / R2 / R3 tiers | Coverage per feature; manual-only list |')
L.append("")
L.append("## Features\n")
L.append("| # | Feature | Cases | ★ | P1 | Smoke | Auto | Manual | Source sheet(s) |")
L.append("|---|---|---|---|---|---|---|---|---|")
groups = [("Billing", ["INV", "UO", "UOI", "EMF"]), ("Collection & cash", ["PAY", "CR", "CONC", "CO", "CT", "CBA"]),
          ("Apartment ledgers", ["APT", "CON", "WAL", "DEP"]),
          ("Balances (OB / CB)", ["OBCB-SOA", "OBCB-WAL", "OBCB-DEP", "OBCB-ACS"]),
          ("Receivables & reporting", ["DASH", "AR", "RPT", "SRCH"]), ("Platform", ["AUTH", "SET", "RBAC", "API"])]
for g, codes in groups:
    L.append(f"| | **{g}** | | | | | | | |")
    for code in sorted(codes, key=lambda c: FMETA[c]["no"]):
        m, s = FMETA[code], stats[code]
        L.append(f'| {m["no"]:02d} | [{m["name"]}]({m["path"]}) | {s["canon"]} | {s["crit"]} | {s["P1"]} | {s["smoke"]} | {s["auto"]} | {s["manual"]} | {", ".join(s["sheets"])} |')
L.append("")
L.append(open(os.path.join(OUT, "_build", "readme_tail.md")).read())
open(os.path.join(OUT, F), "w").write("\n".join(L))
print("smoke", smoke_n, "review rows", len(review), "manual", len(manual))
