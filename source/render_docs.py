import re, sys, json, subprocess, pathlib
sys.path.insert(0, "data")
import markdown
from sources import S

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"; OUT.mkdir(exist_ok=True)

CSS = """
:root{--g:#3B4A2F;--o:#6B7F3A;--l:#E8EFDC;--ink:#1d211a;--mute:#5b6352;--rule:#d5dccb}
@page{size:A4;margin:16mm 16mm 18mm 16mm}
*{box-sizing:border-box}
body{font-family:Inter,Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:var(--ink);margin:0;background:#fff}
.wrap{max-width:180mm;margin:0 auto}
header.doc{border-left:6px solid var(--o);padding:2mm 0 2mm 5mm;margin-bottom:6mm}
header.doc .track{font-size:9pt;letter-spacing:.06em;text-transform:uppercase;color:var(--o);font-weight:600}
header.doc h1{font-size:22pt;line-height:1.15;margin:1mm 0 1mm;color:var(--g)}
header.doc .sub{font-size:13pt;color:var(--mute)}
h2{font-size:15pt;color:var(--g);margin:7mm 0 2mm;padding-bottom:1mm;border-bottom:1px solid var(--rule);break-after:avoid}
h3{font-size:12.5pt;color:var(--o);margin:5mm 0 1.5mm;break-after:avoid}
p{margin:0 0 2.6mm}
ol,ul{margin:0 0 2.6mm;padding-left:6mm}
li{margin-bottom:1mm}
table{border-collapse:collapse;width:100%;margin:2mm 0 4mm;font-size:9.6pt;break-inside:avoid}
th{background:var(--g);color:#fff;text-align:left;padding:1.6mm 2mm;font-weight:600}
td{border-bottom:1px solid var(--rule);padding:1.6mm 2mm;vertical-align:top}
tr:nth-child(even) td{background:#f6f8f2}
blockquote{margin:2mm 0 4mm;padding:2mm 4mm;background:var(--l);border-left:3px solid var(--o)}
blockquote p{margin:0 0 1.5mm}
sup.c{font-size:7pt;color:var(--o);font-weight:600}
sup.c a{color:inherit;text-decoration:none}
.refs{font-size:7.6pt;line-height:1.3;color:var(--mute);margin-top:6mm;border-top:1px solid var(--rule);padding-top:2mm}
.refs h2{font-size:11pt;border:0;margin:0 0 2mm}
.refs ol{padding-left:5mm;column-count:2;column-gap:6mm}.refs li{break-inside:avoid}
.refs a{color:var(--g);word-break:break-all}
.tier{display:inline-block;font-size:7.5pt;padding:0 1.2mm;border-radius:2px;background:var(--l);color:var(--g);font-weight:600;margin-right:1mm}
em{color:var(--mute)}
strong{color:#141812}
@media screen{body{background:#f3f5ef;padding:12mm 0}.wrap{background:#fff;padding:14mm 16mm;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
"""

def render(md_path, title_override=None):
    raw = pathlib.Path(md_path).read_text()
    fm = {}
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            k, v = line.split(":", 1); fm[k.strip()] = v.strip()
        raw = raw[m.end():]
    order = []
    def cite(mm):
        sid = mm.group(1)
        if sid not in S: raise SystemExit(f"unknown source {sid}")
        if sid not in order: order.append(sid)
        n = order.index(sid) + 1
        return f'<sup class="c"><a href="#ref-{n}">{n}</a></sup>'
    lines = raw.split("\n"); fixed = []
    for ln in lines:
        is_item = re.match(r"^\s*(- |\d+\. )", ln)
        if is_item and fixed and fixed[-1].strip() and not re.match(r"^\s*(- |\d+\. )", fixed[-1]) and not fixed[-1].startswith(">"):
            fixed.append("")
        fixed.append(ln)
    raw = "\n".join(fixed)
    raw = re.sub(r"\s?\[S:([a-z0-9_]+)\]", cite, raw)
    html = markdown.markdown(raw, extensions=["tables", "sane_lists"])
    refs = "".join(
        f'<li id="ref-{i}"><span class="tier">{S[s][3]}</span>{S[s][1]}, “{S[s][0]}”, {S[s][2]}. <a href="{S[s][4]}">{S[s][4]}</a></li>'
        for i, s in enumerate(order, 1))
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{fm.get('title','')}</title><style>{CSS}</style></head><body><div class="wrap">
<header class="doc"><div class="track">{fm.get('track','')}</div><h1>{fm.get('title','')}</h1><div class="sub">{fm.get('subtitle','')}</div></header>
{html}
<section class="refs"><h2>Sources</h2><p>Tier A: statute or binding act. B: official publication. C-news / C-analysis: news or expert analysis. Retrieved 30 October 2026.</p><ol>{refs}</ol></section>
</div></body></html>"""
    return doc, order

if __name__ == "__main__":
    for name in ["proposal", "charter"]:
        html, order = render(ROOT / "docs" / f"{name}.md")
        (OUT / f"{name}.html").write_text(html)
        print(name, "sources cited:", len(order))
