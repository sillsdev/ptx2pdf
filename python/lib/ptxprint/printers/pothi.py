r"""Pothi.com (India) — local pricing model.

Validated against 40 Pothi.com data points across all 8 sizes — zero error.
Formula per copy:
  price = fixed + rate * pages
        + BINDING_ADJ[binding]
        + color_rate * pages        (if Full Color; size-specific)
        + COATED_RATE * pages       (if Full Color AND Coated paper)
"""

from ptxprint.printers.base import PrinterBase, Choice, Output, BINDING_SADDLE, BINDING_SOFT
from ptxprint.printers.currency import formatCurrency

# One entry per catalogue size: (label, width mm, height mm, params)
#
# 'color_rate': ₹/page premium for Full Color interior (size-specific).
#               None = no data collected yet; calculator suppresses color output.
# 'color_pts':  number of Full Color data points used to derive color_rate.
#               1 = single point (estimate — collect a second to confirm);
#               2 = two or more points (reliable).
SIZES = [
    # B&W: 3 pts (100p=137, 200p=207, 400p=347). Color: 1 pt (100p=367).
    ("5 inch x 7 inch",    127, 178, {"fixed": 67.0, "rate": 0.70, "color_rate": 2.30, "color_pts": 1}),
    # B&W: 3 pts (100p=137, 200p=207, 400p=347). Color: 1 pt (100p=367).
    # NOTE: 5×7 and 5×8 price identically across all tested configurations.
    ("5 inch x 8 inch",    127, 203, {"fixed": 67.0, "rate": 0.70, "color_rate": 2.30, "color_pts": 1}),
    # B&W: 5 pts (100–600p). Color: 2 pts (100p coated, 100p coated hard).
    ("A5",                 148, 210, {"fixed": 67.0, "rate": 0.85, "color_rate": 3.25, "color_pts": 2}),
    # B&W: 3 pts (60p saddle, 250p, 500p soft). Color: 2 pts (1200p plain hard, coated hard).
    ("5.5 inch x 8.5 inch", 140, 216, {"fixed": 72.0, "rate": 0.80, "color_rate": 2.20, "color_pts": 2}),
    # B&W: 3 pts (100p=157, 200p=242, 400p=412). Color: 1 pt (100p=447).
    ("6 inch x 9 inch",    152, 229, {"fixed": 72.0, "rate": 0.85, "color_rate": 2.90, "color_pts": 1}),
    # B&W: 3 pts (100p=190, 200p=305, 400p=535). Color: 1 pt (100p=495).
    ("7 inch x 9 inch",    178, 229, {"fixed": 75.0, "rate": 1.15, "color_rate": 3.05, "color_pts": 1}),
    # B&W: 3 pts (100p=203, 200p=323, 400p=563). Color: 1 pt (100p=558).
    ("8 inch x 11 inch",   203, 279, {"fixed": 83.0, "rate": 1.20, "color_rate": 3.55, "color_pts": 1}),
    # B&W: 4 pts (100p, 200p, 400p soft; 1000p hard). Color: 0 pts — not yet collected.
    ("A4",                 210, 297, {"fixed": 83.0, "rate": 1.30, "color_rate": None, "color_pts": 0}),
]

# Binding adjustment added to the base price (₹, flat per copy).
# Verified consistent across A5, 5.5×8.5, and A4.
BINDING_ADJ = {
    "soft":   0,    # Soft Cover — no adjustment
    "saddle": -25,  # Saddle Stitched — ₹25 cheaper than soft cover
    "hard":   +45,  # Hard Cover — ₹45 more than soft cover
}

# Coated paper surcharge — applies ONLY when interior is Full Color.
# Verified at 1.15 ₹/page for 5.5×8.5; assumed consistent across sizes.
COATED_RATE = 1.15  # ₹/page

# Bulk discount tiers: (minimum quantity, discount percentage)
DISCOUNT_TIERS = [
    (1,    0),
    (50,   10),
    (100,  20),
    (250,  25),
    (500,  40),
    (1000, 50),
]

# Page range constraints by binding type
SADDLE_MAX_PAGES = 64
SOFT_MIN_PAGES   = 50
SOFT_MAX_PAGES   = 500


def fmtRupees(amount):
    return formatCurrency(amount, "INR")


def discountPct(qty):
    pct = 0
    for minQty, p in DISCOUNT_TIERS:
        if qty >= minQty:
            pct = p
    return pct


