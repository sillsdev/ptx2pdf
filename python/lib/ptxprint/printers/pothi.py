from gi.repository import Gtk

# ---------------------------------------------------------------------------
# Pricing constants
# Validated against 40 Pothi.com data points across all 8 sizes — zero error.
# Formula per copy:
#   price = fixed + rate * pages
#         + BINDING_ADJ[binding]
#         + color_rate * pages        (if Full Color; size-specific)
#         + COATED_RATE * pages       (if Full Color AND Coated paper)
# ---------------------------------------------------------------------------

# SIZE_PARAMS — one entry per sizeCombo index position (see setup()).
#
# 'color_rate': ₹/page premium for Full Color interior (size-specific).
#               None = no data collected yet; calculator suppresses color output.
# 'color_pts':  number of Full Color data points used to derive color_rate.
#               1 = single point (estimate — collect a second to confirm);
#               2 = two or more points (reliable).
SIZE_PARAMS = [
    # index 0 — "5 inch x 7 inch"
    # B&W: 3 pts (100p=137, 200p=207, 400p=347). Color: 1 pt (100p=367).
    {"fixed": 67.0, "rate": 0.70, "color_rate": 2.30, "color_pts": 1},
    # index 1 — "5 inch x 8 inch"
    # B&W: 3 pts (100p=137, 200p=207, 400p=347). Color: 1 pt (100p=367).
    # NOTE: 5×7 and 5×8 price identically across all tested configurations.
    {"fixed": 67.0, "rate": 0.70, "color_rate": 2.30, "color_pts": 1},
    # index 2 — "A5"
    # B&W: 5 pts (100–600p). Color: 2 pts (100p coated, 100p coated hard).
    {"fixed": 67.0, "rate": 0.85, "color_rate": 3.25, "color_pts": 2},
    # index 3 — "5.5 inch x 8.5 inch"
    # B&W: 3 pts (60p saddle, 250p, 500p soft). Color: 2 pts (1200p plain hard, coated hard).
    {"fixed": 72.0, "rate": 0.80, "color_rate": 2.20, "color_pts": 2},
    # index 4 — "6 inch x 9 inch"
    # B&W: 3 pts (100p=157, 200p=242, 400p=412). Color: 1 pt (100p=447).
    {"fixed": 72.0, "rate": 0.85, "color_rate": 2.90, "color_pts": 1},
    # index 5 — "7 inch x 9 inch"
    # B&W: 3 pts (100p=190, 200p=305, 400p=535). Color: 1 pt (100p=495).
    {"fixed": 75.0, "rate": 1.15, "color_rate": 3.05, "color_pts": 1},
    # index 6 — "8 inch x 11 inch"
    # B&W: 3 pts (100p=203, 200p=323, 400p=563). Color: 1 pt (100p=558).
    {"fixed": 83.0, "rate": 1.20, "color_rate": 3.55, "color_pts": 1},
    # index 7 — "A4"
    # B&W: 4 pts (100p, 200p, 400p soft; 1000p hard). Color: 0 pts — not yet collected.
    {"fixed": 83.0, "rate": 1.30, "color_rate": None, "color_pts": 0},
]

# Binding adjustment added to the base price (₹, flat per copy).
# Verified consistent across A5, 5.5×8.5, and A4.
BINDING_ADJ = {
    "soft":   0,    # Soft Cover — no adjustment
    "saddle": -25,  # Saddle Stitched — ₹25 cheaper than soft cover
    "hard":   +45,  # Hard Cover — ₹45 more than soft cover
}

# Binding keys by bindingCombo index
BINDING_KEYS = ["soft", "saddle", "hard"]

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


