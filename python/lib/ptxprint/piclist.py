
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.view import refKey
from ptxprint.utils import refKey, universalopen
from ptxprint.texmodel import TexModel
from gi.repository import Gtk, GdkPixbuf
import configparser
import os, re, random, sys

posparms = ["alt", "src", "size", "pgpos", "copy", "caption", "ref", "x-xetex", "mirror", "scale"]
pos3parms = ["src", "size", "pgpos", "ref", "copy", "alt", "x-xetex", "mirror", "scale"]

_piclistfields = ["anchor", "caption", "src", "size", "scale", "pgpos", "ref", "alt", "copyright", "mirror", "disabled", "cleardest"]
_form_structure = {
    'anchor':   't_plAnchor',
    'caption':  't_plCaption',
    'src':      't_plFilename',
    'size':     'fcb_plSize',
    'scale':    's_plScale',
    'pgpos':    'fcb_plPgPos',
    'ref':      't_plRef',
    'alt':      't_plAltText',
    'copyright':    't_plCopyright',
    'mirror':   'fcb_plMirror',
    'hpos':     'fcb_plHoriz',
    'nlines':   's_plLines',
}
_comblist = ['pgpos', 'hpos', 'nlines']

def newBase(fpath):
    doti = fpath.rfind(".")
    f = os.path.basename(fpath[:doti])
    cl = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abc]?$", f)
    if cl:
        return cl[0].lower()
    else:
        return re.sub('[()&+,.;: \-]', '_', f.lower())

