"""Normalize the EM manual test-case workbook into one JSON list.
usage: python normalize.py <workbook.xlsx> <out.json>
"""
import sys, json, re, warnings, openpyxl
warnings.filterwarnings("ignore")
wb = openpyxl.load_workbook(sys.argv[1], data_only=True)
OUT = sys.argv[2]

def clean(v):
    if v is None: return ""
    s = str(v).replace("\xa0", " ").strip()
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s

def grid(ws, maxcol=26):
    # value grid with merged ranges filled from top-left
    mr = ws.max_row
    g = [[clean(ws.cell(r, c).value) for c in range(1, maxcol+1)] for r in range(1, mr+1)]
    for rng in ws.merged_cells.ranges:
        v = clean(ws.cell(rng.min_row, rng.min_col).value)
        for r in range(rng.min_row, min(rng.max_row, mr)+1):
            for c in range(rng.min_col, min(rng.max_col, maxcol)+1):
                g[r-1][c-1] = v
    return g

L = lambda s: ord(s) - 65
# standard sheets: column letters
STD = {
 "Login":        dict(pfx="LOGIN", id="A", t="B", pre="C", data="D", steps="E", exp="F", area=None, pri="G", res="H", rem="I", cm=["K"]),
 "Dashboard":    dict(pfx="DASH",  id="A", t="B", pre="C", data="D", steps="E", exp="F", area=None, pri="G", res="H", rem="I", cm=["K"]),
 "Accounts Receivable": dict(pfx="AR", id="A", t="B", pre="C", data="D", steps="E", exp="F", area=None, pri="G", res="H", rem="I", cm=["K"]),
 "Reports":      dict(pfx="RPT",   id="A", t="B", pre="C", data="D", steps="E", exp="F", area=None, pri="G", res="H", rem="I", cm=["K"]),
 "Global Search":dict(pfx="GS",    id="A", t="B", pre="C", data="D", steps="E", exp="F", area=None, pri="G", res="H", rem="I", cm=["K"]),
 "API":          dict(pfx="API",   id="A", t="B", pre="C", data="D", steps="E", exp="F", area=None, pri="G", res="J", rem="I", cm=["I","K","L"], hdr=3),
 "Role&Permission": dict(pfx="RBAC", id="A", t="C", pre="F", data="D", steps="E", exp="G", area="B", pri="H", res="I", rem="J", cm=["K"], hdr=2),
}
for n,p in [("Invoice-Debit Note","INV"),("Make Payment","PAY"),("Cash Received","CR"),("Cash Outflow","CO"),
            ("Cash Transfer","CT"),("Apartments","APT"),("UO","UO"),("EM","EM"),("Contacts","CON"),("Wallet","WAL"),
            ("Deposit","DEP"),("Cash and Bank Account","CBA"),("Setting","SET")]:
    STD[n] = dict(pfx=p, id="A", t="B", pre="C", data="D", steps="E", exp="F", area="G", pri="H", res="I", rem="J", cm=["L","M"])

cases = []
def add(**k):
    cases.append(k)

