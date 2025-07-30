
from ptxprint.gtkutils import getWidgetVal, setWidgetVal
from ptxprint.piclist import newBase, Picture
from ptxprint.utils import refSort, getlang, _, f2s, pycodedir
from gi.repository import Gtk, GdkPixbuf, GObject, Gdk, GLib
from typing import Dict
from shutil import rmtree
import os, re
import logging

logger = logging.getLogger(__name__)

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
    'medW':     'c_plMediaW',
    'x-xetex':  't_picXetex'
}

_singlefields = ("anchor", "caption", "src", "ref", "alt", "x-xetex")

_piclistfields = ["anchor", "caption", "src", "size", "scale", "pgpos", "ref", "alt", "copy", "mirror", "captionR",
                  "disabled", "cleardest", "key", "media", "x-xetex"]
_pickeys = {k:i for i, k in enumerate(_piclistfields)}

_sizekeys = {"P": "page", "F": "full", "c": "col", "s": "span"}

_comblist = ['pgpos', 'hpos', 'nlines']
_comblistcr = ['crVpos', 'crHpos']

newrowcounter = 1
previewBuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(pycodedir(), "picLocationPreviews.png"))

_locGrid = {
"1"   :    (0,0),"1-b":     (1,0),"1-cl":    (2,0),"1-cr":   (3,0),"1-hc":    (4,0),"1-hl":    (5,0),"1-hr":    (6,0),"1-p":     (7,0),
"1-pa":    (0,1),"1-pb":    (1,1),"1-t":     (2,1),"2":      (3,1),"2-col-bl":(4,1),"2-col-br":(5,1),"2-col-cl":(6,1),"2-col-cr":(7,1),
"2-col-hc":(0,2),"2-col-hl":(1,2),"2-col-hr":(2,2),"2-col-p":(3,2),"2-col-pa":(4,2),"2-col-pb":(5,2),"2-col-tl":(6,2),"2-col-tr":(7,2),
"2-span-b":(0,3),"2-span-t":(1,3),"full":    (2,3),"page":   (3,3)
}
    
def dispLocPreview(key):
    x,y = _locGrid.get(key, (7,3))
    x = x * 212 + 14
    y = y * 201 + 10
    pic = previewBuf.new_subpixbuf(x,y,130,180)
    return pic

def getLocnKey(cols, frSize, pgposLocn):
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
    locnKey = re.sub(r'\-?\d*\.?\d$', '', locnKey)
    locnKey = re.sub(r'B', 'b', locnKey)  # Until we get some updated graphics
    # print(f"{cols=} {frSize=} {pgposLocn=} ==> {locnKey=}")
    return locnKey

class PicList:
    def __init__(self, view, builder, parent):
        self.view = view
        self.loading = False
        self.checkinv = False
        self.checkfilt = 0
        self.coremodel = view.get_model()
        self.model = self.coremodel.filter_new()
        self.model.set_visible_func(self.checkfilter)
        self.view.set_model(self.model)
        self.builder = builder
        self.parent = parent
        self.picinfo: Optional[Piclist] = None
        self.selection = view.get_selection()
        self.picrect = None
        self.currows = []
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
        # self.previewBuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(pycodedir(), "picLocationPreviews.png"))
        self.clear()
        self.loading = False

    def checkfilter(self, model, i, data):
        if self.loading:
            return False
        if self.checkfilt <= 0:
            return True
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
        for a in ["cr_caption", "cr_caption2"]:
            w = self.builder.get_object(a)
            w.set_property("font-desc", p)

    def isEmpty(self):
        return len(self.model) == 0

    def clear(self):
        self.coremodel.clear()
        self.clearPreview()

    def pause(self):
        self.view.set_model(None)

    def unpause(self):
        self.view.set_model(self.model)
        self.model.refilter()

    def _loadrow(self, pic):
        row = []
        #defaultmedia = _picLimitDefault.get(v.get('src', '')[:2].lower(), ('paw', 'paw', 'Default'))
        defaultmedia = self.parent.readCopyrights().get(pic.get('src', '')[:2].lower(),
            { "default": "paw", "limit": "paw", "tip": {"en": "Default"}})
        for e in _piclistfields:
            if e == 'key':
                val = pic.key
            elif e == "scale":
                try:
                    val = float(pic.get(e, 1)) * 100
                except (ValueError, TypeError):
                    val = 100.
            elif e == 'cleardest':
                val = False
            elif e == "disabled":
                val = pic.get(e, False)
            elif e == 'captionR':
                val = pic.get(e, pic.get('captionL', ""))
            elif e == "media":
                val = pic.get(e, None)
                if val is None:
                    val = self.parent.picMedia(pic.get('src', ''))[0]
                else:
                    limit = self.parent.picMedia(pic.get('src',''))[1]
                    val = "".join(x for x in val if x in limit)
            else:
                val = pic.get(e, "")
            row.append(val)
        return row

    def load(self, picinfo, bks=None):
        self.loading = True
        self.picinfo = picinfo
        #self.view.set_model(None)
        self.coremodel.clear()
        self.clearPreview()
        self.bookfilters = bks
        if picinfo is not None:
            for v in sorted(picinfo.get_pics(), key=lambda x:refSort(x['anchor'])):
                if bks is not None and len(bks) and v['anchor'][:3] not in bks:
                    continue
                row = self._loadrow(v)
                self.coremodel.append(row)
        #self.view.set_model(self.model)
        self.loading = False
        self.model.refilter()
        self.select_row(0)

    def get(self, wid, default=None):
        wid = _form_structure.get(wid, wid)
        w = self.builder.get_object(wid)
        res = getWidgetVal(wid, w, default=default)
        if wid.startswith("s_"):
            res = float(res) if res.find(".") >= 0 else int(res)
        return res

    def updateinfo(self, picinfos):
        allkeys = set()
        for row in self.model:
            k = row[_pickeys['key']]
            # if k.startswith("row"):
                # print(f"{k} added")
            p = picinfos.get(k, {})
            for i, e in enumerate(_piclistfields):
                if e == 'key':
                    allkeys.add(row[i])
                    continue
                elif e == 'scale':
                    val = f2s(row[i] / 100.)
                elif e == "cleardest":
                    if row[i] and 'destfile' in p:
                        del p['destfile']
                    continue
                else:
                    val = row[i]
                p[e] = val
