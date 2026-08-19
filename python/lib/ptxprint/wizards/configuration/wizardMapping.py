# Generated from PTXprintWizardMatrix.xlsx
# Source of truth: wizards/configuration/PTXprintWizardMatrix.xlsx
# Application order (last wins): outputMedium → layout → modifiers → printer → binding → columns

# Config-file values keyed by layout id. Only keys that differ from PTXprint's default are included.
LAYOUT_OVERRIDES = {
    "teamCheck": {
        "paper/margins":            "18",
        "paper/allowunbalanced":    True,
        "document/sensitive":       True,
        "document/hidemptyverses":  True,
        "header/mirrorlayout":      False,
    },
    "communityCheck": {
        "paper/margins":            "15",
        "paper/allowunbalanced":    True,
        "document/ifinclfigs":      True,
        "notes/includefootnotes":   False,
        "notes/includexrefs":       False,
        "document/hidemptyverses":  True,
    },
    "consultantUns": {
        "paper/margins":            "20",
        "paper/allowunbalanced":    True,
        "document/sensitive":       True,
        "document/hidemptyverses":  True,
        "header/mirrorlayout":      False,
    },
    "exegeticalCheck": {
        "paper/margins":            "18",
        "paper/allowunbalanced":    True,
        "document/sensitive":       True,
        "document/hidemptyverses":  True,
        "header/mirrorlayout":      False,
    },
    "pewBible": {
        "paper/ifaddgutter":        True,
        "paper/gutter":             "8",
        "paragraph/ifhyphenate":    True,
        "document/toc":             True,
        "document/preventorphans":  True,
        "document/preventwidows":   True,
        "thumbtabs/ifthumbtabs":    True,
    },
    "childrensBible": {
        "paper/columns":            False,
        "paper/margins":            "15",
        "paper/ifverticalrule":     False,
        "paper/fontfactor":         "13",
        "paragraph/linespacing":    "17",
        "paragraph/ifjustify":      False,
        "document/ifinclfigs":      True,
        "document/iffigshowcaptions": True,
        "notes/includefootnotes":   False,
        "notes/includexrefs":       False,
        "document/toc":             True,
        "document/introoutline":    False,
        "fancy/pageborders":        True,
        "fancy/booktitleborder":    True,
    },
    "pastorsBible": {
        "paper/margins":            "10",
        "paper/ifaddgutter":        True,
        "paper/gutter":             "8",
        "paper/fontfactor":         "10",
        "paragraph/linespacing":    "13",
        "paragraph/ifhyphenate":    True,
        "notes/showextxrefs":       True,
        "notes/xrlocation":         "centre",
        "notes/xrpos":              "centre",
        "studynotes/includextfn":   True,
        "document/toc":             True,
        "document/preventorphans":  True,
        "document/preventwidows":   True,
        "thumbtabs/ifthumbtabs":    True,
    },
    "largePrintBible": {
        "paper/columns":            False,
        "paper/margins":            "14",
        "paper/ifaddgutter":        True,
        "paper/gutter":             "8",
        "paper/ifverticalrule":     False,
        "paper/fontfactor":         "16",
        "paragraph/linespacing":    "21",
    },
    "lifeApplicationBible": {
        "paper/ifaddgutter":        True,
        "paper/gutter":             "8",
        "paragraph/ifhyphenate":    True,
        "document/ifinclfigs":      True,
        "document/iffigshowcaptions": True,
        "notes/showextxrefs":       True,
        "studynotes/includextfn":   True,
        "studynotes/includesidebar": True,
        "document/toc":             True,
        "document/preventorphans":  True,
        "document/preventwidows":   True,
        "fancy/booktitleborder":    True,
    },
    "journalingBible": {
        "paper/columns":            False,
        "paper/ifaddgutter":        True,
        "paper/gutter":             "25",
        "paper/ifoutergutter":      True,
        "paper/ifverticalrule":     False,
        "paper/notelines":          True,
        "paragraph/ifjustify":      False,
        "notes/includexrefs":       False,
        "document/marginalverses":  True,
    },
    "lectionary": {
        "paper/columns":            False,
        "paper/margins":            "16",
        "paper/ifaddgutter":        True,
        "paper/gutter":             "8",
        "paper/ifverticalrule":     False,
        "paper/fontfactor":         "14",
        "paragraph/linespacing":    "18",
        "notes/includefootnotes":   False,
        "notes/includexrefs":       False,
        "document/preventorphans":  True,
        "document/preventwidows":   True,
        "document/bookintro":       False,
        "document/introoutline":    False,
    },
}

