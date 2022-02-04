import re
from gi.repository import Gtk
from ptxprint.utils import textocol
import re

fieldmap = {
    "filename":     "lb_sbFilename",
    "width":        "s_sbi_scaleWidth",
    "height":       "s_sbi_scaleHeight",
    "lockratio":    "c_sbi_lockRatio"
}

bgfieldmap = {
    "color":    "col_sbiBgColor",
    "alpha":    "s_sbiAlpha",
    "low":      "fcb_sbiLayerOrder",
    "oversize": "fcb_sbiOversize"
}

fgfieldmap = {
    "above":    "fcb_sbi_posn_above",
    "beside":   "fcb_sbi_posn_beside",
    "cutout":   "fcb_sbi_posn_cutout"
}
    

def imageStyleFromStyle(tgt, mkr, isbg):
    needres = False
    prefix = "BgImage" if isbg else "FgImage"
    if not tgt.haskey(mkr, prefix):
        return None
    self = ImageStyle(isbg)
    self.filename = tgt.getval(mkr, prefix)
    if isbg:
        for k in bgfieldmap.keys():
            val = tgt.getval(mkr, prefix + k.title())
            setattr(self, k, val)
    else:
        self.pos = tgt.getval(mkr, "FgImagePos") or "t"
        if self.pos[0] in "bt":
            self.position = "above"
        elif self.pos[0] == "s":
            self.position = "beside"
        elif self.pos[0] == "c":
            self.position = "cutout"
            m = re.match(r"^(\D+)(\d*)", self.pos)
            if m:
                self.lines = m.group(2) or "0"
                self.pos = m.group(1)
        else:
            raise SyntaxError("Unknown FgImagePos for {}".format(mkr))
    scales = tgt.getval(mkr, prefix+"Scale", "").split("x")
    for i, v in enumerate(("width", "height")):
        setattr(self, v, (scales[i] if i < len(scales) else None) or "1.0")
    self.lockratio = self.width == self.height
    return self


class ImageStyle:
    def __init__(self, isBackground=True):
        self.isbg = isBackground

    def run(self, view):
        dialog = view.builder.get_object("dlg_SBimage")
        groundframe = view.builder.get_object("fr_sbBackground" if self.isbg else "fr_sbForeground")
        groundframe.set_visible(True)
        groundoframe = view.builder.get_object("fr_sbForeground" if self.isbg else "fr_sbBackground")
        groundoframe.set_visible(False)
        frtitle = view.builder.get_object("l_sbFGorBG")
        frtitle.set_label("Sidebar Background" if self.isbg else "Sidebar Foreground")
        dialog.set_keep_above(True)
        self.initdialog(dialog, view)
        response = dialog.run()
        # print(f"{Gtk.ResponseType.__enum_values__[response]=}")
        if response == Gtk.ResponseType.OK:
            self.fromdialog(dialog, view)
            res = True
        else:
            res = False
        dialog.set_keep_above(False)
        dialog.hide()
        return res

    def _dialogfrommap(self, dialog, view, fmap):
        for k, v in fmap.items():
            val = getattr(self, k, None)
            if val is not None:
                view.set(v, val)

    def initdialog(self, dialog, view):
        self._dialogfrommap(dialog, view, fieldmap)
        if self.isbg:
            self._dialogfrommap(dialog, view, bgfieldmap)
            self.color = textocol(getattr(self, "color", "x000000"))
        else:
            posn = getattr(self, 'position', 'above')
            view.set("r_sbiPosn", posn)
            view.set("fcb_sbi_posn_{}".format(posn), getattr(self, 'pos', None))
            if posn == "cutout":
                view.set("s_sbiCutoutLines", getattr(self, 'lines', "2"))

    def _fromdialogmap(self, dialog, view, fmap):
        for k, v in fmap.items():
            val = view.get(v)
            setattr(self, k, val)

    def fromdialog(self, dialog, view):
        self._fromdialogmap(dialog, view, fieldmap)
        if self.lockratio:
            self.height = self.width
        if self.isbg:
            self._fromdialogmap(dialog, view, bgfieldmap)
            self.color = textocol(self.color)
        else:
            self.position = view.get("r_sbiPosn")
            self.pos = view.get("fcb_sbi_posn_{}".format(self.position))
            if self.position == "cutout":
                self.lines = int(view.get("s_sbiCutoutLines"))

    def _tostylemap(self, tgt, mkr, prefix, fmap):
        for k, v in fmap.items():
            val = getattr(self, k, None)
            if val is None:
                continue
            key = prefix + k.title() if prefix is not None else k
            tgt.setval(mkr, key, val)

    def toStyle(self, tgt, mkr):
        fname = getattr(self, 'filename', "")
        if not len(fname):      # no filename, all else is pointless
            return
        if self.isbg:
            prefix = "BgImage"
            self._tostylemap(tgt, mkr, prefix, bgfieldmap)
        else:
            pos = getattr(self, 'pos', 'tl')
            if self.position == "cutout":
                cut = int(getattr(self, 'lines', "2"))
                if cut != 0:
                    pos += str(cut)
            tgt.setval(mkr, 'FgImagePos', pos)
            prefix = "FgImage"
        tgt.setval(mkr, prefix, fname)
        scales = [float(getattr(self, a, "0")) for a in ('width', 'height')]
        scale = str(scales[0]) if 0. < scales[0] != 1. else ""
        scale += "x{}".format(scales[1]) if 0. < scales[1] != 1. else ""
        if len(scale):
            tgt.setval(mkr, prefix+"Scale", scale)

    def removeStyle(self, tgt, mkr):
        prefix = "BgImage" if self.isbg else "FgImage"
        for k in fieldmap.keys():
            if k == "filename":
                k = ""
            tgt.setval(mkr, prefix + k.title(), None)
        if self.isbg:
            for k in bgfieldmap.keys():
                tgt.setval(mkr, prefix + k.title(), None)
        else:
            tgt.setval(mkr, 'FgImagePos', None)
            
