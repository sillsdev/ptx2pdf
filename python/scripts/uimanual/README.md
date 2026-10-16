# PTXprint UI manual generator

Builds the PTXprint user manual (for the AI support bot, and as a PDF for people) from the
UI definition plus hand/AI-written explanations.

```
python python/scripts/uimanual/extract_ui.py            # glade + code -> docs/uimanual/data/ui_map.json
python python/scripts/uimanual/build_manual.py          # ui_map.json + docs/uimanual/content/*.md -> docs/uimanual/output/
python python/scripts/uimanual/build_manual.py --skeleton --nopdf   # also refresh data/chapters/*.md, skip the PDF
```

Requires PyMuPDF (`fitz`) and `markdown-it-py` (both already used by PTXprint).

* `extract_ui.py` – reads `ptxprint.glade`, `gtkview.py` (view levels, sensitivities),
  `modelmap.py` (config keys) and `texpert.py` (Advanced › Other settings). No GTK needed.
* `chapters.py` – the chapter list and which tab/dialog goes in which chapter.
* `build_manual.py` – merges everything; see `docs/uimanual/output/build-report.txt` afterwards
  for new controls that still need an explanation.

See `docs/uimanual/WRITING-GUIDE.md` for the content format and writing rules.
