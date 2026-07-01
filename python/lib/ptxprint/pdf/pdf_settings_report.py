"""
Generate HTML settings reports from PTXprint-generated PDFs.
Extracts the embedded settings ZIP and renders a summary similar to
the live PTXprint HTML report, sourced entirely from the PDF itself.
"""

import configparser, io, os, re, zipfile, logging
import html as _html
from datetime import datetime
from ptxprint.utils import getPDFconfig, pycodedir

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_font_spec(spec):
    """Parse 'FontName||bold|italic|features' into a readable string."""
    if not spec:
        return ""
    parts = str(spec).split("|")
    name = parts[0].strip()
    if not name:
        return str(spec)
    extras = []
    if len(parts) > 2 and parts[2].lower() == "true":
        extras.append("Bold")
    if len(parts) > 3 and parts[3].lower() == "true":
        extras.append("Italic")
    if len(parts) > 4 and parts[4].strip():
        extras.append(f"[{parts[4].strip()}]")
    return f"{name} ({', '.join(extras)})" if extras else name


def _parse_pagesize(s):
    """Parse '210mm, 297mm (A4)' → (width_mm, height_mm, label) or None."""
    if not s:
        return None
    m = re.match(r"(\d+(?:\.\d+)?)\s*mm\s*,\s*(\d+(?:\.\d+)?)\s*mm\s*(?:\((.+?)\))?", str(s))
    if m:
        return float(m.group(1)), float(m.group(2)), m.group(3) or ""
    return None


def _fval(extractor, section, key, fallback=""):
    """Get a cfg float value safely."""
    v = extractor.get(section, key, fallback)
    try:
        return float(v)
    except (TypeError, ValueError):
        return float(fallback) if fallback else 0.0


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------

class PDFSettingsExtractor:
    """Extracts PTXprint settings from the ZIP embedded in a PDF."""

    def __init__(self, pdf_path):
        self.pdf_path = str(pdf_path)
        self.cfg = None
        self.sty_text = None
        self.runinfo = ""
        self.changes_txt = None
        self.found = False
        self._zip_names = []

    def extract(self):
        """Returns True if PTXprint settings were found in the PDF."""
        zip_bytes = getPDFconfig(self.pdf_path)
        if not zip_bytes:
            return False
        try:
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                self._zip_names = zf.namelist()
                if "ptxprint.cfg" in self._zip_names:
                    cfg_text = zf.read("ptxprint.cfg").decode("utf-8", errors="replace")
                    self.cfg = configparser.ConfigParser(interpolation=None)
                    self.cfg.read_string(cfg_text)
                # Prefer ptxprint.sty; fall back to any .sty in the ZIP
                sty_candidates = [n for n in self._zip_names
                                  if n.endswith(".sty") and "ptxprint" in n.lower()]
                if not sty_candidates:
                    sty_candidates = [n for n in self._zip_names if n.endswith(".sty")]
                if sty_candidates:
                    self.sty_text = zf.read(sty_candidates[0]).decode("utf-8", errors="replace")
                if "_runinfo.txt" in self._zip_names:
                    self.runinfo = zf.read("_runinfo.txt").decode("utf-8", errors="replace").strip()
                if "changes.txt" in self._zip_names:
                    self.changes_txt = zf.read("changes.txt").decode("utf-8", errors="replace")
        except Exception as e:
            logger.warning(f"Failed to extract settings from {self.pdf_path}: {e}")
            return False
        self.found = self.cfg is not None
        return self.found

    def get(self, section, key, fallback=None):
        if self.cfg is None:
            return fallback
        return self.cfg.get(section, key, fallback=fallback)

    def getbool(self, section, key, fallback=False):
        if self.cfg is None:
            return fallback
        try:
            return self.cfg.getboolean(section, key, fallback=fallback)
        except ValueError:
            return fallback

    def get_modified_markers(self):
        """Diff embedded .sty against usfm_sb.sty; return {marker: [changed_fields]}."""
        if not self.sty_text:
            return {}
        _candidates = [
            os.path.join(pycodedir(), "ptx2pdf", "usfm_sb.sty"),
            os.path.normpath(os.path.join(pycodedir(), "..", "..", "..", "src", "usfm_sb.sty")),
        ]
        base_sty_path = next((p for p in _candidates if os.path.exists(p)), None)
        if not base_sty_path:
            logger.debug(f"Base stylesheet not found; tried: {_candidates}")
            return {}
        try:
            from ptxprint.styleditor import StyleEditor

            class _NullModel:
                def get(self, key, default=None):
                    return default
                def changed(self):
                    pass
                def getFont(self, _):
                    return None

            se = StyleEditor(_NullModel(), basepath=base_sty_path)
            se._read_styfh(io.StringIO(self.sty_text), sheet=se.sheet)
            changed = {}
            for mrk in se.allStyles():
                diffs = se.haschanged(mrk, styleonly=True)
                if diffs:
                    changed[mrk] = sorted(diffs)
            return changed
        except Exception as e:
            logger.warning(f"Failed to parse .sty: {e}")
            return {}


