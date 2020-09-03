from gi.repository import Gtk

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
    # elif wid.startswith("f_"):
        # v = w.get_font_name()
    elif wid.startswith("c_"):
        v = w.get_active()
    elif wid.startswith("s_"):
        v = "{:.3f}".format(w.get_value())
    elif wid.startswith("btn_"):
        v = w.get_tooltip_text()
    elif wid.startswith("bl_"):
        v = getattr(w, 'font_info', (None, None))
        if asstr:
            v = "\n".join(v)
    elif wid.startswith("lb_"):
        v = w.get_label()
    elif wid.startswith("l_"):
        v = w.get_text()
    if v is None:
        return default
    return v

def setWidgetVal(wid, w, value):
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
    elif wid.startswith("f_"):
        w.set_font_name(value)
        # w.emit("font-set")
    elif wid.startswith("c_"):
        w.set_active(value)
    elif wid.startswith("s_"):
        w.set_value(float(value))
    elif wid.startswith("btn_"):
        w.set_tooltip_text(value)
    elif wid.startswith("bl_"):
        setFontButton(w, *value)
    elif wid.startswith("lb_"):
        w.set_label(value)
    elif wid.startswith("l_"):
        w.set_text(value)

def setFontButton(btn, name, style):
    btn.font_info = (name, style)
    btn.set_label("{}\n{}".format(name, style))


