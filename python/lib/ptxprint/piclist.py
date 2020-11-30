
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.view import refKey
from ptxprint.utils import refKey, universalopen, print_traceback
from ptxprint.texmodel import TexModel
from gi.repository import Gtk, GdkPixbuf, GObject, Gdk
from threading import Thread
import configparser
import regex
import os, re, random, sys

posparms = ["alt", "src", "size", "pgpos", "copy", "caption", "ref", "x-xetex", "mirror", "scale"]
pos3parms = ["src", "size", "pgpos", "ref", "copy", "alt", "x-xetex", "mirror", "scale", "media"]

_piclistfields = ["anchor", "caption", "src", "size", "scale", "pgpos", "ref", "alt", "copy", "mirror", "disabled", "cleardest", "key", "media"]
_pickeys = {k:i for i, k in enumerate(_piclistfields)}

_form_structure = {
    'anchor':   't_plAnchor',
    'caption':  't_plCaption',
    'src':      't_plFilename',
    'size':     'fcb_plSize',
    'scale':    's_plScale',
    'pgpos':    'fcb_plPgPos',
    'ref':      't_plRef',
    'alt':      't_plAltText',
    'copy':     't_plCopyright',
    'mirror':   'fcb_plMirror',
    'hpos':     'fcb_plHoriz',
    'nlines':   's_plLines',
    'medP':     'c_plMediaP',
    'medA':     'c_plMediaA',
    'medW':     'c_plMediaW'
}
_comblist = ['pgpos', 'hpos', 'nlines']
_defaults = {
    'scale':    "1.000"
}

_picLimitDefault = {
    'ab': ('paw','paw', 'Permission requirements unknown'),
    'cn': ('paw','paw', 'Any media, but needs written permission'),
    'co': ('paw','paw', 'Any media, but needs written permission'),
    'hk': ('pa','p', 'Print is fine, but App use requires a formal agreement and reporting. Web use is not permitted.'),
    'lb': ('pa','p', 'Print is fine, but App use requires a formal agreement and reporting. Web use is not permitted.'),
    'bk': ('pa','p', 'Print is fine, but App use requires a formal agreement and reporting. Web use is not permitted.'),
    'ba': ('paw','paw', 'Any media is fine without restriction'),
    'dy': ('paw','paw', 'Any media is fine without restriction'),
    'gt': ('paw','paw', 'Any media is fine without restriction'),
    'dh': ('paw','paw', 'Any media is fine without restriction'),
    'mh': ('paw','paw', 'Any media is fine without restriction'),
    'mn': ('paw','paw', 'Any media is fine without restriction'),
    'wa': ('p','p', 'Only Print media'),
    'dn': ('p','p', 'Only Print media'),
    'ib': ('p','p', 'Only Print media')
}

newrowcounter = 1

def newBase(fpath):
    doti = fpath.rfind(".")
    f = os.path.basename(fpath[:doti])
    cl = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abc]?$", f)
    if cl:
        return cl[0].lower()
    else:
        return re.sub('[()&+,.;: \-]', '_', f.lower())