# ---------------------------------------------------------------------------
# Flat settings list used by both single and comparison reports
# ---------------------------------------------------------------------------

# Each entry: (display_label, section, key, format_fn)
# format_fn(raw_value) → display string, or None to use raw value
def _fmt_bool(v):
    return "Yes" if v and str(v).lower() not in ("false", "0", "") else "No"

def _fmt_font(v):
    return _parse_font_spec(v) if v else ""

def _fmt_books(extractor):
    scope = extractor.get("project", "bookscope", "single")
    if scope == "multiple":
        return extractor.get("project", "booklist", "") or extractor.get("project", "book", "")
    return extractor.get("project", "book", "")

def _fmt_direction(v):
    if not v:
        return "LTR"
    return v.upper()

def _fmt_pgspread(v):
    return f"{v}-up" if v else "1-up"

def _fmt_columns(v):
    return "Double (2)" if str(v).lower() in ("true", "2") else "Single (1)"


_SETTINGS_MANIFEST = [
    # (section_heading, [(label, cfg_section, cfg_key, fmt_fn_or_None)])
    ("1. Project", [
        ("Project ID",      "project",  "id",          None),
        ("Configuration",   "config",   "name",        None),
        ("Books",           None,       None,          None),   # handled specially
        ("Copyright",       "project",  "copyright",   None),
        ("License",         "project",  "license",     None),
    ]),
    ("2. Layout", [
        ("Page Size",       "paper",    "pagesize",    None),
        ("Top Margin",      "paper",    "topmargin",   lambda v: f"{v} mm"),
        ("Bottom Margin",   "paper",    "bottommargin",lambda v: f"{v} mm"),
        ("Side Margin",     "paper",    "margins",     lambda v: f"{v} mm"),
        ("Font Size",       "paper",    "fontfactor",  lambda v: f"{float(v):.2f} pt"),
        ("Line Spacing",    "paragraph","linespacing",  lambda v: f"{float(v):.2f} pt"),
        ("Columns",         "paper",    "columns",     _fmt_columns),
        ("Base Indent",     "document", "indentunit",  lambda v: f"{float(v):.3f} in"),
        ("Mirrored Headers","header",   "mirrorlayout", _fmt_bool),
    ]),
    ("4. Fonts", [
        ("Regular",         "document", "fontregular",    _fmt_font),
        ("Bold",            "document", "fontbold",       _fmt_font),
        ("Italic",          "document", "fontitalic",     _fmt_font),
        ("Bold Italic",     "document", "fontbolditalic", _fmt_font),
        ("Fallback",        "document", "fontextraregular",_fmt_font),
    ]),
    ("5. Writing System", [
        ("Script Code",     "document", "script",      None),
        ("Text Direction",  "document", "ifrtl",       _fmt_direction),
    ]),
    ("6. Features", [
        ("Page Borders",    "fancy",    "pageborders",     _fmt_bool),
        ("Ornaments",       "fancy",    "enableornaments", _fmt_bool),
        ("Thumb Tabs",      "thumbtabs","ifthumbtabs",     _fmt_bool),
        ("Interlinear",     "document", "interlinear",     _fmt_bool),
    ]),
    ("7. Peripheral Components", [
        ("Front Matter PDF","project",  "ifinclfrontpdf",  _fmt_bool),
        ("Front Matter",    "project",  "iffrontmatter",   _fmt_bool),
        ("Table of Contents","document","toc",             _fmt_bool),
        ("Colophon",        "project",  "ifcolophon",      _fmt_bool),
        ("Back Matter PDF", "project",  "ifinclbackpdf",   _fmt_bool),
    ]),
    ("8. Output Format", [
        ("Pagination",      "finishing","pgsperspread",    _fmt_pgspread),
        ("Crop Marks",      "paper",    "cropmarks",       _fmt_bool),
        ("Watermark",       "paper",    "ifwatermark",     _fmt_bool),
        ("PDF/X-1a",        "document", "printarchive",    _fmt_bool),
    ]),
]

