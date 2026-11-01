# AI Safety Institutes: A roadmap for India's AI Safety Institute

Submission package for the Mangrove Middle Powers Hackathon, Track B (Investment: safety institutes).

## Contents

| Path | What it is |
|---|---|
| `submission/proposal.pdf` | The written submission |
| `submission/charter.pdf` | Annex A: draft founding charter of the IndiaAI Safety Institute, with a model statutory clause |
| `submission/demo.mp4` | A voice-over walkthrough of the explorer |
| `explorer/index.html` | The interactive 3D explorer |
| `evidence/aisi-comparison-v1.xlsx` | The comparative analysis of legislative mandates, accountability and funding of important AISI features across US, 9 middle powers, EU and India |
| `evidence/access-terms-audit-v0.xlsx` | Companion annex: AI-safety conditions in 11 public compute programmes |
| `evidence/research-notes.md` | Raw research notes, in the order sources were read |
| `AI_USE_LOG.md` | Log of AI-based research |
| `source/` | Everything needed to rebuild: data (`data/*.py`), document sources (`docs/*.md`), build scripts and the app source |

## Rebuild

```
cd source
python3 build_workbook_v1.py evidence.xlsx      # workbook; recalculate in Excel or LibreOffice
python3 render_docs.py                           # proposal and charter HTML (print to PDF from a browser)
python3 export_json.py                           # app data
cd app && npm install && npm run build           # explorer -> app/dist/index.html
```

Edit facts, features and sources in `source/data/`. The workbook, documents and app all read from those files.

## Source tiers

- **A:** statute or binding legal act.
- **B:** official government or institute publication (press release, budget, plan, parliamentary answer, FOI release).
- **C-news:** a news outlet.
- **C-analysis:** think tank, academic or expert commentary.
