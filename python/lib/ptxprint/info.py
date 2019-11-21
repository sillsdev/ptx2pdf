import configparser, re, os
import regex
from ptxprint.font import TTFont
from ptxprint.ptsettings import chaps, books, oneChbooks
from ptxprint.snippets import FancyIntro

class Info:
    _mappings = {
        "project/id":               (None, lambda w,v: w.get("cb_project")),
        "project/hideadvsettings":  ("c_hideAdvancedSettings", lambda w,v: "true" if v else "false"),
        "project/keeptempfiles":    ("c_keepTemporaryFiles", lambda w,v: "true" if v else "false"),
        "project/useptmacros":      ("c_usePTmacros", lambda w,v: "true" if v else "false"),
        "project/ifuseptmacros":    ("c_usePTmacros", lambda w,v: "%" if v else ""),
        "project/multiplebooks":    ("c_multiplebooks", lambda w,v: "true" if v else "false"),
        "project/combinebooks":     ("c_combine", lambda w,v: "true" if v else "false"),
        "project/book":             ("cb_book", None),
        "project/booklist":         ("t_booklist", lambda w,v: v or ""),
        "project/ifinclfrontpdf":   ("c_inclFrontMatter", lambda w,v: "true" if v else "false"),
        "project/frontincludes":    ("btn_selectFrontPDFs", lambda w,v: "\n".join('\\includepdf{{"{}"}}'.format(re.sub(r"\\","/", s)) for s in w.FrontPDFs) if (w.FrontPDFs is not None and w.FrontPDFs != 'None') else ""),
        "project/ifinclbackpdf":    ("c_inclBackMatter", lambda w,v: "true" if v else "false"),
        "project/backincludes":     ("btn_selectBackPDFs", lambda w,v: "\n".join('\\includepdf{{"{}"}}'.format(re.sub(r"\\","/", s)) for s in w.BackPDFs) if (w.BackPDFs is not None and w.BackPDFs != 'None') else ""),
        "project/useprintdraftfolder": ("c_useprintdraftfolder", lambda w,v :"true" if v else "false"),
        "project/processscript":    ("c_processScript", lambda w,v :"true" if v else "false"),
        "project/runscriptafter":   ("c_processScriptAfter", lambda w,v :"true" if v else "false"),
        "project/selectscript":     ("btn_selectScript", lambda w,v: re.sub(r"\\","/", w.CustomScript) if w.CustomScript is not None else ""),
        "project/usechangesfile":   ("c_usePrintDraftChanges", lambda w,v :"true" if v else "false"),
        "project/ifusemodstex":     ("c_useModsTex", lambda w,v: "" if v else "%"),
        "project/ifusemodssty":     ("c_useModsSty", lambda w,v: "" if v else "%"),
        "project/ifusenested":      (None, lambda w,v: "" if (w.get("c_omitallverses") or not w.get("c_includeFootnotes") or not w.get("c_includeXrefs")) or w.get("c_prettyIntroOutline") else "%"),
        "project/ifstarthalfpage":  ("c_startOnHalfPage", lambda w,v :"true" if v else "false"),
        "project/randompicposn":    ("c_randomPicPosn", lambda w,v :"true" if v else "false"),

        "paper/height":             (None, lambda w,v: re.sub(r"^.*?,\s*(.+?)\s*(?:\(.*|$)", r"\1", w.get("cb_pagesize")) or "210mm"),
        "paper/width":              (None, lambda w,v: re.sub(r"^(.*?)\s*,.*$", r"\1", w.get("cb_pagesize")) or "148mm"),
        "paper/pagesize":           ("cb_pagesize", None),
        "paper/ifwatermark":        ("c_applyWatermark", lambda w,v: "" if v else "%"),
        "paper/watermarkpdf":       ("btn_selectWatermarkPDF", lambda w,v: re.sub(r"\\","/", w.watermarks) if (w.watermarks is not None and w.watermarks != 'None') else "A5-Draft.pdf"),
        "paper/ifcropmarks":        ("c_cropmarks", lambda w,v :"true" if v else "false"),  
        "paper/ifverticalrule":     ("c_verticalrule", lambda w,v :"true" if v else "false"),
        "paper/margins":            ("s_margins", lambda w,v: round(v) or "14"),
        "paper/topmarginfactor":    ("s_topmarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/bottommarginfactor": ("s_bottommarginfactor", lambda w,v: round(v, 2) or "1.15"),
        "paper/sidemarginfactor":   ("s_sidemarginfactor", lambda w,v: round(v, 2) or "1.00"),
        "paper/ifaddgutter":        ("c_pagegutter", lambda w,v :"true" if v else "false"),
        "paper/gutter":             ("s_pagegutter", lambda w,v: round(v) or "14"),
        "paper/columns":            ("c_doublecolumn", lambda w,v: "2" if v else "1"),
        "paper/fontfactor":         ("s_fontsize", lambda w,v: round((v / 12), 3) or "1.000"),

        "paragraph/varlinespacing": ("c_variableLineSpacing", lambda w,v: "" if v else "%"),
        "paragraph/linespacing":    ("s_linespacing", lambda w,v: "{:.3f}".format(v) or "15.000"),
        "paragraph/linemin": ("s_linespacingmin", lambda w,v: "minus {:.3f}pt".format(w.get("s_linespacing") - v) if v < w.get("s_linespacing") else ""),
        "paragraph/linemax": ("s_linespacingmax", lambda w,v: "plus {:.3f}pt".format(v - w.get("s_linespacing")) if v > w.get("s_linespacing") else ""),
        "paragraph/ifjustify":       ("c_justify", lambda w,v: "true" if v else "false"),
        "paragraph/ifhyphenate":     ("c_hyphenate", lambda w,v: "true" if v else "false"),

        "document/toc":             ("c_autoToC", lambda w,v: "" if v else "%"),
        "document/toctitle":        ("t_tocTitle", lambda w,v: v or ""),
        "document/usetoc1":         ("c_usetoc1", lambda w,v :"true" if v else "false"),
        "document/usetoc2":         ("c_usetoc2", lambda w,v :"true" if v else "false"),
        "document/usetoc3":         ("c_usetoc3", lambda w,v :"true" if v else "false"),
        "document/chapfrom":        ("cb_chapfrom", lambda w,v: w.builder.get_object("cb_chapfrom").get_active_id()),
        "document/chapto":          ("cb_chapto", lambda w,v: w.builder.get_object("cb_chapto").get_active_id()),
        "document/colgutterfactor": ("s_colgutterfactor", lambda w,v: round(v) or "15"),
        "document/ifrtl":           ("c_rtl", lambda w,v :"true" if v else "false"),
        "document/iflinebreakon":   ("c_linebreakon", lambda w,v: "" if v else "%"),
        "document/linebreaklocale": ("t_linebreaklocale", lambda w,v: v or ""),
        "document/script":          ("cb_script", lambda w,v: ";script="+w.builder.get_object('cb_script').get_active_id().lower() if w.builder.get_object('cb_script').get_active_id() != "Zyyy" else ""),
        "document/digitmapping":    ("cb_digits", lambda w,v: ";mapping="+v.lower()+"digits" if v != "Default" else ""),
        "document/ch1pagebreak":    ("c_ch1pagebreak", lambda w,v: "true" if v else "false"),
        "document/marginalverses":  ("c_marginalverses", lambda w,v: "" if v else "%"),
        "document/ifomitchapternum":   ("c_omitchapternumber", lambda w,v: "true" if v else "false"),
        "document/ifomitallchapters":  ("c_omitchapternumber", lambda w,v: "" if v else "%"),
        "document/ifomitsinglechnum":  ("c_omitChap1ChBooks", lambda w,v: "true" if v else "false"),
        "document/ifomitverseone":  ("c_omitverseone", lambda w,v: "true" if v else "false"),
        "document/ifomitallverses": ("c_omitallverses", lambda w,v: "" if v else "%"),
        "document/ifmainbodytext":  ("c_mainBodyText", lambda w,v: "true" if v else "false"),
        "document/glueredupwords":  ("c_glueredupwords", lambda w,v :"true" if v else "false"),
        "document/ifinclfigs":      ("c_includeillustrations", lambda w,v :"true" if v else "false"),
        "document/iffigfrmtext":    ("c_includefigsfromtext", lambda w,v :"true" if v else "false"),
        "document/iffigexclwebapp": ("c_figexclwebapp", lambda w,v: "true" if v else "false"),
        "document/iffigskipmissing": ("c_skipmissingimages", lambda w,v: "true" if v else "false"),
        "document/iffigplaceholders": ("c_figplaceholders", lambda w,v :"true" if v else "false"),
        "document/iffighiderefs":   ("c_fighiderefs", lambda w,v :"true" if v else "false"),
        "document/usefigsfolder":   ("c_useFiguresFolder", lambda w,v :"" if v else "%"),
        "document/uselocalfigs":    ("c_useLocalFiguresFolder", lambda w,v :"" if v else "%"),
        "document/customfiglocn":   ("c_useCustomFolder", lambda w,v :"" if v else "%"),
        "document/customfigfolder": ("btn_selectFigureFolder", lambda w,v: re.sub(r"\\","/", w.customFigFolder) if w.customFigFolder is not None else ""),
        "document/ifusepiclist":    ("c_usePicList", lambda w,v :"" if v else "%"),
        "document/spacecntxtlztn":  ("cb_spaceCntxtlztn", lambda w,v: "0" if v == "None" else "1" if v == "Some" else "2"),
        "document/glossarymarkupstyle":  ("cb_glossaryMarkupStyle", lambda w,v: w.builder.get_object("cb_glossaryMarkupStyle").get_active_id()),
        "document/hangpoetry":      ("c_hangpoetry", lambda w,v: "" if v else "%"),
        "document/preventorphans":  ("c_preventorphans", lambda w,v: "true" if v else "false"),
        "document/preventwidows":   ("c_preventwidows", lambda w,v: "true" if v else "false"),
        "document/supresssectheads": ("c_omitSectHeads", lambda w,v: "true" if v else "false"),
        "document/supressparallels": ("c_omitParallelRefs", lambda w,v: "true" if v else "false"),
        "document/supressbookintro": ("c_omitBookIntro", lambda w,v: "true" if v else "false"),
        "document/supressintrooutline": ("c_omitIntroOutline", lambda w,v: "true" if v else "false"),
        "document/supressindent":   ("c_omit1paraIndent", lambda w,v: "false" if v else "true"),

        "header/headerposition":    ("s_headerposition", lambda w,v: round(v, 2) or "0.50"),
        "header/footerposition":    ("s_footerposition", lambda w,v: round(v, 2) or "0.50"),
        "header/ifomitrhchapnum":   ("c_omitrhchapnum", lambda w,v :"true" if v else "false"),
        "header/ifverses":          ("c_hdrverses", lambda w,v :"true" if v else "false"),
        "header/ifrhrule":          ("c_rhrule", lambda w,v: "" if v else "%"),
        "header/ruleposition":      ("s_rhruleposition", lambda w,v: v or "10"),
        "header/hdrleftinner":      ("cb_hdrleft", lambda w,v: v or "-empty-"),
        "header/hdrcenter":         ("cb_hdrcenter", lambda w,v: v or "-empty-"),
        "header/hdrrightouter":     ("cb_hdrright", lambda w,v: v or "-empty-"),
        "header/mirrorlayout":      ("c_mirrorpages", lambda w,v: "true" if v else "false"),
        
        "footer/includefooter":     ("c_runningFooter", lambda w,v :"true" if v else "false"),
        "footer/ftrcenter":         ("t_runningFooter", lambda w,v: v if w.get("c_runningFooter") else ""),

        "notes/iffootnoterule":     ("c_footnoterule", lambda w,v: "%" if v else ""),
        "notes/ifblendfnxr":        ("c_blendfnxr", lambda w,v :"true" if v else "false"),
        "notes/blendedxrmkr":       ("cb_blendedXrefCaller", lambda w,v: w.builder.get_object("cb_blendedXrefCaller").get_active_id()),

        "notes/includefootnotes":   ("c_includeFootnotes", lambda w,v: "%" if v else ""),
        "notes/iffnautocallers":    ("c_fnautocallers", lambda w,v :"true" if v else "false"),
        "notes/fncallers":          ("t_fncallers", lambda w,v: v if w.get("c_fnautocallers") else ""),
        "notes/fnresetcallers":     ("c_fnpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/fnomitcaller":       ("c_fnomitcaller", lambda w,v: "%" if v else ""),
        "notes/fnparagraphednotes": ("c_fnparagraphednotes", lambda w,v: "" if v else "%"),

        "notes/includexrefs":       ("c_includeXrefs", lambda w,v: "%" if v else ""),
        "notes/ifxrautocallers":    ("c_xrautocallers", lambda w,v :"true" if v else "false"),
        "notes/xrcallers":          ("t_xrcallers", lambda w,v: v if w.get("c_xrautocallers") else ""),
        "notes/xrresetcallers":     ("c_xrpageresetcallers", lambda w,v: "" if v else "%"),
        "notes/xromitcaller":       ("c_xromitcaller", lambda w,v: "%" if v else ""),
        "notes/xrparagraphednotes": ("c_paragraphedxrefs", lambda w,v: "" if v else "%"),

        "fontbold/fakeit":          ("c_fakebold", lambda w,v :"true" if v else "false"),
        "fontitalic/fakeit":        ("c_fakeitalic", lambda w,v :"true" if v else "false"),
        "fontbolditalic/fakeit":    ("c_fakebolditalic", lambda w,v :"true" if v else "false"),
        "fontbold/embolden":        ("s_boldembolden", lambda w,v: ";embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebold") else ""),
        "fontitalic/embolden":      ("s_italicembolden", lambda w,v: ";embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakeitalic") else ""),
        "fontbolditalic/embolden":  ("s_bolditalicembolden", lambda w,v: ";embolden={:.2f}".format(v) if v != 0.00 and w.get("c_fakebolditalic") else ""),
        "fontbold/slant":           ("s_boldslant", lambda w,v: ";slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebold") else ""),
        "fontitalic/slant":         ("s_italicslant", lambda w,v: ";slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakeitalic") else ""),
        "fontbolditalic/slant":     ("s_bolditalicslant", lambda w,v: ";slant={:.4f}".format(v) if v != 0.0000 and w.get("c_fakebolditalic") else ""),
    }
    _fonts = {
        "fontregular/name": "f_body",
        "fontbold/name": "f_bold",
        "fontitalic/name": "f_italic",
        "fontbolditalic/name": "f_bolditalic"
    }
    _hdrmappings = {
        "First Reference":  r"\firstref",
        "Last Reference":   r"\lastref",
        "Page Number":      r"\pagenumber",
        "Reference Range":  r"\rangeref",
        "-empty-":          r"\empty"
    }
    _settingmappings = {
        "notes/xrcallers": "crossrefs",
        "notes/fncallers": "footnotes"
    }
    _glossarymarkup = {
        "None":                    r"\1",
        "format as bold":          r"\\bd \1\\bd*",
        "format as italics":       r"\\it \1\\it*",
        "format as bold italics":  r"\\bdit \1\\bdit*",
        "format with emphasis":    r"\\em \1\\em*",
        "with ⸤floor⸥ brackets":   r"\u2E24\1\u2E25", # Question for MH - using this option makes it crash with an encoding issue. Help!
        "star *before word":       r"*\1",
        "star after* word":        r"\1*",
        "circumflex ^before word": r"^\1",
        "circumflex after^ word":  r"\1^"
    }
    _snippets = {
        "snippets/fancyintro": ("c_prettyIntroOutline", FancyIntro)
    }
    
    def __init__(self, printer, path, prjid = None):
        print("  info: __init__",self, printer, path)
        self.printer = printer
        self.changes = None
        self.localChanges = None
        self.dict = {"/ptxpath": path}
        self.prjid = prjid
        self.update()

    def update(self):
        print("  info: update",self)
        printer = self.printer
        for k, v in self._mappings.items():
            val = printer.get(v[0]) if v[0] is not None else None
            if v[1] is not None:
                self.dict[k] = v[1](printer, val)
        if self.prjid is not None:
            self.dict['project/id'] = self.prjid
        self.processFonts(printer)
        self.processHdrFtr(printer)
        self.makelocalChanges(printer)

    def __getitem__(self, key):
        print("  info: __getitem__",self, key)
        return self.dict[key]

    def __setitem__(self, key, value):
        print("  info: __setitem__",self, key, value)
        self.dict[key] = value

    def processFonts(self, printer):
        print("  info: processFonts",self, printer)
        # \def\regular{"Gentium Plus/GR:litr=1;ital=1"}   ???
        silns = "{urn://www.sil.org/ldml/0.1}"
        for p, wid in self._fonts.items():
            f = TTFont(printer.get(wid))
            d = self.printer.ptsettings.ldml.find('.//special/{1}external-resources/{1}font[@name="{0}"]'.format(f.family, silns))
            if d is not None:
                f.features = {}
                for l in d.get('features', '').split(','):
                    if '=' in l:
                        k, v = l.split('=')
                        f.features[k.strip()] = v.strip()
                self.dict['font/features'] = ";".join("{0}={1}".format(f.feats.get(fid, fid),
                                                    f.featvals.get(fid, {}).get(int(v), v)) for fid, v in f.features.items()) + \
                                             (";" if len(f.features) else "")
            else:
                self.dict['font/features'] = ""
            if 'Silf' in f:
                engine = "/GR"
            else:
                engine = ""
            s = ""
            if len(f.style):
                s = "/" + "".join(x[0].upper() for x in f.style.split(" "))
            self.dict[p] = f.family + engine + s

    def processHdrFtr(self, printer):
        print("  info: processHdrFtr",self, printer)
        mirror = printer.get('c_mirrorpages')
        for side in ('left', 'center', 'right'):
            v = printer.get("cb_hdr" + side)
            t = self._hdrmappings.get(v, v)
            if side == 'left':
                if mirror:
                    self.dict['header/even{}'.format('right')] = t
                else:
                    self.dict['header/even{}'.format(side)] = t
            elif side == 'right':
                if mirror:
                    self.dict['header/even{}'.format('left')] = t
                else:
                    self.dict['header/even{}'.format(side)] = t
            else: # centre
                self.dict['header/even{}'.format(side)] = t
            
            self.dict['header/odd{}'.format(side)] = t

    def texfix(self, path):
        return path.replace(" ", r"\ ")

    def asTex(self, template="template.tex", filedir="."):
        print("  info: asTex",self, "template.tex", "filedir=.")
 #       import pdb;pdb.set_trace()
        for k, v in self._settingmappings.items():
            if self.dict[k] == "":
                self.dict[k] = self.printer.ptsettings.dict.get(v, "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z")
        res = []
        with open(os.path.join(os.path.dirname(__file__), template), encoding="utf-8") as inf:
            for l in inf.readlines():
                if l.startswith(r"\ptxfile"):
                    res.append("\\PtxFilePath={"+filedir.replace("\\","/")+"/}\n")
                    le = len(self.dict['project/books'])
                    for i, f in enumerate(self.dict['project/books']):
                        if self.dict['document/ifomitsinglechnum'] and f[2:5] in oneChbooks:
                            res.append("\\OmitChapterNumbertrue\n")
                            res.append("\\ptxfile{{{}}}\n".format(f))
                            res.append("\\OmitChapterNumberfalse\n")
                        else:
                            res.append("\\ptxfile{{{}}}\n".format(f))
                elif l.startswith(r"%\snippets"):
                    for k, c in self._snippets.items():
                        v = self.printer.get(c[0])
                        if v:
                            res.append(c[1].texCode)
                else:
                    res.append(l.format(**self.dict))
        return "".join(res).replace("\OmitChapterNumberfalse\n\OmitChapterNumbertrue\n","")

    def convertBook(self, bk, outdir, prjdir):
        print("  info: convertBook",self, bk, outdir, prjdir)
        if self.changes is None and self.dict['project/usechangesfile'] == "true":
            self.changes = self.readChanges(os.path.join(prjdir, 'PrintDraftChanges.txt'))
        else:
            self.changes = []
        customsty = os.path.join(prjdir, 'custom.sty')
        if not os.path.exists(customsty):
            open(customsty, "w").close()
        fbkfm = self.printer.ptsettings['FileNameBookNameForm']
        bknamefmt = fbkfm.replace("MAT","{bkid}").replace("41","{bknum:02d}") + \
                    self.printer.ptsettings['FileNamePostPart']
        fname = bknamefmt.format(bkid=bk, bknum=books.get(bk, 0))
        infname = os.path.join(prjdir, fname)
        if self.changes is not None or self.localChanges is not None:
            outfname = fname
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:]
            outfpath = os.path.join(outdir, outfname)
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                for c in self.changes + self.localChanges:
                    if c[0] is None:
                        dat = c[1].sub(c[2], dat)
                    else:
                        newdat = [c[0].split(dat)]
                        for i in range(1, len(newdat), 2):
                            newdat[i] = c[  1].sub(c[2], newdat[i])
                        dat = "".join(newdat)
            with open(outfpath, "w", encoding="utf-8") as outf:
                outf.write(dat)
            return outfname
        else:
            return fname

    def readChanges(self, fname):
        print("  info: readChanges",self, fname)
        changes = []
        if not os.path.exists(fname):
            return []
        with open(fname, "r", encoding="utf-8") as inf:
            for l in inf.readlines():
                l = l.strip().replace(u"\uFEFF", "")
                l = re.sub(r"\s*#.*$", "", l)
                if not len(l):
                    continue
                if l.startswith("in"):
                    # in "\\w .+?\\w\*": "\|.+?\\w\*" > "\w*"
                    print("WARNING: 'in x: change y to z' rule encountered in PrintDraftChanges has been ignored.")
                    continue
                m = re.match(r"^(['\"])(.*?)(?<!\\)\1\s*>\s*(['\"])(.*?)(?<!\\)\3", l)
                if m:
                    changes.append((None, regex.compile(m.group(2), flags=regex.M), m.group(4)))
                    continue
                m = re.match(r"^in\s+(['\"])(.*?)(?<!\\)\1\s*:\s*(['\"])(.*?)(?<!\\)\3\s*>\s*(['\"])(.*?)(?<!\\)\5", l)
                if m:
                    changes.append((regex.compile("("+m.group(2)+")", flags=regex.M), regex.compile(m.group(4), flags=regex.M), m.group(6)))
        if not len(changes):
            return None
        return changes

    def makelocalChanges(self, printer):
        print("  info: makelocalChanges",self, printer)
        self.localChanges = []
        first = int(printer.get("cb_chapfrom"))
        last = int(printer.get("cb_chapto"))
        
        # This section handles PARTIAL books (from chapter X to chapter Y)
        if not printer.get("c_multiplebooks"):
            bk = printer.get("cb_book")
            if first > 1:
                self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+(?=\\c {} ?\r?\n)".format(first), flags=regex.S), ""))
            if last < int(chaps.get(bk)):
                self.localChanges.append((None, regex.compile(r"\\c {} ?\r?\n.+".format(last+1), flags=regex.S), ""))
            
        # Glossary Word markup: Remove the second half of the \w word|glossary-form\w* and apply chosen glossary markup
        v = printer.get("cb_glossaryMarkupStyle")
        gloStyle = self._glossarymarkup.get(v, v)
        self.localChanges.append((None, regex.compile(r"\\w (.+?)(\|.+?)?\\w\*", flags=regex.M), gloStyle))

        if printer.get("c_includeillustrations") and printer.get("c_includefigsfromtext"):
            self.localChanges.append((None, regex.compile(r"\.[Tt][Ii][Ff]\|", flags=regex.M), r".jpg|"))           # Rename all TIF extensions to JPGs
            if printer.get("c_skipmissingimages"):
                msngfigs = self.ListMissingPics(printer)
                if len(msngfigs):
                    for f in msngfigs:
                        print("Skipping over missing illustration: ",f)
                        self.localChanges.append((None, regex.compile(r"\\fig .*\|{}\|.+?\\fig\*".format(f), flags=regex.M), ""))
            if printer.get("c_fighiderefs"):
                self.localChanges.append((None, regex.compile(r"(\\fig .*?)(\d+\:\d+([-,]\d+)?)(.*?\\fig\*)", flags=regex.M), r"\1\4")) # del ch:vs from caption
        else:
            self.localChanges.append((None, regex.compile(r"\\fig .*?\\fig\*", flags=regex.M), ""))             # Drop ALL Figures
        
        if printer.get("c_omitBookIntro"):
            self.localChanges.append((None, regex.compile(r"\\i(s|m|mi|p|pi|li\d?|pq|mq|pr|b|q\d?) .+?\r?\n", flags=regex.M), "")) # Drop Introductory matter

        if printer.get("c_omitIntroOutline"):
            self.localChanges.append((None, regex.compile(r"\\(iot|io\d) [^\\]+", flags=regex.M), ""))          # Drop ALL Intro Outline matter
            self.localChanges.append((None, regex.compile(r"\\ior .+?\\ior\*\s?\r?\n", flags=regex.M), ""))     # and remove Intro Outline References

        if printer.get("c_omitSectHeads"):
            self.localChanges.append((None, regex.compile(r"\\s .+", flags=regex.M), ""))                       # Drop ALL Section Headings

        if printer.get("c_omitParallelRefs"):
            self.localChanges.append((None, regex.compile(r"\\r .+", flags=regex.M), ""))                       # Drop ALL Parallel Passage References

        if printer.get("c_blendfnxr"): 
            XrefCaller = printer.get("cb_blendedXrefCaller")
            # To merge/blend \f and \x together, simply change all (\x to \f) (\xo to \fr) (\xq to \fq) (\xt to \ft) and (\f* to \x*)
            self.localChanges.append((None, regex.compile(r"\\x . ", flags=regex.M), r"\\f {} ".format(XrefCaller)))
            self.localChanges.append((None, regex.compile(r"\\x\* ", flags=regex.M), r"\\f* "))
            self.localChanges.append((None, regex.compile(r"\\xq ", flags=regex.M), r"\\fq "))
            self.localChanges.append((None, regex.compile(r"\\xt ", flags=regex.M), r"\\ft "))

        if printer.get("c_preventorphans"): 
            # Keep final two words of \q lines together [but this doesn't work if there is an \f or \x at the end of the line] 
            self.localChanges.append((None, regex.compile(r"(\\q\d?(\s?\r?\n?\\v)?( \S+)+( (?!\\)\S+)) (\S+\s*\n)", flags=regex.M), r"\1\u00A0\5"))   

        if printer.get("c_preventwidows"):
            # Push the verse number onto the next line (using NBSP) if there is a short widow word (3 characters or less) at the end of the line
            self.localChanges.append((None, regex.compile(r"(\\v \d+ [\w][\w]?[\w]?) ", flags=regex.M), r"\1\u00A0")) 

        if printer.get("c_ch1pagebreak"):
            self.localChanges.append((None, regex.compile(r"(\\c 1 ?\r?\n)", flags=regex.M), r"\pagebreak\r\n\1"))

        if printer.get("c_glueredupwords"):
            self.localChanges.append((None, regex.compile(r"(?<=[ ])(\w\w\w+) \1(?=[\s,.!?])", flags=regex.M), r"\1\u00A0\1")) # keep reduplicated words together
            
        for c in range(1,4):
            if not printer.get("c_usetoc{}".format(c)):
                self.localChanges.append((None, regex.compile(r"(\\toc{} .+)".format(c), flags=regex.M), ""))
            
        # self.localChanges.append((None, regex.compile(r"(\\c\s1\s?\r?\n)", flags=regex.S), r"\skipline\n\hrule\r\n\1")) # this didn't work.

        if not printer.get("c_mainBodyText"):
            self.localChanges.append((None, regex.compile(r"\\c 1 ?\r?\n.+".format(first), flags=regex.S), ""))

        # Apply any changes specified in snippets
        for w, c in self._snippets.items():
            # print("In snippets Changes................................")
            if self.printer.get(c[0]): # if the c_checkbox is true then extend the list with those changes
                # print("Snippet {} is ON.".format(w))
                self.localChanges.extend(c[1].regexes)

        if printer.get("c_tracing"):
            report = "\n".join("{} -> {}".format(p[1].pattern, p[2]) for p in self.localChanges)
            if getattr(printer, "logger", None) is not None:
                printer.logger.insert_at_cursor(v)
            else:
                print(report)
        return self.localChanges

    def ListMissingPics(self, printer):
        print("  info: ListMissingPics",self, printer)
        # When should this function be called? At present it is happening at startup, and I think it should happen later.
        msngpiclist = []
        prjid = self.dict['project/id']
        prjdir = os.path.join(self.dict['/ptxpath'], prjid)
        # prjdir = os.path.join(self.printer.settings_dir, prjid)
        if printer.get("c_useFiguresFolder"): # Therefore this is always true!
            picdir = os.path.join(prjdir, "Figures")
        elif printer.get("c_useLocalFiguresFolder"):
            picdir = os.path.join(prjdir, "local", "Figures")
        elif printer.get("c_useCustomFolder"):
            picdir = self.dict['document/customfigfolder']
        if picdir is None or picdir == "": # shouldn't happen, but just in case!
            print("No folder of illustrtations has been specified")
            return(msngpiclist)  # send back an empty list
        print("Picture Path:",picdir)
        for bk in printer.getBooks():
            fname = printer.getBookFilename(bk, prjdir)
            infname = os.path.join(prjdir, fname)
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                # Finds USFM2-styled markup in text:
                m = re.findall(r"\\fig .*\|(.+?\....)\|.+?\\fig\*", dat)          # Finds USFM2-styled markup in text:
                if m is None:
                    m = re.findall(r'\\fig .*+src="(.+?\....)" .+?\\fig\*', dat)  # Finds USFM3-styled markup in text:
                if m is not None:
                    for f in m:
                        f = re.sub(r"\.[Tt][Ii][Ff]", r".jpg",f)
                        fname = os.path.join(picdir,f)
                        if not os.path.exists(fname):
                            msngpiclist.append(f)
                if len(msngpiclist):
                    print("In {} these pics are missing:\n".format(bk),"\n".join(msngpiclist))
        return(msngpiclist)

    def _configset(self, config, key, value):
        (sect, k) = key.split("/")
        if not config.has_section(sect):
            config.add_section(sect)
        config.set(sect, k, value)

    def createConfig(self, printer):
        print("  info: createConfig",self, printer)
        config = configparser.ConfigParser()
        for k, v in self._mappings.items():
            if v[0] is None:
                continue
            val = printer.get(v[0], asstr=True)
            if k in self._settingmappings:
                if val == "" or val == self.printer.ptsettings.dict.get(self._settingmappings[k], ""):
                    continue
            self._configset(config, k, str(val))
        for k, v in self._fonts.items():
            self._configset(config, k, printer.get(v, asstr=True))
        for k, v in self._snippets.items():
            self._configset(config, k, str(printer.get(v[0], asstr=True)))
        return config

    def loadConfig(self, printer, config):
        print("  info: loadConfig",self, printer, config)
        for sect in config.sections():
            for opt in config.options(sect):
                key = "{}/{}".format(sect, opt)
                val = config.get(sect, opt)
                if key in self._mappings:
                    v = self._mappings[key]
                    if v[0].startswith("cb_") or v[0].startswith("t_") or v[0].startswith("f_") or v[0].startswith("btn_"):
                        pass
                    elif v[0].startswith("s_"):
                        val = float(val)
                    elif v[0].startswith("c_"):
                        val = config.getboolean(sect, opt)
                    else:
                        val = None
                    if val is not None:
                        self.dict[key] = val
                        printer.set(v[0], val)
                elif key in self._fonts:
                    v = self._fonts[key]
                    printer.set(v, val)
                elif key in self._snippets:
                    printer.set(self._snippets[key][0], val.lower() == "true")
        for k, v in self._settingmappings.items():
            (sect, name) = k.split("/")
            try:
                val = config.get(sect, name)
            except configparser.NoOptionError:
                printer.set(self._mappings[k][0], self.printer.ptsettings.dict.get(v, ""))
                self.dict[k] = self.printer.ptsettings.get(v, "")
        # Handle specials here:
        printer.CustomScript = self.dict['project/selectscript']
        printer.customFigFolder = self.dict['document/customfigfolder']
        printer.FrontPDFs = self.dict['project/frontincludes']
        printer.watermarks = self.dict['paper/watermarkpdf']
        printer.BackPDFs = self.dict['project/backincludes']
        self.update()

    def GenerateNestedStyles(self):
        print("  info: GenerateNestedStyles",self)
        prjid = self.printer.get("cb_project")
        prjdir = os.path.join(self.printer.settings_dir, prjid)
        nstyfname = os.path.join(prjdir, "PrintDraft/NestedStyles.sty")
        nstylist = []
        if self.printer.get("c_omitallverses"):
            nstylist.append("##### Remove all verse numbers\n\\Marker v\n\\TextProperties nonpublishable\n\n")
        if not self.printer.get("c_includeFootnotes"):
            nstylist.append("##### Remove all footnotes\n\\Marker f\n\\TextProperties nonpublishable\n\n")
        if not self.printer.get("c_includeXrefs"):
            nstylist.append("##### Remove all cross-references\n\\Marker x\n\\TextProperties nonpublishable\n\n")

        for w, c in self._snippets.items():
            if self.printer.get(c[0]): # if the c_checkbox is true then add the stylesheet snippet for that option
                nstylist.append(c[1].styleInfo+"\n")

        if nstylist == []:
            if os.path.exists(nstyfname):
                os.remove(nstyfname)
        else:
            with open(nstyfname, "w", encoding="utf-8") as outf:
                outf.write("".join(nstylist))