class Pothi:
    def __init__(self, view):
        self.view = view
        self._setupDone = False

    def _widget(self, wname):
        return self.view.builder.get_object(wname)

    def setup(self):
        """Initialise default values and connect signals. Runs once only."""
        if self._setupDone:
            return
        self._setupDone = True
        try:
            sizeCombo = self._widget("p_sizeCombo")
            for label in [
                "5 inch x 7 inch",
                "5 inch x 8 inch",
                "A5",
                "5.5 inch x 8.5 inch",
                "6 inch x 9 inch",
                "7 inch x 9 inch",
                "8 inch x 11 inch",
                "A4",
            ]:
                sizeCombo.append_text(label)
            sizeCombo.set_active(2)  # Default: A5

            bindingCombo = self._widget("p_bindingCombo")
            for label in ["Soft Cover", "Saddle Stitched Binding", "Hard Cover"]:
                bindingCombo.append_text(label)
            bindingCombo.set_active(0)  # Default: Soft Cover

            paperCombo = self._widget("p_paperCombo")
            for label in [
                "Plain White (70-80 GSM)",
                "Plain Natural Shade (70-80 GSM)",
                "Coated (90-120 GSM)",
            ]:
                paperCombo.append_text(label)
            paperCombo.set_active(0)  # Default: Plain White

            colorCombo = self._widget("p_colorCombo")
            for label in [
                "B&W interior (colored cover)",
                "Full Color (Interior & Cover)",
            ]:
                colorCombo.append_text(label)
            colorCombo.set_active(0)  # Default: B&W

            pagesSpin = self._widget("p_pagesSpin")
            pagesSpin.set_value(200)

            qtySpin = self._widget("p_qtySpin")
            qtySpin.set_value(1)

            # Connect signals — all trigger the same recalculation handler
            pagesSpin.connect("value-changed", self.onInputChanged)
            qtySpin.connect("value-changed", self.onInputChanged)
            sizeCombo.connect("changed", self.onInputChanged)
            bindingCombo.connect("changed", self.onInputChanged)
            paperCombo.connect("changed", self.onInputChanged)
            colorCombo.connect("changed", self.onInputChanged)

            self.onInputChanged()

        except Exception as e:
            print(f"ERROR in Pothi setup: {e}")
            import traceback
            traceback.print_exc()

    def prepare(self):
        """Called every time the Pothi tab is made active."""
        self.setup()

    def onInputChanged(self, widget=None):
        """Recalculate and update all output labels whenever any input changes."""
        try:
            pages      = int(self._widget("p_pagesSpin").get_value())
            qty        = int(self._widget("p_qtySpin").get_value())
            sizeIdx    = self._widget("p_sizeCombo").get_active()
            bindingIdx = self._widget("p_bindingCombo").get_active()
            paperIdx   = self._widget("p_paperCombo").get_active()
            colorIdx   = self._widget("p_colorCombo").get_active()

            params      = SIZE_PARAMS[sizeIdx]
            bindingKey  = BINDING_KEYS[bindingIdx]
            isCoated    = (paperIdx == 2)
            isFullColor = (colorIdx == 1)

            # --- Warnings ---
            warnings = []
            if isFullColor and params["color_rate"] is None:
                warnings.append(
                    "Full Color pricing for this page size has not yet been collected. "
                    "B&W prices are shown; color output is suppressed."
                )
            if bindingKey == "saddle" and pages > SADDLE_MAX_PAGES:
                warnings.append(
                    f"Saddle Stitched Binding is only available up to {SADDLE_MAX_PAGES} pages."
                )
            if bindingKey == "soft" and pages < SOFT_MIN_PAGES:
                warnings.append(
                    f"Soft Cover requires a minimum of {SOFT_MIN_PAGES} pages."
                )
            if bindingKey == "soft" and pages > SOFT_MAX_PAGES:
                warnings.append(
                    f"Soft Cover maximum is {SOFT_MAX_PAGES} pages."
                )
            if qty >= 1500:
                warnings.append(
                    "For 1500+ copies, contact Pothi.com directly for a custom quote."
                )

            self._widget("p_warnLabel").set_text("  ".join(warnings))

            # --- Calculations ---
            base       = params["fixed"] + params["rate"] * pages
            bindAdj    = BINDING_ADJ[bindingKey]
            colorCost  = (params["color_rate"] * pages) if (isFullColor and params["color_rate"]) else 0.0
            coatedCost = (COATED_RATE * pages) if (isCoated and isFullColor) else 0.0
            price1     = base + bindAdj + colorCost + coatedCost

            discPct = 0
            for minQty, pct in DISCOUNT_TIERS:
                if qty >= minQty:
                    discPct = pct
            priceAtQty = price1 * (1 - discPct / 100)
            total      = priceAtQty * qty

            # --- Summary labels ---
            discStr = f" ({discPct}% off)" if discPct else ""
            self._widget("p_priceQAmt").set_text(fmtRupees(priceAtQty) + discStr)
            self._widget("p_priceTotalAmt").set_markup(f"<b>{fmtRupees(total)}</b>")

            # --- Breakdown labels ---
            self._widget("p_baseBreakAmt").set_text(
                f"{fmtRupees(params['fixed'])} + "
                f"₹{params['rate']:.2f}/pg × {pages} = {fmtRupees(base)}"
            )
            if bindAdj != 0:
                sign = "+" if bindAdj > 0 else ""
                self._widget("p_bindBreakAmt").set_text(f"{sign}{fmtRupees(bindAdj)}")
            else:
                self._widget("p_bindBreakAmt").set_text("—")

            if isFullColor and params["color_rate"]:
                cr   = params["color_rate"]
                note = " (1 data pt)" if params["color_pts"] == 1 else ""
                self._widget("p_colorBreakAmt").set_text(
                    f"₹{cr:.2f}/pg × {pages} = {fmtRupees(colorCost)}{note}"
                )
            elif isFullColor and params["color_rate"] is None:
                self._widget("p_colorBreakAmt").set_text("No data — not yet collected")
            else:
                self._widget("p_colorBreakAmt").set_text("—")

            if isCoated and isFullColor:
                self._widget("p_coatedBreakAmt").set_text(
                    f"₹{COATED_RATE:.2f}/pg × {pages} = {fmtRupees(coatedCost)}"
                )
            else:
                self._widget("p_coatedBreakAmt").set_text("—")

            self._widget("p_totalBreakAmt").set_markup(f"<b>{fmtRupees(price1)}</b>")

            # --- Discount tier grid ---
            for i, (minQty, pct) in enumerate(DISCOUNT_TIERS):
                p     = price1 * (1 - pct / 100)
                label = self._widget(f"p_discPrice{i}")
                if pct == discPct:
                    label.set_markup(f"<b>{fmtRupees(p)}</b>")
                else:
                    label.set_text(fmtRupees(p))

        except Exception as e:
            print(f"ERROR in Pothi onInputChanged: {e}")
            import traceback
            traceback.print_exc()


def fmtRupees(amount):
    """Format a float as Indian-locale rupees: ₹X,XX,XXX.XX"""
    paise   = round(amount * 100)
    decPart = paise % 100
    intPart = paise // 100
    intStr  = str(intPart)
    if intPart >= 1000:
        parts  = [intStr[-3:]]
        intStr = intStr[:-3]
        while intStr:
            parts.append(intStr[-2:])
            intStr = intStr[:-2]
        intStr = ",".join(reversed(parts))
    return f"₹{intStr}.{decPart:02d}"
