#!/usr/bin/env python3
"""
Extract all tooltips from a GTK .glade file and write them in various formats.

Supported output formats (inferred from -o extension):
    .jsonl  - one JSON object per line (UTF-8)
    .txt    - human-readable text
    .csv    - UTF-8 CSV
    .docx   - simple Word document (OOXML)
    .xlsx   - simple Excel workbook (OOXML)   [also accepts .xslx]

Each record contains:
    - breadcrumbs  (e.g. "Basic > Project > Copyright & Licensing")
    - widget_type  (e.g. "Checkbox", "Button")
    - label        (widget label/title if available)
    - tooltip      (full tooltip text, possibly multi-line)
"""

import argparse
import csv
import json
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape
import zipfile
from datetime import datetime
import os

# ---------- XML helpers ----------

def tag(elem):
    """Return local tag name without XML namespace."""
    return elem.tag.split('}')[-1]


def get_property_text(elem, name):
    """Return the text of the first <property name="name"> under elem (or None)."""
    for child in elem:
        if tag(child) == 'property' and child.get('name') == name:
            if child.text:
                return child.text.strip()
    return None


# ---------- Pass 1: build WIDGETS and PARENTS ----------

def build_ui_maps(root):
    """
    Walk the whole .glade XML and build:

      WIDGETS[id] = <object ...>
      PARENTS[child_id] = parent_id

    Only elements with an 'id' attribute are included in WIDGETS.
    PARENTS maps between those id'ed widgets, skipping anonymous
    boxes/alignments etc.
    """
    widgets = {}
    parents = {}

    def walk(node, current_parent_id):
        # Treat any <object> with an id as a widget
        if tag(node) == 'object':
            obj_id = node.get('id')
            if obj_id:
                widgets[obj_id] = node
                if current_parent_id is not None:
                    parents[obj_id] = current_parent_id
                # From here down, this becomes the parent
                current_parent_id = obj_id

        for child in node:
            walk(child, current_parent_id)

    walk(root, None)
    return widgets, parents


# ---------- Pass 2: map tab page IDs to titles ----------

def get_label_from_label_child(container):
    """
    For GtkFrame/GtkExpander that use a separate label widget:
        <child type="label"><object class="GtkLabel">...</object></child>
    """
    for child in container:
        if tag(child) == 'child' and child.get('type') == 'label':
            for grand in child:
                if tag(grand) == 'object':
                    text = get_property_text(grand, 'label')
                    if text:
                        return text
    return None


def build_page_title_map(widgets):
    """
    Find GtkNotebook and GtkStack widgets and build a map:

        page_id -> "Page Title"
    """
    page_titles = {}

    for wid, obj in widgets.items():
        cls = obj.get('class', '')
        if cls not in ('GtkNotebook', 'GtkStack'):
            continue

        for child in obj:
            if tag(child) != 'child':
                continue

            page_obj = None
            packing = None
            for sub in child:
                t = tag(sub)
                if t == 'object':
                    page_obj = sub
                elif t == 'packing':
                    packing = sub

            if page_obj is None:
                continue

            page_id = page_obj.get('id')
            if not page_id:
                continue

            title = None

            if packing is not None:
                if cls == 'GtkNotebook':
                    tprop = get_property_text(packing, 'tab-label')
                    if tprop:
                        title = tprop

                    if not title:
                        for p in packing:
                            if tag(p) == 'property' and p.get('name') == 'tab':
                                for tab_child in p:
                                    if tag(tab_child) == 'object':
                                        lab = get_property_text(tab_child, 'label')
                                        if lab:
                                            title = lab
                                            break
                            if title:
                                break

                elif cls == 'GtkStack':
                    tprop = get_property_text(packing, 'title')
                    if tprop:
                        title = tprop

            if not title:
                title = (get_property_text(page_obj, 'label') or
                         get_property_text(page_obj, 'title'))

            if title:
                page_titles[page_id] = title.strip()

    return page_titles


# ---------- Labels & tooltips ----------

def get_widget_label(obj):
    """Label for the widget itself."""
    label = (get_property_text(obj, 'label') or
             get_property_text(obj, 'text') or
             get_property_text(obj, 'title'))
    return label or ''


def get_container_label(obj):
    """Label for GtkFrame / GtkExpander containers."""
    cls = obj.get('class', '')

    label = (get_property_text(obj, 'label') or
             get_property_text(obj, 'title'))
    if label:
        return label.strip()

    if cls in ('GtkFrame', 'GtkExpander'):
        label = get_label_from_label_child(obj)
        if label:
            return label.strip()

    return None


def get_widget_tooltip(obj):
    """Prefer tooltip-markup over tooltip-text."""
    tt = get_property_text(obj, 'tooltip-markup')
    if tt:
        return tt.strip()
    tt = get_property_text(obj, 'tooltip-text')
    if tt:
        return tt.strip()
    return None


# ---------- Friendly widget type names ----------

