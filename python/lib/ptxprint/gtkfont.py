import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ptxprint.font import TTFont, initFontCache, fccache, FontRef, parseFeatString
from ptxprint.gtkutils import makeSpinButton
import logging

logger = logging.getLogger(__name__)


def setupGtkFonts(view):
    res = GtkFonts(view)

class GtkFonts:
    _methods = """onRefreshFontsclicked onFontRclicked onLocateDigitMappingClicked
                  onFontBclicked onFontIclicked onFontBIclicked onFontRowSelected
                  getFontNameFace onFontFeaturesClicked onFontIsGraphiteClicked
                  checkFontsMissing
               """.split()
    def __init__(self, view):
        self.view = view
        self.builder = view.builder
        self.view.register(self, self._methods)

    def get(self, *a, **kw):
        return self.view.get(*a, **kw)

    def set(self, *a, **kw):
        return self.view.set(*a, **kw)

    def onRefreshFontsclicked(self, btn):
        fc = fccache()
        lsfonts = self.builder.get_object("ls_font")
        fc.fill_liststore(lsfonts)

    def onFontRclicked(self, btn, highlightWid=None):
        if self.getFontNameFace("bl_fontR", highlightWid=highlightWid):
            btn = self.builder.get_object("bl_fontR")
            self.onFontChanged(btn)
        self.checkFontsMissing()

    def onLocateDigitMappingClicked(self, btn):
        self.onFontRclicked(None, highlightWid='fcb_fontdigits')

    def onFontBclicked(self, btn):
        self.getFontNameFace("bl_fontB")
        self.checkFontsMissing()
        
    def onFontIclicked(self, btn):
        self.getFontNameFace("bl_fontI")
        self.checkFontsMissing()
        
    def onFontBIclicked(self, btn):
        self.getFontNameFace("bl_fontBI")
        self.checkFontsMissing()
        
    def onFontRowSelected(self, dat):
        lsstyles = self.builder.get_object("ls_fontFaces")
        lb = self.builder.get_object("tv_fontFamily")
        sel = lb.get_selection()
        ls, row = sel.get_selected()
        if row is not None:
            name = ls.get_value(row, 0)
            initFontCache().fill_cbstore(name, lsstyles)
            self.builder.get_object("fcb_fontFaces").set_active(0)
            self.set("t_fontFeatures", "")

    def _getSelectedFont(self, fallback=""):
        lb = self.builder.get_object("tv_fontFamily")
        sel = lb.get_selection()
        ls, row = sel.get_selected()
        if row is None:
            return (fallback, None)
        name = ls.get_value(row, 0) or fallback
        style = self.get("fcb_fontFaces")
        if style.lower() == "regular":
            style = ""
        return (name, style)

    def checkFontsMissing(self):
        self.view.setPrintBtnStatus(4, "")
        for f in ['R','B','I','BI']:
            if self.get("bl_font" + f) is None:
                logger.debug(f"bl_font: {f} is None. {getcaller()}")
                self.view.setPrintBtnStatus(4, _("Font(s) not set"))
                return True
        return False

    def getFontNameFace(self, btnid, noStyles=False, noFeats=False, highlightWid=None):
        btn = self.builder.get_object(btnid) if btnid is not None else None
        f = self.get(btnid) if btnid is not None else None
        lb = self.builder.get_object("tv_fontFamily")
        ls = lb.get_model()
        fc = initFontCache()
        fc.wait()
        fc.fill_liststore(ls)
        dialog = self.builder.get_object("dlg_fontChooser")
        if f is None:
            i = 0
            isGraphite = False
            feats = ""
            hasfake = False
            embolden = None
            italic = None
            extend = None
            isCtxtSpace = False
            mapping = "Default"
            tfont = self.get("bl_fontR")
            name = tfont.name if tfont is not None else None
        else:
            for i, row in enumerate(ls):
                if row[0] == f.name:
                    break
            else:
                i = 0
            isGraphite = f.isGraphite
            isCtxtSpace = f.isCtxtSpace
            feats = f.asFeatStr()
            embolden = f.getFake("embolden")
            italic = f.getFake("slant")
            extend = f.getFake("extend") or "1.0"
            hasfake = embolden is not None or italic is not None
            mapping = f.getMapping()
            name = f.name
        lb.set_cursor(i)
        lb.scroll_to_cell(i)
        if name is not None:
            tv = self.builder.get_object("tv_fontFamily")
            tm = self.builder.get_object("ls_font")
            try:
                tp = [x[0] for x in tm].index(name)
            except ValueError:
                tp = None
            if tp is not None:
                ti = tm.get_iter(Gtk.TreePath.new_from_indices([tp]))
                tv.get_selection().select_iter(ti)
                logger.debug("Found {} in font dialog at {}".format(name, tp))
        self.builder.get_object("t_fontSearch").set_text("")
        self.builder.get_object("t_fontSearch").has_focus()
        self.builder.get_object("fcb_fontFaces").set_sensitive(not noStyles)
        self.builder.get_object("t_fontFeatures").set_text(feats)
        self.builder.get_object("t_fontFeatures").set_sensitive(not noFeats)
        self.builder.get_object("c_fontGraphite").set_active(isGraphite)
        self.builder.get_object("c_fontCtxtSpaces").set_active(isCtxtSpace)
        self.builder.get_object("s_fontBold").set_value(float(embolden or 0.))
        self.builder.get_object("s_fontItalic").set_value(float(italic or 0.))
        self.builder.get_object("s_fontExtend").set_value(float(extend or 1.0))
        self.builder.get_object("c_fontFake").set_active(hasfake)
        self.builder.get_object("fcb_fontdigits").set_active_id(mapping)
        for a in ("Bold", "Italic"):
            self.builder.get_object("s_font"+a).set_sensitive(hasfake)
        # dialog.set_default_response(Gtk.ResponseType.OK)

        if highlightWid is not None:
            w = self.builder.get_object(highlightWid)
            w.get_style_context().add_class("highlighted")
            
        response = dialog.run()
        if highlightWid is not None:
            w = self.builder.get_object(highlightWid)
            w.get_style_context().remove_class("highlighted")
        if response == Gtk.ResponseType.OK:
            (name, style) = self._getSelectedFont(name)
            if self.get("c_fontFake"):
                bi = (self.get("s_fontBold"), self.get("s_fontItalic"))
            else:
                bi = None
            f = FontRef.fromDialog(name, style, self.get("c_fontGraphite"), 
                                   self.get("c_fontCtxtSpaces"), self.get("t_fontFeatures"),
                                   bi, self.get("s_fontExtend"), self.get("fcb_fontdigits"))
            if btnid is not None:
                self.set(btnid, f)
            res = True
        else:
            res = False
        dialog.hide()
        return res

    def onFontFeaturesClicked(self, btn):
        (name, style) = self._getSelectedFont()
        if name is None:
            return
        f = TTFont(name, style)
        if f is None:
            return
        isGraphite = self.get("c_fontGraphite")
        dialog = self.builder.get_object("dlg_features")
        featbox = self.builder.get_object("box_featsFeatures")
        lslangs = self.builder.get_object("ls_featsLangs")
        if isGraphite:
            feats = f.feats
            vals = f.featvals
            langs = getattr(f, 'grLangs', {})
            self.currdefaults = f.featdefaults
            langfeats = f.langfeats
            tips = {}
        else:
            feats = f.otFeats
            vals = f.otVals
            langs = f.otLangs
            self.currdefaults = {}
            langfeats = {}
            tips = f.tipFeats

        numrows = len(feats)
        (lang, setfeats) = parseFeatString(self.get("t_fontFeatures"), defaults=self.currdefaults, langfeats=langfeats)
        for i, (k, v) in enumerate(sorted(feats.items())):
            featbox.insert_row(i)
            l = Gtk.Label(label=v+":")
            l.set_halign(Gtk.Align.END)
            if k in tips:
                l.set_tooltip_markup(tips[k])
            featbox.attach(l, 0, i, 1, 1)
            l.show()
            inival = int(setfeats.get(k, -1))
            if k in vals:
                if len(vals[k]) < 3:
                    obj = Gtk.CheckButton()
                    if k in vals and len(vals[k]) > 1:
                        obj.set_tooltip_text(vals[k][1])
                    obj.set_active(max(inival, 0))
                else:
                    obj = Gtk.ComboBoxText()
                    for j, n in sorted(vals[k].items()):
                        obj.append(str(j), n)
                    obj.set_active(inival+1)
                    obj.set_entry_text_column(1)
            elif k == "aalt":
                obj = makeSpinButton(0, 100, 0)
                obj.set_value(max(inival, 0))
            else:
                obj = Gtk.CheckButton()
                obj.set_active(max(inival, 0))
            obj.set_halign(Gtk.Align.START)
            featbox.attach(obj, 1, i, 1, 1)
            obj.show()
        lslangs.clear()
        for k, v in sorted(langs.items()):
            lslangs.append([v, k])
        if lang is not None:
            self.set("fcb_featsLangs", lang, mod=False)
        def onLangChanged(fcb):
            newlang = self.get("fcb_featsLangs")
            newdefaults = langfeats.get(newlang, self.currdefaults)
            logger.debug("New defaults for lang {}: {}".format(newlang, newdefaults))
            for i, (k, v) in enumerate(sorted(feats.items())):
                if newdefaults.get(k, 0) == self.currdefaults.get(k, 0):
                    continue
                obj = featbox.get_child_at(1, i)
                logger.debug("Changing feature {} in lang {}".format(k, newlang))
                if isinstance(obj, Gtk.CheckButton):
                    if (1 if obj.get_active() else 0) == self.currdefaults.get(k, 0):
                        obj.set_active(newdefaults.get(k, 0) == 1)
                elif isinstance(obj, GtkSpinButton):
                    if obj.get_value() == self.currdefaults.get(k, 0):
                        obj.set_value(newdefaults.get(k, 0))
                elif isinstance(obj, Gtk.ComboBoxText):
                    if obj.get_active_id() == self.currdefaults.get(k, 0):
                        ob.set_active_id(newdefaults.get(k, 0))
            self.currdefaults = newdefaults
        langChangedId = self.builder.get_object("fcb_featsLangs").connect("changed", onLangChanged)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            results = []
            lang = self.get("fcb_featsLangs")
            if lang is not None:
                results.append("language="+lang)
                self.currdefaults = langfeats.get(lang, self.currdefaults)
            for i, (k, v) in enumerate(sorted(feats.items())):
                obj = featbox.get_child_at(1, i)
                if isinstance(obj, Gtk.CheckButton):
                    val = 1 if obj.get_active() else None
                elif isinstance(obj, Gtk.SpinButton):
                    val = int(obj.get_value()) or None
                elif isinstance(obj, Gtk.ComboBoxText):
                    val = int(obj.get_active_id())
                    val = val - 1 if val else None
                if val is not None and str(self.currdefaults.get(k, None)) != str(val):
                    results.append("{}={}".format(k, val))
            self.set("t_fontFeatures", ", ".join(results), mod=False)
        for i in range(numrows-1, -1, -1):
            featbox.remove_row(i)
        self.builder.get_object("fcb_featsLangs").disconnect(langChangedId)
        dialog.hide()

    def onFontIsGraphiteClicked(self, btn):
        self.onSimpleClicked(btn)
        self.set("t_fontFeatures", "", mod=False)