class PicList:
    def __init__(self, view, listview, builder, parent):
        self.view = view
        self.model = view.get_model()
        self.listview = listview
        self.builder = builder
        self.parent = parent
        self.selection = view.get_selection()
        for w in ("tv_picList", "tv_picListEdit", "tv_picListEdit1"):
            wid = self.builder.get_object(w)
            sel = wid.get_selection()
            sel.set_mode=Gtk.SelectionMode.SINGLE
            sel.connect("changed", self.row_select)
        for k, v in _form_structure.items():
            w = builder.get_object(v)
            w.connect("value-changed" if v[0].startswith("s_") else "changed", self.item_changed, k)
        self.clear()

    def modify_font(self, p):
        for a in ("", "1", "2"):
            w = self.builder.get_object("cr_caption"+a)
            w.set_property("font-desc", p)

    def isEmpty(self):
        return len(self.model) == 0

    def clear(self):
        self.model.clear()

    def load(self, picinfo):
        self.view.set_model(None)
        self.listview.set_model(None)
        self.model.clear()
        if picinfo is not None:
            for k, v in sorted(picinfo.items(), key=lambda x:(refKey(x[0]), x[1])):
                row = [k]
                for e in _piclistfields[1:]:
                    if e == "scale":
                        try:
                            val = float(v.get(e, 1)) * 100
                        except (ValueError, TypeError):
                            val = 100.
                    elif e == 'cleardest':
                        val = False
                    elif e == "disabled":
                        val = v.get(e, False)
                    else:
                        val = v.get(e, "")
                    row.append(val)
                self.model.append(row)
        self.view.set_model(self.model)
        self.listview.set_model(self.model)

    def get(self, wid, default=None):
        wid = _form_structure.get(wid, wid)
        w = self.builder.get_object(wid)
        res = getWidgetVal(wid, w, default=default)
        if wid.startswith("s_"):
            res = int(res[:res.find(".")]) if res.find(".") >= 0 else int(res)
        return res

    def getrowinfo(self, row):
        e = {k: row[i+1] for i, k in enumerate(_piclistfields[1:])}
        e['scale'] = e['scale'] / 100. if e['scale'] != 100 else None
        return e

    def updateinfo(self, picinfos):
        res = {}
        for row in self.model:
            if len(row[0]) > 5:
                k = row[0]
                p = picinfos.setdefault(k, {})
                for i, e in enumerate(_piclistfields[1:]):
                    if e == 'scale':
                        val = "{:.3f}".format(row[i+1] / 100.)
                    elif e == "cleardest":
                        if row[i+1] and 'dest file' in p:
                            del p['dest file']
                    else:
                        val = row[i+1]
                    p[k] = val
        return res

    def row_select(self, selection):
        if selection.count_selected_rows() != 1:
            return
        model, i = selection.get_selected()
        for w in (self.builder.get_object(x) for x in ("tv_picList", "tv_picListEdit", "tv_picListEdit1")):
            s = w.get_selection()
            if s != selection:
                s.select_iter(i)
                p = w.get_model().get_path(i)
                w.scroll_to_cell(p)
        if selection != self.selection:
            return
        if self.model.get_path(i).get_indices()[0] >= len(self.model):
            return
        row = self.model[i]
        pgpos = re.sub(r'([PF])([lcr])([tb])', r'\1\3\2', row[5])
        for j, (k, v) in enumerate(_form_structure.items()): # relies on ordered dict
            if k == 'pgpos':
                val = pgpos[:2] if pgpos[0] in "PF" else pgpos[0]
            elif k == 'hpos':
                if row[3] == "span":
                    val = "-"
                elif pgpos[0] in "PF":
                    val = pgpos[2:] or "c"
                else:
                    val = pgpos[1:] or ""
            elif k == 'nlines':
                val = re.sub(r'^\D*', "", pgpos)
                val = int(val) if len(val) > 0 else 0
            elif k == 'mirror':
                val = row[j] or "None"
            else:
                val = row[j]
            w = self.builder.get_object(v)
            setWidgetVal(v, w, val)

    def select_row(self, i):
        if i >= len(self.model):
            i = len(self.model) - 1
        treeiter = self.model.get_iter_from_string(str(i))
        self.selection.select_iter(treeiter)

    def get_pgpos(self):
        res = "".join(self.get(k, default="") for k in _comblist[:-1]).replace("-", "")
        if res.startswith("c"):
            res += str(self.get(_comblist[-1]))
        res = re.sub(r'([PF])([tcb])([lcr])', r'\1\3\2', res)
        if len(res) and res[0] in "PF":
            res = res.strip("c")
        return res

    def item_changed(self, w, key):
        if key in _comblist:
            val = self.get_pgpos()
            key = "pgpos"
        else:
            val = self.get(key)
        if self.model is not None and len(self.model):
            row = self.model[self.selection.get_selected()[1]]
            fieldi = _piclistfields.index(key)
            oldval = res[fieldi]
            row[fieldi] = val
            if key == "src":
                tempinfo = {}
                e = self.getrowinfo(row)
                tempinfo[row[0]] = e
                self.parent.getFigureSources(tempinfo)
                pic = self.builder.get_object("img_picPreview")
                picc = self.builder.get_object("img_piccheckPreview")
                if 'src path' in e:
                    self.parent.updatePicChecks(val)       # only update checks if src exists
                    picframe = self.builder.get_object("fr_picPreview")
                    rect = picframe.get_allocation()
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(e['src path'], rect.width - 6, rect.height - 6)
                    pic.set_from_pixbuf(pixbuf)
                    picc.set_from_pixbuf(pixbuf)
                else:
                    pic.clear()
                    picc.clear()
                if val != oldval:
                    row[_piclistfields.index('cleardest')] = True
            elif key == "scale" and val != oldval:
                row[_piclistfields.index('cleardest')] = True
            elif key == "mirror" and val == "None":
                row[fieldi] = ""

    def get_row_from_items(self):
        row = [self.get(k, default="") for k in _piclistfields]
        if row[9] == "None":
            row[9] = ""
        row[_piclistfields.index('pgpos')] = self.get_pgpos()
        return row

    def add_row(self):
        if len(self.model) > 0:
            row = self.model[self.selection.get_selected()[1]][:]
            row[0] = ""
        else:
            row = self.get_row_from_items()
        self.model.append(row)
        self.select_row(len(self.model)-1)

    def del_row(self):
        model, i = self.selection.get_selected()
        del self.model[i]
        self.select_row(model.get_path(i).get_indices()[0])


_checks = {
    "r_picclear":       "unknown",
    "fcb_picaccept":    "Unknown",
    "r_picreverse":     "unknown",
    "fcb_pubusage":     "Unknown",
    "r_pubclear":       "unchecked",
    "r_pubnoise":       "unchecked",
    "fcb_pubaccept":    "Unknown"
}

