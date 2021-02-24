
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.piclist import newBase
from ptxprint.utils import refKey, lang, _
from gi.repository import Gtk, GdkPixbuf, GObject, Gdk
import os

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

_piclistfields = ["anchor", "caption", "src", "size", "scale", "pgpos", "ref", "alt", "copy", "mirror", 
                  "disabled", "cleardest", "key", "media"]
_pickeys = {k:i for i, k in enumerate(_piclistfields)}

_comblist = ['pgpos', 'hpos', 'nlines']
_comblistcr = ['crVpos', 'crHpos']

newrowcounter = 1


class PicList:
    def __init__(self, view, builder, parent):
        self.view = view
        self.loading = False
        self.checkinv = False
        self.checkfilt = 0
        self.coremodel = view.get_model()
        self.model = self.coremodel.filter_new()
        self.model.set_visible_func(self.checkfilter)
        self.view. set_model(self.model)
        self.builder = builder
        self.parent = parent
        self.picinfo = None
        self.selection = view.get_selection()
        self.picrect = None
        self.currow = None
        self.curriter = None
        self.bookfilters = None
        sel = self.view.get_selection()
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
        self.model.refilter()

    def modify_font(self, p):
        w = self.builder.get_object("cr_caption")
        w.set_property("font-desc", p)

    def isEmpty(self):
        return len(self.model) == 0

    def clear(self):
        self.coremodel.clear()

    def load(self, picinfo, bks=None):
        self.picinfo = picinfo
        #self.view.set_model(None)
        self.coremodel.clear()
        self.bookfilters = bks
        if picinfo is not None:
            for k, v in sorted(picinfo.items(), key=lambda x:refKey(x[1]['anchor'])):
                if bks is not None and len(bks) and v['anchor'][:3] not in bks:
                    continue
                row = []
                #defaultmedia = _picLimitDefault.get(v.get('src', '')[:2].lower(), ('paw', 'paw', 'Default'))
                defaultmedia = self.parent.copyrightInfo.get(v.get('src', '')[:2].lower(),
                    { "default": "paw", "limit": "paw", "tip": {"en": "Default"}})
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
                            val = defaultmedia["default"]
                        else:
                            val = "".join(x for x in val if x in defaultmedia["limit"])
                    else:
                        val = v.get(e, "")
                    row.append(val)
                self.coremodel.append(row)
        #self.view.set_model(self.model)
        self.model.refilter()
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
            if k.startswith("row"):
                print(f"{k} added")
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
                if k.startswith("row"):
                    print(f"{k} removed")
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
        s = self.view.get_selection()
        if s != selection:
            self.loading = True
            m = self.view.get_model()
            fpath = cpath if s == self.selection else m.convert_child_path_to_path(cpath)
            if fpath is not None:
                s.select_path(fpath)
                self.view.scroll_to_cell(fpath)
            else:
                s.unselect_all()
            self.loading = False
        if selection != self.selection:
            self.parent.savePicChecks()
            if not self.model.do_visible(self.model, self.model.get_model(), cit):
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
            # print(j, k, v)
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
            elif k == 'copy': # If we already have the copyright information, then don't let them enter it unnecessarily
                val = self.currow[j]
                figname = self.currow[_pickeys['src']]
                status = True if len(re.findall(r"(?i)_?((?=cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abc]?", figname)) else False
                self.builder.get_object('l_autoCopyAttrib').set_visible(status)
                self.builder.get_object(v).set_visible(not status)
            else:
                try:
                    val = self.currow[j]
                except IndexError: 
                    print("k, j:", k, j)
            w = self.builder.get_object(v)
            try:
                setWidgetVal(v, w, val)
            except (ValueError, TypeError):
                print(v, w, val)
            
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
        inf = self.parent.copyrightInfo.get(src.lower(), {"limit": "paw", "tip": {"en": "Default"}})
        tip = inf["tip"].get(lang, inf["tip"]["en"])
        if inf["tip"]["en"] == 'Default':
            self.builder.get_object("l_plMedia").set_tooltip_text(_("Media permissions unknown\nfor this illustration"))
        else:
            self.builder.get_object("l_plMedia").set_tooltip_text(_("Permission for {} series:\n{}").format(src.upper(), tip))
        val = row[_pickeys['media']]
        for c in 'paw':
            w = _form_structure["med"+c.upper()]
            wid = self.builder.get_object(w)
            if wid is not None:
                wid.set_sensitive(c in inf["limit"])
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

    def get_crpos(self):
        res = "".join(self.get(k, default="") for k in _comblistcr)
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
                        dat = self.picinfo.getFigureSources(data={'1': {'src': val}},
                                    key='path', exclusive=self.parent.get("c_exclusiveFiguresFolder"))
                        fpath = dat['1'].get('path', None)
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
            elif key == "size" and val != oldval: # Trigger a new copy of the image, since ratio may change
                self.currow[_piclistfields.index('cleardest')] = True
            elif key == "mirror" and val == "None":
                self.currow[fieldi] = ""
            if not self.loading:
                self.model.set_value(self.curriter, fieldi, self.currow[fieldi])

    def setPreview(self, pixbuf, tooltip=None):
        pic = self.builder.get_object("img_picPreview")
        if pixbuf is None:
            pic.clear()
            tooltip = ""
        else:
            pic.set_from_pixbuf(pixbuf)
        if tooltip is not None:
            pic.set_tooltip_text(tooltip)
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
        global newrowcounter
        if len(self.model) > 0:
            row = self.model[self.selection.get_selected()[1]][:]
        else:
            row = self.get_row_from_items()
        row[_pickeys['key']] = "row{}".format(newrowcounter)
        print(f"{row[_pickeys['key']]}", sorted(self.picinfo.keys()))
        newrowcounter += 1
        self.coremodel.append(row)
        self.select_row(len(self.model)-1)

    def del_row(self):
        model, i = self.selection.get_selected()
        ci = model.convert_iter_to_child_iter(i)
        del self.coremodel[ci]
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

