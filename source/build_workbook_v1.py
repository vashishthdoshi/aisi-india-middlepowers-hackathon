import sys; sys.path.insert(0, "data")
from model import JUR, COMP, NAME, DIMS, F, FEAT, FEAT_EVID, BUDGET, FX_DEFAULT, FEAS
from sources import S
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

OUT = sys.argv[1] if len(sys.argv) > 1 else "aisi-comparison-v1.xlsx"
GREEN = "3B4A2F"; LIGHT = "E8EFDC"; OLIVE = "6B7F3A"
A = "Arial"
f_body = Font(name=A, size=11); f_bold = Font(name=A, size=11, bold=True)
f_hdr = Font(name=A, size=11, bold=True, color="FFFFFF"); fill_hdr = PatternFill("solid", fgColor=GREEN)
f_in = Font(name=A, size=11, color="0000FF"); f_link = Font(name=A, size=11, color="0563C1", underline="single")
f_title = Font(name=A, size=16, bold=True, color=GREEN)
thin = Side(style="thin", color="C8C8C8"); BD = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top"); CEN = Alignment(horizontal="center", vertical="top")
CODEFILL = {"Y": "D9EAD3", "N": "F4CCCC", "U": "EDEDED"}
TIERFILL = {"A": "C9DDB5", "B": "E8EFDC", "C-news": "FFF2CC", "C-analysis": "FCE5CD"}

def header(ws, row, labels, height=40):
    for c, t in enumerate(labels, 1):
        x = ws.cell(row, c, t); x.font = f_hdr; x.fill = fill_hdr; x.border = BD
        x.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[row].height = height

def body(ws, r1, r2, c1, c2, align=WRAP):
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            x = ws.cell(r, c); x.font = x.font if x.font and x.font.color and x.font.color.rgb in ("FF0000FF", "FF0563C1") else f_body
            x.border = BD; x.alignment = align

def widths(ws, ws_w):
    for i, w in enumerate(ws_w, 1): ws.column_dimensions[L(i)].width = w

wb = Workbook()

# ---------- Sources
so = wb.active; so.title = "Sources"
header(so, 1, ["Source id", "Title", "Publisher", "Date", "Tier", "Link"])
for i, (k, v) in enumerate(S.items(), 2):
    so.append([k, *v])
    so.cell(i, 6).hyperlink = v[4]; so.cell(i, 6).font = f_link
n_src = len(S) + 1
body(so, 2, n_src, 1, 5)
for r in range(2, n_src + 1):
    t = so.cell(r, 5).value
    if t in TIERFILL: so.cell(r, 5).fill = PatternFill("solid", fgColor=TIERFILL[t])
    so.cell(r, 6).border = BD; so.cell(r, 6).alignment = WRAP
widths(so, [16, 60, 34, 12, 11, 70]); so.freeze_panes = "B2"; so.auto_filter.ref = f"A1:F{n_src}"
SRC_ID = f"Sources!$A$2:$A${n_src}"
def lk(col, ref):  # lookup a Sources column by id
    return f'IFERROR(INDEX(Sources!${col}$2:${col}${n_src},MATCH({ref},{SRC_ID},0)),"")'

# ---------- Facts
fa = wb.create_sheet("Facts", 0)
header(fa, 1, ["Code", "Jurisdiction", "Dimension", "Finding", "Primary source id", "Primary source tier", "Primary source link", "Other source ids", "Key"])
for i, (j, d, txt, ids) in enumerate(F, 2):
    fa.append([j, NAME[j], d, txt, ids[0], f"={lk('E', f'E{i}')}", f"={lk('F', f'E{i}')}", "; ".join(ids[1:]), f'=A{i}&"|"&C{i}'])
n_f = len(F) + 1
body(fa, 2, n_f, 1, 9)
widths(fa, [6, 16, 24, 90, 16, 11, 50, 26, 22]); fa.freeze_panes = "D2"; fa.auto_filter.ref = f"A1:I{n_f}"
for t, col in TIERFILL.items():
    fa.conditional_formatting.add(f"F2:F{n_f}", CellIsRule(operator="equal", formula=[f'"{t}"'], fill=PatternFill("solid", fgColor=col)))