# Keys that should only appear when their value is "Yes" / truthy
_SHOW_ONLY_IF_TRUE = {
    ("fancy",    "pageborders"),
    ("fancy",    "enableornaments"),
    ("thumbtabs","ifthumbtabs"),
    ("document", "interlinear"),
    ("project",  "ifinclfrontpdf"),
    ("project",  "iffrontmatter"),
    ("document", "toc"),
    ("project",  "ifcolophon"),
    ("project",  "ifinclbackpdf"),
    ("paper",    "cropmarks"),
    ("paper",    "ifwatermark"),
    ("document", "printarchive"),
    ("header",   "mirrorlayout"),
}


def _get_value(extractor, section, key, fmt_fn):
    """Return (raw, display) for a setting, or (None, None) if unavailable."""
    if section is None and key is None:
        # Special: books
        raw = _fmt_books(extractor)
        return raw, raw
    raw = extractor.get(section, key)
    if raw is None:
        return None, None
    display = fmt_fn(raw) if fmt_fn else raw
    return raw, display


# ---------------------------------------------------------------------------
# Single-PDF report (uses the existing Report class for consistent styling)
# ---------------------------------------------------------------------------

def generate_single_html(extractor, out_path):
    """
    Generate a settings report HTML for one PDF.
    Returns True on success, False if no settings were found.
    """
    if not extractor.found:
        return False

    from ptxprint.report import Report
    import logging as _logging

    r = Report()
    # Prevent log noise during our section-building from going into "1. Runtime"
    logging.getLogger().removeHandler(r.reporthandler)
    r.sections.clear()

    _build_single_sections(r, extractor)

    proj_id  = extractor.get("project", "id", "unknown") or "unknown"
    cfg_name = extractor.get("config",  "name", "unknown") or "unknown"
    texmodel = {"project/id": proj_id, "config/name": cfg_name}

    try:
        r.generate_html(out_path, texmodel)
        return True
    except Exception as e:
        logger.error(f"Failed to write settings report: {e}")
        return False


def _build_single_sections(r, extractor):
    import logging as _logging

    # Section 1 prefix: note this is from embedded config, not a live run
    r.add("1. Project/Source",
          f"Settings extracted from: {os.path.basename(extractor.pdf_path)}",
          severity=_logging.DEBUG)
    if extractor.runinfo:
        r.add("1. Project/Source", f"Build info: {extractor.runinfo}",
              severity=_logging.DEBUG)

    # Walk the manifest
    for section_heading, settings in _SETTINGS_MANIFEST:
        for label, sec, key, fmt_fn in settings:
            raw, display = _get_value(extractor, sec, key, fmt_fn)
            if raw is None or display is None:
                continue
            # Skip empty strings
            if not str(display).strip():
                continue
            # For "show only if true" fields, skip when false
            if (sec, key) in _SHOW_ONLY_IF_TRUE and display == "No":
                continue
            r.add(section_heading, f"{label}: {_html.escape(str(display))}",
                  severity=_logging.DEBUG)

    # Section 3: Modified markers from .sty
    changed = extractor.get_modified_markers()
    if changed:
        rows = ['<table style="width:100%">']
        for mkr, fields in sorted(changed.items(),
                                  key=lambda x: list(reversed(x[0].split("|")))):
            rows.append(
                f'<tr><td></td>'
                f'<td style="width:15%">{_html.escape(mkr)}</td>'
                f'<td>{_html.escape(" ".join(fields))}</td></tr>'
            )
        rows.append('</table>')
        r.add("3. Markers/Modified markers", "".join(rows), txttype="html")
    elif extractor.sty_text is not None:
        r.add("3. Markers", "No marker changes detected (matches base stylesheet)",
              severity=_logging.INFO)
    else:
        r.add("3. Markers", "No stylesheet (.sty) found in embedded settings",
              severity=_logging.DEBUG)

    # Section 2: page spread visual (added after other layout entries so it sorts last)
    _add_page_visual(r, extractor)

    # Section 9: Files
    if extractor.changes_txt is not None:
        r.add("9. Files/changes.txt", extractor.changes_txt,
              severity=_logging.NOTSET, txttype="pretext")


