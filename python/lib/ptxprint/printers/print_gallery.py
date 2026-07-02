r"""Print Gallery (Ernakulam, India) — local pricing model.

Rates were derived by querying the print shop directly; interiors are
printed on A3 sheets (4 book pages per sheet), A5 books 2-up in pairs.
"""

from ptxprint.printers.base import PrinterBase, Choice, Output, BINDING_SADDLE
from ptxprint.printers.currency import formatCurrency

RATES = {
    "cover300": 20,      # ₹/A3 sheet (300 GSM wrap cover)
    "cover130": 19,      # ₹/A3 sheet (130 GSM board cover)
    "bw": 10,            # ₹/A3 sheet (B&W interior, plain white 70 gsm base)
    "color": 14,         # ₹/A3 sheet (colour interior, plain white 70 gsm base)
    "lam": 10,           # ₹/copy (thermal lamination per book cover)
    "perfect": 150,      # ₹/copy (perfect binding)
    "case": 250,         # ₹/copy (case binding)
    "staple": 55         # ₹/copy (staple binding)
}

# Interior cost multiplier and label per paper option
PAPERS = [
    ("70",  "Plain white (70 gsm)",  1.0),
    ("80",  "Plain white (80 gsm)",  1.1),
    ("85",  "Off white (85 gsm)",    1.15),
    ("120", "Glossy (120 gsm)",      1.6),
]

# Shared binding class → (rate key, label)
BINDINGS = {
    "soft":   ("perfect", "Perfect (Glued)"),
    "hard":   ("case",    "Case (Hardcover)"),
    "saddle": ("staple",  "Stapled (Center pinned)"),
}

STAPLE_MAX_PAGES = 100

# Largest trim size that can still go 2-up on A3 (A5 plus a little grace)
TWOUP_MAX_W = 150
TWOUP_MAX_H = 212


def fmtRupees(amount):
    return formatCurrency(amount, "INR")


class PrintGallery(PrinterBase):
    pid = "print_gallery"
    displayName = "Print Gallery"
    country = "IN"
    countryName = "India"
    homeCurrency = "INR"
    url = "https://www.printgallery.in/"

    options = [
        Choice("fcb_pg_paper", "Paper type:",
               [(k, lbl) for k, lbl, m in PAPERS], default="70"),
        Choice("fcb_pg_lam", "Lamination:",
               [("no", "No"), ("yes", "Yes")], default="no"),
    ]

    outputs = [
        Output("l_pg_impose",   "Imposition:"),
        Output("l_pg_covers",   "Covers:"),
        Output("l_pg_interior", "Interior:"),
        Output("l_pg_lam",      "Lamination:"),
        Output("l_pg_bind",     "Binding:"),
    ]

    def _bindingKey(self, job):
        key = BINDINGS.get(job.binding, ("perfect",))[0]
        if key == "staple" and self._roundPages(job) > STAPLE_MAX_PAGES:
            key = "perfect"     # staple not suitable for thick books
        return key

    def _isTwoUp(self, job):
        return job.widthMm <= TWOUP_MAX_W and job.heightMm <= TWOUP_MAX_H

    def _roundPages(self, job):
        return ((job.pages + 3) // 4) * 4      # A3 sheets hold 4 pages

    def _paperMultiplier(self):
        pid = self.get("fcb_pg_paper") or "70"
        for k, lbl, m in PAPERS:
            if k == pid:
                return m
        return 1.0

    def costs(self, job, copies):
        """Cost components (total ₹, not per copy) at the given quantity."""
        twoUp = self._isTwoUp(job)
        pages = self._roundPages(job)
        if twoUp and copies % 2:
            copies += 1                         # 2-up books are printed in pairs
        sheetsPerCopy = pages / 4
        sets = copies / 2 if twoUp else copies  # A3 print runs
        printRate = RATES["color" if job.color else "bw"] * self._paperMultiplier()
        lamRate = RATES["lam"] if self.get("fcb_pg_lam") == "yes" else 0
        return {
            "copies":   copies,
            "covers":   sets * RATES["cover300"],
            "interior": sets * sheetsPerCopy * printRate,
            "lam":      copies * lamRate,
            "bind":     copies * RATES[self._bindingKey(job)],
        }

    def warnings(self, job):
        w = []
        pages = self._roundPages(job)
        if pages != job.pages:
            w.append(f"Pages rounded up to {pages} (multiple of 4).")
        if self._isTwoUp(job) and job.copies % 2:
            w.append(f"Copies rounded up to {job.copies + 1} (A5 books are printed in pairs).")
        if job.binding == BINDING_SADDLE and pages > STAPLE_MAX_PAGES:
            w.append(f"Stapled binding is unsuitable beyond {STAPLE_MAX_PAGES} pages; "
                     "Perfect binding is priced instead.")
        return w

    def estimate(self, job, quantities):
        if not job.pages:
            return None
        result = {}
        for qty in quantities:
            if qty <= 0:
                continue
            c = self.costs(job, qty)
            total = c["covers"] + c["interior"] + c["lam"] + c["bind"]
            result[qty] = total / c["copies"]
        return result

    def update(self, job):
        if self._isTwoUp(job):
            self.set("l_pg_impose", "A5, 2-up on A3")
        else:
            self.set("l_pg_impose", "1-up on A3")
        copies = max(job.copies, 1)
        c = self.costs(job, copies)
        self.set("l_pg_covers", fmtRupees(c["covers"]))
        self.set("l_pg_interior", fmtRupees(c["interior"]))
        self.set("l_pg_lam", fmtRupees(c["lam"]))
        self.set("l_pg_bind", fmtRupees(c["bind"]))