#        breakpoint()
#        for k,v in list(picinfos.items()):
#            if k not in allkeys and (self.bookfilters is None or v['anchor'][:3] in self.bookfilters):
#                if k.startswith("row"):
#                    print(f"{k} removed")
#                picinfos.remove(v)
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
                    if row[i] and 'destfile' in p:
                        del p['destfile']
                    continue

    def row_select(self, selection, update=True): # Populate the form from the model
        if self.loading or selection.count_selected_rows() == 0:
            return
        if update and self.currows:
            if not self.currows[-1][_pickeys['anchor']]:
                w = self.builder.get_object("t_plAnchor")
                w.get_style_context().add_class("highlighted")
                self.parent.doError(_("Missing: 'Anchor Ref'"), secondary=_("You must provide a Book Ch.Vs reference as an anchor for the picture. For example: GEN 14.19"))
                return
            for k, s in ((k, x) for k,x in _form_structure.items() if x.startswith("s_")):
                w = self.builder.get_object(s)
                if w.has_focus():
                    e = Gdk.Event(Gdk.EventType.FOCUS_CHANGE)
                    e.window = w
                    e.send_event = True
                    w.emit("focus-out-event", e)
        model, paths = selection.get_selected_rows()
        self.currows = []
        for i, path in enumerate(paths):
            cpath = model.convert_path_to_child_path(path)
            cit = self.model.get_iter(cpath)
            if i == 0 and self.curriter != cit:
                self.parent.savePicChecks()
                if not self.model.do_visible(self.model, self.model.get_model(), cit):
                    return
                self.curriter = cit
            self.currows.append(self.model[cit][:])    # copy it so that any edits don't mess with the model if the iterator moves
            self.currows[-1].append(cit)
        currow = self.currows[0]
        if not currow[_pickeys['pgpos']]:
            pgpos = ""
        else:
            pgpos = re.sub(r'^([PF])([lcrio])([tfb])', r'\1\3\2', currow[_pickeys['pgpos']])
        self.parent.pause_logging()
        # self.loading = True
        for j, (k, v) in enumerate(_form_structure.items()): # relies on ordered dict
            # print(j, k, v)
            if k == 'pgpos':
                val = pgpos[1:2] if pgpos[0:1] in "PF" else (pgpos[0:1] or "t")
            elif k == 'hpos':
                if currow[_pickeys['size']] == "span":
                    val = "-"
                elif pgpos[0:1] in "PF":
                    val = pgpos[2:] or "c"
                else:
                    val = pgpos[1:] or ""
            elif k == 'nlines':
                val = re.sub(r'^[^\-\d.]*', "", pgpos)
                try:
                    val = int(float(val) * 100) / 100.
                except (ValueError, TypeError):
                    val = 0
            elif k.startswith("med"):
                val = v[-1].lower() in (currow[_pickeys['media']] or "paw")
            elif k == 'mirror':
                val = currow[j] or "None"
            elif k == 'copy': # If we already have the copyright information, then don't let them enter it unnecessarily
                val = currow[j]
                figname = currow[_pickeys['src']]
                status = True if len(re.findall(r"(?i)_?((?=cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abc]?", figname)) else False
                self.builder.get_object('l_autoCopyAttrib').set_visible(status)
                self.builder.get_object(v).set_visible(not status)
            elif k == 'size':
                val = pgpos[0:1] if pgpos[0:1] in "PF" else ("c" if any(x in pgpos for x in "rl") else "s")
                val = _sizekeys.get(val, "span")
            else:
                try:
                    val = currow[j]
                except IndexError: 
                    print("k, j:", k, j)
            w = self.builder.get_object(v)
            if k in _singlefields:
                w.set_sensitive(len(self.currows) == 1)
            try:
                setWidgetVal(v, w, val)
            except (ValueError, TypeError):
                print(v, w, val)
            
        self.mask_media(currow)
        self.parent.unpause_logging()
        self.loading = False

    def select_row(self, i):
        if isinstance(i, Gtk.TreeIter):
            treeiter = i
        else:
            if i >= len(self.model):
                i = len(self.model) - 1
            if i < 0:
                return
            treeiter = self.model.get_iter_from_string(str(i))
        self.selection.unselect_all()
        self.selection.select_iter(treeiter)

    def find_row(self, anchor):
        ''' returns an iterator for a give anchor or None '''
        it = self.model.get_iter_first()
        while it is not None:
            r = self.model[it]
            if r[_pickeys['anchor']] == anchor:
                return it
            it = self.model.iter_next(it)
        return None

    def set_val(self, it, **kw):
        r = self.model[it]
        for k, v in kw.items():
            if k in _pickeys:
                # if k == 'scale':
                    # r[_pickeys[k]] = int(float(v) * 100)
                # else:
                r[_pickeys[k]] = v
        if self.selection is not None and self.selection.iter_is_selected(it):
            self.row_select(self.selection, update=False)

    def mask_media(self, row):
        src = row[_pickeys['src']][:2]
        inf = self.parent.copyrightInfo['copyrights'].get(src.lower(), {"media": {"default": "paw", "limit": "paw", "tip": {"en": "Default"}}})["media"]
        tip = inf["tip"].get(getlang()[0], inf["tip"]["en"])
        if inf["tip"]["en"] == 'Default':
            self.builder.get_object("l_plMedia").set_tooltip_text(_("Media permissions unknown\nfor this illustration"))
        else:
            self.builder.get_object("l_plMedia").set_tooltip_text(_("Permission for {} series:\n{}").format(src.upper(), tip))
        val = row[_pickeys['media']]
        for c in 'paw':
            w = _form_structure["med"+c.upper()]
            wid = self.builder.get_object(w)
            if val is None or val == "":
                isactive = c in inf["default"]
                # isactive = False # c in inf["limit"]
            else:
                isactive = c in val
            if wid is not None:
                wid.set_sensitive(c in inf["limit"])
            wid.set_active(isactive)

    def get_pgpos(self):
        res = "".join(self.get(k, default="") for k in _comblist[:-1]).replace("-", "")
        # if res.startswith("c"):
            # res += str(self.get(_comblist[-1]))
        res = re.sub(r'([PF])([tcb])([lcrio])', r'\1\3\2', res)
        if len(res) and res[0] in "PF":
            res = res.strip("c")
        lines = self.get("nlines", 0)
        if lines != 0 and len(res) and res[0] in "pc":
            res += str(lines)
        return res

    def get_crpos(self):
        res = "".join(self.get(k, default="") for k in _comblistcr)
        return res

    def item_changed(self, w, *a):
        key = a[-1]
        if self.loading: # and key not in ("src", ):
            return
        if key in _comblist:
            val = self.get_pgpos()
            key = "pgpos"
        elif key.startswith("med"):
            val = "".join(v[-1].lower() for k, v in _form_structure.items() if k.startswith("med") and self.get(v))
            if val == "":
                val = "x"
            key = "media"
        else:
            val = self.get(key)
        for i, currow in enumerate(self.currows):
            fieldi = _piclistfields.index(key)
            oldval = currow[fieldi]
            currow[fieldi] = val
            r_image = self.parent.get("r_image", default="preview")
            if i == 0 and r_image == "location":
                if self.get("c_doublecolumn"):
                    cols = 2
                else:
                    cols = 1
                if not self.get("c_plMediaP"):
                    locKey = "1" if cols == 1 else "2"
                else:
                    frSize = self.currows[0][_pickeys['size']]
                    pgposLocn = self.currows[0][_pickeys['pgpos']]
                    locKey = getLocnKey(cols, frSize, pgposLocn)
                pic = dispLocPreview(locKey)
                self.setPreview(pic)
            if key == "src":
                if r_image == "preview":
                    fpath = None
                    if self.picinfo is not None:
                        exclusive = self.parent.get("c_exclusiveFiguresFolder")
                        fldr      = self.parent.get("lb_selectFigureFolder", "") if self.parent.get("c_useCustomFolder") else ""
                        imgorder  = self.parent.get("t_imageTypeOrder")
                        lowres    = self.parent.get("r_pictureRes") == "Low"
                        a = currow[_pickeys['anchor']]
                        for p in self.picinfo.find(anchor=a):
                            p.clear_src_paths()
                        dat = self.picinfo.getFigureSources(data=[{'src': val}], key='path', exclusive=exclusive,
                                    mode=self.picinfo.mode, figFolder=fldr, imgorder=imgorder, lowres=lowres)
                        fpath = dat[0].get('path', None)
                        logger.debug(f"Figure Path={fpath}, {dat[0]}")
                    if fpath is not None and os.path.exists(fpath):
                        if self.picrect is None:
                            picframe = self.builder.get_object("fr_picPreview")
                            self.picrect = picframe.get_allocation()
                        if self.picrect.width > 10 and self.picrect.height > 10:
                            try:
                                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(fpath, self.picrect.width - 6, self.picrect.height - 6)
                            except GLib.GError:
                                pixbuf = None
                            self.setPreview(pixbuf, tooltip=fpath)
                        else:
                            self.setPreview(None)
                    else:
                        self.setPreview(None)
                self.parent.updatePicChecks(val)       # only update checks if src exists
                self.mask_media(currow)
                if True: # val != oldval: # New source implies new destination file
                    currow[_piclistfields.index('cleardest')] = True
            elif key == "size" and val != oldval: # Trigger a new copy of the image, since ratio may change
                currow[_piclistfields.index('cleardest')] = True
            elif key == "mirror" and val == "None":
                currow[fieldi] = ""
            if not self.loading:
                self.model.set_value(currow[-1], fieldi, currow[fieldi])

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
        if self.loading or self.parent.loadingConfig:
            return
        tmpPicpath = os.path.join(self.parent.project.printPath(self.parent.cfgid), "tmpPics")
        # rmtree(tmpPicpath, ignore_errors = True)
        exclusive = self.parent.get("c_exclusiveFiguresFolder")
        fldr      = self.parent.get("lb_selectFigureFolder", "") if self.parent.get("c_useCustomFolder") else ""
        imgorder  = self.parent.get("t_imageTypeOrder")
        lowres    = self.parent.get("r_pictureRes") == "Low"
        self.picinfo.build_searchlist(figFolder=fldr, exclusive=exclusive, imgorder=imgorder, lowres=lowres)
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

    def add_row(self, pic=None):
        global newrowcounter
        model, sel = self.selection.get_selected_rows()
        #if sel is not None and len(sel):
        #    sel = model.convert_path_to_child_path(sel[0])
        #if sel is not None and len(self.model) > 0:
        #    row = self.model[self.model.get_iter(sel)][:]
        #else:
        if pic is None:
            key = "row{}".format(newrowcounter)
            newrowcounter += 1
            row = self.get_row_from_items()
        else:
            key = pic.key
            row = self._loadrow(pic)
        row[_pickeys['key']] = key
        self.picinfo[key] = pic or Picture()
        logger.debug(f"{row[_pickeys['key']]}"+", ".join(sorted([k for k, v in self.picinfo.items()])))
        self.coremodel.append(row)
        self.select_row(len(self.model)-1)
        self.row_select(self.selection)

    def del_row(self):
        self.clearPreview()
        model, paths = self.selection.get_selected_rows()
        inds = [model.convert_path_to_child_path(i) for i in paths]
        for i in reversed(sorted(inds)):
            ci = self.coremodel.get_iter(i)
            del self.picinfo[self.coremodel[ci][_pickeys['key']]]
            del self.coremodel[ci]
        if not len(inds):
            indt = model.get_iter_first()
            if indt is not None:
                ind = model.get_path(indt)
            else:
                ind = None
        else:
            ind = inds[0]
        if ind is not None:  # otherwise we have an empty list
            self.select_row(ind.get_indices()[0])

    def clearPreview(self):
        pic = self.builder.get_object("img_picPreview")
        pic.clear()
        tooltip = ""
        
    def set_src(self, src):
        wid = _form_structure.get('src', 'src')
        w = self.builder.get_object(wid)
        setWidgetVal(wid, w, src)

    def clearSrcPaths(self):
        if self.picinfo is not None:
            self.picinfo.clearSrcPaths()

    def multiSelected(self, ismulti=False):
        pass