def _add_page_visual(r, extractor):
    """Append the page spread diagram to section 2."""
    import logging as _logging
    pagesize_str = extractor.get("paper", "pagesize", "")
    parsed = _parse_pagesize(pagesize_str)
    if parsed is None:
        return
    width_mm, height_mm, label = parsed
    top    = _fval(extractor, "paper", "topmargin",    "12")
    bottom = _fval(extractor, "paper", "bottommargin", "12")
    side   = _fval(extractor, "paper", "margins",      "12")
    gutter = _fval(extractor, "paper", "gutter",       "0")
    cols   = 2 if extractor.getbool("paper", "columns", False) else 1
    rtl    = extractor.get("document", "ifrtl", "ltr")
    binding = "RTL" if str(rtl).lower() == "rtl" else "LTR"
    colgap = _fval(extractor, "document", "colgutterfactor", "5")
    fontfactor  = _fval(extractor, "paper",     "fontfactor",  "11")
    linespacing = _fval(extractor, "paragraph", "linespacing", "14")

    try:
        from ptxprint.report import Report as _Report

        _r = _Report.__new__(_Report)

        class _View:
            def get(self, key, default=None):
                if key == "s_fontsize":    return fontfactor
                if key == "s_linespacing": return linespacing
                return default

        page_data = {"width_mm": width_mm, "height_mm": height_mm}
        margin_data = {
            "top_mm": top, "bottom_mm": bottom,
            "side_margin_mm": side, "binding_gutter_mm": gutter,
        }
        layout_options = {
            "num_columns": cols, "binding_direction": binding,
            "column_gap_mm": colgap, "apply_gutter_to_outer_edge": False,
        }
        summary = (
            f"<b>Page Size (per page):</b> {width_mm:.2f}mm x {height_mm:.2f}mm<br/>"
            f"<b>Margins (mm):</b> Top: {top:.1f}, Bottom: {bottom:.1f}, "
            f"Side: {side:.1f}, Gutter: {gutter:.1f}"
        )
        try:
            vis = _r.generatePageSpreadVisualization(
                _View(), page_data, margin_data, layout_options, max_page_height_px=300)
        except Exception:
            vis = ""
        r.add("2. Layout/ Page Spread Preview", summary + vis,
              severity=_logging.DEBUG, txttype="html")
    except Exception as e:
        logger.debug(f"Could not render page visual: {e}")


# ---------------------------------------------------------------------------
# Comparison report (custom HTML with JS toggle)
# ---------------------------------------------------------------------------

