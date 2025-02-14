import re
from gi.repository import Gtk
from ptxprint.utils import textocol

fieldmap = {
    "BorderStyle":         "fcb_sbBorderStyle",
    "BorderRef":           "fcb_sbBorderOrnament",
    "BorderWidth":         "s_sbBorderWidth",
    "BorderLineWidth":     "s_sbBorderLineWidth",
    "BoxTPadding":         "s_sbBoxPadT",
    "BoxBPadding":         "s_sbBoxPadB",
    "BoxLPadding":         "s_sbBoxPadL",
    "BoxRPadding":         "s_sbBoxPadR",
    "BorderTPadding":      "s_sbBdrPadT",
    "BorderBPadding":      "s_sbBdrPadB",
    "BorderLPadding":      "s_sbBdrPadL",
    "BorderRPadding":      "s_sbBdrPadR",
    "BorderColor":         "col_sbBorderColor",
    "BorderFillColor":     "col_sbBorderFillColor",
}

styVals = {"none": 0, "plain": 1, "double": 2, "ornaments": 4}
sensitivity = {
    "lb_openOrnamentsCatalog": 4,
    "fcb_sbBorderOrnament": 4,
    "lb_sbBorderWidth": 7,
    "s_sbBorderWidth": 7,
    "lb_sbBorderLineWidth": 6,
    "s_sbBorderLineWidth": 6,
    "lb_sbBorderColor": 7,
    "col_sbBorderColor": 7,
    "lb_sbBorderFillColor": 6,
    "col_sbBorderFillColor": 6,
    "gr_bdrSides": 7,
    "fr_padding": 7,
    "fr_previewBorder": 7,
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
    if bitfield == 128: # none
        bitfield = 0
    elif bitfield == 64: # all
        bitfield = 15
    if bitfield == 0: 
        return None
    self = BorderStyle()
    for k in fieldmap.keys():
        val = tgt.getval(mkr, k)
        setattr(self, k, val)
    for i,k in enumerate(brdrs):
        if bitfield & (1<<i) != 0:
            setattr(self, k, True)
        else:
            setattr(self, k, False)
    # unpack BoxVPadding, BoxHPadding, BorderVPadding, BorderHPadding
    # remember to set c_boxPadSymmetrical and/or c_bdrPadSymmetrical
    # if the 4 values are identical when unpacking.
    # Note that BoxPadding and BorderPadding are also possible values 
    # coming back from the stylesheet.
    return self


class BorderStyle:

    def run(self, view):
        self.view = view
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
        self.BorderColor = textocol(getattr(self, "BorderColor", "x000000"))
        self.BorderFillColor = textocol(getattr(self, "BorderFillColor", "x000000"))
        self._dialogfrommap(dialog, view, fieldmap)
        self._dialogfrommap(dialog, view, bordermap)

    def _fromdialogmap(self, dialog, view, fmap):
        for k, v in fmap.items():
            val = view.get(v)
            setattr(self, k, val)

    def fromdialog(self, dialog, view):
        self._fromdialogmap(dialog, view, fieldmap)
        self._fromdialogmap(dialog, view, bordermap)
        self.BorderColor = textocol(self.BorderColor)
        self.BorderFillColor = textocol(self.BorderFillColor)

    def _tostylemap(self, tgt, mkr, fmap):
        for k, v in fmap.items():
            val = getattr(self, k, None)
            if val is None:
                continue
            tgt.setval(mkr, k, val)

    def toStyle(self, tgt, mkr):
        self._tostylemap(tgt, mkr, fieldmap)
        bitfield = sum(1<<i if getattr(self, k, False) else 0 for i,k in enumerate(brdrs))
        if bitfield == 15 or bitfield == 51: # t,b,l,r   or  t,b,i,o
            bitfield = 64
        elif bitfield == 0: # none
            bitfield = 128
        values = [brdrs[i].title() for i in range(len(brdrs)) if bitfield & (1<<i) != 0]
        tgt.setval(mkr, "Border", " ".join(values))
        # if all 4 are identical then just set BoxPadding and/or BorderPadding
        # if T&B identical, set BoxVPadding; if L&R (or I&O) identical, set BoxHPadding
        # pack BoxVPadding, BoxHPadding, BorderVPadding, BorderHPadding

    def onSBborderSettingsChanged(self):
        builder = self.view.builder
        bdrType = self.view.get('fcb_sbBorderStyle')
        borderVal = styVals[bdrType]
        for w, bits in sensitivity.items():
            sensitive = (borderVal & bits) != 0
            builder.get_object(w).set_sensitive(sensitive)
        
        thickness = float(self.view.get('s_sbBorderWidth'))
        for x in ['ox', 'dr']:
            if self.view.get(f"c_b{x}PadSymmetrical"):
                for w in "LRB":
                    self.view.set(f"s_sbB{x}Pad{w}", self.view.get(f"s_sbB{x}PadT"))
            oi = "o" if x == 'ox' else 'i'
            for w in "TBLR":
                v = float(self.view.get(f's_sbB{x}Pad{w}'))
                setattr(self, oi+w, v) # if v >= 0 else 0)
                if oi == "o":
                    outside = thickness + v
                    setattr(self, "x"+w, outside * -1.0 if outside < 0.0 else 0.0)

        builder.get_object("oT").set_visible(self.view.get('c_sbBorder_top'))
        builder.get_object("oB").set_visible(self.view.get('c_sbBorder_bot'))
        builder.get_object("oL").set_visible(self.view.get('c_sbBorder_lhs') or self.view.get('c_sbBorder_inn'))
        builder.get_object("oR").set_visible(self.view.get('c_sbBorder_rhs') or self.view.get('c_sbBorder_out'))
        builder.get_object("oT").set_size_request(-1, thickness)
        builder.get_object("oB").set_size_request(-1, thickness)
        builder.get_object("oL").set_size_request(thickness, -1)
        builder.get_object("oR").set_size_request(thickness, -1)

        # xTBLR is the [colored] box area OUTSIDE of the border 
        builder.get_object("xT").set_size_request(-1, self.xT)
        builder.get_object("xB").set_size_request(-1, self.xB)
        builder.get_object("xL").set_size_request(self.xL, -1)
        builder.get_object("xR").set_size_request(self.xR, -1)

        builder.get_object("e_box").set_property("height-request", self.iL + (self.oT / 2))
        builder.get_object("e_box").set_property("width-request", self.iT + (self.oL / 2))

        builder.get_object("tT").set_size_request(-1, self.oT)
        builder.get_object("tB").set_size_request(-1, self.oB)
        builder.get_object("tL").set_size_request(self.oL, -1)
        builder.get_object("tR").set_size_request(self.oR, -1)

        for w in "TLR":
            builder.get_object(f"o{w}").set_property("margin-top", 0) # self.oT)
            builder.get_object(f"i{w}").set_property("margin-top", self.iT)

        for w in "BLR":
            builder.get_object(f"o{w}").set_property("margin-bottom", 0) # self.oB)
            builder.get_object(f"i{w}").set_property("margin-bottom", self.iB)
        
        builder.get_object("oL").set_property("margin-left", 0) # self.oL)
        builder.get_object("oR").set_property("margin-right", 0) # self.oR)

        builder.get_object("iL").set_property("margin-left", self.iL)
        builder.get_object("iR").set_property("margin-right", self.iR)

    def boxPaddingUniformClicked(self):
        status = self.view.sensiVisible("c_boxPadSymmetrical")
        if status:
            for w in "LRB":
                self.view.set(f"s_sbBoxPad{w}", self.view.get("s_sbBoxPadT"))
        self.view.onSBborderSettingsChanged(None)
        
    def bdrPaddingUniformClicked(self):
        status = self.view.sensiVisible("c_bdrPadSymmetrical")
        if status:
            for w in "LRB":
                self.view.set(f"s_sbBdrPad{w}", self.view.get("s_sbBdrPadT"))
        self.view.onSBborderSettingsChanged(None)

    