class PicList:
    def __init__(self, view, checkview, builder, parent):
        self.view = view
        self.checkview = checkview
        self.loading = False
        self.checkinv = False
        self.checkfilt = 0
        self.model = view.get_model()
        self.checkmodel = self.model.filter_new()
        self.checkmodel.set_visible_func(self.checkfilter)
        self.checkview.set_model(self.checkmodel)
        self.builder = builder
        self.parent = parent
        self.picinfo = None
        self.selection = view.get_selection()
        self.picrect = None
        self.currow = None
        self.curriter = None
        self.bookfilters = None
        for wid in (self.view, self.checkview):
            sel = wid.get_selection()
            sel.set_mode=Gtk.SelectionMode.SINGLE
            sel.connect("changed", self.row_select)
        for k, v in _form_structure.items():
            w = builder.get_object(v)
            sig = "changed"
            if v.startswith("s_"):
                sig = "value-changed"
                w.connect("focus-out-event", self.item_changed, k)
            elif v.startswith("c_"):
                sig = "clicked"
            w.connect(sig, self.item_changed, k)
        self.previewBuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(os.path.dirname(__file__), "picLocationPreviews.png"))
        self.clear()
        self.loading = False

    def checkfilter(self, model, i, data):
        if self.loading:
            return False
        try:
            v = newBase(model[i][_pickeys['src']])
        except TypeError:
            print("Failed to load src for", model.get_string_from_iter(i), model, i)
            return False
        res = True
        if self.checkfilt > 0:
            res = self.parent.picChecksFilter(v, self.checkfilt)
        return not res if self.checkinv else res

    def setCheckFilter(self, invert, filt):
        self.checkinv = invert
        self.checkfilt = filt
        self.checkmodel.refilter()

    def modify_font(self, p):
        for a in ("", "2"):
            w = self.builder.get_object("cr_caption"+a)
            w.set_property("font-desc", p)

    def isEmpty(self):
        return len(self.model) == 0

    def clear(self):
        self.model.clear()

    def load(self, picinfo, bks=None):
        self.picinfo = picinfo
        #self.view.set_model(None)
        self.model.clear()
        self.bookfilters = bks
        if picinfo is not None:
            for k, v in sorted(picinfo.items(), key=lambda x:refKey(x[1]['anchor'])):
                if bks is not None and len(bks) and v['anchor'][:3] not in bks:
                    continue
                row = []
                defaultmedia = _picLimitDefault.get(v.get('src', '')[:2].lower(), ('paw', 'paw', 'Default'))
                for e in _piclistfields:
                    if e == 'key':
                        val = k
                    elif e == "scale":
                        try:
                            val = float(v.get(e, 1)) * 100
                        except (ValueError, TypeError):
                            val = 100.
                    elif e == 'cleardest':
                        val = False
                    elif e == "disabled":
                        val = v.get(e, False)
                    elif e == "media":
                        val = v.get(e, None)
                        if val is None:
                            val = defaultmedia[1]
                        else:
                            val = "".join(x for x in val if x in defaultmedia[0])
                    else:
                        val = v.get(e, "")
                    row.append(val)
                self.model.append(row)
        #self.view.set_model(self.model)
        self.checkmodel.refilter()
        self.loading = False

    def get(self, wid, default=None):
        wid = _form_structure.get(wid, wid)
        w = self.builder.get_object(wid)
        res = getWidgetVal(wid, w, default=default)
        if wid.startswith("s_"):
            res = int(res[:res.find(".")]) if res.find(".") >= 0 else int(res)
        return res

    def updateinfo(self, picinfos):
        allkeys = set()
        for row in self.model:
            k = row[_pickeys['key']]
            p = picinfos.setdefault(k, {})
            for i, e in enumerate(_piclistfields):
                if e == 'key':
                    allkeys.add(row[i])
                    continue
                elif e == 'scale':
                    val = "{:.3f}".format(row[i] / 100.)
                elif e == "cleardest":
                    if row[i] and 'dest file' in p:
                        del p['dest file']
                    continue
                else:
                    val = row[i]
                p[e] = val
        for k,v in list(picinfos.items()):
            if k not in allkeys and (self.bookfilters is None or v['anchor'][:3] in self.bookfilters):
                del picinfos[k]
        return picinfos

    def clearPicSources(self, picinfos):
        allkeys = set()
        for row in self.model:
            k = row[_pickeys['key']]
            p = picinfos.setdefault(k, {})
            for i, e in enumerate(_piclistfields):
                if e == 'key':
                    allkeys.add(row[i])
                    continue
                elif e == "cleardest":
                    if row[i] and 'dest file' in p:
                        del p['dest file']
                    continue

    def row_select(self, selection): # Populate the form from the model
        model, it = selection.get_selected()
        if self.loading or selection.count_selected_rows() != 1:
            return
        if self.currow is not None:
            for k, s in ((k, x) for k,x in _form_structure.items() if x.startswith("s_")):
                w = self.builder.get_object(s)
                if w.has_focus():
                    e = Gdk.Event(Gdk.EventType.FOCUS_CHANGE)
                    e.window = w
                    e.send_event = True
                    w.emit("focus-out-event", e)
        model, it = selection.get_selected()
        path = model.get_path(it)
        cpath = path if selection == self.selection else model.convert_path_to_child_path(path)
        cit = self.model.get_iter(cpath)
        for w in (self.view, self.checkview): # keep both views in sync
            s = w.get_selection()
            if s != selection:
                self.loading = True
                m = w.get_model()
                fpath = cpath if s == self.selection else m.convert_child_path_to_path(cpath)
                if fpath is not None:
                    s.select_path(fpath)
                    w.scroll_to_cell(fpath)
                else:
                    s.unselect_all()
                self.loading = False
        if selection != self.selection:
            self.parent.savePicChecks()
            if not self.checkmodel.do_visible(self.checkmodel, self.checkmodel.get_model(), cit):
                return
        if cpath.get_indices()[0] >= len(self.model):
            print("Too Long!")
            return
        else:
            self.currow = self.model[cit][:]    # copy it so that any edits don't mess with the model if the iterator moves
            self.curriter = cit
        pgpos = re.sub(r'^([PF])([lcr])([tb])', r'\1\3\2', self.currow[_pickeys['pgpos']])
        self.parent.pause_logging()
        self.loading = True
        for j, (k, v) in enumerate(_form_structure.items()): # relies on ordered dict
            if k == 'pgpos':
                val = pgpos[:2] if pgpos[0:1] in "PF" else (pgpos[0:1] or "t")
            elif k == 'hpos':
                if self.currow[_pickeys['size']] == "span":
                    val = "-"
                elif pgpos[0:1] in "PF":
                    val = pgpos[2:] or "c"
                else:
                    val = pgpos[1:] or ""
            elif k == 'nlines':
                val = re.sub(r'^\D*', "", pgpos)
                try:
                    val = int(val)
                except (ValueError, TypeError):
                    val = 0
            elif k.startswith("med"):
                val = v[-1].lower() in (self.currow[_pickeys['media']] or "paw")
            elif k == 'mirror':
                val = self.currow[j] or "None"
            else:
                val = self.currow[j]
            w = self.builder.get_object(v)
            setWidgetVal(v, w, val)
        self.mask_media(self.currow)
        self.parent.unpause_logging()
        self.loading = False

    _locGrid = {
"1"   :    (0,0),"1-b":     (1,0),"1-cl":    (2,0),"1-cr":   (3,0),"1-hc":    (4,0),"1-hl":    (5,0),"1-hr":    (6,0),"1-p":     (7,0),
"1-pa":    (0,1),"1-pb":    (1,1),"1-t":     (2,1),"2":      (3,1),"2-col-bl":(4,1),"2-col-br":(5,1),"2-col-cl":(6,1),"2-col-cr":(7,1),
"2-col-hc":(0,2),"2-col-hl":(1,2),"2-col-hr":(2,2),"2-col-p":(3,2),"2-col-pa":(4,2),"2-col-pb":(5,2),"2-col-tl":(6,2),"2-col-tr":(7,2),
"2-span-b":(0,3),"2-span-t":(1,3),"full":    (2,3),"page":   (3,3)
}
    
    def dispLocPreview(self, key):
        x,y = self._locGrid.get(key, (7,3))
        x = x * 212 + 14
        y = y * 201 + 10
        pic = self.previewBuf.new_subpixbuf(x,y,130,180)
        return pic

    def getLocnKey(self):
        if self.get("c_doublecolumn"):
            cols = 2
        else:
            cols = 1
        if not self.get("c_plMediaP"):
            locnKey = "1" if cols == 1 else "2"
        else:
            frSize = self.currow[_pickeys['size']]
            pgposLocn = self.currow[_pickeys['pgpos']]
            locnKey = "{}-{}-{}".format(cols, frSize, pgposLocn)
            locnKey = re.sub(r'^\d\-(page|full)\-.+', r'\1', locnKey)
            locnKey = re.sub(r'^1\-(col|span)\-', '1-', locnKey)
            locnKey = re.sub(r'^(.+)i(\d?)$', r'\1l\2', locnKey)
            locnKey = re.sub(r'^(.+)o(\d?)$', r'\1r\2', locnKey)
            locnKey = re.sub(r'^(1\-[tb])[lcrio]$', r'\1', locnKey)
            locnKey = re.sub(r'^1\-p[lcrio]', '1-p', locnKey)
            locnKey = re.sub(r'^2\-col\-p[lcrio]', '2-col-p', locnKey)
            locnKey = re.sub(r'^2\-col\-h$', '2-col-hc', locnKey)
            locnKey = re.sub(r'^2\-col\-c$', '2-col-cl', locnKey)
            locnKey = re.sub(r'^1\-c$', '1-cl', locnKey)
            locnKey = re.sub(r'\d$', '', locnKey)
        return locnKey

    def select_row(self, i):
        if i >= len(self.model):
            i = len(self.model) - 1
        treeiter = self.model.get_iter_from_string(str(i))
        self.selection.select_iter(treeiter)

    def mask_media(self, row):
        src = row[_pickeys['src']][:2]
        inf = _picLimitDefault.get(src.lower(), ("paw", "paw", "Default"))
        if inf[2] == 'Default':
            self.builder.get_object("l_plMedia").set_tooltip_text("Media permissions unknown\nfor this illustration")
        else:
            self.builder.get_object("l_plMedia").set_tooltip_text("Permission for {} series:\n{}".format(src.upper(),inf[2]))
        val = row[_pickeys['media']]
        for c in 'paw':
            w = _form_structure["med"+c.upper()]
            wid = self.builder.get_object(w)
            if wid is not None:
                wid.set_sensitive(c in inf[0])
            if val is None or val == "":
                wid.set_active(True)
            else:
                wid.set_active(c in val)

    def get_pgpos(self):
        res = "".join(self.get(k, default="") for k in _comblist[:-1]).replace("-", "")
        # if res.startswith("c"):
            # res += str(self.get(_comblist[-1]))
        res = re.sub(r'([PF])([tcb])([lcr])', r'\1\3\2', res)
        if len(res) and res[0] in "PF":
            res = res.strip("c")
        lines = self.get("nlines", 0)
        if lines > 0 and len(res) and res[0] in "pc":
            res += str(lines)
        return res

    def item_changed(self, w, *a):
        key = a[-1]
        if self.loading and key not in ("src", ):
            return
        if key in _comblist:
            val = self.get_pgpos()
            key = "pgpos"
        elif key.startswith("med"):
            val = "".join(v[-1].lower() for k, v in _form_structure.items() if k.startswith("med") and self.get(v))
            # if self.currow is not None:
                # src = self.currow[_pickeys['src']][:2]
                # inf = _picLimitDefault.get(src.lower(), ("paw", "paw", "Default"))
            if sorted(val) == sorted("paw"):
                val = ""
            key = "media"
        else:
            val = self.get(key)
        if self.currow is not None:
            fieldi = _piclistfields.index(key)
            oldval = self.currow[fieldi]
            self.currow[fieldi] = val
            r_image = self.parent.get("r_image", default="preview")
            if r_image == "location":
                locKey = self.getLocnKey()
                pic = self.dispLocPreview(locKey)
                self.setPreview(pic)
            if key == "src":
                if r_image == "preview":
                    fpath = None
                    if self.picinfo is not None:
                        fpath = self.picinfo.get_sourcefile(val, exclusive=self.parent.get("c_exclusiveFiguresFolder"))
                    if fpath is not None:
                        if self.picrect is None:
                            picframe = self.builder.get_object("fr_picPreview")
                            self.picrect = picframe.get_allocation()
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(fpath, self.picrect.width - 6, self.picrect.height - 6)
                        self.setPreview(pixbuf, tooltip=fpath)
                    else:
                        self.setPreview(None)
                self.parent.updatePicChecks(val)       # only update checks if src exists
                self.mask_media(self.currow)
                if val != oldval: # New source implies new destination file
                    self.currow[_piclistfields.index('cleardest')] = True
            elif key == "scale" and val != oldval: # Not sure why we need to do this
                self.currow[_piclistfields.index('cleardest')] = True
            elif key == "mirror" and val == "None":
                self.currow[fieldi] = ""
            if not self.loading:
                self.model.set_value(self.curriter, fieldi, self.currow[fieldi])

    def setPreview(self, pixbuf, tooltip=None):
        pic = self.builder.get_object("img_picPreview")
        picc = self.builder.get_object("img_piccheckPreview")
        if pixbuf is None:
            pic.clear()
            picc.clear()
            tooltip = ""
        else:
            pic.set_from_pixbuf(pixbuf)
            picc.set_from_pixbuf(pixbuf)
        if tooltip is not None:
            pic.set_tooltip_text(tooltip)
            picc.set_tooltip_text(tooltip)
            self.builder.get_object("t_plFilename").set_tooltip_text(tooltip)

    def drawPreview(self, wid, cr):
        if self.previewScales:
            pixbuf = self.pixbuf.scale_simple(width, height, GdkPixbuf.InterpType.BILINEAR)
        else:
            pixbuf = self.pixbuf
        cr.set_source_pixbuf(pixbuf, 0, 0)
        cr.paint()
        return False

    
    def onRadioChanged(self):
        self.item_changed(None, "src")

    def onResized(self):
        picframe = self.builder.get_object("fr_picPreview")
        self.picrect = picframe.get_allocation()
        self.item_changed(None, "src")

    def get_row_from_items(self):
        row = [self.get(k, default="") for k in _piclistfields]
        if row[9] == "None": # mirror
            row[9] = ""
        row[_piclistfields.index('pgpos')] = self.get_pgpos()
        return row

    def add_row(self):
        if len(self.model) > 0:
            row = self.model[self.selection.get_selected()[1]][:]
        else:
            row = self.get_row_from_items()
        row[_pickeys['key']] = "row{}".format(newrowcounter)
        newrowcounter += 1
        self.model.append(row)
        self.select_row(len(self.model)-1)

    def del_row(self):
        model, i = self.selection.get_selected()
        del self.model[i]
        ind = model.get_path(i)
        if ind is None:
            indt = model.get_iter_first()
            ind = model.get_path(indt)
        if ind is not None:         # otherwise we have an empty list
            self.select_row(ind.get_indices()[0])

    def set_src(self, src):
        wid = _form_structure.get('src', 'src')
        w = self.builder.get_object(wid)
        setWidgetVal(wid, w, src)

    def clearSrcPaths(self):
        self.picinfo.clearSrcPaths()