_COMPARE_CSS_EXTRA = """
body { max-width: 1200px; }
/* ---- page header ---- */
.page-header { display: flex; justify-content: space-between; align-items: center;
               gap: 20px; margin-bottom: 0.3em; }
.page-header h1 { margin: 0; }
.page-header-right { flex-shrink: 0; text-align: right; }
/* ---- toggle button ---- */
.toggle-btn { padding: 6px 18px; cursor: pointer; border: 1px solid #1a5fb4;
              border-radius: 4px; background: #1a5fb4; color: white;
              font-size: 0.95em; font-weight: bold; white-space: nowrap; }
.toggle-btn.diff-mode { background: #f0f0f0; color: #333;
                        border-color: #aaa; font-weight: normal; }
.diff-badge { display: inline-block; background: #e74c3c; color: white;
              border-radius: 10px; padding: 2px 8px; font-size: 0.85em; margin-top: 6px; }
/* ---- column-label bar ---- */
.col-label-bar { display: grid; grid-template-columns: 13em 1fr 1fr;
                 border-bottom: 2px solid #ccc; margin-bottom: 0.3em; }
.col-label-bar span { padding: 2px 8px; font-size: 0.8em; color: #666;
                      font-style: italic; overflow: hidden; text-overflow: ellipsis;
                      white-space: nowrap; }
.col-label-bar span:first-child { color: #999; }
/* ---- comparison table ---- */
table.compare { width: 100%; border-collapse: collapse; margin-bottom: 0.5em;
                table-layout: fixed; }
table.compare td { padding: 3px 8px; vertical-align: top;
                   overflow-wrap: break-word; word-break: break-word; }
table.compare td:first-child { width: 13em; }
table.compare tr.diff td { background-color: #fff3cd; }
table.compare tr.diff td:first-child { font-weight: bold; }
table.compare tr.same td { color: #888; }
body.hide-same table.compare tr.same { display: none; }
/* ---- misc ---- */
.section-header  { margin-top: 1.2em; border-bottom: 2px solid #ccc; padding-bottom: 3px; }
.identical-note  { color: #555; font-style: italic; margin: 0 0 0.5em 0.5em; font-size: 0.9em; }
"""

_COMPARE_JS = """
var showAll = true;
function toggleView() {
    showAll = !showAll;
    document.body.classList.toggle('hide-same', !showAll);
    var btn = document.getElementById('btn-toggle');
    btn.textContent = showAll ? 'Show differences only' : 'Show all settings';
    btn.classList.toggle('diff-mode', !showAll);
}
"""