def friendly_widget_type(cls):
    """Map GTK widget class to human-friendly control names."""
    if not cls:
        return ''

    mapping = {
        'GtkButton': 'Button',
        'GtkToggleButton': 'Toggle Button',
        'GtkCheckButton': 'Checkbox',
        'GtkRadioButton': 'Radio Button',
        'GtkSwitch': 'Switch',
        'GtkEntry': 'Text Field',
        'GtkSpinButton': 'Number Field',
        'GtkComboBox': 'Dropdown',
        'GtkComboBoxText': 'Dropdown',
        'GtkNotebook': 'Tab Notebook',
        'GtkStack': 'Stack',
        'GtkLabel': 'Label',
        'GtkWindow': 'Window',
        'GtkDialog': 'Dialog',
        'GtkFrame': 'Section',
        'GtkExpander': 'Expandable Section',
        'GtkTreeView': 'List/Table',
        'GtkTextView': 'Multi-line Text',
        'GtkScrolledWindow': 'Scroll Area',
    }

    if cls in mapping:
        return mapping[cls]

    base = cls[3:] if cls.startswith('Gtk') else cls
    pretty = re.sub(r'(?<!^)([A-Z])', r' \1', base)
    return pretty or cls


# ---------- Breadcrumbs ----------

def _add_segment(segments, text):
    """Append a breadcrumb segment, avoiding adjacent duplicates."""
    if not text:
        return
    text = text.strip()
    if not text:
        return
    if not segments or segments[-1] != text:
        segments.append(text)


def _derive_tab_name_from_id(name):
    """Fallback for tab names from IDs, e.g. tb_PageLayout -> 'Page Layout'."""
    base = name[3:]  # strip 'tb_'
    base = base.replace('_', ' ')
    base = re.sub(r'(?<!^)([A-Z])', r' \1', base)
    return base.strip() if base else None


def build_breadcrumb(widget_id, widgets, parents, page_titles):
    """
    Crawl UP parents and build breadcrumbs:

      - tb_* pages -> title (from map or derived)
      - GtkFrame / GtkExpander -> their labels
      - Root:
          * 'mainapp_win' omitted
          * 'dlg_xxx'  -> 'Xxx dialog'
          * 'menu_main' -> 'Main menu'
    """
    segments = []
    current_id = widget_id

    while True:
        parent_id = parents.get(current_id)
        if parent_id is None:
            break

        parent = widgets.get(parent_id)
        if parent is None:
            break

        name = parent_id
        cls = parent.get('class', '')

        page_title = None
        if name in page_titles:
            page_title = page_titles[name]
        elif name and name.startswith('tb_'):
            page_title = _derive_tab_name_from_id(name)

        if page_title:
            _add_segment(segments, page_title)
        else:
            if cls in ('GtkFrame', 'GtkExpander'):
                label = get_container_label(parent)
                if label:
                    _add_segment(segments, label)

        current_id = parent_id

    root_id = current_id if current_id in widgets else None
    if root_id:
        _add_segment(segments, root_id)

    segments.reverse()

    if segments:
        root = segments[0]
        if root == 'mainapp_win':
            segments = segments[1:]
        elif root.startswith('dlg_'):
            base = root[4:]
            base = base.replace('_', ' ')
            base = re.sub(r'(?<!^)([A-Z])', r' \1', base)
            pretty = base.strip().title() if base else 'Dialog'
            segments[0] = f"{pretty} dialog"
        elif root == 'menu_main':
            segments[0] = "Main menu"

    return ' > '.join(segments)


# ---------- Collect records ----------

def collect_records(glade_path):
    """Parse the glade and return list of dicts with breadcrumbs, widget_type, label, tooltip."""
    with open(glade_path, "r", encoding="utf-8") as f:
        tree = ET.parse(f)
    root = tree.getroot()

    widgets, parents = build_ui_maps(root)
    page_titles = build_page_title_map(widgets)

    records = []
    for wid in sorted(widgets.keys()):
        obj = widgets[wid]
        tooltip = get_widget_tooltip(obj)
        if not tooltip:
            continue

        rec = {
            "breadcrumbs": build_breadcrumb(wid, widgets, parents, page_titles),
            "widget_type": friendly_widget_type(obj.get('class', '')),
            "label": get_widget_label(obj),
            "tooltip": tooltip,
        }
        records.append(rec)

    return records


# ---------- Writers ----------

def write_jsonl(records, path):
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            json.dump(rec, f, ensure_ascii=False)
            f.write("\n")