class PicChecks:

    fname = "picChecks.txt"

    def __init__(self, parent):
        self.cfgShared = configparser.ConfigParser()
        self.cfgProject = configparser.ConfigParser()
        self.parent = parent
        self.src = None

    def _init_default(self, cfg, prefix):
        if not cfg.has_section('DEFAULT'):
            for k, v in _checks.items():
                t, n = k.split("_")
                if n.startswith(prefix):
                    cfg['DEFAULT'][n] = v

    def init(self, basepath, configid):
        if basepath is None or configid is None:
            return
        self.cfgShared.read(os.path.join(basepath, self.fname), encoding="utf-8")
        self._init_default(self.cfgShared, "pic")
        self.cfgProject.read(os.path.join(basepath, configid, self.fname), encoding="utf-8")
        self._init_default(self.cfgProject, "pub")

    def writeCfg(self, basepath, configid):
        if not len(self.cfgShared) or configid is None:
            return
        self.savepic()
        with open(os.path.join(basepath, "shared", "ptxprint", self.fname), "w", encoding="utf-8") as outf:
            self.cfgShared.write(outf)
        with open(os.path.join(basepath, "shared", "ptxprint", configid, self.fname), "w", encoding="utf-8") as outf:
            self.cfgProject.write(outf)

    def loadpic(self, src):
        if self.src == newBase(src):
            return
        self.src = newBase(src)
        for k, v in _checks.items():
            t, n = k.split("_")
            cfg = self.cfgShared if n.startswith("pic") else self.cfgProject
            val = cfg.get(self.src, n, fallback=v)
            self.parent.set(k, val)

    def savepic(self):
        if self.src is None:
            return
        for k, v in _checks.items():
            val = self.parent.get(k)
            t, n = k.split("_")
            cfg = self.cfgShared if n.startswith("pic") else self.cfgProject
            try:
                cfg.set(self.src, n, val)
            except configparser.NoSectionError:
                cfg.add_section(self.src)
                cfg.set(self.src, n, val)