def generate_compare_html(extractor_a, extractor_b, out_path):
    """
    Generate a side-by-side comparison HTML for two PDFs.
    Both extractors must already have .extract() called.
    Returns True on success.
    """
    css_path = os.path.join(pycodedir(), "sakura.css").replace("\\", "/")
    name_a = os.path.basename(extractor_a.pdf_path)
    name_b = os.path.basename(extractor_b.pdf_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Count differences for the summary badge
    diff_count = _count_diffs(extractor_a, extractor_b)

    esc_a = _html.escape(name_a)
    esc_b = _html.escape(name_b)

    lines = [
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"',
        '  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
        '<html><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>',
        f'<head><title>PTXprint Settings Comparison</title>',
        f'<link rel="stylesheet" href="{_html.escape(css_path)}" type="text/css"/>',
        f'<style>{_COMPARE_CSS_EXTRA}</style>',
        '</head><body>',
        '<div class="page-header">',
        '  <h1>PTXprint Settings Comparison</h1>',
        '  <div class="page-header-right">',
        '    <button id="btn-toggle" class="toggle-btn" onclick="toggleView()">Show differences only</button>',
        f'    <div><span class="diff-badge">{diff_count} different</span></div>',
        '  </div>',
        '</div>',
        '<div class="col-label-bar">',
        f'  <span>{timestamp}</span>',
        f'  <span>PDF A &#x2014; {esc_a}</span>',
        f'  <span>PDF B &#x2014; {esc_b}</span>',
        '</div>',
    ]

    # Settings sections — section 3 (Markers) is injected in order after section 2
    markers_emitted = False

    def _emit_markers():
        nonlocal markers_emitted
        changed_a = extractor_a.get_modified_markers()
        changed_b = extractor_b.get_modified_markers()
        all_mkrs = sorted(set(list(changed_a.keys()) + list(changed_b.keys())),
                          key=lambda x: list(reversed(x.split("|"))))
        mkr_rows = []
        for mkr in all_mkrs:
            fa = " ".join(changed_a.get(mkr, []))
            fb = " ".join(changed_b.get(mkr, []))
            mkr_rows.append(("diff" if fa != fb else "same", mkr, fa, fb))
        has_diffs = any(r[0] == "diff" for r in mkr_rows)
        lines.append('<h2 class="section-header" id="section-3">3. Markers</h2>')
        if not mkr_rows or not has_diffs:
            lines.append('<p class="identical-note">&#x2714; All marker styles identical</p>')
        else:
            lines.append('<table class="compare">')
            for row_cls, mkr, fa, fb in mkr_rows:
                lines.append(
                    f'<tr class="{row_cls}"><td>{_html.escape(mkr)}</td>'
                    f'<td>{_html.escape(fa) or "<em>unmodified</em>"}</td>'
                    f'<td>{_html.escape(fb) or "<em>unmodified</em>"}</td></tr>'
                )
            lines.append('</table>')
        markers_emitted = True

    for section_heading, settings in _SETTINGS_MANIFEST:
        sec_num = section_heading.split(".")[0].strip()
        if not markers_emitted and int(sec_num) > 3:
            _emit_markers()
        rows_html = _build_compare_rows(extractor_a, extractor_b, settings)
        if not rows_html:
            continue
        has_diffs = any('class="diff"' in r for r in rows_html)
        lines.append(
            f'<h2 class="section-header" id="section-{sec_num}">'
            f'{_html.escape(section_heading)}</h2>'
        )
        if not has_diffs:
            lines.append('<p class="identical-note">&#x2714; All settings identical</p>')
        else:
            lines += ['<table class="compare">'] + rows_html + ['</table>']

    if not markers_emitted:
        _emit_markers()

    # Section 9: changes.txt
    if extractor_a.changes_txt is not None or extractor_b.changes_txt is not None:
        txt_diff = extractor_a.changes_txt != extractor_b.changes_txt
        lines.append('<h2 class="section-header" id="section-9">9. Files / changes.txt</h2>')
        if not txt_diff:
            lines.append('<p class="identical-note">&#x2714; changes.txt identical</p>')
        else:
            txt_a = _html.escape(extractor_a.changes_txt or "(not present)")
            txt_b = _html.escape(extractor_b.changes_txt or "(not present)")
            lines += [
                '<table class="compare">',
                f'<tr class="diff"><td>changes.txt</td>'
                f'<td><pre style="white-space:pre-wrap;font-size:0.72em">{txt_a}</pre></td>'
                f'<td><pre style="white-space:pre-wrap;font-size:0.72em">{txt_b}</pre></td></tr>',
                '</table>',
            ]

    lines += [
        '<hr/>',
        f'<script>{_COMPARE_JS}</script>',
        '</body></html>',
    ]

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True
    except Exception as e:
        logger.error(f"Failed to write comparison report: {e}")
        return False


def _build_compare_rows(extractor_a, extractor_b, settings):
    rows = []
    for label, sec, key, fmt_fn in settings:
        raw_a, disp_a = _get_value(extractor_a, sec, key, fmt_fn)
        raw_b, disp_b = _get_value(extractor_b, sec, key, fmt_fn)
        disp_a = str(disp_a) if disp_a is not None else ""
        disp_b = str(disp_b) if disp_b is not None else ""
        if not disp_a and not disp_b:
            continue
        row_cls = "diff" if disp_a != disp_b else "same"
        rows.append(
            f'<tr class="{row_cls}">'
            f'<td>{_html.escape(label)}</td>'
            f'<td>{_html.escape(disp_a)}</td>'
            f'<td>{_html.escape(disp_b)}</td>'
            '</tr>'
        )
    return rows


def _count_diffs(extractor_a, extractor_b):
    count = 0
    for _, settings in _SETTINGS_MANIFEST:
        for _, sec, key, fmt_fn in settings:
            _, da = _get_value(extractor_a, sec, key, fmt_fn)
            _, db = _get_value(extractor_b, sec, key, fmt_fn)
            if str(da or "") != str(db or ""):
                count += 1
    # markers
    ca = extractor_a.get_modified_markers()
    cb = extractor_b.get_modified_markers()
    all_mkrs = set(list(ca.keys()) + list(cb.keys()))
    for m in all_mkrs:
        if ca.get(m) != cb.get(m):
            count += 1
    return count
