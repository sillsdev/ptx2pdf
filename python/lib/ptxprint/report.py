import html # Added for html.escape
import logging, os
import xml.etree.ElementTree as et

# DEBUG is informational
# INFO is something that could fail, passed
loglabels = ["\u00A0", "\u00A0", "\u2714", "W", "E", "F", "C"]
logcolors = ["white", "lightskyblue", "palegreen", "orange", "orangered", "fuchsia", "Aqua"]

_rtlScripts = {
    "Arab",  # Arabic
    "Armi",  # Imperial Aramaic
    "Avst",  # Avestan
    "Hebr",  # Hebrew
    "Mand",  # Mandaic, Mandaean
    "Mani",  # Manichaean
    "Nkoo",  # N’Ko
    "Phli",  # Inscriptional Pahlavi
    "Phlp",  # Psalter Pahlavi
    "Phnx",  # Phoenician
    "Prti",  # Inscriptional Parthian
    "Samr",  # Samaritan
    "Sarb",  # Old South Arabian
    "Sogd",  # Sogdian
    "Sogo",  # Old Sogdian
    "Syrc",  # Syriac
    "Thaa",  # Thaana
    "Yezi"   # Yezidi
}
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
    <link rel="stylesheet" href="{css}/sakura.css" type="text/css" />
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
        # for s, t in sorted(self.sections.items()):
        for s, t in self.sections.items():
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
        self.get_usfms(view)
        self.get_general_info(view)
        self.get_files(view)

    def get_layout(self, view):
        if hasattr(view, 'ufPages') and len(view.ufPages):
            self.add("Layout", f"Underfilled pages <b>({len(view.ufPages)})</b>: "+ " ".join([str(x) for x in view.ufPages]), severity=logging.WARN)
        textheight, linespacing = view.calcBodyHeight()
        lines = textheight / linespacing
        if abs(lines - int(lines + 0.5)) > 0.05:
            self.add("Layout", f"Lines on page (suboptimal): {lines:.1f}", severity=logging.WARN)
        else:
            self.add("Layout", f"Lines on page (optimized): {int(lines + 0.5)}", severity=logging.INFO)

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
        for a in ("R", "B", "I", "BI", "ExtraR"): # To do: flag the (fallback) font
            f = view.get("bl_font"+a, skipmissing=True)
            if f is not None:
                mainfonts.add(f.name)
                results.setdefault(f.name, [])
        for k, v in sorted(results.items()):
            line = "{}: {}".format("<b>{}</b>".format(k) if k in mainfonts or any(m in mrkrset for m in v) else k,
                                   " ".join(["<b>{}</b>".format(m) if m in mrkrset else m for m in sorted(v)]))
            self.add("Fonts/Usage", line, txttype="html")
        self.add("USFM", "Markers used: "+" ".join(sorted(mrkrset)), txttype="text")
        self.add("USFM", "Modified markers: " + " ".join(modified), txttype="html")

    def get_files(self, view):
        for a in (("changes.txt", "c_usePrintDraftChanges"),
                  ("ptxprint-mods.tex", "c_useModsTex")):
            if view.get(a[1]):
                f = os.path.join(view.project.srcPath(view.cfgid), a[0])
                if not os.path.exists(f):
                    continue
                with open(f, encoding="utf-8") as inf:
                    data = inf.read()
                self.add("Files/"+a[0], data, severity=logging.NOTSET, txttype="pretext")

    def get_usfms(self, view):
        usfms = view.get_usfms()
        passed = []
        # self.add("USFMs", f"Books in Publication: {' '.join(view.getBooks())}", severity=logging.INFO)
        for bk in view.getBooks():
            doc = usfms.get(bk)
            if doc is None:
                self.add("USFMs", f"No USFM for {bk}", severity=logging.WARN)
                continue
            if self.get_usfm(view, doc, bk):
                if bk != "ISA":        # for testing only - remove this line later
                    passed.append(bk)  # for testing only - fix indentation
        if len(passed):
            self.add("USFM Checks", f"Books passed: {' '.join(passed)}", severity=logging.INFO)
        if len(passed) != len(view.getBooks()):
            self.add("USFM Checks", f"Books <b>failed</b>: {' '.join(set(view.getBooks()) - set(passed))}", severity=logging.WARN)
        if "GLO" in view.getBooks():
            fltr = "Filtered" if view.get("c_filterGlossary", False) else "Unfiltered"
            asfn = "As Footnotes" if view.get("c_glossaryFootnotes", False) else ""
            self.add("Peripheral Components", f"Glossary: {fltr} {asfn}", severity=logging.DEBUG)

    def get_usfm(self, view, doc, bk):
        r = doc.getroot()
        essentials = "h toc1 toc2 toc3 p".split() # How do we check for other non-para USFM's?  c v etc.
        missing = [a for a in essentials if r.find(f'.//para[@style="{a}"]') is None]
        if len(missing):
            self.add("USFMs", f'{bk} is missing the following essential markers: {" ".join(missing)}', severity=logging.ERROR)
            return False
        return True

        def myhackylambda(view, widget):
            return ("", logging.DEBUG)

    def get_general_info(self, view):
        widget_map = {
            "Project Name":               ("Project/Overview", "l_projectFullName", 100, \
                                            lambda v,w: (v.get("l_projectFullName", ""), logging.DEBUG)),
            "Copyright":                  ("Project/Overview", "t_copyrightStatement", 80, \
                                            lambda v,w: (v.get("t_copyrightStatement", ""), logging.DEBUG)),
            "License":                    ("Project/Overview", "ecb_licenseText", 60, \
                                            lambda v,w: (v.get("ecb_licenseText", ""), logging.DEBUG)),
                                                         
            "Diglot Configuration":       ("Diglot/Setup", "c_diglot", 0, None), # More details to be added for this
            "Page Size":                  ("Layout", "ecb_pagesize", 0, None),
            "Two Column Layout":          ("Layout", "c_doublecolumn", 0, None),
            "Mirrored Headers":           ("Layout", "c_mirrorpages", 0, None),
            "Decorative Border":          ("Layout", "c_inclPageBorder", 0, \
                                            lambda v,w: (v.get("r_border").upper() if v.get("c_useOrnaments", False) else "ON, but Ornamental Decorations are <b>Off</b>", \
                                            logging.DEBUG if v.get("c_useOrnaments", False) else logging.WARN)),
            "Ornamental Features":        ("Layout", "c_useOrnaments", 0, None),
            "Thumb Tabs":                 ("Layout", "c_thumbtabs", 0, None),
            "Interlinear":                ("Writing System", "c_interlinear", 0, \
                                            lambda v,w: ("Language Code: " + (v.get("t_interlinearLang") or "<b>Missing!</b>"), \
                                            logging.WARN if len(v.get("t_interlinearLang")) != 2 else logging.DEBUG)),
            "Study Bible/Extended Notes": ("Notes and Refs", "c_extendedFnotes", 0, None), # how to count how many there are?
            "Footnotes":                  ("Notes and Refs", "c_includeFootnotes", 0, None),
            "Cross-References":           ("Notes and Refs", "c_includeXrefs", 0, None),
            "Cross-Refs (other)":         ("Notes and Refs", "c_useXrefList", 0, \
                                            lambda v,w: ("External List: " + (v.get("fcb_xRefExtListSource") or "<b>Unknown!</b>"), logging.DEBUG)),
            "Pictures Enabled":           ("Illustrations", "c_includeillustrations", 0, None),
            "Missing Images":             ("Illustrations", "l_missingPictureString", 0, \
                                            lambda v,w: (v.get("l_missingPictureString", "")[18:], logging.WARN)),
            "Only Placeholders":          ("Illustrations", "c_figplaceholders", 0, \
                                            lambda v,w: ("", logging.WARN if v.get(w, False) else logging.DEBUG)),
            "PDF Version PDF/X-1a":       ("Output Format", "c_printArchive", 100, None),
            "Crop Marks":                 ("Output Format", "c_cropmarks", 200, None),
            "Watermark":                  ("Output Format", "c_applyWatermark", 50, \
                                            lambda v,w: (v.get("lb"+w[1:], "").strip("."), logging.DEBUG)),
            "Booklet Pagination":         ("Output Format", "fcb_pagesPerSpread", 30, \
                                            lambda v,w: (v.get(w, "")+"-up", logging.DEBUG)),
            "Front Matter PDF(s)":        ("Peripheral Components", "c_inclFrontMatter", 0, \
                                            lambda v,w: (v.get("lb"+w[1:], "").strip("."), logging.DEBUG)),
            "Table of Contents":          ("Peripheral Components", "c_autoToC", 0, None),
            "Thumb Tabs":                 ("Peripheral Components", "c_thumbtabs", 0, None),
            "Front Matter":               ("Peripheral Components", "c_frontmatter", 0, \
                                            lambda v,w: ("", logging.WARN if v.get(w, False) and v.get("c_colophon", False) else logging.DEBUG)),
            "Colophon":                   ("Peripheral Components", "c_colophon", 0, \
                                            lambda v,w: ("", logging.WARN if v.get(w, False) and v.get("c_frontmatter", False) else logging.DEBUG)),
            "Back Matter PDF(s)":         ("Peripheral Components", "c_inclBackMatter", 0, \
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
            self.add(section, f"{title}{extra}", severity=severity, order=order, txttype="html")

    def get_writingSystems(self, view):  # to do: use the actual script name from a _allscripts lookup instead of just the code
        s = view.get("fcb_script") or "Zyyy"
        s = "Default/Unknown" if s == "Zyyy" else s
        self.add("Writing System", f"Script Code: {s}", severity=logging.WARN if len(s) > 4 else logging.DEBUG, order=100, txttype="html")

        d = (view.get("fcb_textDirection") or "ltr").upper()
        rtl = s in _rtlScripts
        sev = logging.WARN if (d == "RTL" and not rtl) or (d == "LTR" and rtl) or (d == "TTB" and s != "Mong") else logging.DEBUG
        suffix = " - <b>unexpected!</b>" if sev == logging.WARN else ""
        self.add("Writing System", f"Text Direction: {d}{suffix}", severity=sev, txttype="html")
        
        bb = view.get("c_RTLbookBinding", False)
        sev = logging.WARN  if (bb and d != "RTL" and not rtl) or (not bb and (d == "RTL" or rtl)) else logging.DEBUG
        if bb or sev == logging.WARN:
            suffix = " - <b>unexpected!</b>" if sev == logging.WARN else ""
            self.add("Writing System", f"RTL Book Binding: {bb}{suffix}", severity=sev, txttype="html")
            
        # to do: add other Additional Script Settings (snippet settings for the script)
        #    and also Specific Line Break Locale (flagging an issue if we have unexpected values there for CJK languages)

def test():
    import sys
    outfile = sys.argv[1]
    rep = Report()
    rep.add("Introduction", "Hello World")
    tm = {"project/id": "Test", "config/name": "test"}
    rep.generate_html(outfile, tm)

if __name__ == "__main__":
    test()