for ws in wb.worksheets:
    name = ws.title.strip()
    if name in STD:
        c = STD[name]; g = grid(ws, 16)
        start = c.get("hdr", 4)
        section = ""
        for i, row in enumerate(g[start:], start=start+1):
            get = lambda col: row[L(col)] if col else ""
            sid, title = get(c["id"]), get(c["t"])
            if sid.lower() == "module":
                section = next((x for x in row[1:] if x and x.lower()!="module"), section); continue
            if sid.lower() in ("prepared by","id","tc_no") or (not sid and get(c["pri"]).lower().startswith("priority")):
                continue
            body = [get(c[x]) for x in ("pre","data","steps","exp")]
            if not sid and not any(body) and not get(c["pri"]):
                if title or row[0]: section = title or row[0]
                continue
            if not sid and title and not get(c["exp"]) and not get(c["steps"]):
                section = title; continue
            add(sheet=name, row=i, src_id=sid, section=section, title=title, pre=get(c["pre"]), data=get(c["data"]),
                steps=get(c["steps"]), expected=get(c["exp"]), area=get(c["area"]), priority=get(c["pri"]),
                result=get(c["res"]), remarks=get(c["rem"]),
                comments=" | ".join(x for x in dict.fromkeys(get(cc) for cc in c["cm"]) if x))
    elif name in ("SOA - OB & CB","Wallet - OB & CB","Deposit - OB & CB","Acc Statement - OB & CB"):
        pfx = {"SOA - OB & CB":"SOA","Wallet - OB & CB":"WOB","Deposit - OB & CB":"DOB","Acc Statement - OB & CB":"ASOB"}[name]
        g = grid(ws, 11); n = 0; block = ""
        for i, row in enumerate(g[2:], start=3):
            ttype, cat, sub, way, chk, area, exp, pri = row[:8]
            if not (cat or sub or way) or not pri and not exp: 
                if not pri: continue
            if pri.lower().startswith("priority") or exp.lower() in ("excepted result","expected result"):
                block = " / ".join(x for x in (ttype, cat) if x); continue
            n += 1
            add(sheet=name, row=i, src_id=f"{pfx}-R{i}", section=ttype, title=" / ".join(x for x in (cat, sub) if x),
                pre="", data=way, steps="", expected=exp, area=area, check_point=chk, priority=pri,
                result=row[8], remarks=row[9], comments=row[10] if len(row)>10 else "")
    elif name == "1Inv 2RV":
        g = grid(ws, 9)
        for i, row in enumerate(g[3:], start=4):
            if not row[6] and not row[4]: continue
            add(sheet=name, row=i, src_id=f"1INV2RV-R{i}", section=row[0], title=row[1], pre="",
                data=f"1st: {row[2]} | 2nd: {row[3]}", steps="", expected=f"UI: {row[4]}" + (f" | API: {row[5]}" if row[5] else ""),
                area="", priority=row[6], result=row[7] or row[8], remarks="", comments="")
    elif name == "1RV 2Inv":
        g = grid(ws, 5)
        for i, row in enumerate(g[2:], start=3):
            if not row[3]: continue
            add(sheet=name, row=i, src_id=f"1RV2INV-R{i}", section=row[0], title=row[1], pre="", data=row[2], steps="",
                expected=row[3], area="", priority="", result=row[4], remarks="", comments="")
    elif name == "Uo import":
        g = grid(ws, 15)
        for i, row in enumerate(g[2:], start=3):
            if not row[1] and not row[5]: continue
            if row[5].lower().startswith("expected result"): continue
            add(sheet=name, row=i, src_id=f"UOIMP-R{i}", section=row[0], title=row[1], pre=row[2], data=row[3], steps="",
                expected=row[5], area="", priority=row[12], result=row[13] or row[10] or row[7], remarks=" ".join(x for x in (row[8],row[11]) if x),
                comments=row[14])

FEATURE = {"Login":"AUTH","Dashboard":"DASH","Accounts Receivable":"AR","Global Search":"SRCH","Reports":"RPT",
  "Invoice-Debit Note":"INV","UO":"UO","Uo import":"UOI","EM":"EMF","Apartments":"APT","Contacts":"CON","Wallet":"WAL",
  "Deposit":"DEP","Make Payment":"PAY","Cash Received":"CR","1Inv 2RV":"CONC","1RV 2Inv":"CONC","Cash Outflow":"CO",
  "Cash Transfer":"CT","Cash and Bank Account":"CBA","SOA - OB & CB":"OBCB-SOA","Wallet - OB & CB":"OBCB-WAL",
  "Deposit - OB & CB":"OBCB-DEP","Acc Statement - OB & CB":"OBCB-ACS","Setting":"SET","Role&Permission":"RBAC","API":"API"}
for c in cases:
    c["key"] = f'{c["sheet"]}#{c["row"]}'
    c["feature"] = FEATURE[c["sheet"]]

json.dump(cases, open(OUT,"w"), ensure_ascii=False, indent=1)
from collections import Counter
cnt = Counter(c["sheet"] for c in cases)
for k,v in cnt.items(): print(f"{v:5d}  {k}")
print("TOTAL", len(cases))
print("priorities:", Counter(c["priority"] for c in cases))
