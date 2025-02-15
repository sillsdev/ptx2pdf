import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from ptxprint.utils import _, f2s
from PIL import Image
import logging
from ptxprint.view import GitVersionStr, VersionStr

logger = logging.getLogger(__name__)

def _getcomboval(w, sub):
    model = w.get_model()
    i = w.get_active()
    if i < 0:
        e = w.get_child()
        if e is not None and isinstance(e, Gtk.Entry):
            return e.get_text()
    elif model is not None:
        return model[i][w.get_entry_text_column() if sub < 0 else sub]

def getWidgetVal(wid, w, default=None, asstr=False, sub=-1):
    v = None
    if wid.startswith("ecb_"):
        v = _getcomboval(w, sub)
    elif wid.startswith("fcb_"):
        if sub < 0:
            v = w.get_active_id()
        else:
            v = _getcomboval(w, sub)
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

def _setcomboval(w, value, sub):
        model = w.get_model()
        e = w.get_child()
        for i, v in enumerate(model):
            if v[w.get_entry_text_column() if sub < 0 else sub] == value:
                w.set_active(i)
                break
        else:
            if e is not None and isinstance(e, Gtk.Entry):
                e.set_text(value)

def setWidgetVal(wid, w, value, noui=False, useMarkup=False, sub=-1):
    try:
        if wid.startswith("ecb_"):
            _setcomboval(w, value, sub)
        elif wid.startswith("fcb_"):
            if sub < 0:
                w.set_active_id(value)
            else:
                _setcomboval(w, value, sub)
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

def doError(text, secondary="", title=None, copy2clip=False, show=True, who2email="ptxprint_support@sil.org", **kw):
    logger.error(text)
    if secondary:
        logger.error(secondary)
    if copy2clip:
        if who2email.startswith("ptxp"):
            if secondary is not None:
                secondary += _("\nPTXprint Version {}").format(GitVersionStr)
            lines = [title or ""]
        else:
            lines = [""]
        if text is not None and len(text):
            lines.append(text)
        if secondary is not None and len(secondary):
            lines.append(secondary)
        s = _(f"Mailto: <{who2email}>") + "\n{}".format("\n".join(lines))
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(s, -1)
        clipboard.store() # keep after app crashed
        if secondary is not None:
            if who2email.startswith("ptxp"):
                secondary += "\n\n" + " "*18 + "[" + _("This message has been copied to the clipboard.")+ "]"
            else:
                secondary += "\n" + _("The letter above has been copied to the clipboard.")
                secondary += "\n" + _("Send it by e-mail to: {}").format(who2email)
        else:
            secondary = " "*18 + "[" + _("This message has been copied to the clipboard.")+ "]"
    if show:
        dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.ERROR,
                 buttons=Gtk.ButtonsType.OK, text=text)
        if title is None and who2email.startswith("ptxp"):
            title = "PTXprint Version " + VersionStr
        dialog.set_title(title)
        if secondary is not None:
            dialog.format_secondary_text(secondary)
        dialog.run()
        dialog.destroy()
    else:
        print(text)
        if secondary is not None:
            print(secondary)


