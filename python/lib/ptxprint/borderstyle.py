import re
from gi.repository import Gtk

fieldmap = {
    "width":      "s_sbBorderWidth",
    "vpadding":   "s_sbVpadding",
    "hpadding":   "s_sbHpadding",
    "color":      "col_sbBorderColor"
}
bordermap = {
    "top":        "c_sbBorder_top",
    "bottom":     "c_sbBorder_bot",
    "left":       "c_sbBorder_lhs",
    "right":      "c_sbBorder_rhs",
    "inner":      "c_sbBorder_inn",
    "outer":      "c_sbBorder_out"
}
              
brdrs = ["top", "bottom", "left", "right", "inner", "outer", "all", "none"]

def borderStyleFromStyle(tgt, mkr):
    needres = False
    borders = set((x.lower() for x in tgt.getval(mkr, "Border", "").split(" ")))
    bitfield = sum(1<<i if k in borders else 0 for i,k in enumerate(brdrs))
    if bitfield == 128:
        bitfield = 0
    elif bitfield == 64:
        bitfield = 15
    if bitfield == 0:
        return None
    self = BorderStyle()
    for k in fieldmap.keys():
        val = tgt.getval(mkr, "Border"+k.title())
        setattr(self, k, val)
    for i,k in enumerate(brdrs):
        if bitfield & (1<<i) != 0:
            setattr(self, k, True)
        else:
            setattr(self, k, False)
    return self


class BorderStyle:

    def run(self, view):
        dialog = view.builder.get_object("dlg_borders")
        dialog.set_keep_above(True)
        self.initdialog(dialog, view)
        response = dialog.run()
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
            elif v.startswith("c_"):
                view.set(v, False)

    def initdialog(self, dialog, view):
        self._dialogfrommap(dialog, view, fieldmap)
        self._dialogfrommap(dialog, view, bordermap)

    def _fromdialogmap(self, dialog, view, fmap):
        for k, v in fmap.items():
            val = view.get(v)
            setattr(self, k, val)

    def fromdialog(self, dialog, view):
        self._fromdialogmap(dialog, view, fieldmap)
        self._fromdialogmap(dialog, view, bordermap)

    def _tostylemap(self, tgt, mkr, fmap):
        for k, v in fmap.items():
            val = getattr(self, k, None)
            if val is None:
                continue
            tgt.setval(mkr, "Border"+k.title(), val)

    def toStyle(self, tgt, mkr):
        self._tostylemap(tgt, mkr, fieldmap)
        bitfield = sum(1<<i if getattr(self, k, False) else 0 for i,k in enumerate(brdrs))
        if bitfield == 15 or bitfield == 51:
            bitfield = 64
        elif bitfield == 0:
            bitfield = 128
        values = [brdrs[i].title() for i in range(len(brdrs)) if bitfield & (1<<i) != 0]
        tgt.setval(mkr, "Border", " ".join(values))