def write_txt(records, path):
    with open(path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(rec["breadcrumbs"] + "\n")
            header = f"[{rec['widget_type']}]"
            if rec["label"]:
                header += " " + rec["label"]
            f.write(header + "\n")
            f.write(rec["tooltip"] + "\n\n")


def write_csv(records, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["breadcrumbs", "widget_type", "label", "tooltip"])
        for rec in records:
            writer.writerow([
                rec["breadcrumbs"],
                rec["widget_type"],
                rec["label"],
                rec["tooltip"],
            ])


def write_docx(records, path):
    """Create a minimal Word document containing all records."""
    # Build document.xml
    body_parts = []
    for rec in records:
        bc = xml_escape(rec["breadcrumbs"])
        wt = xml_escape(rec["widget_type"])
        label = xml_escape(rec["label"])
        tooltip_lines = rec["tooltip"].splitlines() or [""]

        body_parts.append(
            f'<w:p><w:r><w:t>{bc}</w:t></w:r></w:p>'
        )
        summary = f"[{wt}]"
        if label:
            summary += " " + label
        body_parts.append(
            f'<w:p><w:r><w:t>{xml_escape(summary)}</w:t></w:r></w:p>'
        )

        # Tooltip as one paragraph with line breaks
        tooltip_xml = '<w:p><w:r><w:t xml:space="preserve">'
        first = True
        for line in tooltip_lines:
            if not first:
                tooltip_xml += '</w:t></w:r><w:r><w:br/><w:t xml:space="preserve">'
            tooltip_xml += xml_escape(line)
            first = False
        tooltip_xml += '</w:t></w:r></w:p>'
        body_parts.append(tooltip_xml)

        # Blank line
        body_parts.append('<w:p/>')

    body_xml = "".join(body_parts)
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>
"""

    content_types_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""

    rels_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml)
        z.writestr("_rels/.rels", rels_xml)
        z.writestr("word/document.xml", document_xml)


def col_ref(col_index):
    """Convert 0-based column index to Excel column ref (A, B, ..., Z, AA, AB, ...)."""
    result = ""
    col = col_index
    while True:
        col, rem = divmod(col, 26)
        result = chr(ord('A') + rem) + result
        if col == 0:
            break
        col -= 1
    return result


def write_xlsx(records, path):
    """Create a minimal Excel workbook with one sheet."""
    # Sheet data
    headers = ["breadcrumbs", "widget_type", "label", "tooltip"]

    rows_xml = []

    # Header row
    r = 1
    cells = []
    for c, h in enumerate(headers):
        ref = f"{col_ref(c)}{r}"
        cells.append(
            f'<c r="{ref}" t="inlineStr"><is><t>{xml_escape(h)}</t></is></c>'
        )
    rows_xml.append(f'<row r="{r}">{"".join(cells)}</row>')

    # Data rows
    for rec in records:
        r += 1
        cells = []
        values = [rec[h] for h in headers]
        for c, val in enumerate(values):
            ref = f"{col_ref(c)}{r}"
            text = xml_escape(val)
            cells.append(
                f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{text}</t></is></c>'
            )
        rows_xml.append(f'<row r="{r}">{"".join(cells)}</row>')

    sheet_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    {''.join(rows_xml)}
  </sheetData>
</worksheet>
"""

    content_types_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

    rels_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

    workbook_xml = """<?xml version="1.0" encoding="UTF-8"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Tooltips" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"""

    workbook_rels_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>
"""

    now = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    core_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>PTXprint Tooltips</dc:title>
  <dc:creator>PTXprint Tooltip Export</dc:creator>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
</cp:coreProperties>
"""

    app_xml = """<?xml version="1.0" encoding="UTF-8"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Python</Application>
</Properties>
"""

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml)
        z.writestr("_rels/.rels", rels_xml)
        z.writestr("xl/workbook.xml", workbook_xml)
        z.writestr("xl/worksheets/sheet1.xml", sheet_xml)
        z.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
        z.writestr("docProps/core.xml", core_xml)
        z.writestr("docProps/app.xml", app_xml)


# ---------- Main CLI ----------

def main():
    parser = argparse.ArgumentParser(
        description="Extract PTXprint tooltips from a GTK .glade file."
    )
    parser.add_argument("gladefile", help="Path to the .glade file (e.g. ptxprint.glade)")
    parser.add_argument(
        "-o", "--output",
        help="Output file (extension decides format: .jsonl, .txt, .csv, .docx, .xlsx)"
    )

    args = parser.parse_args()
    glade_path = args.gladefile

    default_output = glade_path + ".tooltips.jsonl"
    out_path = args.output or default_output

    records = collect_records(glade_path)

    ext = os.path.splitext(out_path)[1].lower()
    if ext == ".jsonl" or not ext:
        write_jsonl(records, out_path)
    elif ext == ".txt":
        write_txt(records, out_path)
    elif ext == ".csv":
        write_csv(records, out_path)
    elif ext == ".docx":
        write_docx(records, out_path)
    elif ext in (".xlsx", ".xslx"):
        write_xlsx(records, out_path)
    else:
        raise SystemExit(f"Unsupported output extension '{ext}'. "
                         "Use .jsonl, .txt, .csv, .docx, .xlsx")

    print(f"Wrote {len(records)} tooltip records to: {out_path}")


if __name__ == "__main__":
    main()
