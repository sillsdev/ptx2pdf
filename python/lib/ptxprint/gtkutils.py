import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from ptxprint.utils import _, f2s
from PIL import Image

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
    elif wid.startswith("txbf_"):
        v = w.get_text(w.get_start_iter(), w.get_end_iter(), True)
    # elif wid.startswith("f_"):
        # v = w.get_font_name()
    elif wid.startswith("c_"):
        v = w.get_active()
    elif wid.startswith("s_"):
        v = f2s(w.get_value())
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

def setWidgetVal(wid, w, value, noui=False, useMarkup=False):
    try:
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
            w.set_text(value or "")
        elif wid.startswith("txbf_"):
            w.set_text(value or "")
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
            w.set_tooltip_text(value or "")
        elif wid.startswith("bl_"):
            setFontButton(w, value or None)
        elif wid.startswith("lb_"):
            w.set_label(value or "")
        elif wid.startswith("l_"):
            if useMarkup:
                w.set_markup(value or "")
            else:
                w.set_text(value or "")
        elif wid.startswith("col_"):
            c = Gdk.RGBA()
            c.parse(value)
            w.set_rgba(c)
        elif wid.startswith("nbk_"):
            w.set_current_page(value)
    except Exception as e:
        raise type(e)("Setting {}, {}".format(w, e))

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
        if value.isBold:
            styles.append("Bold")
        if value.isItalic:
            styles.append("Italic")
        style = " ".join(styles)
    btn.set_label("{}\n{}".format(value.name, style))

def makeSpinButton(mini, maxi, start, step=1, page=1):
    adj = Gtk.Adjustment(upper=maxi, lower=mini, step_increment=step, page_increment=page)
    res = Gtk.SpinButton()
    res.set_adjustment(adj)
    return res

class HelpTextViewWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="PTXPrint help")
        self.set_default_size(580, 740)
        #self.vb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        #self.add(self.vb)
        self.connect("destroy", Gtk.main_quit)
        self.create_textview()
        
    def create_textview(self):
        sw = Gtk.ScrolledWindow()
        sw.set_hexpand(True)
        sw.set_vexpand(True)
        self.add(sw)
        #self.vb.attach(sw)

        self.tv = Gtk.TextView()
        self.tv.set_monospace(True)
        self.tv.set_wrap_mode(Gtk.WrapMode.WORD)
        self.tb = self.tv.get_buffer()
        sw.add(self.tv)

    def print_message(self, message):
        self.tb.set_text(message, -1)
        self.show_all()
        Gtk.main()