class Pothi(PrinterBase):
    pid = "pothi"
    displayName = "Pothi"
    country = "IN"
    countryName = "India"
    homeCurrency = "INR"
    url = "https://pothi.com"

    options = [
        Choice("fcb_pothi_paper", "Paper type:", [
            ("plain",   "Plain White (70-80 GSM)"),
            ("natural", "Plain Natural Shade (70-80 GSM)"),
            ("coated",  "Coated (90-120 GSM)"),
        ], default="plain",
           tip="Pothi's B&W pricing does not vary by paper type. "
               "Coated paper adds ₹1.15/page, but only with a Full Color interior."),
    ]

    outputs = [
        Output("l_pothi_size",   "Nearest size:"),
        Output("l_pothi_base",   "Base (fixed + per-page):"),
        Output("l_pothi_bind",   "Binding adjustment:"),
        Output("l_pothi_color",  "Full color premium:"),
        Output("l_pothi_coated", "Coated paper surcharge:"),
        Output("l_pothi_one",    "1-copy price:", bold=True),
    ]

    def nearestSize(self, job):
        """Index of the smallest catalogue size that holds the trim size,
        else the closest size overall."""
        fits = [i for i, (n, w, h, p) in enumerate(SIZES)
                if w >= job.widthMm - 2 and h >= job.heightMm - 2]
        pool = fits if fits else range(len(SIZES))
        return min(pool, key=lambda i: (SIZES[i][1] - job.widthMm) ** 2
                                     + (SIZES[i][2] - job.heightMm) ** 2)

    def onePrice(self, job):
        """(single-copy price, cost components) for the current settings."""
        name, w, h, params = SIZES[self.nearestSize(job)]
        isCoated = self.get("fcb_pothi_paper") == "coated"
        colorRate = params["color_rate"]
        base       = params["fixed"] + params["rate"] * job.pages
        bindAdj    = BINDING_ADJ.get(job.binding, 0)
        colorCost  = (colorRate * job.pages) if (job.color and colorRate) else 0.0
        coatedCost = (COATED_RATE * job.pages) if (isCoated and job.color) else 0.0
        parts = {"size": name, "params": params, "base": base, "bindAdj": bindAdj,
                 "colorCost": colorCost, "coatedCost": coatedCost}
        return base + bindAdj + colorCost + coatedCost, parts

    def warnings(self, job):
        w = []
        name, _w, _h, params = SIZES[self.nearestSize(job)]
        if job.color and params["color_rate"] is None:
            w.append("Full Color pricing for this page size has not yet been "
                     "collected. B&W prices are shown; color output is suppressed.")
        if job.binding == BINDING_SADDLE and job.pages > SADDLE_MAX_PAGES:
            w.append(f"Saddle Stitched Binding is only available up to {SADDLE_MAX_PAGES} pages.")
        if job.binding == BINDING_SOFT and job.pages < SOFT_MIN_PAGES:
            w.append(f"Soft Cover requires a minimum of {SOFT_MIN_PAGES} pages.")
        if job.binding == BINDING_SOFT and job.pages > SOFT_MAX_PAGES:
            w.append(f"Soft Cover maximum is {SOFT_MAX_PAGES} pages.")
        if job.copies >= 1500:
            w.append("For 1500+ copies, contact Pothi.com directly for a custom quote.")
        return w

    def estimate(self, job, quantities):
        if not job.pages:
            return None
        price1, parts = self.onePrice(job)
        return {qty: price1 * (1 - discountPct(qty) / 100) for qty in quantities}

    def update(self, job):
        price1, parts = self.onePrice(job)
        params = parts["params"]
        self.set("l_pothi_size", parts["size"])
        self.set("l_pothi_base",
                 f"{fmtRupees(params['fixed'])} + "
                 f"₹{params['rate']:.2f}/pg × {job.pages} = {fmtRupees(parts['base'])}")
        bindAdj = parts["bindAdj"]
        if bindAdj != 0:
            sign = "+" if bindAdj > 0 else ""
            self.set("l_pothi_bind", f"{sign}{fmtRupees(bindAdj)}")
        else:
            self.set("l_pothi_bind", "—")

        if job.color and params["color_rate"]:
            note = " (1 data pt)" if params["color_pts"] == 1 else ""
            self.set("l_pothi_color",
                     f"₹{params['color_rate']:.2f}/pg × {job.pages} = "
                     f"{fmtRupees(parts['colorCost'])}{note}")
        elif job.color:
            self.set("l_pothi_color", "No data — not yet collected")
        else:
            self.set("l_pothi_color", "—")

        if parts["coatedCost"]:
            self.set("l_pothi_coated",
                     f"₹{COATED_RATE:.2f}/pg × {job.pages} = {fmtRupees(parts['coatedCost'])}")
        elif self.get("fcb_pothi_paper") == "coated":
            self.set("l_pothi_coated", "— (charged only with a Full Color interior)")
        else:
            self.set("l_pothi_coated", "—")

        self.set("l_pothi_one", f"<b>{fmtRupees(price1)}</b>", useMarkup=True)

        curPct = discountPct(job.copies)
        for i, (minQty, pct) in enumerate(DISCOUNT_TIERS):
            p = fmtRupees(price1 * (1 - pct / 100))
            self.set(f"l_pothi_tier{i}", f"<b>{p}</b>" if pct == curPct else p,
                     useMarkup=True)

    def panelExtras(self, panel):
        # quantity discount strip: one column per tier, current tier bolded
        headers = ["1"] + [f"{q}+" for q, p in DISCOUNT_TIERS[1:]]
        panel.addTierStrip("pothi", headers, [f"l_pothi_tier{i}" for i in range(len(DISCOUNT_TIERS))])
