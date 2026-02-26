import os
import re
import argparse
from ptxprint.pdfrw import PdfReader, PdfWriter, PageMerge, PdfDict, PdfName

def normalize_path(p: str) -> str:
    # Allow Windows-style paths; normalize to forward slashes.
    # Example: C:\MyProject\LAD\local -> C:/MyProject/LAD/local
    p = p.strip().strip('"').strip("'")
    p = p.replace("\\", "/")
    p = re.sub(r"(?<!:)/{2,}", "/", p)  # collapse duplicate slashes (keep C:/)
    return p

def build_range_suffix(start_page, end_page, num_pages) -> str:
    """
    start_page/end_page are 1-based (or None).
    Suffix rules:
      - no range: ""
      - start+end: "-{start}-{end}"
      - start only: "-{start}ff"
    """
    if start_page is None:
        return ""
    if end_page is None:
        return f"-{start_page}ff"
    return f"-{start_page}-{min(end_page, num_pages)}"

def make_blank_page_like(first_page):
    """
    Create a blank page with same MediaBox/Rotate as first_page.
    Keeps it minimal; PageMerge will manage Resources/XObjects as needed.
    """
    blank = PdfDict(
        Type=PdfName.Page,
        MediaBox=first_page.MediaBox,
        Resources=PdfDict(),
        Contents=[]
    )
    # Preserve rotation if present (helps when PDFs are rotated)
    if getattr(first_page, "Rotate", None) is not None:
        blank.Rotate = first_page.Rotate
    return blank

def overlay_pages_onto_blank(blank_page, pages_to_overlay):
    """
    Overlay each page in pages_to_overlay onto blank_page (stacked).
    """
    base = blank_page
    for p in pages_to_overlay:
        # Add as an XObject over the base
        PageMerge(base).add(p).render()
    return base

def blend_pdf(pdf_path: str, start_page: int | None = None, end_page: int | None = None, mirrored: bool = False):
    """
    Blend (overlay) selected pages of a PDF into a single page.
    - pdf_path: input PDF (Windows or forward-slash path accepted)
    - start_page: optional 1-based start page
    - end_page: optional 1-based inclusive end page
    - mirrored: if True, output odd/even blends separately

    Output:
      - normal:  <src>-blend{range}.pdf
      - mirrored: <src>-blend-odd{range}.pdf and <src>-blend-even{range}.pdf
    """
    pdf_path = normalize_path(pdf_path)

    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    print("PDF:", pdf_path)

    pdf = PdfReader(pdf_path)
    pages = list(pdf.pages)
    num_pages = len(pages)
    if num_pages == 0:
        raise ValueError("PDF has no pages.")

    # Convert 1-based inclusive range -> 0-based slice [start_idx, end_idx_excl)
    if start_page is None:
        start_idx = 0
    else:
        if start_page < 1:
            raise ValueError("start_page must be >= 1")
        start_idx = start_page - 1

    if end_page is None:
        end_idx_excl = num_pages
    else:
        if end_page < 1:
            raise ValueError("end_page must be >= 1")
        end_idx_excl = min(end_page, num_pages)  # inclusive -> exclusive index is end_page (clamped)

    if start_idx >= end_idx_excl:
        raise ValueError(
            f"Invalid page range: start={start_idx+1}, end={end_idx_excl} "
            f"(PDF has {num_pages} pages)."
        )

    # Selected pages in order
    selected = pages[start_idx:end_idx_excl]

    # Output naming
    src_dir = normalize_path(os.path.dirname(pdf_path))
    src_base = os.path.splitext(os.path.basename(pdf_path))[0]
    range_suffix = build_range_suffix(start_page, end_page, num_pages)

    def write_one(output_file, pages_to_overlay):
        blank = make_blank_page_like(pages[0])
        blended_page = overlay_pages_onto_blank(blank, pages_to_overlay)
        PdfWriter(output_file).addpage(blended_page).write()
        print("Wrote:", output_file)

    if not mirrored:
        out = f"{src_dir}/{src_base}-blend{range_suffix}.pdf"
        write_one(out, selected)
        return

    # Mirrored: odd/even based on original document page numbers (1-based)
    # selected pages correspond to indices start_idx..end_idx_excl-1
    odd_pages = []
    even_pages = []
    for offset, p in enumerate(selected):
        page_number = (start_idx + offset) + 1  # 1-based
        if page_number % 2 == 1:
            odd_pages.append(p)
        else:
            even_pages.append(p)

    if odd_pages:
        out_odd = f"{src_dir}/{src_base}-blend-odd{range_suffix}.pdf"
        write_one(out_odd, odd_pages)
    else:
        print("No odd pages in the selected range; no -blend-odd PDF written.")

    if even_pages:
        out_even = f"{src_dir}/{src_base}-blend-even{range_suffix}.pdf"
        write_one(out_even, even_pages)
    else:
        print("No even pages in the selected range; no -blend-even PDF written.")


def main():
    parser = argparse.ArgumentParser(description="Blend (overlay) PDF pages into a single page (pdfrw).")
    parser.add_argument("pdf_path", help="PDF path (Windows or forward-slash style).")
    parser.add_argument("start_page", nargs="?", type=int, default=None,
                        help="Optional start page (1-based).")
    parser.add_argument("end_page", nargs="?", type=int, default=None,
                        help="Optional end page (1-based, inclusive).")
    parser.add_argument("-m", "--mirrored", action="store_true",
                        help="Blend odd/even pages separately into two PDFs.")
    args = parser.parse_args()

    blend_pdf(args.pdf_path, args.start_page, args.end_page, args.mirrored)


if __name__ == "__main__":
    main()
