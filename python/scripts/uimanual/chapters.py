r"""
Chapter plan for the PTXprint UI manual.

Each chapter collects the controls whose first breadcrumb (the tab or dialog they live in)
is listed in "places". Chapters with no places are prose-only (guides, glossary, etc.).
The prose for each chapter lives in docs/uimanual/content/<file>.md
"""

chapters = [
    # (id, title, places)
    ("00-introduction", "About this manual", []),
    ("01-getting-started", "Getting started with PTXprint", []),
    ("02-main-window", "The main window, menu and view levels",
        ["Main window", "Main menu (top-right ☰ button)"]),
    ("03-basic", "Basic tab",
        ["Basic tab", "Save Current Configuration As... (dialog)", "Lock/Unlock Configuration (dialog)",
         "Copy Configuration To... (dialog)", "Select Books To Export to PDF (dialog)",
         "Import Scripture... (dialog)", "Please Confirm... (dialog)"]),
    ("04-layout", "Layout tab", ["Layout tab", "Change the Grid Settings (dialog)"]),
    ("05-fonts", "Fonts+Script tab",
        ["Fonts+Script tab", "Pick a Font (and Typeface) (dialog)", "Select Font Features... (dialog)",
         "Create Hyphenation List (dialog)", "Add Tatweel (kashida) Rules (dialog)"]),
    ("06-body", "Body tab", ["Body tab"]),
    ("07-notes", "Notes+Refs tab", ["Notes+Refs tab", "Generate Strong's Index... (dialog)"]),
    ("08-headfoot", "Header+Footer tab", ["Header+Footer tab"]),
    ("09-pictures", "Pictures tab",
        ["Pictures tab", "Select Images... (dialog)", "Download & Install Image Sets (dialog)",
         "Illustration Credit Overlay (dialog)", "Add Map (dialog)", "Generate PicList (dialog)"]),
    ("10-diglot", "Diglot tab (two or more languages)", ["Diglot tab", "Save As Monoglot... (dialog)"]),
    ("11-tabsborders", "Tabs+Borders tab", ["Tabs+Borders tab", "Border Settings (dialog)"]),
    ("12-styles", "Styles tab",
        ["Styles tab", "Add/Edit Style (dialog)", "Sidebar Image Settings (dialog)",
         "Size and Position Settings (dialog)"]),
    ("13-advanced", "Advanced tab", ["Advanced tab"]),
    ("14-viewedit", "View+Edit tab", ["View+Edit tab", "Generate Front Matter (dialog)"]),
    ("15-peripherals", "Peripherals tab (front and back matter)", ["Peripherals tab", "Cover tab"]),
    ("16-publications", "Publications tab", ["Publications tab"]),
    ("17-finishing", "Finishing tab", ["Finishing tab"]),
    ("18-printers", "Printers tab", ["Printers tab"]),
    ("19-preview", "PDF Preview window, layout analysis and page filling",
        ["PDF Preview (dialog)", "PDF Preview > Issue types popup", "SpeedSlice (dialog)",
         "Enter new anchor verse ref (dialog)"]),
    ("20-import", "Importing settings", ["Import Settings... (dialog)"]),
    ("21-help", "Help tab and getting support", ["Help tab", "Log tab", "About dialog"]),
    ("30-howto", "How do I...? (step-by-step tasks)", []),
    ("31-troubleshooting", "Problems and solutions", []),
    ("32-glossary", "Glossary of terms", []),
]


def chapterFor(breadcrumbs):
    first = breadcrumbs[0] if breadcrumbs else None
    for cid, title, places in chapters:
        if first in places:
            return cid
    return None
