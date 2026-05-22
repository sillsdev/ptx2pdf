#!/usr/bin/python3

import argparse, sys, os, re, configparser, subprocess, platform
import site, logging, shutil
import tempfile
import uuid
from shutil import rmtree
from zipfile import ZipFile

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    site.USER_BASE = os.path.join(os.path.expanduser("~"), ".local")
    if not hasattr(site, 'getuserbase'):
        site.getuserbase = lambda : site.USER_BASE
    os.putenv("PATH", sys._MEIPASS)

try:
    import ptxprint
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib"))
    import ptxprint
from ptxprint.utils import saferelpath
from ptxprint.pdf.pdfsig import make_signatures, get_page_size
from ptxprint.pdf.pdfdiff import createDiff
from ptxprint.pdf.procpdf import procpdf
from ptxprint.pdfrw import PdfReader, PdfWriter, PageMerge
from ptxprint.pdfblender import blend_pdf

from pathlib import Path
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Poppler', '0.18')
from gi.repository import Gtk
from ptxprint.gtkutils import getWidgetVal, setWidgetVal, setFontButton, makeSpinButton, doError
from ptxprint.utils import pycodedir

def getnsetlang(config):
    envlang = os.getenv("LANG", None)
    oldlang = config.get("init", "syslang", fallback=None)
    newlang = config.get("init", "lang", fallback=None)
    if envlang is None or oldlang == envlang:
        return newlang
    config.set("init", "lang", envlang or "")
    config.set("init", "syslang", envlang or "")
    return envlang


