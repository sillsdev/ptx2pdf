import html # Added for html.escape
import logging, os
import xml.etree.ElementTree as et
from ptxprint.utils import rtlScripts

# DEBUG is informational
# INFO is something that could fail, passed
loglabels = ["\u00A0", "\u00A0", "\u2714", "W", "E", "F", "C"]
logcolors = ["white", "lightskyblue", "palegreen", "orange", "orangered", "fuchsia", "Aqua"]

class ReportEntry:
    def __init__(self, msg, severity=logging.DEBUG, order=0, txttype="html"):
        self.msg = msg
        self.severity = severity
        self.order = order
        self.txttype = txttype

    def ashtml(self):
        if self.txttype == "html":
            try:
                return et.fromstring("<node>"+ self.msg +"</node>")
            except et.ParseError as e:
                e.add_note("text: "+self.msg)
                raise e
        elif self.txttype == "pretext":
            e = et.Element("node")
            pre = et.SubElement(e, "pre")
            pre.text = self.msg
            return e
        elif self.txttype == "text":
            e = et.Element("node")
            e.text = self.msg
            return e

html_template = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
<head>
    <title>PTXprint report on {project/id}/{config/name}</title>
    <link rel="stylesheet" href="{css}" type="text/css" />
</head>
<body>
</body></html>
"""

class Report:
    def __init__(self):
        self.sections = {}

    def add(self, section, msg, **kw):
        """ section is a hierarchy of sections separated by / in the string """
        self.sections.setdefault(section, []).append(ReportEntry(msg, **kw))

    def generate_html(self, fname, texmodel):
        doc = et.fromstring(html_template.format(css=os.path.join(os.path.dirname(__file__), "sakura.css"), **texmodel))
        body = doc.find("body")
        lasts = []
        curr = body
        for s, t in sorted(self.sections.items()):
        # for s, t in self.sections.items():
            if not len(t):
                continue
            nexts = s.split("/")
            done = True
            for i, p in enumerate(nexts):
                if not done or i >= len(lasts) or lasts[i] != p:
                    h = et.SubElement(body, "h{}".format(i+1))
                    h.text = p
                    done = False
            table = et.SubElement(body, "table")
            for m in sorted(t, key=lambda x:(-x.order, -x.severity, x.msg)):
                tr = et.SubElement(table, "tr")
                score = et.SubElement(tr, "td", style="background-color:"+logcolors[m.severity // 10])
                score.text = loglabels[m.severity // 10]
                msg = et.SubElement(tr, "td")
                msge = m.ashtml()
                msg.text = msge.text
                for c in msge:
                    msg.append(c)
            lasts = nexts
        with open(fname, "w", encoding="utf-8") as outf:
            outf.write(et.tostring(doc, method="html", encoding="unicode"))

    def run_view(self, view):
        self.get_styles(view)
        self.get_writingSystems(view)
        self.get_layout(view)
        self.get_layout_preview(view)
        self.get_usfms(view)
        self.get_files(view)
        self.get_general_info(view)

    def get_layout(self, view):
        if hasattr(view, 'ufPages') and len(view.ufPages):
            self.add("2. Layout", f"Underfilled pages <b>({len(view.ufPages)})</b>: "+ " ".join([str(x) for x in view.ufPages]), severity=logging.WARN)
        textheight, linespacing = view.calcBodyHeight()
        lines = textheight / linespacing
        if abs(lines - int(lines + 0.5)) > 0.05:
            self.add("2. Layout", f"Lines on page (suboptimal): {lines:.1f}", severity=logging.WARN)
        else:
            self.add("2. Layout", f"Lines on page (optimized): {int(lines + 0.5)}", severity=logging.INFO)
        fntsz, lnspc = self.getSizeSpacing(view)
        ratio = lnspc / fntsz
        varls = view.get("c_noGrid", False)
        self.add("2. Layout", f"Font Size/Line Spacing: {fntsz:.2f}pt/{lnspc:.2f}pt ({'<b>variable</b>' if varls else 'on grid'})", severity=logging.WARN if varls else logging.DEBUG)
        self.add("2. Layout", f"Linespacing Ratio: {ratio:.2f}", severity=logging.WARN if ratio < 1.0 or ratio > 1.5 else logging.DEBUG)
        # Could we also calculate all the derived font sizes from the styles to work out what 
        #   * the LARGEST font size used (and in which marker) 
        # and the smallest (in ? marker:)

    def getSizeSpacing(self, view):
        fntsz = float(view.get("s_fontsize", 11.0))
        lnspc = float(view.get("s_linespacing", 14.0))
        return fntsz, lnspc
        
    def get_styles(self, view):
        results = {}
        modified = []
        mrkrset = view.get_usfms().get_markers(view.getBooks())
        for s in sorted(view.styleEditor.allStyles()):
            if view.styleEditor.haschanged(s, styleonly=True):
                modified.append("<b>"+s+"</b>" if s in mrkrset else s)
            if (f := view.styleEditor.getval(s, 'fontname', None, includebase=True)) is None:
                continue
            results.setdefault(f, []).append(s)
        mainfonts = set()
        for a in ("R", "B", "I", "BI"):
            f = view.get("bl_font"+a, skipmissing=True)
            if f is not None:
                mainfonts.add(f.name)
                results.setdefault(f.name, [])
        for k, v in sorted(results.items()):
            line = "{}: {}".format("<b>{}</b>".format(k) if k in mainfonts or any(m in mrkrset for m in v) else k,
                                   " ".join(["<b>{}</b>".format(m) if m in mrkrset else m for m in sorted(v)]))
            self.add("4. Fonts/Usage", line, txttype="html")
        fb = view.get("bl_fontExtraR", skipmissing=True)
        if fb is not None:
            if view.get("c_useFallbackFont", False):
                line = f"<b>{fb.name}</b>: Active Fallback Font"
            else:
                line = f"{fb.name}: <b>Inactive</b> Fallback Font"
            self.add("4. Fonts/Usage", line, txttype="html")
            
        self.add("3. USFM/Markers", "Markers used: "+" ".join(sorted(mrkrset)), txttype="text")
        self.add("3. USFM/Markers", "Modified markers: " + " ".join(modified), txttype="html")

    def get_files(self, view):
        for a in (("changes.txt", "c_usePrintDraftChanges"),
                  ("ptxprint-mods.tex", "c_useModsTex")):
            if view.get(a[1]):
                f = os.path.join(view.project.srcPath(view.cfgid), a[0])
                if not os.path.exists(f):
                    continue
                with open(f, encoding="utf-8") as inf:
                    data = inf.read()
                self.add("9. Files/"+a[0], data, severity=logging.NOTSET, txttype="pretext")

    def get_usfms(self, view):
        usfms = view.get_usfms()
        passed = []
        failed = []
        # self.add("3. USFM/Checks", f"Books in Publication: {' '.join(view.getBooks())}", severity=logging.INFO)
        for bk in view.getBooks():
            doc = usfms.get(bk)
            if doc is None:
                self.add("3. USFM/Checks", f"No USFM for {bk}", severity=logging.WARN)
                continue
            
            if doc.xml.errors is None or not len(doc.xml.errors):
                passed.append(bk)
            else:
                for e in doc.xml.errors:
                    (msg, pos, ref) = e #pos.l, pos.c = char num
                    emsg = f"{ref} {msg} at line {pos.l}, char {pos.c}"
                    failed.setdefault(bk, []).append(emsg)
        if len(passed):
            self.add("3. USFM/Checks", f"Books passed: {' '.join(passed)}", severity=logging.INFO)
        if len(failed):
            for bk, elist in failed.items():
                for m in elist:
                    self.add(f"3. USFM Checks/{bk}", m, severity=logging.WARN)
        if "GLO" in view.getBooks():
            fltr = "Filtered" if view.get("c_filterGlossary", False) else "Unfiltered"
            asfn = "As Footnotes" if view.get("c_glossaryFootnotes", False) else ""
            self.add("7. Peripheral Components", f"Glossary: {fltr} {asfn}", severity=logging.DEBUG)

    def get_usfm(self, view, doc, bk):
        r = doc.getroot()
        essentials = "h toc1 toc2 toc3 p".split() # How do we check for other non-para USFM's?  c v etc.
        missing = [a for a in essentials if r.find(f'.//para[@style="{a}"]') is None]
        if len(missing):
            self.add("3. USFM/Checks", f'{bk} is missing the following essential markers: {" ".join(missing)}', severity=logging.ERROR)
            return False
        return True

        def myhackylambda(view, widget):
            return ("", logging.DEBUG)

    def get_general_info(self, view):
        widget_map = {
            "Project Name":               ("1. Project/Overview", "l_projectFullName", 1100, \
                                            lambda v,w: (v.get("l_projectFullName", ""), logging.DEBUG)),
            "Copyright":                  ("1. Project/Overview", "t_copyrightStatement", 1080, \
                                            lambda v,w: (v.get("t_copyrightStatement", ""), logging.DEBUG)),
            "License":                    ("1. Project/Overview", "ecb_licenseText", 1060, \
                                            lambda v,w: (v.get("ecb_licenseText", ""), logging.DEBUG)),
                                                         
            "Diglot Configuration":       ("2. Layout/Diglot", "c_diglot", 0, None), # More details to be added for this
            "Two Column Layout":          ("2. Layout", "c_doublecolumn", 0, None),
            "Mirrored Headers":           ("2. Layout", "c_mirrorpages", 0, None),
            "Decorative Border":          ("6. Features", "c_inclPageBorder", 0, \
                                            lambda v,w: (v.get("r_border").upper() if v.get("c_useOrnaments", False) else "ON, but Ornamental Decorations are <b>Off</b>", \
                                            logging.DEBUG if v.get("c_useOrnaments", False) else logging.WARN)),
            "Ornamental Features":        ("6. Features", "c_useOrnaments", 0, None),
            "Thumb Tabs":                 ("6. Features", "c_thumbtabs", 0, None),
            "Interlinear":                ("6. Features", "c_interlinear", 0, \
                                            lambda v,w: ("Language Code: " + (v.get("t_interlinearLang") or "<b>Missing!</b>"), \
                                            logging.WARN if len(v.get("t_interlinearLang")) != 2 else logging.DEBUG)),
            "Study Bible/Extended Notes": ("2. Layout/Notes and Refs", "c_extendedFnotes", 0, None), # how to count how many there are?
            "Footnotes":                  ("2. Layout/Notes and Refs", "c_includeFootnotes", 0, None),
            "Cross-References":           ("2. Layout/Notes and Refs", "c_includeXrefs", 0, None),
            "Cross-Refs (other)":         ("2. Layout/Notes and Refs", "c_useXrefList", 0, \
                                            lambda v,w: ("External List: " + (v.get("fcb_xRefExtListSource") or "<b>Unknown!</b>"), logging.DEBUG)),
            "Pictures Enabled":           ("2. Layout/Illustrations", "c_includeillustrations", 0, None),
            "Missing Images":             ("2. Layout/Illustrations", "l_missingPictureString", 0, \
                                            lambda v,w: (v.get("l_missingPictureString", "")[18:], logging.WARN)),
            "Only Placeholders":          ("2. Layout/Illustrations", "c_figplaceholders", 0, \
                                            lambda v,w: ("", logging.WARN if v.get(w, False) else logging.DEBUG)),
            "PDF Version PDF/X-1a":       ("8. Output Format", "c_printArchive", 100, None),
            "Crop Marks":                 ("8. Output Format", "c_cropmarks", 200, None),
            "Watermark":                  ("8. Output Format", "c_applyWatermark", 50, \
                                            lambda v,w: (v.get("lb"+w[1:], "").strip("."), logging.DEBUG)),
            "Booklet Pagination":         ("8. Output Format", "fcb_pagesPerSpread", 30, \
                                            lambda v,w: (v.get(w, "")+"-up", logging.DEBUG)),
            "Front Matter PDF(s)":        ("7. Peripheral Components", "c_inclFrontMatter", 0, \
                                            lambda v,w: (v.get("lb"+w[1:], "").strip("."), logging.DEBUG)),
            "Table of Contents":          ("7. Peripheral Components", "c_autoToC", 0, None),
            "Thumb Tabs":                 ("6. Features", "c_thumbtabs", 0, None),
            "Front Matter":               ("7. Peripheral Components", "c_frontmatter", 0, \
                                            lambda v,w: ("", logging.WARN if v.get(w, False) and v.get("c_colophon", False) else logging.DEBUG)),
            "Colophon":                   ("7. Peripheral Components", "c_colophon", 0, \
                                            lambda v,w: ("", logging.WARN if v.get(w, False) and v.get("c_frontmatter", False) else logging.DEBUG)),
            "Back Matter PDF(s)":         ("7. Peripheral Components", "c_inclBackMatter", 0, \
                                            lambda v,w: (v.get("lb"+w[1:], "").strip("."), logging.DEBUG)),
        }
        
        check_order = 100  # Not used, consider removing or integrating
        
        for title, (section, widget_id, order, widget_fn) in widget_map.items():
            if not view.get(widget_id, False):
                continue

            if widget_fn is None:
                extra = ""
                severity = logging.DEBUG
            else:
                (extra, severity) = widget_fn(view, widget_id)
            if len(extra):
                extra = ": " + extra
            self.add(section, f"{title}{extra}", severity=severity, order=order, txttype="text")

    def get_writingSystems(self, view):  # to do: use the actual script name from a _allscripts lookup instead of just the code
        s = view.get("fcb_script") or "Zyyy"
        s = "Default/Unknown" if s == "Zyyy" else s
        self.add("5. Writing System", f"Script Code: {s}", severity=logging.WARN if len(s) > 4 else logging.DEBUG, order=100, txttype="html")

        d = (view.get("fcb_textDirection") or "ltr").upper()
        rtl = s in rtlScripts
        sev = logging.WARN if (d == "RTL" and not rtl) or (d == "LTR" and rtl) or (d == "TTB" and s != "Mong") else logging.DEBUG
        suffix = " - <b>unexpected!</b>" if sev == logging.WARN else ""
        self.add("5. Writing System", f"Text Direction: {d}{suffix}", severity=sev, txttype="html")
        
        bb = view.get("c_RTLbookBinding", False)
        sev = logging.WARN  if (bb and d != "RTL" and not rtl) or (not bb and (d == "RTL" or rtl)) else logging.DEBUG
        if bb or sev == logging.WARN:
            suffix = " - <b>unexpected!</b>" if sev == logging.WARN else ""
            self.add("5. Writing System", f"RTL Book Binding: {bb}{suffix}", severity=sev, txttype="html")
            
        # to do: add other Additional Script Settings (snippet settings for the script)
        #    and also Specific Line Break Locale (flagging an issue if we have unexpected values there for CJK languages)


    def renderSinglePage(self, view, page_side, scaled_page_w_px, scaled_page_h_px, scaled_m_top_px, scaled_m_bottom_px,
                         scaled_physical_left_margin_px, scaled_physical_right_margin_px, margin_labels_mm, 
                         page_num_text, num_columns, scaled_column_gap_px, label_font_size_px, binding_dir):

        fntsz, lnspc = self.getSizeSpacing(view)
        text_block_content_text = f"Single<br/>Column<br/>Text Block<br/><br/>{fntsz:.2f}pt/{lnspc:.2f}pt" if num_columns == 1 \
                             else f"Double<br/>Column<br/>Text Block<br/><br/>{fntsz:.2f}pt/{lnspc:.2f}pt"

        scaled_text_block_w_px = scaled_page_w_px - scaled_physical_left_margin_px - scaled_physical_right_margin_px
        scaled_text_block_h_px = scaled_page_h_px - scaled_m_top_px - scaled_m_bottom_px
        if scaled_text_block_w_px < 0: scaled_text_block_w_px = 0
        if scaled_text_block_h_px < 0: scaled_text_block_h_px = 0

        column_divider_html = ""
        if num_columns == 2:
            column_divider_html = f"""
            <div style="position: absolute; top: 0; left: 50%; transform: translateX(-50%);
                        width: 1px; height: 100%; background-color: #aaa;"></div>"""

        page_num_style = f"position: absolute; top: 5px; font-size: {label_font_size_px*1.2:.0f}px; color: #555;"
        if page_side == 'left': page_num_style += "left: 5px;"
        else: page_num_style += "right: 5px;"
        
        page_html = f"""
        <div class="page-dummy" style="
            width: {scaled_page_w_px:.2f}px; height: {scaled_page_h_px:.2f}px;
            padding-top: {scaled_m_top_px:.2f}px;
            padding-left: {scaled_physical_left_margin_px:.2f}px;
            padding-right: {scaled_physical_right_margin_px:.2f}px;
            padding-bottom: {scaled_m_bottom_px:.2f}px;
            background-color: #e0e8ff; border: 1px solid #333;
            box-sizing: border-box; position: relative;">
            <div style="{page_num_style}">{page_num_text}</div>
            <div class="text-block-area" style="
                width: 100%; height: 100%; background-color: white;
                border: 1px dashed #666; box-sizing: border-box;
                display: flex; flex-direction: column; align-items: center; justify-content: center;
                font-size: {max(8, scaled_page_h_px / 18):.0f}px; color: #444;
                position: relative; text-align: center; line-height: 1.1;">
                {text_block_content_text}
                {column_divider_html if num_columns == 2 else ""}
            </div>
            <div title="Top Margin: {margin_labels_mm['top']:.1f}mm" style="position: absolute; text-align:center; width:{scaled_text_block_w_px:.2f}px; top: {scaled_m_top_px/2 - label_font_size_px/2 -1:.2f}px; left: {scaled_physical_left_margin_px:.2f}px; font-size:{label_font_size_px:.0f}px; color: #36c; overflow:hidden; white-space:nowrap;">{margin_labels_mm['top']:.1f}mm</div>
            <div title="Bottom Margin: {margin_labels_mm['bottom']:.1f}mm" style="position: absolute; text-align:center; width:{scaled_text_block_w_px:.2f}px; bottom: {scaled_m_bottom_px/2 - label_font_size_px/2 -1:.2f}px; left: {scaled_physical_left_margin_px:.2f}px; font-size:{label_font_size_px:.0f}px; color: #36c; overflow:hidden; white-space:nowrap;">{margin_labels_mm['bottom']:.1f}mm</div>
            <div title="Left Margin: {margin_labels_mm['left']:.1f}mm" style="position: absolute; text-align:center; height:{scaled_text_block_h_px:.2f}px; left: {(scaled_physical_left_margin_px/2 - label_font_size_px*1.2/2):.2f}px; top: {scaled_m_top_px:.2f}px; writing-mode: tb-rl; transform: rotate(-180deg); display:flex; align-items:center; justify-content:center; font-size:{label_font_size_px:.0f}px; color: #36c; overflow:hidden; white-space:nowrap;">{margin_labels_mm['left']:.1f}mm</div>
            <div title="Right Margin: {margin_labels_mm['right']:.1f}mm" style="position: absolute; text-align:center; height:{scaled_text_block_h_px:.2f}px; right: {(scaled_physical_right_margin_px/2 - label_font_size_px*1.2/2):.2f}px; top: {scaled_m_top_px:.2f}px; writing-mode: tb-rl; transform: rotate(-180deg); display:flex; align-items:center; justify-content:center; font-size:{label_font_size_px:.0f}px; color: #36c; overflow:hidden; white-space:nowrap;">{margin_labels_mm['right']:.1f}mm</div>
        </div>"""
        return page_html

    def generatePageSpreadVisualization(self, view, page_data, margin_data, layout_options, max_page_height_px=150):
        if not all([page_data, margin_data, layout_options]):
            return "<p><em>Page, margin, or layout option data not available for visualization.</em></p>"
        try:
            page_w_mm = float(page_data['width_mm']); page_h_mm = float(page_data['height_mm'])
            m_top_mm = float(margin_data['top_mm']); m_bottom_mm = float(margin_data['bottom_mm'])
            m_side_mm = float(margin_data['side_margin_mm']); m_gutter_mm = float(margin_data['binding_gutter_mm'])
            num_columns = int(layout_options.get('num_columns', 1))
            binding_dir = layout_options.get('binding_direction', 'LTR').upper()
            apply_gutter_to_outer = bool(layout_options.get('apply_gutter_to_outer_edge', False))
            col_gap_mm = float(layout_options.get('column_gap_mm', 4.0 if num_columns == 2 else 0.0))
        except (ValueError, TypeError, KeyError) as e:
            return f"<p><em>Invalid data for spread visualization: {html.escape(str(e))}</em></p>"

        if page_w_mm <= 0 or page_h_mm <= 0: return "<p><em>Page dimensions must be positive.</em></p>"
        scale = max_page_height_px / page_h_mm
        scaled_page_w = page_w_mm * scale; scaled_page_h = page_h_mm * scale
        scaled_m_top = m_top_mm * scale; scaled_m_bottom = m_bottom_mm * scale
        scaled_col_gap = col_gap_mm * scale
        label_font_size = max(7, min(11, scaled_page_h / 20)) 

        true_inner_mm = m_side_mm + m_gutter_mm if not apply_gutter_to_outer else m_side_mm
        true_outer_mm = m_side_mm if not apply_gutter_to_outer else m_side_mm + m_gutter_mm
        
        page_num_left_visual, page_num_right_visual = ("4", "5") if binding_dir == 'LTR' else ("7", "6")

        left_page_html_content = self.renderSinglePage(view,
            'left', scaled_page_w, scaled_page_h, scaled_m_top, scaled_m_bottom,
            true_outer_mm * scale, true_inner_mm * scale,
            {'top': m_top_mm, 'bottom': m_bottom_mm, 
             'left': true_outer_mm, 
             'right': true_inner_mm},
            page_num_left_visual, num_columns, scaled_col_gap, label_font_size, binding_dir)

        right_page_html_content = self.renderSinglePage(view,
            'right', scaled_page_w, scaled_page_h, scaled_m_top, scaled_m_bottom,
            true_inner_mm * scale, true_outer_mm * scale,
            {'top': m_top_mm, 'bottom': m_bottom_mm, 
             'left': true_inner_mm, 
             'right': true_outer_mm},
            page_num_right_visual, num_columns, scaled_col_gap, label_font_size, binding_dir)
        
        scaled_spine_gap_px = max(2, scaled_page_w / 40) 
        text_block_w_mm_summary = page_w_mm - true_inner_mm - true_outer_mm 
        text_block_h_mm_summary = page_h_mm - m_top_mm - m_bottom_mm
        gutter_desc = "Outer Edge" if apply_gutter_to_outer else "Spine/Inner Edge"

        html_output = f"""
        <div class="page-spread-visualization" style="text-align: center; padding: 10px 5px 5px 5px; margin-top:10px; border: 1px solid #eee; background-color:#f9f9f9;">
            <div class="spread-container" style="display: flex; justify-content: center; align-items: flex-start; gap: {scaled_spine_gap_px:.2f}px;">
                {left_page_html_content}
                {right_page_html_content}
            </div>
        </div>"""
        return html_output.replace("\n", "")

    def get_layout_preview(self, view, scenario_title=None, scenario_order=None):
        """Generates a layout preview spread.
        If scenario_title is provided, it's used as a sub-section name."""
        
        base_section = "2. Layout/ Page Spread Preview"
        section_path = f"{base_section}/{scenario_title}" if scenario_title else base_section
        item_order = 100
        width, height = view.calcPageSize()
        page_data =   {'width_mm': width, 'height_mm': height}
        marginmms, topmarginmms, bottommarginmms, headerposmms, footerposmms, rulerposmms, headerlabel, footerlabel, hfontsizemms = view.getMargins()
        # print(f"{topmarginmms=}\n{bottommarginmms=}\n{headerposmms=}\n{footerposmms=}\n{rulerposmms=}\n{headerlabel=}\n{footerlabel=}\n{hfontsizemms=}")
        gutter = float(view.get("s_pagegutter")) if view.get("c_pagegutter", False) else 0
        # margin_data = {'top_mm': headerlabel, 'bottom_mm': footerlabel,  # To discuss: whether we want to display top of text or top of header
        margin_data = {'top_mm': topmarginmms, 'bottom_mm': bottommarginmms,
                       'side_margin_mm': marginmms, 'binding_gutter_mm': gutter}
        cols = 2 if view.get("c_doublecolumn", False) else 1
        bb = "RTL" if view.get("c_RTLbookBinding", False) else "LTR"
        colgap = float(view.get("s_colgutterfactor", 4))
        outgut = view.get("c_outerGutter", False)
        layout_options = {'num_columns': cols, 'binding_direction': bb, 
                          'column_gap_mm': colgap, 'apply_gutter_to_outer_edge': outgut}
        
        page_layout_summary_parts = []
        if page_data:
            width_html = html.escape(str(page_data.get('width_mm','?')))
            height_html = html.escape(str(page_data.get('height_mm','?')))
            page_layout_summary_parts.append(f"<b>Page Size (per page):</b> {float(width_html):.2f}mm x {float(height_html):.2f}mm")
        else:
            page_layout_summary_parts.append("<b>Page Size:</b> Data not available")

        if margin_data and layout_options: # Need layout_options to describe gutter application
            top_html = html.escape(str(margin_data.get('top_mm','?')))
            bottom_html = html.escape(str(margin_data.get('bottom_mm','?')))
            side_html = html.escape(str(margin_data.get('side_margin_mm','?')))
            gutter_html = html.escape(str(margin_data.get('binding_gutter_mm','?')))
            apply_gutter_to_outer = bool(layout_options.get('apply_gutter_to_outer_edge', False))
            
            try:
                side_val = float(margin_data.get('side_margin_mm',0))
                gutter_val = float(margin_data.get('binding_gutter_mm',0))
                true_inner_mm_val = side_val + gutter_val if not apply_gutter_to_outer else side_val
                true_outer_mm_val = side_val if not apply_gutter_to_outer else side_val + gutter_val
                margin_desc = f"Top: {float(top_html):.1f}, Bottom: {bottom_html}, Side: {side_html}, Gutter: {gutter_html} (Effective Inner: {true_inner_mm_val:.1f}, Effective Outer: {true_outer_mm_val:.1f})"
            except ValueError:
                margin_desc = f"Top: {top_html}, Bottom: {bottom_html}, Side: {side_html}, Gutter: {gutter_html}"
            
            page_layout_summary_parts.append(f"<b>Margins (mm):</b> {margin_desc}")
        else:
            page_layout_summary_parts.append("<b>Margins (mm):</b> Data not available")
        
        visualization_html = ""
        if page_data and margin_data and layout_options:
            try: # This is where to change the size of the visualization
                visualization_html = self.generatePageSpreadVisualization(view, page_data, margin_data, layout_options, max_page_height_px=300)
            except Exception as e:
                logging.error(f"Error during page spread visualization generation: {e}", exc_info=True)
                visualization_html = f"<p style='color:red;'><i>Error generating page layout visualization: {html.escape(str(e))}</i></p>"
        
        full_page_layout_msg = "<br/>".join(page_layout_summary_parts) + visualization_html
        self.add(section_path, full_page_layout_msg, order=item_order, txttype="html")

def test():
    import sys
    outfile = sys.argv[1]
    rep = Report()
    rep.add("Introduction", "Hello World")
    tm = {"project/id": "Test", "config/name": "test"}
    rep.generate_html(outfile, tm)

if __name__ == "__main__":
    test()
