#!/usr/bin/python3

import sys, os, re, regex, gi, random, subprocess, collections
gi.require_version('Gtk', '3.0')
from shutil import copyfile, copytree, rmtree
from gi.repository import Gtk, Pango, GObject
# gi.require_version('GtkSource', '4') 
from gi.repository import GtkSource
import xml.etree.ElementTree as et
from ptxprint.font import TTFont, initFontCache
from ptxprint.runner import StreamTextBuffer
from ptxprint.ptsettings import ParatextSettings, allbooks, books, bookcodes, chaps
from ptxprint.info import Info
import configparser
import traceback
from time import sleep
from threading import Thread

# xmlstarlet sel -t -m '//iso_15924_entry' -o '"' -v '@alpha_4_code' -o '" : "' -v '@name' -o '",' -n /usr/share/xml/iso-codes/iso_15924.xml
_allscripts = { "Zyyy" : "Default", "Adlm" : "Adlam", "Afak" : "Afaka", "Aghb" : "Caucasian Albanian", "Ahom" : "Ahom, Tai Ahom", 
    "Arab" : "Arabic", "Aran" : "Arabic (Nastaliq)", "Armi" : "Imperial Aramaic", "Armn" : "Armenian", "Avst" : "Avestan", "Bali" : "Balinese",
    "Bamu" : "Bamum", "Bass" : "Bassa Vah", "Batk" : "Batak", "Beng" : "Bengali", "Bhks" : "Bhaiksuki", "Blis" : "Blissymbols", "Bopo" : "Bopomofo",
    "Brah" : "Brahmi", "Brai" : "Braille", "Bugi" : "Buginese", "Buhd" : "Buhid", "Cakm" : "Chakma", "Cans" : "Canadian Aboriginal Syllabics",
    "Cari" : "Carian", "Cham" : "Cham", "Cher" : "Cherokee", "Cirt" : "Cirth", "Copt" : "Coptic", "Cprt" : "Cypriot", "Cyrl" : "Cyrillic",
    "Cyrs" : "Cyrillic (Old Church Slavonic)", "Deva" : "Devanagari", "Dsrt" : "Deseret (Mormon)", "Egyd" : "Egyptian demotic", 
    "Egyh" : "Egyptian hieratic", "Elba" : "Elbasan", "Ethi" : "Ethiopic (Geʻez)", "Geok" : "Khutsuri (Asomtavruli & Nuskhuri)", 
    "Geor" : "Georgian (Mkhedruli)", "Glag" : "Glagolitic", "Gong" : "Gunjala-Gondi", "Gonm" : "Masaram-Gondi",
    "Goth" : "Gothic", "Gran" : "Grantha", "Grek" : "Greek", "Gujr" : "Gujarati", "Guru" : "Gurmukhi",
    "Hanb" : "Han with Bopomofo", "Hang" : "Hangul (Hangŭl, Hangeul)", "Hani" : "Han (Hanzi, Kanji, Hanja)",
    "Hano" : "Hanunoo (Hanunóo)", "Hans" : "Han (Simplified)", "Hant" : "Han (Traditional)", "Hatr" : "Hatran", "Hebr" : "Hebrew",
    "Hira" : "Hiragana", "Hmng" : "Pahawh-Hmong", "Hrkt" : "Japanese (Hiragana+Katakana)", "Hung" : "Old Hungarian (Runic)",
    "Ital" : "Old Italic (Etruscan, Oscan)", "Jamo" : "Jamo (subset of Hangul)", "Java" : "Javanese",
    "Jpan" : "Japanese (Han+Hiragana+Katakana)", "Jurc" : "Jurchen", "Kali" : "Kayah-Li", "Kana" : "Katakana", "Khar" : "Kharoshthi",
    "Khmr" : "Khmer", "Khoj" : "Khojki", "Kitl" : "Khitan (large)", "Kits" : "Khitan (small)", "Knda" : "Kannada", "Kore" : "Korean (Hangul+Han)",
    "Kpel" : "Kpelle", "Kthi" : "Kaithi", "Lana" : "Tai Tham (Lanna)", "Laoo" : "Lao", "Latf" : "Latin (Fraktur)",
    "Latg" : "Latin (Gaelic)", "Latn" : "Latin", "Leke" : "Leke", "Lepc" : "Lepcha (Róng)", "Limb" : "Limbu", "Lina" : "Linear A",
    "Linb" : "Linear B", "Lisu" : "Lisu (Fraser)", "Loma" : "Loma", "Lyci" : "Lycian", "Lydi" : "Lydian", "Mahj" : "Mahajani", 
    "Mand" : "Mandaic, Mandaean", "Mani" : "Manichaean", "Marc" : "Marchen", "Mend" : "Mende Kikakui", "Merc" : "Meroitic Cursive",
    "Mlym" : "Malayalam", "Modi" : "Modi", "Mong" : "Mongolian", "Mroo" : "Mro, Mru", "Mtei" : "Meitei-Mayek", "Mult" : "Multani", 
    "Mymr" : "Myanmar (Burmese)", "Narb" : "North Arabian (Ancient)", "Nbat" : "Nabataean", "Newa" : "New (Newar, Newari)",
    "Nkgb" : "Nakhi Geba (Naxi Geba)", "Nkoo" : "N’Ko", "Nshu" : "Nüshu", "Ogam" : "Ogham", "Olck" : "Ol Chiki (Ol Cemet’, Santali)", 
    "Orkh" : "Old Turkic, Orkhon Runic", "Orya" : "Oriya", "Osge" : "Osage", "Osma" : "Osmanya", "Palm" : "Palmyrene",
    "Pauc" : "Pau Cin Hau", "Perm" : "Old Permic", "Phag" : "Phags-pa", "Phli" : "Inscriptional Pahlavi", "Phlp" : "Psalter Pahlavi",
    "Phlv" : "Book Pahlavi", "Phnx" : "Phoenician", "Plrd" : "Miao (Pollard)", "Prti" : "Inscriptional Parthian",
    "Rjng" : "Rejang (Redjang, Kaganga)", "Roro" : "Rongorongo",
    "Runr" : "Runic", "Samr" : "Samaritan", "Sara" : "Sarati", "Sarb" : "Old South Arabian", "Saur" : "Saurashtra", "Shaw" : "Shavian (Shaw)", 
    "Shrd" : "Sharada", "Sidd" : "Siddham, Siddhamātṛkā", "Sind" : "Sindhi, Khudawadi", "Sinh" : "Sinhala", "Sora" : "Sora-Sompeng",
    "Sund" : "Sundanese", "Sylo" : "Syloti Nagri", "Syrc" : "Syriac", "Syre" : "Syriac (Estrangelo)", "Syrj" : "Syriac (Western)",
    "Syrn" : "Syriac (Eastern)", "Tagb" : "Tagbanwa", "Takr" : "Takri, Ṭāṅkrī", "Tale" : "Tai Le", "Talu" : "New-Tai-Lue", 
    "Taml" : "Tamil", "Tang" : "Tangut", "Tavt" : "Tai Viet", "Telu" : "Telugu", "Teng" : "Tengwar", "Tfng" : "Tifinagh (Berber)",
    "Tglg" : "Tagalog (Baybayin, Alibata)", "Thaa" : "Thaana", "Thai" : "Thai", "Tibt" : "Tibetan", "Tirh" : "Tirhuta", "Ugar" : "Ugaritic",
    "Vaii" : "Vai", "Wara" : "Warang-Citi", "Wole" : "Woleai", "Xpeo" : "Old Persian", "Yiii" : "Yi", "Zzzz" : "Uncoded script"
}
# Note that ls_digits (in the glade file) is used to map these "friendly names" to the "mapping table names" (especially the non-standard ones)
_alldigits = [ "Default", "Adlam", "Ahom", "Arabic-Farsi", "Arabic-Hindi", "Balinese", "Bengali", "Bhaiksuki", "Brahmi", "Burmese", 
    "Chakma", "Cham", "Devanagari", "Gujarati", "Gunjala-Gondi", "Gurmukhi", "Hanifi-Rohingya", "Javanese", "Kannada", 
    "Kayah-Li", "Khmer", "Khudawadi", "Lao", "Lepcha", "Limbu", "Malayalam", "Masaram-Gondi", "Meetei-Mayek", "Modi", "Mongolian", 
    "Mro", "Myanmar", "Myanmar-Shan", "Myanmar-Tai-Laing", "New-Tai-Lue", "Newa", "Nko", "Nyiakeng-Puachue-Hmong", "Ol-Chiki", "Oriya", 
    "Osmanya", "Pahawh-Hmong", "Persian", "Saurashtra", "Sharada", "Sinhala-Lith", "Sora-Sompeng", "Sundanese", "Tai-Tham-Hora", 
    "Tai-Tham-Tham", "Takri", "Tamil", "Telugu", "Thai", "Tibetan", "Tirhuta", "Urdu", "Vai", "Wancho", "Warang-Citi" ]

class Splash(Thread):
    def __init__(self, window):
        super(Splash, self).__init__()
        self.window = window
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.set_default_size(400, 250)
        self.window.connect('destroy', Gtk.main_quit)

    def run(self):
        GObject.threads_init()
        self.window.set_auto_startup_notification(False)
        self.window.show_all()
        self.window.set_auto_startup_notification(True)
        Gtk.main()

    def destroy(self):
        self.window.destroy()
        # poor man's queue clearing
        sleep(0.1)