class Finisher(Gtk.Application):
    def __init__(self):
        super().__init__()
        self.builder = Gtk.Builder()
        gladefile = os.path.join(pycodedir(), "pdfinish.glade")
        self.builder.add_from_file(gladefile)
        self.builder.connect_signals(self)
        self.mw = self.builder.get_object("pdfinish")
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_file_1 = None
        self.tmp_file_2 = None
        self.errored = False

        self.mw.show_all()
        Gtk.main()

    def onProcessClicked(self, btn):
        self.errored, self.tmp_file_1, self.tmp_file_2 = False, None, None
        self.input_pdf_path = self.builder.get_object("fp_input").get_filename()
        if not self.input_pdf_path:
            self.show_error("You need to select an input file!")
            return
        elif not self.input_pdf_path.endswith('.pdf'):
            self.show_error("You must select an input file with a .pdf extension.")
            return
        dialog = Gtk.FileChooserDialog(
            title="Select output file",
            parent=self.mw,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )

        checkbox_action_mapping = [
            ('c_watermark',   self._run_watermark),
            ('c_overlay',     self._run_overlay),
            ('c_format',      self._run_procpdf),
            ('c_repaginate',  self._run_pdfsig),
            ('c_diff',        self._run_pdfdiff),
        ]

        actions_to_run = [action for checkbox, action in checkbox_action_mapping if self.builder.get_object(checkbox).get_active()]

        if not actions_to_run:
            self.show_error('There is nothing to do! Select at least one action before clicking Process.')
            return

        for action in actions_to_run:
            self.run_action(action)

        if self.errored:
            return

        dialog.set_do_overwrite_confirmation(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.output_filepath = dialog.get_filename()
        dialog.destroy()
        if response != Gtk.ResponseType.OK:
            return

        if self.tmp_file_1 is not None and os.path.exists(self.tmp_file_1):
            shutil.move(self.tmp_file_1, self.output_filepath)
            self.tmp_file_1, self.tmp_file_2 = None, None

        if not os.path.exists(self.output_filepath):
            self.show_error("File not created as expected!")
            return

        # open output PDF
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', self.output_filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(self.output_filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', self.output_filepath))

    def onCloseClicked(self, btn):
        Gtk.main_quit()

    def onDestroy(self, btn):
        Gtk.main_quit()

    def show_error(self, message):
        self.errored = True
        dialog = Gtk.MessageDialog(
            transient_for=self.mw,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Error",
        )

        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def run_action(self, action):
        """
        Run an action
        """
        self.tmp_file_2 = ''.join([self.tmp_dir.name, '/', str(uuid.uuid4()), '.pdf'])
        if not self.tmp_file_1:
            action(self.input_pdf_path, self.tmp_file_2)
        else:
            action(self.tmp_file_1, self.tmp_file_2)
        self.tmp_file_1, self.tmp_file_2 = self.tmp_file_2, None

    def _run_pdfdiff(self, input_pdf_path, output_pdf_path):
        """
        Run pdfdiff from Gtk application
        """
        base_pdf_path = self.builder.get_object("fp_compare").get_filename()
        input_diff_rgba = self.builder.get_object("col_ndiffColor").get_rgba()
        input_diff_color = (input_diff_rgba.red * 256, input_diff_rgba.green  * 256, input_diff_rgba.blue  * 256)
        base_diff_rgba = self.builder.get_object("col_odiffColor").get_rgba()
        base_diff_color = (base_diff_rgba.red * 256, base_diff_rgba.green  * 256, base_diff_rgba.blue  * 256)
        # TODO: 'Offset starting page' option - what it is?
        onlydiffs = self.builder.get_object("c_onlyDiffs").get_active()
        diffpages = int(self.builder.get_object("s_diffpages").get_value())

        if not base_pdf_path:
            self.show_error("You need to select a file for computing the diff!")
            return
        elif not base_pdf_path.endswith('.pdf'):
            self.show_error("You must select a file with .pdf extension for computing the diff.")
            return
        createDiff(input_pdf_path, base_pdf_path, output_pdf_path, doError, color=input_diff_color,
                                onlydiffs=onlydiffs, oldcolor=base_diff_color, limit=diffpages)

    def _run_pdfsig(self, input_pdf_path, output_pdf_path):
        """
        Run pdfsig from Gtk application
        """
        pages_per_spread = self.builder.get_object("ecb_pagesPerSpread").get_active_id()
        sheetsize_active_text = self.builder.get_object("ecb_sheetSize").get_active_text()
        sheets_per_sig = int(self.builder.get_object("s_sheetsPerSignature").get_value())
        fold_cut_margin = self.builder.get_object("s_foldCutMargin").get_value()
        add_crop_marks = self.builder.get_object("c_cropmarks").get_active()
        right_to_left = str(self.builder.get_object("c_RTL").get_active())  # procpdf wants a string
        fold_first = self.builder.get_object("c_foldFirst").get_active()
        selected_sheet_size = self._get_sheet_size(sheetsize_active_text)
        scale_to_fit = self.builder.get_object("c_scaleToFit").get_active()
        if selected_sheet_size is None:
            return
        outwidth, outheight = get_page_size(selected_sheet_size)
        page_size = f"{outwidth} pt, {outheight} pt"
        procpdf(output_pdf_path, input_pdf_path, "None", doError, None,
                cover=None, pgsperspread=pages_per_spread, sheetsinsigntr=sheets_per_sig,
                sheetsize=page_size, foldcutmargin=fold_cut_margin, cropmarks=add_crop_marks,
                ifrtl=right_to_left, foldfirst=fold_first, scaletofit=scale_to_fit,
                output_filepath=output_pdf_path)

    def _run_procpdf(self, input_pdf_path, output_pdf_path):
        """
        Run formatting from Gtk application
        """
        output_format = self.builder.get_object("ecb_outputFormat").get_active_id()  # aka, ispdfxa
        spot_rgba = self.builder.get_object("col_spotColor").get_rgba()
        spottolerance = self.builder.get_object("s_spotColorTolerance").get_value()
        spotcolor = f"rgb({spot_rgba.red * 256}, {spot_rgba.green  * 256}, {spot_rgba.blue  * 256})"

        # run procpdf - what does outfname do?
        procpdf(output_pdf_path, input_pdf_path, output_format, doError, None, cover=None, spottolerance=spottolerance, spotcolor=spotcolor, scaletofit=scale_to_fit, output_filepath=output_pdf_path)

    def _run_overlay(self, input_pdf_path, output_pdf_path):
        """
        Run overlaying from Gtk application
        """
        mirrored = self.builder.get_object("c_mirrored").get_active()
        blend_pdf(input_pdf_path, output_pdf_path, mirrored=mirrored)

    def _run_watermark(self, input_pdf_path, output_pdf_path):
        """
        Run watermarking from Gtk application
        """
        watermark_pdf_path = self.builder.get_object("fp_watermark").get_filename()

        if not watermark_pdf_path:
            self.show_error("You need to select a file for the watermark!")
            return
        elif not watermark_pdf_path.endswith('.pdf'):
            self.show_error("You must select a file with .pdf extension for the watermark.")
            return

        base = PdfReader(input_pdf_path)
        watermark_page = PdfReader(watermark_pdf_path).pages[0]
        for page in base.pages:
            PageMerge(page).add(watermark_page, prepend=True).render()
        PdfWriter(output_pdf_path, trailer=base).write()

    def _get_sheet_size(self, sheet_text):
        sheet_sizes = {
            "420mm, 594mm (A2)": "a2",
            "297mm, 420mm (A3)": "a3",
            "210mm, 297mm (A4)": "a4",
            "17in, 22in (ANSI C)": "431.8x558.8",
            "11in, 17in (ANSI B)": "279.4x431.8",
            "8.5in, 11in (Letter)": "ltr",
            "353mm, 500mm (B3)": "353x500",
            "250mm, 353mm (B4)": "250x353",
            "176mm, 250mm (B5)": "176x250",
        }
        if sheet_text in sheet_sizes:
            return sheet_sizes[sheet_text]
        if sheet_text.count(',') != 1:
            self.show_error('Format of sheet dimensions not understood. Please specify in format "width, height"')
            return
        width, height = sheet_text.split(',')
        if 'mm' in width:
            width = float(width.split('mm')[0])
        elif 'in' in width:
            width = float(width.split('in')[0]) * 25.4
        else:
            self.show_error('Unknown or unspecified unit!')
            return
        if 'mm' in height:
            height = float(height.split('mm')[0])
        elif 'in' in height:
            height = float(height.split('in')[0]) * 25.4
        else:
            self.show_error('Unknown or unspecified unit!')
            return
        return 'x'.join((str(width), str(height)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile",nargs="?",help="Input PDF file")

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        from ptxprint.gtkutils import HelpTextViewWindow
        tv = HelpTextViewWindow()
        def print_message(message, file=None):
            tv.print_message(message)
        parser._print_message = print_message

    args = parser.parse_args()

    finisher = Finisher()

if __name__=="__main__": main()
