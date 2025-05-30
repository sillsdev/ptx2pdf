
import logging, os
import xml.etree.ElementTree as et

# DEBUG is informational
# INFO is something that could fail, passed
loglabels = ["\u00A0", "\u00A0", "\u2714", "W", "E", "F", "C"]
logcolors = ["white", "lightskyblue", "palegreen", "orange", "orangered", "fuchsia", "Aqua"]

class ReportEntry:
    def __init__(self, msg, severity=logging.DEBUG, order=0):
        self.msg = msg
        self.severity = severity
        self.order = order

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

    def add(self, section, msg, severity=logging.DEBUG, order=0):
        """ section is a hierarchy of sections separated by / in the string """
        self.sections.setdefault(section, []).append(ReportEntry(msg, severity=severity, order=order))

    def generate_html(self, fname, texmodel):
        def gettree(t):
            return et.fromstring("<node>"+t+"</node>")
        doc = et.fromstring(html_template.format(css=os.path.join(os.path.dirname(__file__), "sakura.css"), **texmodel))
        body = doc.find("body")
        lasts = []
        curr = body
        for s, t in sorted(self.sections.items()):
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
                msge = gettree(m.msg)
                msg.text = msge.text
                for c in msge:
                    msg.append(c)
            lasts = nexts
        with open(fname, "w", encoding="utf-8") as outf:
            outf.write(et.tostring(doc, method="html", encoding="unicode"))

    def run_view(self, view):
        self.get_styles(view)
        self.get_layout(view)

    def get_layout(self, view):
        if hasattr(view, 'ufPages') and len(view.ufPages):
            self.add("Layout", f"Underfilled pages <b>({len(view.ufPages)})<\b>: "+ " ".join([str(x) for x in view.ufPages]), severity=logging.WARN)
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
        for s in view.styleEditor.allStyles():
            if s in view.styleEditor.sheet:
                modified.append(s)
            if (f := view.styleEditor.getval(s, 'fontname', None, includebase=True)) is None:
                continue
            results.setdefault(f, []).append(s)
        mainfonts = set()
        for a in ("R", "B", "I", "BI", "ExtraR"):
            f = view.get("bl_font"+a, skipmissing=True)
            if f is not None:
                mainfonts.add(f.name)
                results.setdefault(f.name, [])
        for k, v in sorted(results.items()):
            line = "{}: {}".format("<b>{}</b>".format(k) if k in mainfonts or any(m in mrkrset for m in v) else k,
                                   " ".join(["<b>{}</b>".format(m) if m in mrkrset else m for m in sorted(v)]))
            self.add("Fonts/Usage", line)
        self.add("USFM", "Markers used: "+" ".join(sorted(mrkrset)))
        self.add("USFM", "Modified markers: " + " ".join(sorted(modified)))

def test():
    import sys
    outfile = sys.argv[1]
    rep = Report()
    rep.add("Introduction", "Hello World")
    tm = {"project/id": "Test", "config/name": "test"}
    rep.generate_html(outfile, tm)

if __name__ == "__main__":
    test()
