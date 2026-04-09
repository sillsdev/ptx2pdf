from gi.repository import Gtk

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

# Interior cost multipliers per paper type (index matches paperCombo order)
PAPER_MULTIPLIERS = [1.0, 1.1, 1.15, 1.6]


class PrintGallery:
    def __init__(self, view):
        self.view = view
        self._setupDone = False

    def _widget(self, wname):
        return self.view.builder.get_object(wname)

    def setup(self):
        """Initialize default values and set up the calculator."""
        if self._setupDone:
            return
        self._setupDone = True
        try:
            # Populate combo boxes
            sizeCombo = self._widget("sizeCombo")
            sizeCombo.append_text("A5 (2-up A4 sheets on A3)")
            sizeCombo.append_text("Larger than A5 (1-up on A3)")
            sizeCombo.set_active(0)  # A5 as default

            bindingCombo = self._widget("bindingCombo")
            bindingCombo.append_text("Perfect (Glued)")
            bindingCombo.append_text("Case (Hardcover)")
            bindingCombo.append_text("Stapled (Center pinned)")
            bindingCombo.set_active(2)  # Staple as default

            printCombo = self._widget("printCombo")
            printCombo.append_text("Black & White")
            printCombo.append_text("Color")
            printCombo.set_active(0)  # B&W as default

            paperCombo = self._widget("paperCombo")
            paperCombo.append_text("Plain white (70 gsm)")
            paperCombo.append_text("Plain white (80 gsm)")
            paperCombo.append_text("Off white (85 gsm)")
            paperCombo.append_text("Glossy (120 gsm)")
            paperCombo.set_active(0)

            lamCombo = self._widget("lamCombo")
            lamCombo.append_text("No")
            lamCombo.append_text("Yes")
            lamCombo.set_active(0)  # No lamination as default

            # Set spin button default values
            pagesSpin = self._widget("pagesSpin")
            pagesSpin.set_value(128)

            copiesSpin = self._widget("copiesSpin")
            copiesSpin.set_value(10)

            # Connect signals
            pagesSpin.connect("value-changed", self.onInputChanged)
            copiesSpin.connect("value-changed", self.onInputChanged)
            sizeCombo.connect("changed", self.onInputChanged)
            bindingCombo.connect("changed", self.onInputChanged)
            printCombo.connect("changed", self.onInputChanged)
            paperCombo.connect("changed", self.onInputChanged)
            lamCombo.connect("changed", self.onInputChanged)
            
            # Initial calculation
            self.onInputChanged()
            print("✓ Print Gallery setup complete")
            
        except Exception as e:
            print(f"ERROR in Print Gallery setup: {e}")
            import traceback
            traceback.print_exc()

    def prepare(self):
        """Called when the Print Gallery tab is selected."""
        print("*** Print Gallery prepare() called ***")
        self.setup()

    def onInputChanged(self, widget=None):
        """Handle changes to any input widget and update all output labels."""
        try:
            # Get input values directly from widgets (these IDs have no prefix convention)
            rawPages = int(self._widget("pagesSpin").get_value())
            rawCopies = int(self._widget("copiesSpin").get_value())
            sizeComboIdx = self._widget("sizeCombo").get_active()
            printComboIdx = self._widget("printCombo").get_active()
            paperComboIdx = self._widget("paperCombo").get_active()
            lamComboIdx = self._widget("lamCombo").get_active()

            # Manage staple availability: staple not suitable for > 100 pages
            bindingCombo = self._widget("bindingCombo")
            stapleCurrentlyAvailable = len(bindingCombo.get_model()) == 3
            if rawPages > 100 and stapleCurrentlyAvailable:
                if bindingCombo.get_active() == 2:  # Staple selected — switch to Perfect
                    bindingCombo.set_active(0)
                bindingCombo.remove(2)
            elif rawPages <= 100 and not stapleCurrentlyAvailable:
                bindingCombo.append_text("Staple")
            bindingComboIdx = bindingCombo.get_active()

            # Determine size (A5 = 0, Larger = 1)
            isA5 = (sizeComboIdx == 0)

            # Normalize pages to multiple of 4
            pages = ((rawPages + 3) // 4) * 4
            pageWarnText = ""
            if pages != rawPages:
                pageWarnText = f"Round up: {pages}"
            self._widget("pageWarnLabel").set_text(pageWarnText)

            # Normalize copies for A5 (pair them up if odd)
            copies = rawCopies
            copyWarnText = ""
            if isA5 and (rawCopies % 2) != 0:
                copies = rawCopies + 1
                copyWarnText = f"Round up: {copies}"
            self._widget("copyWarnLabel").set_text(copyWarnText)

            # Calculate interior sheets per copy
            interiorSheetsPerCopy = pages / 4

            # Calculate costs
            bindingRates = [RATES["perfect"], RATES["case"], RATES["staple"]]
            # If staple was removed, index 2 no longer exists — guard against it
            bindingCost = bindingRates[min(bindingComboIdx, len(bindingRates) - 1)]
            printCost = [RATES["bw"], RATES["color"]][printComboIdx] * PAPER_MULTIPLIERS[paperComboIdx]
            lamCost = RATES["lam"] if lamComboIdx == 1 else 0

            # Cover cost calculation
            if isA5:
                coverCost = (copies / 2) * RATES["cover300"]
            else:
                coverCost = copies * RATES["cover300"]

            # Interior cost calculation
            if isA5:
                interiorSheets = (copies / 2) * interiorSheetsPerCopy
            else:
                interiorSheets = copies * interiorSheetsPerCopy

            interiorCost = interiorSheets * printCost

            # Lamination cost: flat ₹10 per book cover
            lamTotalCost = copies * lamCost

            # Binding cost (per copy)
            bindingTotalCost = copies * bindingCost

            # Total cost
            totalCost = coverCost + interiorCost + lamTotalCost + bindingTotalCost
            perCopyCost = totalCost / copies if copies > 0 else 0

            fmt = self.formatIndianCurrency
            self._widget("coverBreakAmt").set_text(fmt(coverCost))
            self._widget("interiorBreakAmt").set_text(fmt(interiorCost))
            self._widget("lamBreakAmt").set_text(fmt(lamTotalCost))
            self._widget("bindBreakAmt").set_text(fmt(bindingTotalCost))
            self._widget("totalBreakAmt").set_markup(f"<b>{fmt(totalCost)}</b>")
            self._widget("perCopyBreakAmt").set_text(fmt(perCopyCost))

        except Exception as e:
            print(f"Error in onInputChanged: {e}")

    def formatIndianCurrency(self, amount):
        """Format amount as Indian currency (₹X,XX,XXX.xx)."""
        # Round to 2 decimal places
        amount = round(amount, 2)
        
        # Split into integer and decimal parts
        intPart = int(amount)
        decPart = int(round((amount - intPart) * 100))
        
        # Format integer part with Indian locale commas
        if intPart < 100000:
            # Standard comma grouping (1,00,000+)
            intStr = "{:,}".format(intPart).replace(",", "X")  # Temp replace
            # Convert to Indian style: every 2 digits from right (after first 3)
            intStr = str(intPart)
            if intPart >= 100000:
                # 1,23,456 format
                intStr = intStr[:-5] + "," + intStr[-5:-3] + "," + intStr[-3:]
            elif intPart >= 1000:
                # 12,345 format
                intStr = intStr[:-3] + "," + intStr[-3:]
        else:
            intStr = str(intPart)
            # Full Indian formatting
            parts = []
            while intStr:
                if len(parts) == 0:
                    parts.append(intStr[-3:])
                    intStr = intStr[:-3]
                else:
                    parts.append(intStr[-2:])
                    intStr = intStr[:-2]
            intStr = ",".join(reversed(parts))
        
        # Format decimal part
        decStr = f"{decPart:02d}"
        
        return f"₹{intStr}.{decStr}"
