from gi.repository import Gtk, Gdk
from ptxprint.utils import _

def getWidgetVal(wid, w, default=None, asstr=False, sub=0):
    v = None
    if wid.startswith("ecb_"):
        model = w.get_model()
        i = w.get_active()
        if i < 0:
            e = w.get_child()
            if e is not None and isinstance(e, Gtk.Entry):
                v = e.get_text()
        elif model is not None:
            v = model[i][sub]
    elif wid.startswith("fcb_"):
        v = w.get_active_id()
    elif wid.startswith("t_"):
        v = w.get_text()
    elif wid.startswith("tb_"):
        v = w.get_text(w.get_start_iter(), w.get_end_iter(), True)
    # elif wid.startswith("f_"):
        # v = w.get_font_name()
    elif wid.startswith("c_"):
        v = w.get_active()
    elif wid.startswith("s_"):
        v = "{:.3f}".format(w.get_value())
    elif wid.startswith("btn_"):
        v = w.get_tooltip_text()
    elif wid.startswith("bl_"):
        v = getattr(w, 'font_info', None)
    elif wid.startswith("lb_"):
        v = w.get_label()
    elif wid.startswith("l_"):
        v = w.get_text()
    elif wid.startswith("col_"):
        v = w.get_rgba().to_string()
    elif wid.startswith("nbk_"):
        v = w.get_current_page()
    if v is None:
        return default
    return v

def setWidgetVal(wid, w, value, noui=False):
    if wid.startswith("ecb_"):
        model = w.get_model()
        e = w.get_child()
        for i, v in enumerate(model):
            if v[w.get_entry_text_column()] == value:
                w.set_active(i)
                break
        else:
            if e is not None and isinstance(e, Gtk.Entry):
                e.set_text(value)
    elif wid.startswith("fcb_"):
        w.set_active_id(value)
    elif wid.startswith("t_"):
        w.set_text(value)
    elif wid.startswith("tb_"):
        w.set_text(value)
    elif wid.startswith("f_"):
        w.set_font_name(value)
        # w.emit("font-set")
    elif wid.startswith("c_"):
        if isinstance(value, str):
            value = value.lower() == "true"
        w.set_active(value)
    elif wid.startswith("s_"):
        w.set_value(float(value or 0))
    elif wid.startswith("btn_"):
        w.set_tooltip_text(value)
    elif wid.startswith("bl_"):
        setFontButton(w, value or None)
    elif wid.startswith("lb_"):
        w.set_label(value)
    elif wid.startswith("l_"):
        w.set_text(value)
    elif wid.startswith("col_"):
        c = Gdk.RGBA()
        c.parse(value)
        w.set_rgba(c)
    elif wid.startswith("nbk_"):
        w.set_current_page(value)

def setFontButton(btn, value):
    btn.font_info = value
    if value is None:
        btn.set_label(_("Set Font..."))
        return
    style = getattr(value, 'style', None)
    if not style:
        styles = []
        if "embolden" in value.feats:
            styles.append("(bold)")
        if "slant" in value.feats:
            styles.append("(italic)")
        style = " ".join(styles)
    btn.set_label("{}\n{}".format(value.name, style))

def makeSpinButton(mini, maxi, start, step=1, page=1):
    adj = Gtk.Adjustment(upper=maxi, lower=mini, step_increment=step, page_increment=page)
    res = Gtk.SpinButton()
    res.set_adjustment(adj)
    return res