# ---------- RACI matrix
mx = wb.create_sheet("RACI matrix", 0)
header(mx, 1, ["Jurisdiction"] + DIMS, 52)
for r, (code, name, grp, inst, est) in enumerate(JUR, 2):
    mx.cell(r, 1, f"{name}\n{inst}")
    for c, d in enumerate(DIMS, 2):
        mx.cell(r, c, f'=IFERROR(INDEX(Facts!$D$2:$D${n_f},MATCH("{code}|{d}",Facts!$I$2:$I${n_f},0)),"Not found in sources read")')
    mx.row_dimensions[r].height = 190
body(mx, 2, len(JUR) + 1, 1, len(DIMS) + 1)
widths(mx, [24] + [40] * len(DIMS)); mx.freeze_panes = "B2"

# ---------- Features
ft = wb.create_sheet("Features", 0)
cols = ["Code", "Feature", "Definition"] + [NAME[c] for c in COMP] + ["India today", "Evidence summary"]
header(ft, 1, cols, 44)
for i, (code, lab, dfn, m) in enumerate(FEAT, 2):
    ft.append([code, lab, dfn] + [m[c] for c in COMP] + [m["IN"], FEAT_EVID.get(code, "")])
n_ft = len(FEAT) + 1
body(ft, 2, n_ft, 1, len(cols))
for r in range(2, n_ft + 1):
    for c in range(4, 4 + len(COMP) + 1): ft.cell(r, c).alignment = CEN
dv = DataValidation(type="list", formula1='"Y,N,U"', allow_blank=False); ft.add_data_validation(dv)
rng_codes = f"D2:{L(4 + len(COMP))}{n_ft}"; dv.add(rng_codes)
for k, col in CODEFILL.items():
    ft.conditional_formatting.add(rng_codes, CellIsRule(operator="equal", formula=[f'"{k}"'], fill=PatternFill("solid", fgColor=col)))
widths(ft, [6, 30, 48] + [11] * len(COMP) + [11, 80]); ft.freeze_panes = "D2"
ft.cell(n_ft + 2, 1, "Codes: Y present in sources read; N absent or explicitly denied; U not stated in sources read. Edit codes here (drop-down) and the Baseline sheet recalculates.").font = f_body

# ---------- Baseline and uplift
bs = wb.create_sheet("Baseline and uplift", 0)
bs["A1"] = "India AI Safety Institute: minimum baseline and safety uplift"; bs["A1"].font = f_title
bs["A2"] = "Formulas over the Features sheet. Blue cells are inputs."; bs["A2"].font = f_body
bs["A4"] = "Baseline if present in at least this many of the 10 comparators"; bs["B4"] = 5
bs["A5"] = "and no more than this many comparators explicitly lack it (N)"; bs["B5"] = 2
for a in ("A4", "A5"): bs[a].font = f_bold
for b in ("B4", "B5"): bs[b].font = f_in
bs["C4"] = "Input. Raise it for a stricter baseline."; bs["C5"] = "Input. Stops a feature counting as common when several peers clearly lack it."
header(bs, 7, ["Code", "Feature", "Y", "N", "U", "Share of known", "Class", "India today", "What India needs"])
for i in range(len(FEAT)):
    r = 8 + i; fr = 2 + i; rr = f"Features!$D${fr}:${L(3 + len(COMP))}${fr}"
    bs.cell(r, 1, f"=Features!A{fr}"); bs.cell(r, 2, f"=Features!B{fr}")
    bs.cell(r, 3, f'=COUNTIF({rr},"Y")'); bs.cell(r, 4, f'=COUNTIF({rr},"N")'); bs.cell(r, 5, f'=COUNTIF({rr},"U")')
    bs.cell(r, 6, f'=IF(C{r}+D{r}=0,"n/a",C{r}/(C{r}+D{r}))'); bs.cell(r, 6).number_format = "0%"
    bs.cell(r, 7, f'=IF(AND(C{r}>=$B$4,D{r}<=$B$5),"Baseline",IF(C{r}>=1,"Uplift","Gap: no peer has it"))')
    bs.cell(r, 8, f"=Features!{L(4 + len(COMP))}{fr}")
    bs.cell(r, 9, f'=IF(H{r}="Y","Has it",IF(G{r}="Baseline","Replicate now",IF(G{r}="Uplift","Candidate safety uplift","Design new")))')
last = 7 + len(FEAT)
body(bs, 8, last, 1, 9)
for r in range(8, last + 1):
    for c in (3, 4, 5, 6): bs.cell(r, c).alignment = CEN