class PicInfo(dict):

    srcfkey = 'src path'

    def __init__(self, model):
        self.model = model
        self.prj = model.prjid
        if model.prjid is None:
            self.basedir = model.settings_dir
        else:
            self.basedir = os.path.join(model.settings_dir, model.prjid)
        self.config = model.configName()

    def load_files(self, suffix="", prjdir=None, prj=None, cfg=None):
        if prjdir is None:
            prjdir = self.basedir
        if prj is None:
            prj = self.prj
        if cfg is None:
            cfg = self.config
        if prjdir is None or prj is None or cfg is None:
            return
        for f in ["shared/ptxprint/{}.piclist".format(prj),
                   "shared/ptxprint/{1}/{0}-{1}.piclist".format(prj, cfg)] \
                + ["shared/ptxprint/{0}/PicLists/{1}".format(cfg, x) \
                        for x in os.listdir(os.path.join(prjdir, "shared", "ptxprint", cfg, "PicLists")) \
                        if x.lower().endswith(".piclist")]:
            p = os.path.join(prjdir, f)
            if os.path.exists(p):
                self.read_piclist(p, suffix=suffix)

    def _fixPicinfo(self, vals):
        p = vals['pgpos']
        if all(x in "apw" for x in p):
            vals['media'] = p
            del vals['pgpos']
        elif re.match(r"^[tbhpc][lrc]?[0-9]?$", p):
            vals['media'] = 'p'
        else:
            vals['loc'] = p
            del vals['pgpos']
        p = vals['size']
        m = re.match(r"(col|span|page|full)(?:\*(\d+(?:\.\d*)))?$", p)
        if m:
            vals['size'] = m[1]
            if m[2] is not None and len(m[2]):
                vals['scale'] = m[2]
        return vals

    def read_piclist(self, fname, suffix=""):
        if not os.path.exists(fname):
            return
        with universalopen(fname) as inf:
            for l in (x.strip() for x in inf.readlines()):
                if not len(l) or l.startswith("%"):
                    continue
                m = l.split("|")
                r = m[0].split(maxsplit=2)
                if suffix == "":
                    k = "{} {}".format(r[0], r[1])
                else:
                    k = "{}{} {}".format(r[0][:3], suffix, r[1])
                pic = {'caption': r[2] if len(r) > 2 else ""}
                self[k] = pic
                if len(m) > 6:
                    for i, f in enumerate(m[1:]):
                        pic[posparms[i+1]] = f
                    self._fixPicinfo(pic)
                else:
                    for d in re.findall(r'(\S+)\s*=\s*"([^"]+)"', m[-1]):
                        pic[d[0]] = d[1]

    def read_sfm(self, bk, fname, suffix="", media=None):
        isperiph = bk in TexModel._peripheralBooks
        with universalopen(fname) as inf:
            dat = inf.read()
            blocks = ["0"] + re.split(r"\\c\s+(\d+)", dat)
            for c, t in zip(blocks[0::2], blocks[1::2]):
                m = re.findall(r"(?ms)(?<=\\v )(\d+?[abc]?([,-]\d+?[abc]?)?) (.(?!\\v ))*"
                               r"\\fig (.*?)\|(.+?\.....?)\|(....?)\|([^\\]+?)?\|([^\\]+?)?"
                               r"\|([^\\]+?)?\|([^\\]+?)?\\fig\*", t)
                if len(m):
                    for f in m:     # usfm 2
                        r = "{}{} {}.{}".format(bk, suffix, c, f[0])
                        pic = {'caption':f[8].strip(), 'anchor': "{}.{}".format(c, f[0])}
                        self[r] = pic
                        for i, v in enumerate(f[3:]):
                            pic[posparms[i]] = v
                        self._fixPicinfo(res[r])
                elif isperiph:
                    m = re.findall(r"(?ms)\\fig (.*?)\|(.+?\.....?)\|(col|span)[^|]*\|([^\\]+?)?\\fig\*", dat)
                    if len(m):
                        for i, f in enumerate(m):
                            r = "{}{} 1.{}".format(bk, suffix, i)
                            pic = {'caption':f[0].strip(), 'src': f[1], 'size': f[2], 'anchor': "1.{}".format(i)}
                            self[r] = pic
                            # self._fixPicinfo(pic)
                m = re.findall(r'(?ms)(?<=\\v )(\d+?[abc]?([,-]\d+?[abc]?)?) (.(?!\\v ))*\\fig ([^\\]*?)\|([^\\]+)\\fig\*', t)
                if len(m):
                    for i, f in enumerate(m):     # usfm 3
                        if "|" in f[4]:
                            break
                        a = (1, i+1) if isperiph else (c, f[0])
                        r = "{}{} {}.{}".format(bk, suffix, *a)
                        pic = {'caption':f[3].strip(), 'anchor': "{}.{}".format(*a)}
                        self[r] = pic
                        labelParams = re.findall(r'([a-z]+?="[^\\]+?")', f[4])
                        for l in labelParams:
                            k,v = l.split("=")
                            pic[k.strip()] = v.strip('"')
                if media is not None and r in self:
                    if 'media' in pic and not any(x in media for x in pic['media']):
                        del self[r]

    def out(self, fpath, bks=[], skipkey=None, usedest=False):
        ''' Generate a picinfo file, with given date.
                bks is a list of 3 letter bkids only to include. If empty, include all.
                skipkey if set will skip a record if there is a non False value associated with skipkey
                usedest says to use dest file rather than src as the file source in the output'''
        hiderefs = self.model.get("c_fighiderefs")
        if usedest:
            p3p = ["dest file"] + pos3parms[1:]
        else:
            p3p = pos3parms
        lines = []
        for k, v in sorted(self.items(),
                           key=lambda x: refKey(x[0][:3]+x[0][4:], info=x[0][3])):
            if (len(bks) and k[:3] not in bks) or (skipkey is not None and v.get(skipkey, False)):
                continue
            lines.append("{} {}|".format(k, v['caption']) + " ".join('{}="{}"' \
                                        .format(pos3parms[i], v[x]) for i, x in enumerate(p3p) \
                                        if x in v and v[x] and (not usedest or not hiderefs or x != 'ref')))
        dat = "\n".join(lines)+"\n"
        with open(fpath, "w", encoding="utf-8") as outf:
            outf.write(dat)

    def build_searchlist(self):
        if self.model.get("c_useCustomFolder"):
            self.srchlist = [self.model.customFigFolder]
        else:
            self.srchlist = []
            if sys.platform == "win32":
                self.srchlist += [os.path.join(self.basedir, "figures")]
                self.srchlist += [os.path.join(self.basedir, "local", "figures")]
            elif sys.platform == "linux":
                chkpaths = []
                for d in ("local", "figures"):
                    chkpaths += [os.path.join(self.basedir, x) for x in (d, d.title())]
                for p in chkpaths:
                    if os.path.exists(p):
                        self.srchlist += [p]
        self.extensions = []
        extdflt = {x:i for i, x in enumerate(["jpg", "jpeg", "png", "tif", "tiff", "bmp", "pdf"])}
        imgord = self.model.get("t_imageTypeOrder").lower()
        extuser = re.sub("[ ,;/><]"," ",imgord).split()
        self.extensions = {x:i for i, x in enumerate(extuser) if x in extdflt}
        if not len(self.extensions):   # If the user hasn't defined any extensions 
            self.extensions = extdflt  # then we can assign defaults

    def getFigureSources(self, filt=newBase, key='src path', keys=None):
        ''' Add source filename information to each figinfo, stored with the key '''
        res = {}
        newfigs = {}
        for k, f in self.items():
            if keys is not None and k[:3] not in keys:
                continue
            newk = filt(f['src']) if filt is not None else f['src']
            newfigs.setdefault(newk, []).append(k)
        for srchdir in self.srchlist:
            if srchdir is None or not os.path.exists(srchdir):
                continue
            if self.get("c_exclusiveFiguresFolder"):
                search = [(srchdir, [], os.listdir(srchdir))]
            else:
                search = os.walk(srchdir)
            for subdir, dirs, files in search:
                for f in files:
                    doti = f.rfind(".")
                    origExt = f[doti:].lower()
                    if origExt[1:] not in self.extensions:
                        continue
                    filepath = os.path.join(subdir, f)
                    nB = filt(f) if filt is not None else f
                    if nB not in newfigs:
                        continue
                    for k in newfigs[nB]:
                        if 'dest file' in self[k]:
                            continue
                        if key in self[k]:
                            old = self.extensions.get(os.path.splitext(self[k][key])[1].lower(), 10000)
                            new = self.extensions.get(os.path.splitext(filepath)[1].lower(), 10000)
                            if old > new:
                                self[k][key] = filepath
                            elif old == new and (self.get("c_useLowResPics") \
                                                != bool(os.path.getsize(self[k][key]) < os.path.getsize(filepath))):
                                self[k][key] = filepath
                        else:
                            self[k][key] = filepath

    def set_positions(self):
        picposns = { "L": {"col":  ("tl", "bl"),             "span": ("t")},
                     "R": {"col":  ("tr", "br"),             "span": ("b")},
                     "":  {"col":  ("tl", "tr", "bl", "br"), "span": ("t", "b")}}
        randomizePosn = self.model.get("c_randomPicPosn")
        isdblcol = self.model.get("c_doublecolumn")
        for k, v in self:
            if not isdblcol: # Single Column layout so change all tl+tr > t and bl+br > b
                if 'pgpos' in v:
                    v['pgpos'] = re.sub(r"([tb])[lr]", r"\1", v['pgpos'])
                else:
                    v['pgpos'] = "t"
            if 'pgpos' not in v:
                if not isTemp and randomizePosn:
                    v['pgpos'] = random.choice(picposn.get(v['size'], 'col')) # Randomize location of illustrations on the page (tl,tr,bl,br)
                else:
                    v['pgpos'] = picposn.get(v['size'], 'col')[0]

    def set_destinations(self, fn=lambda x,y,z:z, keys=None):
        print("Set destinations for {} pics".format(len(self)))
        for k, v in self.items():
            if 'dest file' in v:
                continue            # no need to regenerate
            if keys is not None and k[:3] not in keys:
                continue
            nB = newBase(v['src'])
            if self.srcfkey not in v:
                continue
            fpath = v[self.srcfkey]
            origExt = os.path.splitext(fpath)[1]
            v['dest file'] = fn(v, v[self.srcfkey], nB+origExt.lower())
            if 'media' in v and len(v['media']) and 'p' not in v['media']:
                v['disabled'] = True

    def updateView(self, view, bks=None):
        view.load(self)
        # enable bks filter if set

def PicInfoUpdateProject(model, bks, allbooks, picinfos, suffix=""):
    newpics = PicInfo(model)
    newpics.read_piclist(os.path.join(model.settings_dir, model.prjid, 'shared',
                                      'ptxprint'), "{}.piclist".format(mode.prjid))
    delpics = set()
    for bk in bks:
        bkf = allbooks.get(bk, None)
        if bkf is None or not os.path.exists(bkf):
            continue
        for k in (k for k in newpics.keys() if k[:3] == bk):
            del newpics[k]
            delpics.add(k)
        newpics.read_usfm(bk, bkf)
        for k in (k for k in newpics.keys() if k[:3] == bk):
            if k in delpics:
                delpics.remove(k)
            else:
                picinfos[k+suffix] = newpics[k]
        for k in deplics:
            if k+suffix in picinfos:
                del picinfos[k+suffix]