# Orthogonal overlays; applied on top of layout overrides
MODIFIER_OVERRIDES = {
    "diglot": {
        "document/ifdiglot":            True,
        "poly/fraction":                "50.0",
        "document/diglotmergemode":     "simple",
        "document/diglotsepnotes":      True,
        "document/diglotjoinvrule":     True,
    },
    "interlinear": {
        "project/interlinear":          True,
    },
    "sensitive": {
        "document/sensitive":           True,
    },
    "colour": {
        "snippets/pdfoutput":           "PDF/X-4",
        "transparency_":                "true",
    },
}

# Output medium overrides
OUTPUT_MEDIUM_OVERRIDES = {
    "print": {
        "snippets/pdfoutput":           "PDF/X-1a",
        "transparency_":                "false",
    },
    "digital": {
        "snippets/pdfoutput":           "Screen",
        "transparency_":                "true",
        "paper/columns":                False,
        "paper/fontfactor":             "12",
    },
}

# Per-printer and per-binding overrides (print only)
PRODUCTION_OVERRIDES = {
    "printer.homeInkjet": {
        "snippets/pdfoutput":           "PDF/X-4",
        "transparency_":                "true",
        "finishing/scaletofit":         True,
    },
    "printer.officeLaser": {
        "snippets/pdfoutput":           "PDF/X-1a",
        "finishing/scaletofit":         True,
    },
    "printer.photocopyShop": {
        "snippets/pdfoutput":           "PDF/X-1a",
    },
    "printer.podLow": {
        "snippets/pdfoutput":           "PDF/X-1a",
    },
    "printer.podHigh": {
        "snippets/pdfoutput":           "PDF/X-1a",
        "paper/cropmarks":              True,
    },
    "printer.offset": {
        "snippets/pdfoutput":           "PDF/X-1a",
        "paper/cropmarks":              True,
    },
    "binding.saddleStitch": {
        "paper/ifaddgutter":            False,
        "paper/gutter":                 "3",
        "cover/makecoverpage":          False,
        "cover/includespine":           False,
        "cover/coverbleed":             "2",
    },
    "binding.spiral": {
        "paper/ifaddgutter":            True,
        "paper/gutter":                 "10",
        "cover/makecoverpage":          False,
        "cover/includespine":           False,
        "cover/coverbleed":             "0",
    },
    "binding.sideStitched": {
        "paper/ifaddgutter":            True,
        "paper/gutter":                 "8",
        "cover/makecoverpage":          False,
        "cover/includespine":           False,
        "cover/coverbleed":             "2",
    },
    "binding.perfect": {
        "paper/ifaddgutter":            True,
        "paper/gutter":                 "8",
        "cover/makecoverpage":          True,
        "cover/includespine":           True,
        "cover/totalpages":             None,   # computed from pageCount answer
        "cover/coverbleed":             "3",
    },
    "binding.hardcover": {
        "paper/ifaddgutter":            True,
        "paper/gutter":                 "10",
        "cover/makecoverpage":          True,
        "cover/includespine":           True,
        "cover/totalpages":             None,   # computed from pageCount answer
        "cover/coverbleed":             "5",
    },
}

# Page size presets keyed by wizard option id (matches wizardQuestions.json pageSize option ids).
# Value strings must exactly match entries in PTXprint's ecb_pagesize combo box.
# Sorted small-to-large by area (same order as the wizard options list).
PAGE_SIZE_PRESETS = {
    "pa6":       {"mm": [105, 140], "label": "PA6 (105×140 mm)",      "value": "105mm, 140mm (PA6)"},
    "a6":        {"mm": [105, 148], "label": "A6 (105×148 mm)",       "value": "105mm, 148mm (A6)"},
    "b6":        {"mm": [125, 176], "label": "B6 (125×176 mm)",       "value": "125mm, 176mm (B6)"},
    "compact":   {"mm": [133, 210], "label": "Compact (133×210 mm)",  "value": "5.25in, 8.25in (133x210mm)"},
    "pa5":       {"mm": [140, 210], "label": "PA5 (140×210 mm)",      "value": "140mm, 210mm (PA5)"},
    "halfLetter":{"mm": [140, 216], "label": "Half Letter (140×216 mm)", "value": "5.5in, 8.5in (1/2 Letter)"},
    "a5":        {"mm": [148, 210], "label": "A5 (148×210 mm)",       "value": "148mm, 210mm (A5)"},
    "common":    {"mm": [147, 221], "label": "Common (147×221 mm)",   "value": "5.8in, 8.7in (147x221mm)"},
    "kbsMax":    {"mm": [165, 234], "label": "KBS Max (165×234 mm)",  "value": "165mm, 234mm (KBS max page)"},
    "b5":        {"mm": [176, 250], "label": "B5 (176×250 mm)",       "value": "176mm, 250mm (B5)"},
    "pa4":       {"mm": [210, 280], "label": "PA4 (210×280 mm)",      "value": "210mm, 280mm (PA4)"},
    "letter":    {"mm": [216, 279], "label": "Letter (216×279 mm)",   "value": "8.5in, 11in (Letter)"},
    "a4":        {"mm": [210, 297], "label": "A4 (210×297 mm)",       "value": "210mm, 297mm (A4)"},
}