class PtxPrinterDialog:
    def __init__(self, allprojects, settings_dir, working_dir=None):
        self.initialised = False
        self.pendingPid = None
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(__file__), "ptxprint.glade"))
        self.builder.connect_signals(self)
        self.addCR("cb_digits", 0)
        self.addCR("cb_script", 0)
        self.addCR("cb_chapfrom", 0)
        self.addCR("cb_chapto", 0)
        self.addCR("cb_textDirection", 0)
        self.addCR("cb_blendedXrefCaller", 0)
        self.addCR("cb_glossaryMarkupStyle", 0)
        self.cb_savedConfig = self.builder.get_object("cb_savedConfig")
        # self.addCR("cb_savedConfig", 0)
        # self.addCR("cb_diglotPriProject", 0)
        # self.addCR("cb_diglotSecProject", 0)
        pb = self.builder.get_object("b_print")
        pbc = pb.get_style_context()
        pbc.add_class("printbutton")

        scripts = self.builder.get_object("ls_scripts")
        scripts.clear()
        for k, v in _allscripts.items():
            scripts.append([v, k])
        self.cb_script.set_active_id('Zyyy')

        digits = self.builder.get_object("ls_digits")
        currdigits = {r[0]: r[1] for r in digits}
        digits.clear()
        for d in _alldigits: # .items():
            v = currdigits.get(d, d.lower())
            # print("d,v: ",d, v)
            digits.append([d, v])
        self.cb_digits.set_active_id(_alldigits[0])

        # glostyle = self.builder.get_object("ls_glossaryMarkupStyle")
        # glostyle.clear()
        # for g in Info._glossarymarkup.keys():
            # try:
                # print(g)
            # except UnicodeEncodeError:
                # pass
            # glostyle.append([g])

        dia = self.builder.get_object("dlg_multiBookSelector")
        dia.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK)

        dia = self.builder.get_object("dlg_password")
        dia.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY)

        self.fileViews = []
        for i,k in enumerate(["FinalSFM", "PicList", "AdjList", "TeXfile", "XeTeXlog", "Settings"]):
            buf = GtkSource.Buffer()
            view = GtkSource.View.new_with_buffer(buf)
            scroll = self.builder.get_object("scroll_" + k)
            scroll.add_with_viewport(view)
            self.fileViews.append((buf, view))
            if i > 2:
                view.set_show_line_numbers(True)  # Turn these ON
            else:
                view.set_show_line_numbers(False)  # Turn these OFF

        self.logbuffer = StreamTextBuffer()
        self.builder.get_object("tv_logging").set_buffer(self.logbuffer)
        self.mw = self.builder.get_object("ptxprint")
        self.projects = self.builder.get_object("ls_projects")
        self.info = None
        self.settings_dir = settings_dir
        self.working_dir = working_dir
        self.config_dir = None
        self.ptsettings = None
        self.booklist = []
        self.CustomScript = None
        self.FrontPDFs = None
        self.BackPDFs = None
        self.watermarks = None
        self.pageborder = None
        self.sectionheader = None
        self.versedecorator = None
        self.customFigFolder = None
        self.prjid = None
        self.experimental = None
        for p in sorted(allprojects, key = lambda s: s.casefold()):
            self.projects.append([p])

    def run(self, callback):
        self.callback = callback
        splashw = self.builder.get_object("w_splash")
        self.splash = Splash(splashw)   # threads don't like being gced?
        self.splash.start()

        # do slow stuff here
        initFontCache()
        sleep(1)  # Until we want people to see the splash screen

        self.initialised = True
        if self.pendingPid is not None:
            self.onProjectChange(None)
            self.pendingPid = None
        self.splash.destroy()
        # self.mw.set_resizable(True)
        # self.mw.set_default_size(730, 565)
        self.mw.resize(730, 580)
        self.mw.show_all()
        Gtk.main()

    def ExperimentalFeatures(self, value):
        self.experimental = value
        if value:
                self.builder.get_object("c_experimental").set_visible(True)
                self.builder.get_object("c_experimental").set_active(True)
                self.builder.get_object("c_experimental").set_sensitive(False)
        else:
            for c in ("c_experimental", "c_experimental"):  # "c_startOnHalfPage"
                self.builder.get_object(c).set_active(False)
                self.builder.get_object(c).set_visible(False)
                self.builder.get_object(c).set_sensitive(False)
        for w in ("tb_", "lb_"):
            for exp in ("Illustrations", "Logging"):
                self.builder.get_object("{}{}".format(w, exp)).set_visible(value)

    def addCR(self, name, index):
        v = self.builder.get_object(name)
        setattr(self, name, v)
        c = Gtk.CellRendererText()
        v.pack_start(c, True)
        v.add_attribute(c, "text", index)

    def parse_fontname(self, font):
        m = re.match(r"^(.*?)(\d+(?:\.\d+)?)$", font)
        if m:
            return [m.group(1), int(m.group(2))]
        else:
            return [font, 0]

    def get(self, wid, sub=0, asstr=False):
        w = self.builder.get_object(wid)
        if w is None:
            raise KeyError(wid)
        v = ""
        if wid.startswith("cb_"):
            model = w.get_model()
            i = w.get_active()
            if i < 0:
                e = w.get_child()
                if e is not None:
                    v = e.get_text()
            elif model is not None:
                v = model[i][sub]
        elif wid.startswith("t_"):
            v = w.get_text()
        elif wid.startswith("f_"):
            v = w.get_font_name()
        elif wid.startswith("c_"):
            v = w.get_active()
        elif wid.startswith("s_"):
            v = w.get_value()
        elif wid.startswith("btn_"):
            v = w.get_tooltip_text()
        return v

    def set(self, wid, value):
        w = self.builder.get_object(wid)
        if wid.startswith("cb_"):
            model = w.get_model()
            e = w.get_child()
            if e is not None and isinstance(e, Gtk.Entry):
                e.set_text(value)
                # e.emit("changed")
            else:
                for i, v in enumerate(model):
                    if v[w.get_id_column()] == value:
                        w.set_active_id(value)
                        # w.emit("changed")
                        break
        elif wid.startswith("t_"):
            w.set_text(value)
        elif wid.startswith("f_"):
            w.set_font_name(value)
            # w.emit("font-set")
        elif wid.startswith("c_"):
            w.set_active(value)
        elif wid.startswith("s_"):
            w.set_value(value)
        elif wid.startswith("btn_"):
            w.set_tooltip_text(value)

    def getBooks(self):
        if not self.get('c_multiplebooks'):
            return [self.get('cb_book')]
        elif self.get('t_booklist') != '':
            return self.get('t_booklist').split()
        else:
            return self.booklist

    def getBookFilename(self, bk, prjid):
        if self.ptsettings is None:
            self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
        fbkfm = self.ptsettings['FileNameBookNameForm']
        bknamefmt = (self.ptsettings['FileNamePrePart'] or "") + \
                    fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                    (self.ptsettings['FileNamePostPart'] or "")
        # print(bknamefmt)
        fname = bknamefmt.format(bkid=bk, bkcode=bookcodes.get(bk, 0))
        return fname
        
    def onDestroy(self, btn):
        Gtk.main_quit()

    def onOK(self, btn):
        if self.prjid is not None:
            self.callback(self)
        else:
            dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR, \
                     buttons=Gtk.ButtonsType.OK, message_format="Cannot create a PDF without a Project selected")
            dialog.format_secondary_text("Please select a Paratext Project and try again.")
            dialog.set_keep_above(True)
            dialog.run()
            dialog.destroy()

    def onCancel(self, btn):
        self.onDestroy(btn)

    def onAboutClicked(self, btn_about):
        dia = self.builder.get_object("dlg_about")
        dia.set_keep_above(True)
        response = dia.run()
        dia.hide()
            
    def onConfigNameChanged(self, cb_savedConfig):
        if len(self.get("cb_savedConfig")):
            lockBtn = self.builder.get_object("btn_lockunlock")
            lockBtn.set_label("Lockdown  ;-)")
            lockBtn.set_sensitive(True)
            self.builder.get_object("t_invisiblePassword").set_text("")
            self.builder.get_object("btn_saveConfig").set_sensitive(True)
            self.builder.get_object("btn_deleteConfig").set_sensitive(True)
            if os.path.exists(self.configPath()):
                self.updateProjectSettings(False) # False means DON'T Save!
        else:
            self.config_dir = self.configPath()
            self.builder.get_object("t_configNotes").set_text("")
            lockBtn = self.builder.get_object("btn_lockunlock")
            # lockBtn.set_label("Lock Config")
            lockBtn.set_label("Lockdown  ;-)")
            lockBtn.set_sensitive(False)
            self.builder.get_object("t_invisiblePassword").set_text("")
            self.builder.get_object("l_settings_dir").set_label(self.config_dir or "")
            self.builder.get_object("btn_saveConfig").set_sensitive(False)
            self.builder.get_object("btn_deleteConfig").set_sensitive(False)

    def onSaveConfig(self, btn):
        # Determine whether to save a NEW config or just UPDATE an existing one
        if self.config_dir != self.configPath(): # then it must be new
            self.info.update()
            config = self.info.createConfig(self)
            self.saveConfig(config)
            self.cb_savedConfig.append_text(self.configName())
            # This is the first time to save, so copy other files/folders too
            tgtpath = self.configPath()
            for listname in ["PicLists", "AdjLists"]:
                srcpath = self.config_dir or os.path.join(self.settings_dir, self.get("cb_project"), "shared", "ptxprint")
                if os.path.exists(os.path.join(srcpath, listname)):
                    if srcpath != tgtpath:
                        copytree(os.path.join(srcpath, listname), os.path.join(tgtpath, listname))
                        # print("Copied from: {}\n         to: {}".format(os.path.join(srcpath, listname), os.path.join(tgtpath, listname)))
            self.config_dir = tgtpath # Update the current config folder location (in prep for next change)
            self.builder.get_object("l_settings_dir").set_label(self.config_dir or "")
        else:
            # Just update the existing config file
            self.info.update()
            config = self.info.createConfig(self)
            self.saveConfig(config)

    def configName(self):
        cfgName = re.sub('[^-a-zA-Z0-9_() ]+', '', self.get("cb_savedConfig")).strip(" ")
        return cfgName

    def configPath(self, makePath=False):
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, prjid, "shared", "ptxprint")
        cfgname = self.configName()
        if len(cfgname):
            prjdir = os.path.join(prjdir, cfgname)
        if makePath:
            if not os.path.exists(prjdir):
                os.makedirs(prjdir)
        return prjdir

    def saveConfig(self, config):
        fpath = self.configPath(True)
        if os.path.exists(fpath):
            with open(os.path.join(fpath, "ptxprint.cfg"), "w", encoding="utf-8") as outf:
                config.write(outf)

    def onDeleteConfig(self, btn):
        delCfgPath = self.configPath()
        if len(delCfgPath) > 30: # Just to make sure we're not deleting something closer to Root!
            try: # Delete the entire folder
                rmtree(delCfgPath)
            except OSError:
                dialog = Gtk.MessageDialog(parent=None, modal=True, message_type=Gtk.MessageType.ERROR,
                         buttons=Gtk.ButtonsType.OK, text="Could not find Saved Configuration")
                dialog.format_secondary_text("Folder: " + delCfgPath)
                dialog.set_keep_above(True)
                dialog.run()
                dialog.destroy()
            self.updateSavedConfigList()
            self.builder.get_object("t_savedConfig").set_text("")
            self.builder.get_object("t_configNotes").set_text("")

    def updateSavedConfigList(self):
        currConf = self.builder.get_object("t_savedConfig").get_text()
        self.cb_savedConfig.remove_all()
        savedConfigs = []
        shpath = os.path.join(self.settings_dir, self.prjid, "shared", "ptxprint")
        if os.path.exists(shpath): # Get the list of Saved Configs (folders)
            for f in next(os.walk(shpath))[1]:
                if not f in ["PicLists", "AdjLists"]:
                    savedConfigs.append(f)
        if len(savedConfigs):
            for cfgName in sorted(savedConfigs):
                self.cb_savedConfig.append_text(cfgName)
            try:
                self.builder.get_object("t_savedConfig").set_text(currConf)
            except:
                self.cb_savedConfig.set_active(0)
        else:
            self.builder.get_object("t_savedConfig").set_text("")
            self.builder.get_object("t_configNotes").set_text("")

    def onLockUnlockSavedConfig(self, btn):
        lockBtn = self.builder.get_object("btn_lockunlock")
        dia = self.builder.get_object("dlg_password")
        dia.set_keep_above(True)
        response = dia.run()
        if response == Gtk.ResponseType.APPLY:
            pw = self.get("t_password")
        elif response == Gtk.ResponseType.CANCEL:
            pass # Don't do anything
        else:
            return
        invPW = self.get("t_invisiblePassword")
        if invPW == None or invPW == "": # No existing PW, so set a new one
            self.builder.get_object("t_invisiblePassword").set_text(pw)
            self.onSaveConfig(None)
        else: # try to unlock the settings by removing the settings
            if pw == invPW:
                self.builder.get_object("t_invisiblePassword").set_text("")
            else: # Mismatching password - Don't do anything
                pass
        self.builder.get_object("t_password").set_text("")
        dia.hide()

    def onPasswordChanged(self, t_invisiblePassword):
        lockBtn = self.builder.get_object("btn_lockunlock")
        if self.get("t_invisiblePassword") == "":
            status = True
            # lockBtn.set_label("Lock Config")
            lockBtn.set_label("Lockdown  ;-)")
        else:
            status = False
            lockBtn.set_label("Unlock Config")
        for c in ["btn_saveConfig", "btn_deleteConfig", "t_configNotes"]:
            self.builder.get_object(c).set_sensitive(status)
        
    def onPrevBookClicked(self, btn_NextBook):
        bks = self.getBooks()
        ndx = 0
        try:
            ndx = bks.index(self.get("cb_examineBook"))
        except ValueError:
            self.builder.get_object("cb_examineBook").set_active_id(bks[0])
        if ndx > 0:
            self.builder.get_object("cb_examineBook").set_active_id(bks[ndx-1])
            self.builder.get_object("btn_NextBook").set_sensitive(True)
            if ndx == 1:
                self.builder.get_object("btn_PrevBook").set_sensitive(False)
        else:
            self.builder.get_object("btn_PrevBook").set_sensitive(False)
    
    def onNextBookClicked(self, btn_NextBook):
        bks = self.getBooks()
        ndx = 0
        try:
            ndx = bks.index(self.get("cb_examineBook"))
        except ValueError:
            self.builder.get_object("cb_examineBook").set_active_id(bks[0])
        if ndx < len(bks)-1:
            self.builder.get_object("cb_examineBook").set_active_id(bks[ndx+1])
            self.builder.get_object("btn_PrevBook").set_sensitive(True)
            if ndx == len(bks)-2:
                self.builder.get_object("btn_NextBook").set_sensitive(False)
        else:
            self.builder.get_object("btn_NextBook").set_sensitive(False)
    
    def onExamineBookChanged(self, cb_examineBook):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        self.onViewerChangePage(None,None,pg)

    def onGenerateClicked(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        if pg == 1: # PicList
            bks2gen = self.getBooks()
            if not self.get('c_multiplebooks') and self.get("cb_examineBook") != bks2gen[0]: 
                self.GeneratePicList([self.get("cb_examineBook")])
            else:
                self.GeneratePicList(bks2gen)
        elif pg == 2: # AdjList
            self.GenerateAdjList()
        self.onViewerChangePage(None,None,pg)

    def onRefreshViewerTextClicked(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        self.onViewerChangePage(None, None, pg)

    def onViewerChangePage(self, nbk_Viewer, scrollObject, pgnum):
        self.builder.get_object("gr_editableButtons").set_visible(False)
        # self.builder.get_object("btn_saveEdits").set_sensitive(False)
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        bk = self.get("cb_examineBook")
        genBtn = self.builder.get_object("btn_Generate")
        genBtn.set_sensitive(False)
        genBtn.set_label("Generate")
        self.builder.get_object("c_randomPicPosn").set_sensitive(False)
        if bk == None or bk == "":
            bk = bks[0]
            self.builder.get_object("cb_examineBook").set_active_id(bk)
        for o in ("l_examineBook", "btn_PrevBook", "cb_examineBook", "btn_NextBook", "btn_Generate"):
            self.builder.get_object(o).set_sensitive( 0 < pgnum <= 2)

        fndict = {0 : ("", ""),     1 : ("PicLists", ".piclist"), 2 : ("AdjLists", ".adj"), \
                  3 : ("", ".tex"), 4 : ("", ".log")}
        if pgnum <= 2:  # (SFM,PicList,AdjList)
            fname = self.getBookFilename(bk, prjid)
            if pgnum == 0:
                fpath = os.path.join(self.working_dir, fndict[pgnum][0], fname)
            else:
                fpath = os.path.join(self.configPath(), fndict[pgnum][0], fname)
            doti = fpath.rfind(".")
            if doti > 0:
                fpath = fpath[:doti] + "-draft" + fpath[doti:] + fndict[pgnum][1]
            if pgnum == 1: # PicList
                self.builder.get_object("c_randomPicPosn").set_sensitive(True)
                genTip = "Generate the PicList in the\ncorrect format using the markup\n(\\fig ... \\fig*) within the text."
                genBtn.set_sensitive(True)
                genBtn.set_tooltip_text(genTip)
            elif pgnum == 2: # AdjList
                genTip = "Generate a list of paragraphs\nthat may be adjusted (using\nshrink or expand values)."
                genBtn.set_sensitive(True)
                genBtn.set_tooltip_text(genTip)
            if os.path.exists(fpath):
                genBtn.set_label("Regenerate")

        elif 3 <= pgnum <= 4:  # (TeX,Log)
            if len(bks) > 1:
                fname = "ptxprint-{}_{}{}{}".format(bks[0], bks[-1], prjid, fndict[pgnum][1])
            else:
                fname = "ptxprint-{}{}{}".format(bks[0], prjid, fndict[pgnum][1])
            fpath = os.path.join(self.working_dir, fname)

        elif pgnum == 5: # View/Edit one of the 4 Settings files
            fpath = self.builder.get_object("l_{}".format(pgnum)).get_tooltip_text()
            if fpath == None:
                self.fileViews[pgnum][0].set_text("\n Use the 'Advanced' tab to select which settings you want to view or edit.")
                self.builder.get_object("l_{}".format(pgnum)).set_text("Settings")
                return

        elif pgnum == 6: # Just show the About page with folders in use and other links.
            self.builder.get_object("l_{}".format(pgnum)).set_text("About")
            return
        else:
            # print("Error: Unhandled page in Viewer!")
            return
        if os.path.exists(fpath):
            if 1 <= pgnum <= 2 or pgnum == 5:
                self.builder.get_object("gr_editableButtons").set_visible(True)
            self.builder.get_object("l_{}".format(pgnum)).set_tooltip_text(fpath)
            with open(fpath, "r", encoding="utf-8", errors="ignore") as inf:
                txt = inf.read()
                if len(txt) > 80000:
                    txt = txt[:80000]+"\n\n------------------------------------- \
                                          \n[Display of file has been truncated] \
                                          \nClick on View/Edit... button to see more."
            self.fileViews[pgnum][0].set_text(txt)
        else:
            self.builder.get_object("l_{}".format(pgnum)).set_tooltip_text(None)
            self.fileViews[pgnum][0].set_text("\nThis file doesn't exist yet.\n\nTry... \
                                               \n   * Check option (above) to 'Preserve Intermediate Files and Logs' \
                                               \n   * Generate the PiCList or AdjList \
                                               \n   * Click 'Print' to create the PDF")

    def onSaveEdits(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        buf = self.fileViews[pg][0]
        fpath = self.builder.get_object("l_{}".format(pg)).get_tooltip_text()
        text2save = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        openfile = open(fpath,"w", encoding="utf-8")
        openfile.write(text2save)
        openfile.close()

    def onOpenInSystemEditor(self, btn):
        pg = self.builder.get_object("nbk_Viewer").get_current_page()
        fpath = self.builder.get_object("l_{}".format(pg)).get_tooltip_text() or ""
        if os.path.exists(fpath):
            if sys.platform == "win32":
                os.startfile(fpath)
            elif sys.platform == "linux":
                subprocess.call(('xdg-open', fpath))

    def onScriptChanged(self, cb_script):
        # If there is a matching digit style for the script that has just been set, 
        # then also turn that on (but it can be overridden by the user if needed).
        try:
            self.cb_digits.set_active_id(self.get('cb_script'))
        except:
            pass

    def onFontChanged(self, fbtn):
        # traceback.print_stack(limit=3)
        fnm = self.get("f_body")
        f = TTFont(fnm)
        if f.filename == None:
            self.msgUnsupportedFont(fnm)
        else:
            if "Silf" in f:
                self.builder.get_object("c_useGraphite").set_sensitive(True)
                self.builder.get_object("c_useGraphite").set_active(True)
            else:
                self.builder.get_object("c_useGraphite").set_sensitive(False)
                self.builder.get_object("c_useGraphite").set_active(False)
            font = fbtn.get_font_name()
            (name, size) = self.parse_fontname(font)
            label = self.builder.get_object("l_font")
            for s in ('bold', 'italic', 'bold italic'):
                sid = s.replace(" ", "")
                w = self.builder.get_object("f_"+sid)
                f = TTFont(name, style = " ".join(s.split()))
                fname = f.family + ", " + f.style + " " + str(size)
                w.set_font_name(fname)
                # Still need to do something here to put these defaults in if there aren't any other settings.
                # print(fname, f.family, f.style, f.filename)
                # print(s, fname, f.extrastyles)
                # if 'bold' in f.style.lower():
                    # self.set("s_{}embolden".format(sid), 2)
                # if 'italic' in f.style.lower():
                    # self.set("s_{}slant".format(sid), 0.15)
            self.setEntryBoxFont()

    def setEntryBoxFont(self):
        # Set the font of any GtkEntry boxes to the primary body text font for this project
        p = Pango.font_description_from_string(self.get("f_body"))
        for w in ("t_tocTitle", "cb_ftrcenter", "scroll_FinalSFM", "scroll_PicList"):   # "t_runningFooter",
            self.builder.get_object(w).modify_font(p)

    def updateFakeLabels(self):
        status = self.get("c_fakebold") or self.get("c_fakeitalic") or self.get("c_fakebolditalic")
        for c in ("l_embolden", "l_slant"):
            self.builder.get_object(c).set_sensitive(status)

    def onFakeboldClicked(self, c_fakebold):
        status = self.get("c_fakebold")
        for c in ("s_boldembolden", "s_boldslant"):
            self.builder.get_object(c).set_sensitive(status)
        self.updateFakeLabels()
        
    def onFakeitalicClicked(self, c_fakeitalic):
        status = self.get("c_fakeitalic")
        for c in ("s_italicembolden", "s_italicslant"):
            self.builder.get_object(c).set_sensitive(status)
        self.updateFakeLabels()

    def onFakebolditalicClicked(self, c_fakebolditalic):
        status = self.get("c_fakebolditalic")
        for c in ("s_bolditalicembolden", "s_bolditalicslant"):
            self.builder.get_object(c).set_sensitive(status)
        self.updateFakeLabels()

    def onVariableLineSpacingClicked(self, c_variableLineSpacing):
        status = self.get("c_variableLineSpacing")
        for c in ("s_linespacingmin", "s_linespacingmax", "l_min", "l_max"):
            self.builder.get_object(c).set_sensitive(status)
        lnsp = self.builder.get_object("s_linespacing")
        min = self.builder.get_object("s_linespacingmin")
        max = self.builder.get_object("s_linespacingmax")
        lnspVal = round(lnsp.get_value(),1)
        minVal = round(min.get_value(),1)
        maxVal = round(max.get_value(),1)
        if status and lnspVal == minVal and lnspVal == maxVal:
            min.set_value(lnspVal-1) 
            max.set_value(lnspVal+2) 

    def onVerticalRuleClicked(self, c_verticalrule):
        self.builder.get_object("s_colgutteroffset").set_sensitive(self.get("c_verticalrule"))

    def onMarginalVersesClicked(self, c_marginalverses):
        self.builder.get_object("s_columnShift").set_sensitive(self.get("c_marginalverses"))

    def onHyphenateClicked(self, c_hyphenate):
        prjid = self.get("cb_project")
        fname = os.path.join(self.working_dir, 'hyphen-{}.tex'.format(prjid))
        if not os.path.exists(fname) and self.get("c_hyphenate"):
            dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR, \
                     buttons=Gtk.ButtonsType.OK, message_format="Warning: Standard (English) Hyphenation rules will be used.")
            dialog.format_secondary_text("For optimum hyphenation for this project\nclick 'Create Hyphenation List'.")
            dialog.set_keep_above(True)
            dialog.run()
            dialog.destroy()
            # self.builder.get_object("c_hyphenate").set_active(False)
        
    def onUseIllustrationsClicked(self, c_includeillustrations):
        status = self.get("c_includeillustrations")
        self.builder.get_object("gr_IllustrationOptions").set_sensitive(status)

    def onUseCustomFolderclicked(self, c_useCustomFolder):
        self.builder.get_object("btn_selectFigureFolder").set_sensitive(self.get("c_useCustomFolder"))

    def onBlendedXrsClicked(self, c_blendfnxr):
        status = self.get("c_blendfnxr")
        for c in ("c_includeXrefs", "c_xrautocallers", "t_xrcallers", "c_xromitcaller", "c_xrpageresetcallers", "c_paragraphedxrefs"):
            self.builder.get_object(c).set_sensitive(not status)
        self.builder.get_object("cb_blendedXrefCaller").set_sensitive(status)
    
    def onClickedIncludeFootnotes(self, c_includeFootnotes):
        status = self.get("c_includeFootnotes")
        for c in ("c_fnautocallers", "t_fncallers", "c_fnomitcaller", "c_fnpageresetcallers", "c_fnparagraphednotes"):
            self.builder.get_object(c).set_sensitive(status)
        
    def onClickedIncludeXrefs(self, c_includeXrefs):
        status = self.get("c_includeXrefs")
        for c in ("c_xrautocallers", "t_xrcallers", "c_xromitcaller", "c_xrpageresetcallers", "c_paragraphedxrefs"):
            self.builder.get_object(c).set_sensitive(status)

    def onPageNumTitlePageChanged(self, c_pageNumTitlePage):
        if self.get("c_pageNumTitlePage"):
            self.builder.get_object("c_printConfigName").set_active(False)

    def onPrintConfigNameChanged(self, c_printConfigName):
        if self.get("c_printConfigName"):
            self.builder.get_object("c_pageNumTitlePage").set_active(False)

    def onPageGutterChanged(self, c_pagegutter):
        status = self.get("c_pagegutter")
        gtr = self.builder.get_object("s_pagegutter")
        gtr.set_sensitive(status)
        if status:
            gtr.grab_focus() 

    def onDoubleColumnChanged(self, c_doublecolumn):
        status = self.get("c_doublecolumn")
        for c in ("c_verticalrule", "l_gutterWidth", "s_colgutterfactor"):
            self.builder.get_object(c).set_sensitive(status)

    def onHdrVersesClicked(self, c_hdrverses):
        status = self.get("c_hdrverses")
        for c in ("c_sepPeriod", "c_sepColon"):
            self.builder.get_object(c).set_sensitive(status)

    def onBookSelectorChange(self, c_multiplebooks):
        status = self.get("c_multiplebooks")
        self.set("c_prettyIntroOutline", False)
        if status and self.get("t_booklist") == "" and self.prjid is not None:
            pass
            # self.onChooseBooksClicked(None)
        else:
            for c in ("c_combine", "t_booklist"):
                self.builder.get_object(c).set_sensitive(status)
            toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
            toc.set_sensitive(status)
            if not status:
                toc.set_active(False)
            for c in ("l_singlebook", "cb_book", "l_chapfrom", "cb_chapfrom", "l_chapto", "cb_chapto"):
                self.builder.get_object(c).set_sensitive(not status)
            self.updateDialogTitle()
            bks = self.getBooks()
            if len(bks) > 1:
                self.builder.get_object("cb_examineBook").set_active_id(bks[0])
            
    def onUseFallbackFontchanged(self, c_useFallbackFont):
        status = self.get("c_useFallbackFont")
        self.builder.get_object("gr_fallbackFont").set_sensitive(status)

    def onFigsChanged(self, c_includefigsfromtext):
        status = self.get("c_includefigsfromtext")
        for c in ("c_figexclwebapp", "c_fighiderefs", "c_skipmissingimages", "l_imageTypeOrder", "t_imageTypeOrder"):
            self.builder.get_object(c).set_sensitive(status)

    def onInclFrontMatterChanged(self, c_inclFrontMatter):
        self.builder.get_object("btn_selectFrontPDFs").set_sensitive(self.get("c_inclFrontMatter"))

    def onInclBackMatterChanged(self, c_inclBackMatter):
        self.builder.get_object("btn_selectBackPDFs").set_sensitive(self.get("c_inclBackMatter"))

    def onApplyWatermarkChanged(self, c_applyWatermark):
        self.builder.get_object("btn_selectWatermarkPDF").set_sensitive(self.get("c_applyWatermark"))
    
    def onInclPageBorderChanged(self, c_inclPageBorder):
        self.builder.get_object("btn_selectPageBorderPDF").set_sensitive(self.get("c_inclPageBorder"))

    def onInclSectionHeaderChanged(self, c_inclSectionHeader):
        self.builder.get_object("btn_selectSectionHeaderPDF").set_sensitive(self.get("c_inclSectionHeader"))

    def onInclVerseDecoratorChanged(self, c_inclVerseDecorator):
        status = self.get("c_inclVerseDecorator")
        for c in ("l_verseFont", "f_verseNumFont", "l_verseSize", "s_verseNumSize", "btn_selectVerseDecorator"):
            self.builder.get_object(c).set_sensitive(status)
    
    def onAutoTocChanged(self, c_autoToC):
        atoc = self.builder.get_object("t_tocTitle")
        if self.get("c_autoToC"):
            atoc.set_sensitive(True)
            atoc.grab_focus() 
        else:   
            atoc.set_sensitive(False)

    def onLineBreakChanged(self, c_linebreakon):
        lbrk = self.builder.get_object("t_linebreaklocale")
        if self.get("c_linebreakon"):
            lbrk.set_sensitive(True)
            lbrk.grab_focus() 
        else:   
            lbrk.set_sensitive(False)
            
    def onFnCallersChanged(self, c_fnautocallers):
        fnc = self.builder.get_object("t_fncallers")
        if self.get("c_fnautocallers"):
            fnc.set_sensitive(True)
            fnc.grab_focus() 
        else:   
            fnc.set_sensitive(False)
            
    def onResetFNcallersClicked(self, btn_resetFNcallers):
        self.builder.get_object("t_fncallers").set_text(re.sub(" ", ",", self.ptsettings['footnotes']))
        
    def onResetXRcallersClicked(self, btn_resetXRcallers):
        self.builder.get_object("t_xrcallers").set_text(re.sub(" ", ",", self.ptsettings['crossrefs']))
        
    def onXrCallersChanged(self, c_xrautocallers):
        xrc = self.builder.get_object("t_xrcallers")
        if self.get("c_xrautocallers"):
            xrc.set_sensitive(True)
            xrc.grab_focus() 
        else:   
            xrc.set_sensitive(False)

    def onRHruleChanged(self, c_rhrule):
        rhr = self.builder.get_object("s_rhruleposition")
        if self.get("c_rhrule"):
            rhr.set_sensitive(True)
            rhr.grab_focus() 
        else:   
            rhr.set_sensitive(False)

    def onProcessScriptClicked(self, c_processScript):
        status = self.get("c_processScript")
        for c in ("c_processScriptBefore", "c_processScriptAfter", "btn_selectScript"):
            self.builder.get_object(c).set_sensitive(status)
            
    def onUsePrintDraftChangesClicked(self, c_usePrintDraftChanges):
        status = self.get("c_usePrintDraftChanges")
        for c in ("btn_editChangesFile", "c_processScriptBefore", "c_processScriptAfter", "l_processScript"):
            self.builder.get_object(c).set_sensitive(status)
        if self.info is not None:           # trigger a rereading of the changes
            # this is a kludge. Better to keep the last modified date and test in Info.convertBook
            self.info.changes = None
        
    def onUseModsTexClicked(self, c_useModsTex):
        self.builder.get_object("btn_editModsTeX").set_sensitive(self.get("c_useModsTex"))
        
    def onUseCustomStyClicked(self, c_useCustomSty):
        self.builder.get_object("btn_editCustomSty").set_sensitive(self.get("c_useCustomSty"))
        
    def onUseModsStyClicked(self, c_useModsSty):
        self.builder.get_object("btn_editModsSty").set_sensitive(self.get("c_useModsSty"))
        
    def onOmitOutlineClicked(self, c_omitIntroOutline):
        self.builder.get_object("c_prettyIntroOutline").set_sensitive(not self.get("c_omitIntroOutline"))
        self.builder.get_object("c_prettyIntroOutline").set_active(False)

    def onUsePTmacrosClicked(self, c_usePTmacros):
        self.updateProjectSettings(True)
        status = self.get("c_usePTmacros")
        for c in ("c_variableLineSpacing", "s_linespacingmin", "s_linespacingmax", "l_min", "l_max",
                  "s_colgutteroffset", "l_colgutteroffset", "c_marginalverses", "s_columnShift"):
            self.builder.get_object(c).set_sensitive(not status)
        # Temporarily keep these off (unless testing)
        self.builder.get_object("c_startOnHalfPage").set_sensitive(not status)

    def onHideAdvancedSettingsClicked(self, c_hideAdvancedSettings):
        if self.get("c_hideAdvancedSettings"):
            # Turn Dangerous Settings OFF
            for c in ("c_startOnHalfPage", "c_marginalverses", "c_prettyIntroOutline", "c_blendfnxr", "c_autoToC",
                      "c_figplaceholders", "c_omitallverses", "c_glueredupwords", "c_omit1paraIndent", "c_hangpoetry", 
                      "c_preventwidows", "c_PDFx1aOutput", "c_diglot", "c_hyphenate", "c_variableLineSpacing"):
                self.builder.get_object(c).set_active(False)

            # Turn Essential Settings ON
            for c in ("c_mainBodyText", "c_footnoterule",
                      "c_includefigsfromtext", "c_skipmissingimages", "c_useLowResPics"):
                self.builder.get_object(c).set_active(True)
            self.builder.get_object("c_hideAdvancedSettings").set_opacity(0.2)
            self.builder.get_object("c_hideAdvancedSettings").set_tooltip_text("")
            
        else:
            self.builder.get_object("c_hideAdvancedSettings").set_opacity(1.0)
            self.builder.get_object("c_hideAdvancedSettings").set_tooltip_text("Many of the settings in this tool only need to be\n" + \
                                                                               "set up once, or used on rare occasions. These can\n" + \
                                                                               "be hidden away for most of the time if that helps.\n\n" + \
                                                                               "This setting can be toggled off again later, but\n" + \
                                                                               "is intentionally almost invisible (though located\n" + \
                                                                               "in the same place).")

        # Hide a whole bunch of stuff that they don't need to see   (removed: "tb_Logging", "tb_DiglotTesting", )
        for c in ("tb_Body", "tb_Advanced", "tb_ViewerEditor", "btn_editPicList", "l_imageTypeOrder", "t_imageTypeOrder",
                  "fr_Footer", "bx_TopMarginSettings", "gr_HeaderAdvOptions", "box_AdvFootnoteConfig", "l_colgutteroffset",
                  "c_usePicList", "c_skipmissingimages", "c_useCustomFolder", "btn_selectFigureFolder", 
                  "c_startOnHalfPage", "c_prettyIntroOutline", "c_marginalverses", "s_columnShift", "c_figplaceholders",
                  "fr_FontConfig", "fr_fallbackFont", "fr_paragraphAdjust", "l_textDirection",
                  "bx_fnCallers", "bx_fnCalleeCaller", "bx_xrCallers", "bx_xrCalleeCaller", "row_ToC", "c_hyphenate",
                  "c_omitallverses", "c_glueredupwords", "c_omit1paraIndent", "c_hangpoetry", "c_preventwidows",
                  "l_sidemarginfactor", "s_sidemarginfactor", "l_min", "s_linespacingmin", "l_max", "s_linespacingmax",
                  "c_variableLineSpacing", "c_pagegutter", "s_pagegutter", "cb_textDirection", "l_digits", "cb_digits",
                  "t_invisiblePassword", "t_configNotes", "l_notes"):
                  # "btn_saveConfig", "btn_deleteConfig", "btn_lockunlock", "t_invisiblePassword", "t_configNotes", "l_notes"):
            self.builder.get_object(c).set_visible(not self.get("c_hideAdvancedSettings"))

        # Resize Main UI Window appropriately
        if self.get("c_hideAdvancedSettings"):
            self.mw.resize(710, 316)
        else:
            self.mw.resize(730, 580)

    def onShowBordersTabClicked(self, c_showBordersTab):
        status = self.get("c_showBordersTab")
        self.builder.get_object("tb_FancyBorders").set_visible(status)
        # self.builder.get_object("c_enableDecorativeElements").set_active(status)

    def onShowDiglotTabClicked(self, c_showDiglotTab):
        status = self.get("c_showDiglotTab")
        self.builder.get_object("tb_DiglotTesting").set_visible(status)
        # self.builder.get_object("c_diglot").set_active(status)

    def onKeepTemporaryFilesClicked(self, c_keepTemporaryFiles):
        self.builder.get_object("gr_debugTools").set_sensitive(self.get("c_keepTemporaryFiles"))

    def onChooseBooksClicked(self, btn):
        dia = self.builder.get_object("dlg_multiBookSelector")
        dia.set_keep_above(True)
        mbs_grid = self.builder.get_object("mbs_grid")
        mbs_grid.forall(mbs_grid.remove)
        lsbooks = self.builder.get_object("ls_books")
        bl = self.builder.get_object("t_booklist")
        self.alltoggles = []
        for i, b in enumerate(lsbooks):
            tbox = Gtk.ToggleButton(b[0])
            tbox.show()
            if tbox.get_label() in bl.get_text().split(" "):
                tbox.set_active(True)
            self.alltoggles.append(tbox)
            mbs_grid.attach(tbox, i // 13, i % 13, 1, 1)
        response = dia.run()
        if response == Gtk.ResponseType.OK:
            self.booklist = [b.get_label() for b in self.alltoggles if b.get_active()]
            bl.set_text(" ".join(b for b in self.booklist))
        self.builder.get_object("c_multiplebooks").set_active(not self.booklist == [])
        self.set("c_prettyIntroOutline", False)
        self.updateDialogTitle()
        bks = self.getBooks()
        if len(bks) > 1:
            self.builder.get_object("cb_examineBook").set_active_id(bks[0])
        dia.hide()

    def toggleBooks(self,start,end):
        bp = self.ptsettings['BooksPresent']
        cPresent = sum(1 for x in bp[start:end] if x == "1")
        cActive = 0
        toggle = False
        for b in self.alltoggles:
            if b.get_active() and b.get_label() in allbooks[start:end]:
                cActive += 1
        if cActive < cPresent:
            toggle = True
        for b in self.alltoggles:
            if b.get_label() in allbooks[start:end]:
                b.set_active(toggle)

    def onClickmbs_all(self, btn):
        self.toggleBooks(0,124)

    def onClickmbs_OT(self, btn):
        self.toggleBooks(0,39)
        
    def onClickmbs_NT(self, btn):
        self.toggleBooks(40,67)

    def onClickmbs_DC(self, btn):
        self.toggleBooks(67,85)

    def onClickmbs_xtra(self, btn):
        self.toggleBooks(85,124)

    def onClickmbs_none(self, btn):
        for b in self.alltoggles:
            if b.get_label() in allbooks[0:124]:
                b.set_active(False)

    def onTocClicked(self, c_toc):
        if not self.get("c_usetoc1") and not self.get("c_usetoc2") and not self.get("c_usetoc3"):
            toc = self.builder.get_object("c_usetoc1")
            toc.set_active(True)
            
    def _setchap(self, ls, start, end):
        ls.clear()
        for c in range(start, end+1):
            ls.append([str(c)])

    def onBookChange(self, cb_book):
        self.bk = self.get("cb_book")
        self.set("c_prettyIntroOutline", False)
        if self.bk != "":
            self.chs = int(chaps.get(str(self.bk)))
            self.chapfrom = self.builder.get_object("ls_chapfrom")
            self._setchap(self.chapfrom, 1, self.chs)
            self.cb_chapfrom.set_active_id('1')
        
            self.chapto = self.builder.get_object("ls_chapto")
            self._setchap(self.chapto, 1, self.chs)
            self.cb_chapto.set_active_id(str(self.chs))
            self.builder.get_object("cb_examineBook").set_active_id(self.bk)
        self.updateDialogTitle()

    def onChapFrmChg(self, cb_chapfrom):
        self.bk = self.get("cb_book")
        if self.bk != "":
            self.chs = int(chaps.get(str(self.bk)))
            self.strt = self.builder.get_object("cb_chapfrom").get_active_id()
            self.chapto = self.builder.get_object("ls_chapto")
            self._setchap(self.chapto, (int(self.strt) if self.strt is not None else 0), self.chs)
            self.cb_chapto.set_active_id(str(self.chs))

    def onSpinITclicked(self, btn_spinIT):
        self.builder.get_object("appSpinner").start()

    def onUsePrintDraftChanged(self, cb_upd):
        upd = self.get("c_useprintdraftfolder")
        if upd and self.prjid is not None:
            self.working_dir = os.path.join(self.settings_dir, self.prjid, 'PrintDraft')
        else:
            self.working_dir = "."
        self.builder.get_object("l_working_dir").set_label(self.working_dir)

    def onProjectChange(self, cb_prj):
        if not self.initialised:
            self.pendingPid = self.get("cb_project")
        else:
            self.updateProjectSettings(True)
            self.updateSavedConfigList()

    def updateProjectSettings(self, saveCurrConfig=False):
        currprj = self.prjid
        if currprj is not None:
            if self.info is None:
                self.info = Info(self, self.settings_dir, prjid = currprj)
            config = self.info.createConfig(self)
            self.config_dir = self.configPath()
            fpath = os.path.join(self.settings_dir, currprj, "shared", "ptxprint", "ptxprint.cfg")
            if saveCurrConfig and os.path.exists(fpath):
                with open(fpath, "w", encoding="utf-8") as outf:
                    config.write(outf)
                self.updateSavedConfigList()
                self.builder.get_object("t_savedConfig").set_text("")
                self.builder.get_object("t_configNotes").set_text("")

        self.prjid = self.get("cb_project")
        self.ptsettings = None
        lsbooks = self.builder.get_object("ls_books")
        if currprj is not None:
            cbbook = self.builder.get_object("cb_book")
            cbbook.set_model(None)
            lsbooks.clear()
            cbbook.set_model(lsbooks)
        if not self.prjid:
            return
        if self.get("c_useprintdraftfolder"):
            self.working_dir = os.path.join(self.settings_dir, self.prjid, 'PrintDraft')
        else:
            self.working_dir = '.'

        self.ptsettings = ParatextSettings(self.settings_dir, self.prjid)
        bp = self.ptsettings['BooksPresent']
        for b in allbooks:
            ind = books.get(b, 0)-1
            if 0 <= ind <= len(bp) and bp[ind - 1 if ind > 40 else ind] == "1":
                lsbooks.append([b])
        cb_bk = self.builder.get_object("cb_book")
        cb_bk.set_active(0)
        font_name = self.ptsettings.get('DefaultFont', 'Arial') + ", " + self.ptsettings.get('DefaultFontSize', '12')
        self.set('f_body', font_name)
        configfile = os.path.join(self.configPath(), "ptxprint.cfg")
        if not os.path.exists(configfile): # If they are an pre 0:4:8 user, pick up .cfg from Project folder location
            configfile = os.path.join(self.settings_dir, self.prjid, "ptxprint.cfg")
        if os.path.exists(configfile):
            self.info = Info(self, self.settings_dir, self.prjid)
            config = configparser.ConfigParser()
            config.read(configfile, encoding="utf-8")
            self.info.loadConfig(self, config)
        else:
            try:
                self.info.update()
            except AttributeError:
                self.info = Info(self, self.settings_dir, self.prjid)
                self.info.update()
        status = self.get("c_multiplebooks")
        for c in ("c_combine", "t_booklist"):
            self.builder.get_object(c).set_sensitive(status)
        toc = self.builder.get_object("c_autoToC") # Ensure that we're not trying to build a ToC for a single book!
        toc.set_sensitive(status)
        if not status:
            toc.set_active(False)
        for c in ("l_singlebook", "cb_book", "l_chapfrom", "cb_chapfrom", "l_chapto", "cb_chapto"):
            self.builder.get_object(c).set_sensitive(not status)
        for i in range(0,6):
            self.builder.get_object("l_{}".format(i)).set_tooltip_text(None)
        self.builder.get_object("l_prjdir").set_label(os.path.join(self.settings_dir, self.prjid))
        self.builder.get_object("l_settings_dir").set_label(self.config_dir or "")
        self.builder.get_object("l_working_dir").set_label(self.working_dir)
        self.set("c_prettyIntroOutline", False)
        self.setEntryBoxFont()
        self.onDiglotDimensionsChanged(None)
        self.updateDialogTitle()

    def updateDialogTitle(self):
        prjid = "  -  " + self.get("cb_project")
        bks = self.getBooks()
        if len(bks) > 1:
            bks = bks[0] + "..." + bks[-1]
        else:
            try:
                bks = bks[0]
            except IndexError:
                bks = "No book selected!"
        titleStr = "PTXprint [0.5.0 Beta]" + prjid + " (" + bks + ")"
        self.builder.get_object("ptxprint").set_title(titleStr)

    def editFile(self, file2edit, wkdir=False):
        pgnum = 5
        self.builder.get_object("nbk_Main").set_current_page(7)
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        self.prjid = self.get("cb_project")
        self.prjdir = os.path.join(self.settings_dir, self.prjid)
        if wkdir:
            fpath = os.path.join(self.working_dir, file2edit)
        else:
            fpath = os.path.join(self.settings_dir, self.prjid, file2edit)
        if os.path.exists(fpath):
            self.builder.get_object("gr_editableButtons").set_visible(True)
            self.builder.get_object("l_{}".format(pgnum)).set_text(file2edit)
            self.builder.get_object("l_{}".format(pgnum)).set_tooltip_text(fpath)
            with open(fpath, "r", encoding="utf-8") as inf:
                txt = inf.read()
                # if len(txt) > 32000:
                    # txt = txt[:32000]+"\n\n etc...\n\n"
            self.fileViews[pgnum][0].set_text(txt)
        else:
            self.fileViews[pgnum][0].set_text("\nThis file doesn't exist yet!")

    def onEditChangesFile(self, btn):
        self.editFile("PrintDraftChanges.txt", False)

    def onEditModsTeX(self, btn):
        modfname = "ptxprint-mods.tex"
        self.prjid = self.get("cb_project")
        fpath = os.path.join(self.settings_dir, self.prjid, "shared", "ptxprint", modfname)
        if not os.path.exists(fpath):
            openfile = open(fpath,"w", encoding="utf-8")
            openfile.write("% This is the .tex file specific for the {} project used by PTXprint.\n".format(self.prjid))
            openfile.close()
        self.editFile(modfname, True)

    def onEditCustomSty(self, btn):
        self.editFile("custom.sty", False)

    def onEditModsSty(self, btn):
        self.editFile("PrintDraft-mods.sty", True)

    def onMainBodyTextChanged(self, c_mainBodyText):
        self.builder.get_object("gr_mainBodyText").set_sensitive(self.get("c_mainBodyText"))

    def onSelectScriptClicked(self, btn_selectScript):
        CustomScript = self.fileChooser("Select a Custom Script file", 
                filters = {"Executable Scripts": {"patterns": "*.bat", "mime": "application/bat"}},
                # ),("*.sh", "mime": "application/x-sh")
                multiple = False)
        if CustomScript is not None:
            self.CustomScript = CustomScript
            btn_selectScript.set_tooltip_text("\n".join('{}'.format(s) for s in CustomScript))
        else:
            self.CustomScript = None
            btn_selectScript.set_tooltip_text("")
            self.builder.get_object("btn_selectScript").set_sensitive(False)
            self.builder.get_object("c_processScript").set_active(False)
            for c in ("btn_selectScript", "c_processScriptBefore", "c_processScriptAfter", "l_script2process"):
                self.builder.get_object(c).set_sensitive(False)

    def onFrontPDFsClicked(self, btn_selectFrontPDFs):
        FrontPDFs = self.fileChooser("Select one or more PDF(s) for FRONT matter", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = True)
        if FrontPDFs is not None and FrontPDFs != 'None':
            self.FrontPDFs = FrontPDFs
            self.builder.get_object("c_inclFrontMatter").set_active(True)
            btn_selectFrontPDFs.set_tooltip_text("\n".join('{}'.format(s) for s in FrontPDFs))
            self.builder.get_object("lb_inclFrontMatter").set_text(",".join(re.sub(r".+[\\/](.+)\.pdf",r"\1",s) for s in FrontPDFs))
        else:
            self.FrontPDFs = None
            btn_selectFrontPDFs.set_tooltip_text("")
            self.builder.get_object("lb_inclFrontMatter").set_text("")
            self.builder.get_object("btn_selectFrontPDFs").set_sensitive(False)
            self.builder.get_object("c_inclFrontMatter").set_active(False)

    def onBackPDFsClicked(self, btn_selectBackPDFs):
        BackPDFs = self.fileChooser("Select one or more PDF(s) for BACK matter", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = True)
        if BackPDFs is not None and BackPDFs != 'None':
            self.BackPDFs = BackPDFs
            self.builder.get_object("c_inclBackMatter").set_active(True)
            btn_selectBackPDFs.set_tooltip_text("\n".join('{}'.format(s) for s in BackPDFs))
            self.builder.get_object("lb_inclBackMatter").set_text(",".join(re.sub(r".+[\\/](.+)\.pdf",r"\1",s) for s in BackPDFs))
        else:
            self.BackPDFs = None
            btn_selectBackPDFs.set_tooltip_text("")
            self.builder.get_object("lb_inclBackMatter").set_text("")
            self.builder.get_object("btn_selectBackPDFs").set_sensitive(False)
            self.builder.get_object("c_inclBackMatter").set_active(False)

    def onWatermarkPDFclicked(self, btn_selectWatermarkPDF):
        watermarks = self.fileChooser("Select Watermark PDF file", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = False)
        if watermarks is not None and watermarks != 'None':
            self.watermarks = watermarks[0]
            self.builder.get_object("c_applyWatermark").set_active(True)
            btn_selectWatermarkPDF.set_tooltip_text(watermarks[0])
            self.builder.get_object("lb_applyWatermark").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",watermarks[0]))
        else:
            self.watermarks = None
            btn_selectWatermarkPDF.set_tooltip_text("")
            self.builder.get_object("lb_applyWatermark").set_text("")
            self.builder.get_object("btn_selectWatermarkPDF").set_sensitive(False)
            self.builder.get_object("c_applyWatermark").set_active(False)

    def onSelectFigureFolderClicked(self, btn_selectFigureFolder):
        customFigFolder = self.fileChooser("Select the folder containing image files", 
                filters = None, multiple = False, folder = True)
        if customFigFolder is not None:
            self.customFigFolder = customFigFolder[0]
            btn_selectFigureFolder.set_tooltip_text(customFigFolder[0])
            self.builder.get_object("c_useCustomFolder").set_active(True)
        else:
            self.customFigFolder = None
            btn_selectFigureFolder.set_tooltip_text("")
            self.builder.get_object("c_useCustomFolder").set_active(False)
            self.builder.get_object("btn_selectFigureFolder").set_sensitive(False)
            # self.builder.get_object("c_useLowResPics").set_active(True)

    def onPageBorderPDFclicked(self, btn_selectPageBorderPDF):
        pageborder = self.fileChooser("Select Page Border PDF file", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = False)
        if pageborder is not None and pageborder != 'None':
            self.pageborder = pageborder[0]
            self.builder.get_object("c_inclPageBorder").set_active(True)
            btn_selectPageBorderPDF.set_tooltip_text(pageborder[0])
            self.builder.get_object("lb_inclPageBorder").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",pageborder[0]))
        else:
            self.pageborder = None
            btn_selectPageBorderPDF.set_tooltip_text("")
            self.builder.get_object("lb_inclPageBorder").set_text("")
            self.builder.get_object("btn_selectPageBorderPDF").set_sensitive(False)
            self.builder.get_object("c_inclPageBorder").set_active(False)

    def onSectionHeaderPDFclicked(self, btn_selectSectionHeaderPDF):
        sectionheader = self.fileChooser("Select Section Header PDF file", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = False)
        if sectionheader is not None and sectionheader != 'None':
            self.sectionheader = sectionheader[0]
            self.builder.get_object("c_inclSectionHeader").set_active(True)
            btn_selectSectionHeaderPDF.set_tooltip_text(sectionheader[0])
            self.builder.get_object("lb_inclSectionHeader").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",sectionheader[0]))
        else:
            self.sectionheader = None
            btn_selectSectionHeaderPDF.set_tooltip_text("")
            self.builder.get_object("lb_inclSectionHeader").set_text("")
            self.builder.get_object("btn_selectSectionHeaderPDF").set_sensitive(False)
            self.builder.get_object("c_inclSectionHeader").set_active(False)

    def onVerseDecoratorPDFclicked(self, btn_selectVerseDecoratorPDF):
        versedecorator = self.fileChooser("Select Verse Decorator PDF file", 
                filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                multiple = False)
        if versedecorator is not None and versedecorator != 'None':
            self.versedecorator = versedecorator[0]
            self.builder.get_object("c_inclVerseDecorator").set_active(True)
            btn_selectVerseDecoratorPDF.set_tooltip_text(versedecorator[0])
            self.builder.get_object("lb_inclVerseDecorator").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",versedecorator[0]))
        else:
            self.versedecorator = None
            btn_selectVerseDecoratorPDF.set_tooltip_text("")
            self.builder.get_object("lb_inclVerseDecorator").set_text("")
            self.builder.get_object("btn_selectVerseDecoratorPDF").set_sensitive(False)
            self.builder.get_object("c_inclVerseDecorator").set_active(False)

    # def onXyzPDFclicked(self, btn_selectXyzPDF):
        # xyz = self.fileChooser("Select Xyz PDF file", 
                # filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}},
                # multiple = False)
        # if xyz is not None and xyz != 'None':
            # self.xyz = xyz[0]
            # btn_selectXyzPDF.set_tooltip_text(xyz[0])
            # self.builder.get_object("lb_inclXyz").set_text(re.sub(r".+[\\/](.+)\.pdf",r"\1",xyz[0]))
        # else:
            # self.xyz = None
            # btn_selectXyzPDF.set_tooltip_text("")
            # self.builder.get_object("lb_inclXyz").set_text("")
            # self.builder.get_object("btn_selectXyzPDF").set_sensitive(False)
            # self.builder.get_object("c_inclXyz").set_active(False)

    def GeneratePicList(self, booklist):
        # Format of lines in pic-list file: BBB C.V desc|file|size|loc|copyright|caption|ref
        # MRK 1.16 fishermen...catching fish with a net.|hk00207b.png|span|b||Jesus calling the disciples to follow him.|1.16
        _picposn = {
            "col":      ("tl", "tr", "bl", "br"),
            "span":     ("t", "b")
        }
        existingFilelist = []
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, self.prjid)
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            outfname = os.path.join(self.configPath(), "PicLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".piclist"
            if os.path.exists(outfname):
                existingFilelist.append(outfname.split("/")[-1])
        if len(existingFilelist):
            q1 = "One or more PicList file(s) already exist!"
            q2 = "\n".join(existingFilelist)+"\n\nDo you want to OVERWRITE the above-listed file(s)?"
            if not self.msgQuestion(q1, q2):
                return
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            infname = os.path.join(prjdir, fname)
            outfname = os.path.join(self.configPath(), "PicLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".piclist"
            piclist = []
            piclist.append("% PicList Generated by PTXprint. Note that .TIFs have been changed to .PDF\n")
            piclist.append("% Location   |Image Name|Img.Size|Position on Page||Illustration|Caption\n")
            piclist.append("% book ch.vs |filename.ext|span/col|t/b/tl/tr/bl/br||Caption Text|ch:vs\n")
            piclist.append("% \n")
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                # Finds USFM2-styled markup in text:
                #                0         1       2     3     4              5       
                # \\fig .*\|(.+?\....)\|(....?)\|(.*)\|(.*)\|(.+?)\|(\d+[:.]\d+([-,]\d+)?)\\fig\*
                # \fig |CN01684b.jpg|col|||key-kālk arsi manvan yēsunaga tarval|9:2\fig*
                #           0         1  2 3          4                          5  
                # BKN \5 \|\0\|\1\|tr\|\|\4\|\5
                # MAT 9.2 bringing the paralyzed man to Jesus|CN01684b.jpg|col|tr||key-kālk arsi manvan yēsunaga tarval|9:2
                m = re.findall(r"\\fig .*\|(.+?\....)\|(....?)\|(.+)?\|(.+)?\|(.+)?\|(\d+[\:\.]\d+([\-,]\d+)?)\\fig\*", dat)
                if len(m):
                    for f in m:
                        # XeTeX doesn't handle TIFs, so rename all TIF extensions to PDFs
                        picfname = re.sub(r"(?i)(.+)\.tif", r"\1.pdf",f[0])
                        if self.get("c_randomPicPosn"):
                            pageposn = random.choice(_picposn.get(f[1], f[1]))    # Randomize location of illustrations on the page (tl,tr,bl,br)
                        else:
                            pageposn = (_picposn.get(f[1], f[1]))[0]              # use the t or tl (first in list)
                        piclist.append(bk+" "+re.sub(r":",".", f[5])+" |"+picfname+"|"+f[1]+"|"+pageposn+"||"+f[4]+"|"+f[5]+"\n")
                else:
                    # If none of the USFM2-styled illustrations were found then look for USFM3-styled markup in text 
                    # (Q: How to handle any additional/non-standard xyz="data" ? Will the .* before \\fig\* take care of it adequately?)
                    #         0              1               2                  3      [4]
                    # \\fig (.+?)\|src="(.+?\....)" size="(....?)" ref="(\d+[:.]\d+([-,]\d+)?)".*\\fig\*
                    # \fig hāgartun saṅga dūtal vaḍkval|src="CO00659B.TIF" size="span" ref="21:16"\fig*
                    #                   0                         1                2          3  [4]
                    # BKN \3 \|\1\|\2\|tr\|\|\0\|\3
                    # GEN 21.16 an angel speaking to Hagar|CO00659B.TIF|span|t||hāgartun saṅga dūtal vaḍkval|21:16
                    m = re.findall(r'\\fig (.+?)\|src="(.+?\....)" size="(....?)" ref="(\d+[:.]\d+([-,]\d+)?)".*\\fig\*', dat)
                    if len(m):
                        for f in m:
                            # XeTeX doesn't handle TIFs, so rename all TIF extensions to PDFs
                            picfname = re.sub(r"(?i)(.+)\.tif", r"\1.pdf",f[1])
                            if self.get("c_randomPicPosn"):
                                pageposn = random.choice(_picposn.get(f[2], f[2]))     # Randomize location of illustrations on the page (tl,tr,bl,br)
                            else:
                                pageposn = (_picposn.get(f[2], f[2]))[0]               # use the t or tl (first in list)
                            piclist.append(bk+" "+re.sub(r":",".", f[3])+" |"+picfname+"|"+f[2]+"|"+pageposn+"||"+f[0]+"|"+f[3]+"\n")
                if len(m):
                    plpath = os.path.join(self.configPath(), "PicLists")
                    if not os.path.exists(plpath):
                        os.mkdir(plpath)
                    with open(outfname, "w", encoding="utf-8") as outf:
                        outf.write("".join(piclist))

    def GenerateAdjList(self):
        existingFilelist = []
        booklist = self.getBooks()
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, self.prjid)
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            outfname = os.path.join(self.configPath(), "AdjLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".adj"
            if os.path.exists(outfname):
                existingFilelist.append(outfname.split("/")[-1])
        if len(existingFilelist):
            q1 = "One or more Paragraph Adjust file(s) already exist!"
            q2 = "\n".join(existingFilelist)+"\n\nDo you want to OVERWRITE the above-listed file(s)?"
            if not self.msgQuestion(q1, q2):
                return
        for bk in booklist:
            fname = self.getBookFilename(bk, prjid)
            infname = os.path.join(prjdir, fname)
            outfname = os.path.join(self.configPath(), "AdjLists", fname)
            doti = outfname.rfind(".")
            if doti > 0:
                outfname = outfname[:doti] + "-draft" + outfname[doti:] + ".adj"
            adjlist = []
            with open(infname, "r", encoding="utf-8") as inf:
                dat = inf.read()
                # It would be good to make this more inclusive (\p \m \q1 \q2 etc.) 
                # and also include \s Section Heads as comments to help show whichs parapgraphs are within a single section
                m = re.findall(r"\\p ?\r?\n\\v (\d+)",dat)
                if m is not None:
                    prv = 0
                    ch = 1
                    for v in m:
                        if int(v) < int(prv):
                            ch = ch + 1
                        adjlist.append(bk+" "+str(ch)+"."+v+" +0\n")
                        prv = v
                    adjpath = os.path.join(self.configPath(), "AdjLists")
                    if not os.path.exists(adjpath):
                        os.mkdir(adjpath)
                    with open(outfname, "w", encoding="utf-8") as outf:
                        outf.write("".join(adjlist))

    def onEditAdjListClicked(self, btn_editParaAdjList):
        pgnum = 2
        self.builder.get_object("nbk_Main").set_current_page(7)
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        self.onViewerChangePage(None,None,pgnum)

    def onEditPicListClicked(self, btn_editPicList):
        pgnum = 1
        self.builder.get_object("nbk_Main").set_current_page(7)
        self.builder.get_object("nbk_Viewer").set_current_page(pgnum)
        self.onViewerChangePage(None,None,pgnum)
    
    def ontv_sizeallocate(self, atv, dummy):
        b = atv.get_buffer()
        it = b.get_iter_at_offset(-1)
        atv.scroll_to_iter(it, 0, False, 0, 0)

    def fileChooser(self, title, filters = None, multiple = True, folder = False):
        dialog = Gtk.FileChooserDialog(title, None,
            (Gtk.FileChooserAction.SELECT_FOLDER if folder else Gtk.FileChooserAction.OPEN),
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            ("Select" if folder else Gtk.STOCK_OPEN), Gtk.ResponseType.OK))
        dialog.set_default_size(730, 565)
        dialog.set_select_multiple(multiple)
        if filters != None: # was len(filters):
            # filters = {"PDF files": {"pattern": "*.pdf", "mime": "application/pdf"}}
            filter_in = Gtk.FileFilter()
            for k, f in filters.items():
                filter_in.set_name(k)
                for t, v in f.items():
                    if t == "pattern":
                        filter_in.add_pattern(v)
                    elif t == "patterns":
                        for p in v:
                            filter_in.add_pattern(p)
                    if t == "mime":
                        filter_in.add_mime_type(v)
            dialog.add_filter(filter_in)

        dialog.set_keep_above(True)
        response = dialog.run()
        fcFilepath = None
        if response == Gtk.ResponseType.OK:
            if folder:
                fcFilepath = [dialog.get_filename()+"/"]
            else:
                fcFilepath = dialog.get_filenames()
        dialog.destroy()
        return fcFilepath

    def onDiglotClicked(self, c_diglot):
        status = self.get("c_diglot")
        self.builder.get_object("gr_diglot").set_sensitive(status)
        self.builder.get_object("l_diglotString").set_visible(status)
        if status:
            self.builder.get_object("c_includeillustrations").set_active(False)
        
        self.onDiglotDimensionsChanged(None)

    def onDiglotDimensionsChanged(self, btn):
        if not self.get("c_diglot"):
            DiglotString = ""
        else:
            secprjid = self.get("cb_diglotSecProject")
            # I'm not sure if there's a better way to handle this - looking for the already-created Secondary diglot file
            sectmpdir = os.path.join(self.settings_dir, secprjid, 'PrintDraft') if self.get("c_useprintdraftfolder") else self.working_dir
            jobs = self.getBooks()
            if len(jobs) > 1:
                secfname = os.path.join(sectmpdir, "ptxprint-{}_{}{}.pdf".format(jobs[0], jobs[-1], secprjid))
            else:
                secfname = os.path.join(sectmpdir, "ptxprint-{}{}.pdf".format(jobs[0], secprjid))
            # TO DO: We need to be able to GET the page layout values from the PRIMARY project
            # (even when creating the Secondary PDF so that the dimensions match).
            PageWidth = int(re.split("[^0-9]",re.sub(r"^(.*?)\s*,.*$", r"\1", self.get("cb_pagesize")))[0]) or 148
            
            Margins = self.get("s_diglotMargins")
            MiddleGutter = self.get("s_diglotMiddleGutter")
            BindingGutter = self.get("s_diglotpagegutter")
            PriColWid = self.get("s_PriColWidth")

            SecColWid = PageWidth - PriColWid - MiddleGutter - BindingGutter - (2 * Margins)
            self.builder.get_object("s_SecColWidth").set_value(SecColWid)

            # Calc Pri Settings (right side of page; or outer if mirrored)
            # PriColWid = self.get("s_PriColWidth")
            PriSideMarginFactor = 1
            PriBindingGutter = PageWidth - Margins - PriColWid - Margins

            # Calc Sec Settings (left side of page; or inner if mirrored)
            # SecColWid = PageWidth - PriColWid - MiddleGutter - BindingGutter - (2 * Margins)
            SecSideMarginFactor = (PriColWid + Margins + MiddleGutter) / Margins
            SecRightMargin = PriColWid + Margins + MiddleGutter
            
            SecBindingGutter = PageWidth - (2 * SecRightMargin) - SecColWid 

            PriPercent = round((PriColWid / (PriColWid + SecColWid) * 100),1)
            self.builder.get_object("t_PriPercent").set_text(str(PriPercent)+"%")
            self.builder.get_object("t_SecPercent").set_text(str(100 - PriPercent)+"%")
            hdr = ""
            if self.get("c_outputSecText"):
                if self.get("c_diglotHeaders"):
                    hdr = r"""
\def\RHoddleft{\rangeref}
\def\RHoddcenter{\empty}
\def\RHoddright{\empty}
\def\RHevenleft{\empty}
\def\RHevencenter{\empty}
\def\RHevenright{\rangeref}
"""
                DiglotString = "%% SECONDARY PDF settings"+ \
                               "\n\MarginUnit={}mm".format(Margins)+ \
                               "\n\BindingGuttertrue"+ \
                               "\n\BindingGutter={}mm".format(SecBindingGutter)+ \
                               "\n\def\SideMarginFactor{{{:.2f}}}".format(SecSideMarginFactor)+ \
                               "\n\BodyColumns=1" + hdr
            else:
                if self.get("c_diglotHeaders"):
                    hdr = r"""
\def\RHoddleft{\pagenumber}
\def\RHoddcenter{\empty}
\def\RHoddright{\rangeref}
\def\RHevenleft{\rangeref}
\def\RHevencenter{\empty}
\def\RHevenright{\pagenumber}"""
                DiglotString = "%% PRIMARY (+ SECONDARY) PDF settings"+ \
                               "\n\MarginUnit={}mm".format(Margins)+ \
                               "\n\BindingGuttertrue"+ \
                               "\n\BindingGutter={}mm".format(PriBindingGutter)+ \
                               "\n\def\SideMarginFactor{{{:.2f}}}".format(PriSideMarginFactor)+ \
                               "\n\BodyColumns=1"+ \
                               "\n\def\MergePDF{" + secfname + "}" + hdr
            self.builder.get_object("l_diglotString").set_text(DiglotString) # We probably need a better way to do this

    def onGenerateHyphenationListClicked(self, btn_generateHyphenationList):
        self.info.createHyphenationFile()

    def onPrettyIntroOutlineClicked(self, btn):
        if self.get("c_prettyIntroOutline"): # if turned on...
            badbks = self.checkSFMforFancyIntroMarkers()
            if len(badbks):
                # print("Sorry - but you can't enable this option as the selected files have not got the required markup")
                self.set("c_prettyIntroOutline", False)
                m1 = "Invalid Option for Selected Books"
                m2 = "The book(s) listed below do not have the" + \
                   "\nrequired markup for this feature to be enabled." + \
                   "\n(Refer to Tooltip for further details.)" + \
                   "\n\n{}".format(", ".join(badbks))
                dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR, \
                                            buttons=Gtk.ButtonsType.OK, message_format=m1)
                dialog.format_secondary_text(m2)
                dialog.format_secondary_text(m2)
                dialog.set_keep_above(True)
                dialog.run()
                dialog.destroy()

    def checkSFMforFancyIntroMarkers(self):
        unfitBooks = []
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        for bk in bks:
            fname = self.getBookFilename(bk, prjid)
            fpath = os.path.join(self.settings_dir, prjid, fname)
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as inf:
                    sfmtxt = inf.read()
                # Put strict conditions on the format (including only valid \ior using 0-9, not \d digits from any script)
                if regex.search(r"\\iot .+\r?\n(\\io\d .+\\ior ([0-9]+(:[0-9]+)?[-\u2013][0-9]+(:[0-9]+)?) ?\\ior\* ?\r?\n)+\\c 1", sfmtxt, flags=regex.MULTILINE) \
                   and len(regex.findall(r"\\iot",sfmtxt)) == 1: # Must have exactly 1 \iot per book 
                    pass
                else:
                    unfitBooks.append(bk)
        return unfitBooks

    def onFindMissingCharsClicked(self, btn_findMissingChars):
        count = collections.Counter()
        prjid = self.get("cb_project")
        prjdir = os.path.join(self.settings_dir, prjid)
        bks = self.getBooks()
        for bk in bks:
            fname = self.getBookFilename(bk, prjid)
            fpath = os.path.join(self.settings_dir, prjid, fname)
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as inf:
                    # Strip out all markers themselves, and English content fields
                    sfmtxt = inf.read()
                    sfmtxt = regex.sub(r'\\id .+?\r?\n', '', sfmtxt)
                    sfmtxt = regex.sub(r'\\rem .+?\r?\n', '', sfmtxt)
                    # throw out illustration markup, BUT keep the caption text (USFM2 + USFM3)
                    sfmtxt = regex.sub(r'\\fig (.*\|){5}([^\\]+)?\|[^\\]+\\fig\*', '\2', sfmtxt) 
                    sfmtxt = regex.sub(r'\\fig ([^\\]+)?\|.*src=[^\\]+\\fig\*', '\1', sfmtxt) 
                    sfmtxt = regex.sub(r'\\[a-z]+\d?\*? ?', '', sfmtxt) # remove all \sfm codes
                    sfmtxt = regex.sub(r'[0-9]', '', sfmtxt) # remove all digits
                    bkcntr = collections.Counter(sfmtxt)
                    count += bkcntr
        # slist = sorted(count.items(), key=lambda pair: pair[0])
        reg = self.get("f_body")
        f = TTFont(reg)
        if f.filename == None:
            self.msgUnsupportedFont(reg)
            return 
        allchars = ''.join([i[0] for i in count.items()])
        if self.get("cb_glossaryMarkupStyle") == "with ⸤floor⸥ brackets":
            allchars += "\u2e24\u2e25"
        if self.get("cb_glossaryMarkupStyle") == "with ⌊floor⌋ characters":
            allchars += "\u230a\u230b"
        if self.get("cb_glossaryMarkupStyle") == "with ⌞corner⌟ characters":
            allchars += "\u231e\u231f"
        # print(allchars.encode("raw_unicode_escape"))
        missing = f.testcmap(allchars)
        self.builder.get_object("t_missingChars").set_text(' '.join(missing))
        missingcodes = ""
        for char in missing:
            missingcodes += repr(char.encode('raw_unicode_escape'))[2:-1].replace("\\\\","\\") + " "
        self.builder.get_object("t_missingChars").set_tooltip_text(missingcodes)
        if len(missing):
            self.builder.get_object("c_useFallbackFont").set_active(True)
        else:
            self.builder.get_object("c_useFallbackFont").set_active(False)
            self.builder.get_object("gr_fallbackFont").set_sensitive(False)
            dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR, \
                     buttons=Gtk.ButtonsType.OK, message_format="FYI: The Regular font already supports all the characters in the text.")
            dialog.format_secondary_text("A fallback font is not required.\nThis 'Use Fallback Font' option has been disabled.")
            dialog.set_keep_above(True)
            dialog.run()
            dialog.destroy()

    def onFontBoldChanged(self, f_bold):
        fnm = self.get("f_bold")
        f = TTFont(fnm)
        if f.filename == None:
            self.msgUnsupportedFont(fnm)

    def onFontItalicChanged(self, f_italic):
        fnm = self.get("f_italic")
        f = TTFont(fnm)
        if f.filename == None:
            self.msgUnsupportedFont(fnm)

    def onFontBoldItalicChanged(self, f_bolditalic):
        fnm = self.get("f_bolditalic")
        f = TTFont(fnm)
        if f.filename == None:
            self.msgUnsupportedFont(fnm)

    def onExtraRegularChanged(self, f_extraRegular):
        reg = self.get("f_body")
        xtraReg = self.get("f_extraRegular")
        if reg[:-3] == xtraReg[:-3]:
            dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR, \
                     buttons=Gtk.ButtonsType.OK, message_format="The Fallback Font should to be DIFFERENT from the Regular Font.")
            dialog.format_secondary_text("Please select a different Font.")
            dialog.set_keep_above(True)
            dialog.run()
            dialog.destroy()
        else:
            f = TTFont(xtraReg)
            if f.filename == None:
                self.msgUnsupportedFont(xtraReg)
                return 
            msngchars = self.builder.get_object("t_missingChars").get_text() # .split(" ")
            msngchars = spclChars = re.sub(r"\\[uU]([0-9a-fA-F]{4,6})", lambda m:chr(int(m.group(1), 16)), msngchars)
            stillmissing = f.testcmap(msngchars)
            if len(stillmissing):
                dialog = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.WARNING, \
                         buttons=Gtk.ButtonsType.OK, message_format="The Fallback Font just selected does NOT support all the missing characters listed.")
                dialog.format_secondary_text("Please select a different Font.")
                dialog.set_keep_above(True)
                dialog.run()
                dialog.destroy()

    def msgUnsupportedFont(self, fontname):
        par = self.builder.get_object('ptxprint')  #  flags=Gtk.DialogFlags.MODAL,
        dialog = Gtk.MessageDialog(parent=par, type=Gtk.MessageType.WARNING, \
                 buttons=Gtk.ButtonsType.OK, message_format="The Font: '{}'\ncannot be used as it has\nnot been installed properly.".format(fontname[:-3]))
        # dialog.set_type_hint(GTK_WINDOW(popwindow), GTK_WINDOW_TYPE_HINT_DIALOG)
        dialog.format_secondary_text("Please select a different Font\n  or\nInstall the font for ALL users.")
        dialog.set_keep_above(True)
        dialog.run()
        dialog.destroy()

    def msgQuestion(self, title, question):
        # par = par = self.builder.get_object('ptxprint')
        dialog = Gtk.MessageDialog(parent=self, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO, message_format=title)
        dialog.format_secondary_text(question)
        dialog.set_keep_above(True)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return(True)
        elif response == Gtk.ResponseType.NO:
            return(False)