_checks = {
    "r_picclear":       "unknown",
    "fcb_picaccept":    "Unknown",
    "r_picreverse":     "OK",
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
        for (cfg, n, v, k) in self._allFields():
            val = cfg.get(self.src, n, fallback=v)
            if n == "picreverse" and val == "unknown":
                val = "OK"
            self.parent.set(k, val)
        self.parent.set("tb_picNotes", self.cfgProject.get(self.src, "notes", fallback=""))
        for cfg in (self.cfgShared, self.cfgProject):
            if cfg.getboolean(self.src, "approved", fallback=False):
                self.parent.set("t_pubInits", cfg.get(self.src, "approved_by", fallback=""))
                self.parent.set("t_pubApprDate", cfg.get(self.src, "approved_date", fallback=""))
                self.parent.set("r_pubapprove", "scopeAny" if cfg == self.cfgProject else "scopeProject")
                self.parent.set('c_pubApproved', True)
                break
        else: # this happens if we never got to the break above (neither was found)
            self.parent.set('c_pubApproved', False)
        self.onReverseRadioChanged()

    def savepic(self):
        if self.src is None:
            return
        for (cfg, n, defval, k) in self._allFields():
            val = self.parent.get(k)
            try:
                cfg.set(self.src, n, val)   # update the existing entry if it already exists
            except configparser.NoSectionError:
                cfg.add_section(self.src)   # otherwise add a section/src first
                cfg.set(self.src, n, val)   # and then throw in the values
        val = self.parent.get("c_pubApproved")
        cfg = self.cfgShared if self.parent.get("r_pubapprove") == "scopeAny" else self.cfgProject
        ocfg = self.cfgProject if self.parent.get("r_pubapprove") == "scopeAny" else self.cfgShared
        if val:
            cfg.set(self.src, "approved_by", self.parent.get("t_pubInits"))
            cfg.set(self.src, "approval_date", self.parent.get("t_pubApprDate"))
            cfg.set(self.src, "approved", "true")
        else:
            cfg.set(self.src, "approved", "false")
        ocfg.set(self.src, "approved", "false")
        self.cfgProject.set(self.src, "notes", self.parent.get("tb_picNotes"))

    def filter(self, src, filt):
        if filt == 0:       # All
            return True
        elif filt == 3:     # Approved
            return self.cfgShared.getboolean(src, "approved", fallback=False) \
                or self.cfgProject.getboolean(src, "approved", fallback=False)
        else:
            vals = [cfg.get(src, n, fallback=v) == v for (cfg, n, v, _) in self._allFields()]
            if filt == 1:     # All unknown/unchecked
                return all(vals)
            elif filt == 2:     # Any unknown/unchecked
                return any(vals)
            return True

    def _allFields(self):
        for k, v in _checks.items():
            t, n = k.split("_")
            cfg = self.cfgShared if n.startswith("pic") else self.cfgProject
            yield(cfg, n, v, k)
            
    def onReverseRadioChanged(self):
        r = self.parent.get("r_picreverse")
        self.parent.builder.get_object("fcb_plMirror").set_sensitive(False)
        if r == "always":
            self.parent.set("fcb_plMirror", "both")
        elif r == "never":
            self.parent.set("fcb_plMirror", "None")
        else: # unlock the control
            self.parent.builder.get_object("fcb_plMirror").set_sensitive(True)
        
class PicInfo(dict):

    srcfkey = 'src path'
    stripsp_re = re.compile(r"^(\S+\s+\S+)\s+.*$")

    def __init__(self, model):
        self.clear(model)
        self.inthread = False
        self.keycounter = 0

    def clear(self, model=None):
        super().clear()
        if model is not None:
            self.model = model
            self.prj = model.prjid
            if self.model.prjid is None:
                self.basedir = self.model.settings_dir
            else:
                self.basedir = os.path.join(self.model.settings_dir, model.prjid)
            self.config = model.configId
        self.loaded = False
        self.srchlist = []

    def load_files(self, suffix="", prjdir=None, prj=None, cfg=None):
        if self.inthread:
            return False
        else:
            self.thread = None
        if prjdir is None:
            prjdir = self.basedir
        if prj is None:
            prj = self.prj
        if cfg is None:
            cfg = self.config
        if prjdir is None or prj is None or cfg is None:
            return False
        preferred = os.path.join(prjdir, "shared/ptxprint/{1}/{0}-{1}.piclist".format(prj, cfg))
        if os.path.exists(preferred):
            self.read_piclist(preferred, suffix=suffix)
            self.loaded = True
            return True
        places = ["shared/ptxprint/{}.piclist".format(prj)]
        plistsdir = os.path.join(prjdir, "shared", "ptxprint", cfg, "PicLists")
        if os.path.exists(plistsdir):
            places += ["shared/ptxprint/{0}/PicLists/{1}".format(cfg, x) \
                        for x in os.listdir(plistsdir) if x.lower().endswith(".piclist")]
        havepiclists = False
        for f in places:
            p = os.path.join(prjdir, f)
            if os.path.exists(p):
                self.read_piclist(p, suffix=suffix)
                havepiclists = True
        self.loaded = True
        if not havepiclists:
            self.inthread = True
            self.threadUsfms(suffix)
            #self.thread = Thread(target=self.threadUsfms, args=(suffix,))
            #return False
        else:
            self.model.savePics()
        return True

    def threadUsfms(self, suffix):
        bks = self.model.getAllBooks()
        for bk, bkp in bks.items():
            if os.path.exists(bkp):
                self.read_sfm(bk, bkp, suffix=suffix)
        self.model.savePics()
        self.inthread = False

    def _fixPicinfo(self, vals): # USFM2 to USFM3 converter
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

    def newkey(self, suffix=""):
        self.keycounter += 1
        return "pic{}{}".format(suffix, self.keycounter)

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
                    k = " ".join(r[:2])
                elif len(r) > 1:
                    k = "{}{} {}".format(r[0][:2], suffix, r[1])  # :3 or :2 ?
                else:
                    k = "{}{}".format(r[0], suffix)
                pic = {'anchor': k, 'caption': r[2] if len(r) > 2 else ""}
                self[self.newkey(suffix)] = pic
                if len(m) > 6: # must be USFM2, so|grab|all|the|different|pieces!
                    for i, f in enumerate(m[1:]):
                        if i < len(posparms)-1:
                            pic[posparms[i+1]] = f
                    self._fixPicinfo(pic)
                else: # otherwise USFM3, so find all the named params
                    for d in re.findall(r'(\S+)\s*=\s*"([^"]+)"', m[-1]):
                        pic[d[0]] = d[1]
        self.rmdups()

    def read_sfm(self, bk, fname, suffix="", media=None):
        isperiph = bk in TexModel._peripheralBooks
        with universalopen(fname) as inf:
            dat = inf.read()
            blocks = ["0"] + re.split(r"\\c\s+(\d+)", dat)
            for c, t in zip(blocks[0::2], blocks[1::2]):
                if isperiph:
                    m = re.findall(r"(?ms)\\fig (.*?)\|(.+?\.....?)\|(col|span)[^|]*\|([^\\]+?)?\\fig\*", dat)
                    if len(m):
                        for i, f in enumerate(m):
                            r = "{}{} 1.{}".format(bk, suffix, i)
                            pic = {'anchor': r, 'caption':f[0].strip(), 'src': f[1], 'size': f[2]}
                            key = self.newkey(suffix)
                            self[key] = pic
                    continue
                for v in re.findall(r"(?s)(?<=\\v )(\d+[abc]?(?:[,-]\d+?[abc]?)?) ((?:.(?!\\v ))+)", t):
                    lastv = v[0]
                    s = v[1]
                    key = None
                    m = regex.findall(r"(?ms)\\fig (.*?)\|(.+?\.....?)\|(....?)\|([^\\]+?)?\|([^\\]+?)?"
                                   r"\|([^\\]+?)?\|([^\\]+?)?\\fig\*", s)
                    if len(m):
                        # print("usfm2:", lastv, m)
                        for f in m:     # usfm 2
                            r = "{}{} {}.{}".format(bk, suffix, c, lastv)
                            pic = {'anchor': r, 'caption':f[5].strip()}
                            key = self.newkey(suffix)
                            self[key] = pic
                            for i, v in enumerate(f):
                                pic[posparms[i]] = v
                            self._fixPicinfo(pic)
                    m = regex.findall(r'(?ms)\\fig ([^\\]*?)\|([^\\]+)\\fig\*', s)
                    if len(m):
                        # print("usfm3:", lastv, m)
                        for i, f in enumerate(m):     # usfm 3
                            # lastv = f[0] or lastv
                            if "|" in f[1]:
                                break
                            a = (1, i+1) if isperiph else (c, lastv)
                            r = "{}{} {}.{}".format(bk, suffix, *a)
                            pic = {'caption':f[0].strip(), 'anchor': r}
                            key = self.newkey(suffix)
                            self[key] = pic
                            labelParams = re.findall(r'([a-z]+?="[^\\]+?")', f[1])
                            for l in labelParams:
                                k,v = l.split("=")
                                pic[k.strip()] = v.strip('"')
                            if media is not None and key in self:
                                if 'media' in pic and not any(x in media for x in pic['media']):
                                    del self[key]

    def out(self, fpath, bks=[], skipkey=None, usedest=False, media=None):
        ''' Generate a picinfo file, with given date.
                bks is a list of 3 letter bkids only to include. If empty, include all.
                skipkey if set will skip a record if there is a non False value associated with skipkey
                usedest says to use dest file rather than src as the file source in the output'''
        self.rmdups()
        hiderefs = self.model.get("c_fighiderefs")
        if usedest:
            p3p = ["dest file"] + pos3parms[1:]
        else:
            p3p = pos3parms
        lines = []
        for k, v in sorted(self.items(),
                           key=lambda x: refKey(x[1]['anchor'][:3]+x[0][4:], info=x[1]['anchor'][3:4])):
            if (len(bks) and v['anchor'][:3] not in bks) or (skipkey is not None and v.get(skipkey, False)):
                continue
            outk = self.stripsp_re.sub(r"\1", v['anchor'])
            line = []
            for i, x in enumerate(p3p):
                if x not in v or not v[x]:
                    continue
                elif x in _defaults and _defaults[x] == v[x]:
                    continue
                elif usedest and hiderefs and x == "ref":
                    continue
                elif x == "scale" and float(v[x]) == 1.0:
                    continue
                elif x == "media" and sorted(v[x]) == "apw":
                    if media is not None and media not in v[x]:
                        break
                    continue
                line.append('{}="{}"'.format(pos3parms[i], v[x]))
            else:
                lines.append("{} {}|".format(outk, v.get('caption', ''))+ " ".join(line))
        dat = "\n".join(lines)+"\n"
        with open(fpath, "w", encoding="utf-8") as outf:
            outf.write(dat)

    def rmdups(self): # MH {checking I understand this right} Does this assume we can't have 2 pics with the same anchor?
        allkeys = {}
        for k,v in self.items():
            allkeys.setdefault(self.stripsp_re.sub(r"\1", v['anchor']), []).append(k)
        for k, v in allkeys.items():
            if len(v) == 1:
                continue
            srcset = set()
            for pk in v:
                s = self[pk].get('src', None)
                if s is not None:
                    if s in srcset:
                        del self[pk]
                    else:
                        srcset.add(s)

    def build_searchlist(self):
        if self.model.get("c_useCustomFolder"):
            self.srchlist = [self.model.customFigFolder]
        else:
            self.srchlist = []
            chkpaths = []
            for d in ("local", ""):
                if sys.platform.startswith("win"):
                    chkpaths += [os.path.join(self.basedir, d, "figures")]
                else:
                    chkpaths += [os.path.join(self.basedir, x, y+"igures") for x in (d, d.title()) for y in "fF"]
            for p in chkpaths:
                if os.path.exists(p) and len(os.listdir(p)) > 0:
                    for dp, _, fn in os.walk(p): 
                        if len(fn): 
                            print(dp)
                            self.srchlist += [dp]
        self.extensions = []
        extdflt = {x:i for i, x in enumerate(["jpg", "jpeg", "png", "tif", "tiff", "bmp", "pdf"])}
        imgord = self.model.get("t_imageTypeOrder").lower()
        extuser = re.sub("[ ,;/><]"," ",imgord).split()
        self.extensions = {x:i for i, x in enumerate(extuser) if x in extdflt}
        if not len(self.extensions):   # If the user hasn't defined any extensions 
            self.extensions = extdflt  # then we can assign defaults

    def getFigureSources(self, filt=newBase, key='src path', keys=None, exclusive=False):
        ''' Add source filename information to each figinfo, stored with the key '''
        res = {}
        newfigs = {}
        for k, f in self.items():
            if keys is not None and f['anchor'][:3] not in keys:
                continue
            newk = filt(f['src']) if filt is not None else f['src']
            newfigs.setdefault(newk, []).append(k)
        for srchdir in self.srchlist:
            if srchdir is None or not os.path.exists(srchdir):
                continue
            if exclusive:
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

    def get_sourcefile(self, fname, filt=newBase, exclusive=False):
        if filt is not None:
            fname = filt(fname)
        if self.srchlist is None or not len(self.srchlist):
            self.build_searchlist()
        for srchdir in self.srchlist:
            if srchdir is None or not os.path.exists(srchdir):
                continue
            if exclusive:
                search = [(srchdir, [], os.listdir(srchdir))]
            else:
                search = os.walk(srchdir)
            for subdir, dirs, files in search:
                for f in files:
                    _, origExt = os.path.splitext(f)
                    if origExt[1:] not in self.extensions:
                        continue
                    nB = filt(f) if filt is not None else f
                    if nB == fname:
                        return os.path.join(subdir, f)
        return None

    def set_positions(self, cols=1, randomize=False, suffix=""):
        picposns = { "L": {"col":  ("tl", "bl"),             "span": ("t")},
                     "R": {"col":  ("tr", "br"),             "span": ("b")},
                     "":  {"col":  ("tl", "tr", "bl", "br"), "span": ("t", "b")}}
        isdblcol = self.model.get("c_doublecolumn")
        for k, v in self.items():
            if cols == 1: # Single Column layout so change all tl+tr > t and bl+br > b
                if 'pgpos' in v:
                    v['pgpos'] = re.sub(r"([tb])[lr]", r"\1", v['pgpos'])
                elif randomize:
                    v['pgpos'] = random.choice(picposns[suffix]['span'])
                else:
                    v['pgpos'] = "t"
            elif 'pgpos' not in v:
                posns = picposns[suffix].get(v.get('size', 'col'), picposns[suffix]["col"])
                if randomize:
                    v['pgpos'] = random.choice(posns)
                else:
                    v['pgpos'] = posns[0]

    def set_destinations(self, fn=lambda x,y,z:z, keys=None, cropme=False):
        for v in self.values():
            if v.get(' crop', False) == cropme and 'dest file' in v:
                continue            # no need to regenerate
            if keys is not None and v['anchor'][:3] not in keys:
                continue
            nB = newBase(v['src'])
            if self.srcfkey not in v:
                continue
            fpath = v[self.srcfkey]
            origExt = os.path.splitext(fpath)[1]
            v['dest file'] = fn(v, v[self.srcfkey], nB+origExt.lower())
            v[' crop'] = cropme
            if 'media' in v and len(v['media']) and 'p' not in v['media']:
                v['disabled'] = True

    def updateView(self, view, bks=None, filtered=True):
        if self.inthread:
            GObject.timeout_add_seconds(1, self.updateView, view, bks=bks, filtered=filtered)
        view.load(self, bks=bks if filtered else None)
        
    def clearSrcPaths(self):
        self.build_searchlist()
        for k, v in self.items():
            for a in ('src path', 'dest file'):
                print(k, a, v)
                if a in v:
                    print("Deleting v[a]", v[a])
                    del v[a]        
        
def PicInfoUpdateProject(model, bks, allbooks, picinfos, suffix="", random=False, cols=1, doclear=True):
    newpics = PicInfo(model)
    newpics.read_piclist(os.path.join(model.settings_dir, model.prjid, 'shared',
                                      'ptxprint', "{}.piclist".format(model.prjid)))
    delpics = set()
    if doclear:
        picinfos.clear()
    for bk in bks:
        bkf = allbooks.get(bk, None)
        if bkf is None or not os.path.exists(bkf):
            continue
        for k in [k for k,v in newpics.items() if v['anchor'][:3] == bk]:
            del newpics[k]
        for k in [k for k,v in picinfos.items() if v['anchor'][:3] == bk]:
            del picinfos[k]
        newpics.read_sfm(bk, bkf)
        newpics.set_positions(randomize=random, suffix=suffix, cols=cols)
        for k, v in newpics.items():
            if v['anchor'][:3] == bk:
                picinfos[k+suffix] = v
    picinfos.loaded = True