for t, col in {"Baseline": "D9EAD3", "Uplift": "FFF2CC", "Gap: no peer has it": "F4CCCC"}.items():
    bs.conditional_formatting.add(f"G8:G{last}", CellIsRule(operator="equal", formula=[f'"{t}"'], fill=PatternFill("solid", fgColor=col)))
s0 = last + 2
summ = [("Baseline features", f'=COUNTIF(G8:G{last},"Baseline")'),
        ("Baseline features India must still replicate", f'=COUNTIFS(G8:G{last},"Baseline",I8:I{last},"Replicate now")'),
        ("Uplift features (1 to 4 peers)", f'=COUNTIF(G8:G{last},"Uplift")'),
        ("Uplift features India already has", f'=COUNTIFS(G8:G{last},"Uplift",H8:H{last},"Y")')]
for k, (a, b) in enumerate(summ):
    bs.cell(s0 + k, 1, a).font = f_bold; bs.cell(s0 + k, 2, b).font = f_bold
notes = ["'U' is not 'N'. Most unknowns are sources that do not mention the item, so a peer may have a feature this sheet cannot see.",
         "The threshold is a judgment. At 5 of 10 the baseline is what most peers visibly share; at 7 it shrinks to the near-universal features.",
         "Uplift features are where single peers show the strongest safety design (Korea and the EU on legal hooks, the UK on access, publication and compute, the EU on independence)."]
for k, t in enumerate(notes):
    c = bs.cell(s0 + 5 + k, 1, t); c.font = f_body; c.alignment = WRAP
    bs.merge_cells(start_row=s0 + 5 + k, start_column=1, end_row=s0 + 5 + k, end_column=9); bs.row_dimensions[s0 + 5 + k].height = 32
widths(bs, [8, 34, 6, 6, 6, 12, 18, 11, 24])

# ---------- Budgets
bu = wb.create_sheet("Budgets")
bu["A1"] = "Annual budgets in a common currency"; bu["A1"].font = f_title
bu["A2"] = "Exchange rates are inputs (USD per unit), approximate and for comparison only. Update them before quoting."; bu["A2"].font = f_body
header(bu, 4, ["Currency", "USD per unit"])
for i, (cur, rate) in enumerate(FX_DEFAULT.items(), 5):
    bu.cell(i, 1, cur).font = f_body; c = bu.cell(i, 2, rate); c.font = f_in; c.number_format = "0.0000"
fx_last = 4 + len(FX_DEFAULT)
h0 = fx_last + 2
header(bu, h0, ["Jurisdiction", "Line", "Amount per year (native)", "Currency", "USD per year", "Ratio to India pillar", "Basis", "Source id", "Source link"])
for k, (j, lab, amt, cur, basis, ids) in enumerate(BUDGET):
    r = h0 + 1 + k
    bu.cell(r, 1, NAME[j]); bu.cell(r, 2, lab); c = bu.cell(r, 3, amt); c.font = f_in; c.number_format = "#,##0"
    bu.cell(r, 4, cur)
    bu.cell(r, 5, f"=C{r}*INDEX($B$5:$B${fx_last},MATCH(D{r},$A$5:$A${fx_last},0))"); bu.cell(r, 5).number_format = "$#,##0"
    bu.cell(r, 7, basis); bu.cell(r, 8, ids[0]); bu.cell(r, 9, f"={lk('F', f'H{r}')}")
b_last = h0 + len(BUDGET)
india_row = [h0 + 1 + k for k, b in enumerate(BUDGET) if b[0] == "IN"][0]
for r in range(h0 + 1, b_last + 1):
    bu.cell(r, 6, f"=IF($E${india_row}=0,\"n/a\",E{r}/$E${india_row})"); bu.cell(r, 6).number_format = '0.0"x"'
body(bu, h0 + 1, b_last, 1, 9)
for r in range(h0 + 1, b_last + 1): bu.cell(r, 3).font = f_in
s1 = b_last + 2
bu.cell(s1, 1, "India scenarios (what matching a peer would cost)").font = f_bold
header(bu, s1 + 1, ["Scenario", "Peer anchor (USD/yr)", "In INR crore per year", "Multiple of current pillar"])
scen = [("Australia-level (lean, in-house testing)", f"E{[h0+1+k for k,b in enumerate(BUDGET) if b[0]=='AU'][0]}"),
        ("Canada-level (two research streams)", f"E{[h0+1+k for k,b in enumerate(BUDGET) if b[0]=='CA'][0]}"),
        ("Half of UK (serious evaluator)", f"E{[h0+1+k for k,b in enumerate(BUDGET) if b[0]=='UK'][0]}/2")]