# Paper-weight overrides keyed by paperThickness option id
# TO VERIFY: config key name against PTXprint's paper-weight catalogue
PAPER_WEIGHT_OVERRIDES = {
    "gsm55":  {"paper/paperweight": "55"},
    "gsm60":  {"paper/paperweight": "60"},
    "gsm70":  {"paper/paperweight": "70"},
    "gsm80":  {"paper/paperweight": "80"},
    "gsm90":  {"paper/paperweight": "90"},
    "gsm100": {"paper/paperweight": "100"},
    "gsm115": {"paper/paperweight": "115"},
}

SCREEN_TARGET_SIZES = {
    "phone":  "90mm, 160mm (phone)",
    "tablet": "148mm, 210mm (A5)",
    "pc":     "210mm, 297mm (A4)",
}


def applyAnswers(answers, model):
    """Write wizard answers to the PTXprint model.

    The model must expose .set(widget_id, value, skipmissing=True).
    Config keys are looked up in ptxprint.modelmap.ModelMap; values
    are converted to the widget-appropriate Python type before writing.
    """
    from ptxprint.modelmap import ModelMap

    overrides = {}

    # 1. Output medium
    om = answers.get("outputMedium", "print")
    overrides.update(OUTPUT_MEDIUM_OVERRIDES.get(om, {}))

    # 2. Layout (product type)
    pt = answers.get("productType")
    if pt:
        overrides.update(LAYOUT_OVERRIDES.get(pt, {}))

    # 3. Modifiers
    mods = list(answers.get("diglotInterlinear") or [])
    if answers.get("publicationStage") == "prePublication":
        mods.append("sensitive")
    if answers.get("colour") == "colour":
        mods.append("colour")
    for m in mods:
        overrides.update(MODIFIER_OVERRIDES.get(m, {}))

    # 4. Printer
    if om == "print":
        printer = answers.get("printer")
        if printer:
            overrides.update(PRODUCTION_OVERRIDES.get("printer." + printer, {}))

    # 4b. Paper thickness (print only)
    if om == "print":
        pt_ans = answers.get("paperThickness")
        if pt_ans:
            overrides.update(PAPER_WEIGHT_OVERRIDES.get(pt_ans, {}))

    # 5. Binding
    if om == "print":
        binding = answers.get("binding")
        if binding:
            prod = dict(PRODUCTION_OVERRIDES.get("binding." + binding, {}))
            # Inject computed page count
            if "cover/totalpages" in prod and answers.get("pageCount") is not None:
                prod["cover/totalpages"] = str(int(answers["pageCount"]))
            overrides.update(prod)

    # 6. Explicit column answer (single → False, double → True)
    col = answers.get("columns")
    if col is not None:
        overrides["paper/columns"] = (col == "double")

    # Diglot always forces two-column (one language per column) — overrides step 6
    if "diglot" in (answers.get("diglotInterlinear") or []):
        overrides["paper/columns"] = True

    # 7. Page size
    if om == "digital":
        target = answers.get("screenTarget")
        if target and target in SCREEN_TARGET_SIZES:
            overrides["paper/pagesize"] = SCREEN_TARGET_SIZES[target]
    else:
        ps_id = answers.get("pageSize")
        if ps_id:
            preset = PAGE_SIZE_PRESETS.get(ps_id)
            if preset:
                overrides["paper/pagesize"] = preset["value"]

    # Write each override into the model
    snapshot = {}
    for configKey, configValue in overrides.items():
        if configValue is None:
            continue
        if configKey not in ModelMap:
            continue
        mi = ModelMap[configKey]
        if mi.widget is None:
            continue
        widget = mi.widget
        # Snapshot current value for potential rollback
        try:
            snapshot[widget] = model.get(widget)
        except Exception:
            pass
        # Convert to widget-appropriate Python type
        val = _toWidgetValue(widget, configValue)
        model.set(widget, val, skipmissing=True)

    return snapshot


def _toWidgetValue(widget, configValue):
    if widget.startswith("c_"):
        if isinstance(configValue, bool):
            return configValue
        if isinstance(configValue, str):
            return configValue.lower() not in ("false", "0", "", "none")
        return bool(configValue)
    if widget.startswith("s_"):
        try:
            return float(configValue)
        except (TypeError, ValueError):
            return 0.0
    return configValue