inr = f"INDEX($B$5:$B${fx_last},MATCH(\"INR\",$A$5:$A${fx_last},0))"
for k, (lab, ref) in enumerate(scen):
    r = s1 + 2 + k
    bu.cell(r, 1, lab); bu.cell(r, 2, f"={ref}"); bu.cell(r, 2).number_format = "$#,##0"
    bu.cell(r, 3, f"=B{r}/{inr}/10000000"); bu.cell(r, 3).number_format = "#,##0.0"
    bu.cell(r, 4, f"=B{r}/$E${india_row}"); bu.cell(r, 4).number_format = '0.0"x"'
body(bu, s1 + 2, s1 + 4, 1, 4)
bu.cell(s1 + 6, 1, "India's figure is the whole Safe & Trusted AI pillar of the IndiaAI Mission, not a dedicated AISI budget; no AISI budget is published.").font = f_body
widths(bu, [30, 36, 22, 10, 16, 16, 40, 14, 60])

# ---------- India feasibility
fz = wb.create_sheet("India feasibility")
header(fz, 1, ["Factor", "What the sources show", "Reading", "Source id(s)", "Primary link", "Primary tier"])
for i, (fac, txt, rd, ids) in enumerate(FEAS, 2):
    first = ids.split(";")[0]
    fz.append([fac, txt, rd, ids.replace(";", "; "), None, None])
    fz.cell(i, 5, f'={lk("F", chr(34)+first+chr(34))}'); fz.cell(i, 6, f'={lk("E", chr(34)+first+chr(34))}')
n_fz = len(FEAS) + 1
body(fz, 2, n_fz, 1, 6)
for t, col in {"Enabler": "D9EAD3", "Gap": "FFF2CC", "Constraint": "F4CCCC", "Mixed": "EDEDED"}.items():
    fz.conditional_formatting.add(f"C2:C{n_fz}", CellIsRule(operator="equal", formula=[f'"{t}"'], fill=PatternFill("solid", fgColor=col)))
fz.cell(n_fz + 2, 1, "Count by reading").font = f_bold
for k, t in enumerate(["Enabler", "Gap", "Constraint", "Mixed"]):
    fz.cell(n_fz + 3 + k, 1, t); fz.cell(n_fz + 3 + k, 2, f'=COUNTIF(C2:C{n_fz},A{n_fz + 3 + k})')
widths(fz, [22, 90, 12, 26, 60, 11])

# ---------- Method
mt = wb.create_sheet("Method and limits")
rows = [
("Question", "How are AI safety institutes placed, funded, steered and empowered in the US, the UK and eight middle-power peers plus the EU, and what should India's institute replicate (baseline) and add (safety uplift)?"),
("Sample", "US and UK as frontier benchmarks; Canada, Japan, South Korea, Singapore, France, Germany, Australia as middle powers; EU AI Office as a bloc regulator; India as subject. Kenya is a network member but no institute host was verified; Brazil, Switzerland and Israel have no designated institute in sources read."),
("Tiers", "A: statute or binding legal act. B: official government or institute publication (press release, budget, plan, parliamentary answer, FOI release). C-news: news outlet. C-analysis: think tank, academic or expert commentary."),
("Process", "Web search per jurisdiction, then reading of official pages and PDFs through a fetch tool that paraphrases text. Findings recorded with source ids. Codes on the Features sheet are a judgment from the Facts sheet."),
("Confidence", "High for A and B facts. Medium for C-news. Single-source claims are flagged in the Facts text."),
("Known limits", "Some PDFs and JavaScript pages could not be read; Korea's Enforcement Decree and the EU AI Act application dates were read through secondary hosts; no browser was available. India's AISI budget is not published, so the pillar figure is used and labelled."),
("Not 'none'", "'U' and 'Not found in sources read' mean the sources read are silent. They are not evidence of absence."),
("Companion file", "access-terms-audit-v0.xlsx: AI-safety conditions in 11 public compute programmes (annex)."),
]
header(mt, 1, ["Topic", "Note"])
for r in rows: mt.append(list(r))
body(mt, 2, len(rows) + 1, 1, 2); widths(mt, [18, 130])

# order sheets
order = ["Baseline and uplift", "Features", "RACI matrix", "Facts", "Budgets", "India feasibility", "Sources", "Method and limits"]
wb._sheets = [wb[n] for n in order]
wb.save(OUT); print("saved", OUT)
