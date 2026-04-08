"""
Pricing comparison graph viewer for multi-printer quote analysis.
Uses cairo for rendering and numpy for curve interpolation.
"""

import cairo
import math
from gi.repository import Gtk, Gdk, GdkPixbuf
import numpy as np

# Define fixed colors for each printer (consistent across sessions)
printerColors = {
    "Pretore": (0.2, 0.4, 0.8),      # Blue
    "Snowfall": (0.8, 0.2, 0.2),     # Red
    "Pothi": (0.2, 0.8, 0.2),        # Green
    "Printer4": (0.8, 0.8, 0.2),     # Yellow
    "Printer5": (0.8, 0.4, 0.2),     # Orange
}

defaultColors = [
    (0.2, 0.4, 0.8),    # Blue
    (0.8, 0.2, 0.2),    # Red
    (0.2, 0.8, 0.2),    # Green
    (0.8, 0.8, 0.2),    # Yellow
    (0.8, 0.4, 0.2),    # Orange
]


class PricingGraphViewer:
    """
    GTK dialog for displaying pricing comparison curves.
    
    Data format: {
        "Pretore": {50: 12.50, 100: 9.90, 250: 7.40, 500: 6.10, 1000: 5.20},
        "Snowfall": {50: 13.20, 100: 9.20, 250: 7.00, 500: 5.40, 1000: 4.60},
        "Pothi": {50: 8.80, 100: 7.40, 250: 7.10, 500: 6.50, 1000: 6.00}
    }
    """
    
    def __init__(self, dataDict, parentWindow=None, currencySymbol="€"):
        """
        Initialize the pricing graph viewer.
        
        Args:
            dataDict: Nested dict {printer_name: {quantity: price_per_copy}}
            parentWindow: Parent GTK window for dialog
            currencySymbol: Currency symbol to use in labels/tooltips
        """
        self.dataDict = dataDict
        self.parentWindow = parentWindow
        self.currencySymbol = currencySymbol
        
        # Graph dimensions
        self.width = 1000
        self.height = 700
        self.margin = 80  # Used for left, bottom, and right
        self.topMargin = 45  # Top margin - smaller than sides but not too aggressive
        
        # Data bounds (will be calculated)
        self.minQty = None
        self.maxQty = None
        self.minPrice = None
        self.maxPrice = None
        
        # Current hover point
        self.hoverPoint = None
        self.tooltipText = None
        
        # Graph display options
        self.useCurves = False  # Set to True to use polynomial curves instead of lines
        self.priceMode = "perCopy"  # "perCopy" or "total"
        
        # Printer visibility tracking
        self.printerVisibility = {}
        for printerName in dataDict.keys():
            self.printerVisibility[printerName] = True  # All visible by default
        
        # Max budget filter
        self.maxBudget = None  # None means no filter
        
        # Calculate data bounds
        self._calculateBounds()
        
        # Create dialog
        self.dialog = None
        self.drawingArea = None
        self.surface = None
        self.curvesCheckButton = None
        self.priceModeTotalRadio = None
        self.priorModePerCopyRadio = None
        self.budgetSpinner = None
        self.printerToggleButtons = {}
        
    def _calculateBounds(self):
        """Calculate min/max values for both axes from all data."""
        allQuantities = []
        allPrices = []
        
        for printerName, quantitiesPrices in self.dataDict.items():
            if not self.printerVisibility.get(printerName, True):
                continue  # Skip hidden printers
            
            for qty, pricePerCopy in quantitiesPrices.items():
                # Check budget filter
                if self.maxBudget is not None and (qty * pricePerCopy) > self.maxBudget:
                    continue  # Skip points exceeding budget
                
                allQuantities.append(qty)
                
                if self.priceMode == "total":
                    allPrices.append(qty * pricePerCopy)
                else:
                    allPrices.append(pricePerCopy)
        
        if allQuantities:
            maxQty = max(allQuantities)
            # Always start from 0, go a bit beyond max data
            self.minQty = 0
            self.maxQty = maxQty * 1.05  # 5% padding above max
        else:
            self.minQty = 0
            self.maxQty = 100
        
        if allPrices:
            maxPrice = max(allPrices)
            # Always start from 0, go a bit beyond max data
            self.minPrice = 0
            self.maxPrice = maxPrice * 1.1  # 10% padding above max
        else:
            self.minPrice = 0
            self.maxPrice = 10
    
    def _getPrinterColor(self, printerName, index):
        """Get fixed color for a printer."""
        if printerName in printerColors:
            return printerColors[printerName]
        return defaultColors[index % len(defaultColors)]
    
    def _onPriceModeChanged(self, radioButton):
        """Handle price mode toggle between per-copy and total."""
        if radioButton.get_active():
            if radioButton == self.priceModeTotalRadio:
                self.priceMode = "total"
            else:
                self.priceMode = "perCopy"
            self._calculateBounds()
            self.drawingArea.queue_draw()
    
    def _onBudgetChanged(self, spinButton):
        """Handle max budget spinner change."""
        self.maxBudget = spinButton.get_value()
        if self.maxBudget <= 0:
            self.maxBudget = None
        self._calculateBounds()
        self.drawingArea.queue_draw()
    
    def _onPrinterToggled(self, button, printerName):
        """Handle printer visibility toggle."""
        self.printerVisibility[printerName] = button.get_active()
        self._calculateBounds()
        self.drawingArea.queue_draw()
    
    def _onNoBudgetToggled(self, toggleButton):
        """Handle no-budget toggle."""
        if toggleButton.get_active():
            self.maxBudget = None
            self.budgetSpinner.set_sensitive(False)
        else:
            self.maxBudget = self.budgetSpinner.get_value()
            self.budgetSpinner.set_sensitive(True)
        self._calculateBounds()
        self.drawingArea.queue_draw()
    
    def _dataToCanvas(self, quantity, price):
        """Convert data coordinates to canvas coordinates."""
        plotWidth = self.width - 2 * self.margin
        plotHeight = (self.height - self.margin) - self.topMargin
        
        # Handle edge cases where range is zero
        qtyRange = self.maxQty - self.minQty
        if qtyRange == 0:
            x = self.margin + plotWidth / 2  # Center position
        else:
            x = self.margin + (quantity - self.minQty) / qtyRange * plotWidth
        
        priceRange = self.maxPrice - self.minPrice
        if priceRange == 0:
            y = (self.height - self.margin) - plotHeight / 2  # Center position
        else:
            y = (self.height - self.margin) - (price - self.minPrice) / priceRange * plotHeight
        
        return (x, y)
    
    def _canvasToData(self, x, y):
        """Convert canvas coordinates to data coordinates."""
        plotWidth = self.width - 2 * self.margin
        plotHeight = (self.height - self.margin) - self.topMargin
        
        quantity = self.minQty + (x - self.margin) / plotWidth * (self.maxQty - self.minQty)
        price = self.minPrice + ((self.height - self.margin) - y) / plotHeight * (self.maxPrice - self.minPrice)
        
        return (quantity, price)
    
    def _drawBackground(self, ctx):
        """Draw white background."""
        ctx.set_source_rgb(1, 1, 1)
        ctx.paint()
    
    def _calculateTickInterval(self, rangeVal):
        """Calculate nice tick interval for a range - aims for 5-7 gridlines."""
        if rangeVal <= 0:
            return 1
        
        # Target 6 gridlines across the range
        targetInterval = rangeVal / 6.0
        
        # Get magnitude (10^n)
        magnitude = 10 ** math.floor(math.log10(targetInterval))
        normalized = targetInterval / magnitude
        
        # Pick the nearest nice multiple: 1, 2, 5
        # These produce the cleanest-looking intervals
        if normalized < 1.5:
            niceInterval = magnitude
        elif normalized < 3.5:
            niceInterval = magnitude * 2
        else:
            niceInterval = magnitude * 5
        
        return niceInterval
    
    def _roundDown(self, value, interval):
        """Round value down to nearest interval."""
        if interval <= 0:
            return value
        return math.floor(value / interval) * interval
    
    def _drawCurve(self, ctx, printerName, quantitiesPrices, color):
        """Draw a line through data points (straight lines by default, optional polynomial curve)."""
        # Filter data based on budget and extract
        quantities = []
        prices = []
        
        for qty, pricePerCopy in quantitiesPrices.items():
            # Check budget filter
            if self.maxBudget is not None and (qty * pricePerCopy) > self.maxBudget:
                continue  # Skip points exceeding budget
            
            quantities.append(qty)
            prices.append(self._getYAxisValue(qty, pricePerCopy))
        
        if len(quantities) < 2:
            return
        
        # Sort by quantity
        sortedData = sorted(zip(quantities, prices))
        quantities = np.array([q for q, p in sortedData])
        prices = np.array([p for q, p in sortedData])
        
        ctx.set_source_rgb(*color)
        ctx.set_line_width(1.2)  # Finer lines
        
        if self.useCurves:
            # Create smooth curve using polynomial fitting (degree 2)
            try:
                degree = min(2, max(1, len(quantities) - 1))
                coeffs = np.polyfit(quantities, prices, degree)
                poly = np.poly1d(coeffs)
                
                # Generate smooth curve points
                qtySmooth = np.linspace(quantities[0], quantities[-1], 200)
                pricesSmooth = poly(qtySmooth)
                
                # Clamp prices to stay within visible bounds
                pricesSmooth = np.clip(pricesSmooth, self.minPrice, self.maxPrice)
                
                first = True
                for qty, price in zip(qtySmooth, pricesSmooth):
                    x, y = self._dataToCanvas(qty, price)
                    if first:
                        ctx.move_to(x, y)
                        first = False
                    else:
                        ctx.line_to(x, y)
                ctx.stroke()
            except Exception as e:
                print(f"Error drawing polynomial curve: {e}")
                # Fallback: straight lines
                self._drawStraightLines(ctx, quantities, prices)
        else:
            # Draw straight line segments connecting the points
            self._drawStraightLines(ctx, quantities, prices)
        
        # Draw data points as circles
        ctx.set_source_rgb(*color)
        for qty, price in zip(quantities, prices):
            x, y = self._dataToCanvas(qty, price)
            ctx.arc(x, y, 4, 0, 2 * math.pi)
            ctx.fill()
    
    def _drawStraightLines(self, ctx, quantities, prices):
        """Draw straight line segments connecting data points."""
        for i, (qty, price) in enumerate(zip(quantities, prices)):
            x, y = self._dataToCanvas(qty, price)
            if i == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.stroke()
    
    def _drawLegend(self, ctx):
        """Draw legend showing printer names and colors."""
        if not self.dataDict:
            return
        
        ctx.set_font_size(11)
        legendX = self.width - self.margin - 180
        legendY = self.margin + 20
        
        for index, (printerName, _) in enumerate(self.dataDict.items()):
            color = self._getPrinterColor(printerName, index)
            y = legendY + index * 20
            
            # Color box
            ctx.set_source_rgb(*color)
            ctx.rectangle(legendX, y - 8, 12, 12)
            ctx.fill()
            
            # Printer name
            ctx.set_source_rgb(0, 0, 0)
            ctx.move_to(legendX + 18, y)
            ctx.show_text(printerName)
    
    def _drawCostLabels(self, ctx):
        """Draw labels on data points (price per copy regardless of y-axis mode)."""
        ctx.set_font_size(10)
        
        for printerName, quantitiesPrices in self.dataDict.items():
            if not self.printerVisibility.get(printerName, True):
                continue  # Skip hidden printers
            
            color = self._getPrinterColor(printerName, list(self.dataDict.keys()).index(printerName))
            
            for qty, pricePerCopy in quantitiesPrices.items():
                # Check budget filter
                if self.maxBudget is not None and (qty * pricePerCopy) > self.maxBudget:
                    continue  # Skip points exceeding budget
                
                x, y = self._dataToCanvas(qty, self._getYAxisValue(qty, pricePerCopy))
                
                # Format label parts: price per copy and total cost
                totalCost = qty * pricePerCopy
                perCopyText = f"{self.currencySymbol}{pricePerCopy:.2f}"
                totalCostText = f"{self.currencySymbol}{totalCost:.0f}"
                
                # Draw label above the point with two parts: normal and bold
                ctx.set_source_rgb(*color)
                ctx.set_font_size(10)
                
                # First part: price per copy (normal weight)
                ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                extents1 = ctx.text_extents(perCopyText)
                
                # Second part: total cost (bold)
                spacerText = " "
                extents_space = ctx.text_extents(spacerText)
                
                # Calculate total width
                ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                extents2 = ctx.text_extents(totalCostText)
                
                totalWidth = extents1.width + extents_space.width + extents2.width
                labelX = x - totalWidth / 2
                labelY = y - 8
                
                # Draw price per copy (normal)
                ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                ctx.move_to(labelX, labelY)
                ctx.show_text(perCopyText)
                labelX += extents1.width
                
                # Draw space
                ctx.move_to(labelX, labelY)
                ctx.show_text(spacerText)
                labelX += extents_space.width
                
                # Draw total cost (bold)
                ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                ctx.move_to(labelX, labelY)
                ctx.show_text(totalCostText)
    
    def _getYAxisValue(self, qty, pricePerCopy):
        """Get y-axis value based on current price mode."""
        if self.priceMode == "total":
            return qty * pricePerCopy
        else:
            return pricePerCopy
    
    def _drawGridlines(self, ctx):
        """Draw light gray gridlines at tick intervals, starting from (0, 0)."""
        # Calculate tick intervals using improved logic
        qtyStep = self._calculateTickInterval(self.maxQty)
        priceStep = self._calculateTickInterval(self.maxPrice)
        
        # Set gridline style: medium gray, thin
        ctx.set_source_rgb(0.75, 0.75, 0.75)  # Darker gray
        ctx.set_line_width(0.5)  # Thin lines
        
        # Vertical gridlines at quantity intervals, starting from 0
        qty = 0
        while qty <= self.maxQty:
            if qty > 0:  # Don't draw at zero
                x, _ = self._dataToCanvas(qty, 0)
                ctx.move_to(x, self.topMargin)
                ctx.line_to(x, self.height - self.margin)
                ctx.stroke()
            qty += qtyStep
        
        # Horizontal gridlines at price intervals, starting from 0
        price = 0
        while price <= self.maxPrice:
            if price > 0:  # Don't draw at zero
                _, y = self._dataToCanvas(0, price)
                ctx.move_to(self.margin, y)
                ctx.line_to(self.width - self.margin, y)
                ctx.stroke()
            price += priceStep
    
    def _drawGraph(self, ctx):
        """Draw the complete graph in the correct order."""
        # 1. Background
        self._drawBackground(ctx)
        
        # 2. Gridlines (light gray, behind other elements)
        self._drawGridlines(ctx)
        
        # Calculate tick intervals once (ranges now start from 0)
        qtyStep = self._calculateTickInterval(self.maxQty)
        priceStep = self._calculateTickInterval(self.maxPrice)
        
        # 3. Draw axis lines
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1.5)
        ctx.move_to(self.margin, self.height - self.margin)
        ctx.line_to(self.width - self.margin, self.height - self.margin)
        ctx.move_to(self.margin, self.topMargin)
        ctx.line_to(self.margin, self.height - self.margin)
        ctx.stroke()
        
        # Draw curves
        for index, (printerName, quantitiesPrices) in enumerate(self.dataDict.items()):
            if not self.printerVisibility.get(printerName, True):
                continue  # Skip hidden printers
            color = self._getPrinterColor(printerName, index)
            self._drawCurve(ctx, printerName, quantitiesPrices, color)
        
        # Draw cost labels
        self._drawCostLabels(ctx)
        
        # Draw axis labels and tick marks
        ctx.set_source_rgb(0, 0, 0)  # Black text
        ctx.set_font_size(11)  # Larger font for readability
        
        # X-axis labels and ticks, starting from 0
        qty = 0
        while qty <= self.maxQty:
            if qty > 0:
                x, _ = self._dataToCanvas(qty, 0)
                # Tick mark
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(1)
                ctx.move_to(x, self.height - self.margin)
                ctx.line_to(x, self.height - self.margin + 6)
                ctx.stroke()
                # Label
                ctx.set_source_rgb(0, 0, 0)
                labelText = str(int(qty))
                extents = ctx.text_extents(labelText)
                labelX = x - extents.width / 2
                labelY = self.height - self.margin + 15
                ctx.move_to(labelX, labelY)
                ctx.show_text(labelText)
            qty += qtyStep
        
        # Y-axis labels and ticks, starting from 0
        price = 0
        while price <= self.maxPrice:
            if price > 0:
                _, y = self._dataToCanvas(0, price)
                # Tick mark
                ctx.set_source_rgb(0, 0, 0)
                ctx.set_line_width(1)
                ctx.move_to(self.margin - 6, y)
                ctx.line_to(self.margin, y)
                ctx.stroke()
                # Label
                ctx.set_source_rgb(0, 0, 0)
                labelText = f"{self.currencySymbol}{int(price)}"
                extents = ctx.text_extents(labelText)
                labelX = self.margin - 8 - extents.width
                labelY = y + 4
                ctx.move_to(labelX, labelY)
                ctx.show_text(labelText)
            price += priceStep
        
        # Draw axis titles
        ctx.set_font_size(12)
        
        # X-axis title
        xTitleText = "Number of Copies"
        extents = ctx.text_extents(xTitleText)
        ctx.move_to(self.width / 2 - extents.width / 2, self.height - self.margin + 44)
        ctx.show_text(xTitleText)
        
        # Y-axis title (rotated) - depends on price mode
        ctx.save()
        ctx.translate(30, self.height / 2)
        ctx.rotate(-math.pi / 2)
        yTitleText = "Total Price" if self.priceMode == "total" else "Price per Copy"
        extents = ctx.text_extents(yTitleText)
        ctx.move_to(-extents.width / 2, 0)
        ctx.show_text(yTitleText)
        ctx.restore()
    
    def _findNearestPoint(self, xCanvas, yCanvas, threshold=10):
        """Find the nearest data point to a canvas position."""
        nearest = None
        nearestDist = threshold
        
        for printerName, quantitiesPrices in self.dataDict.items():
            if not self.printerVisibility.get(printerName, True):
                continue  # Skip hidden printers
            
            for qty, pricePerCopy in quantitiesPrices.items():
                # Check budget filter
                if self.maxBudget is not None and (qty * pricePerCopy) > self.maxBudget:
                    continue  # Skip points exceeding budget
                
                yValue = self._getYAxisValue(qty, pricePerCopy)
                x, y = self._dataToCanvas(qty, yValue)
                dist = math.sqrt((x - xCanvas) ** 2 + (y - yCanvas) ** 2)
                if dist < nearestDist:
                    nearest = (printerName, qty, pricePerCopy)
                    nearestDist = dist
        
        return nearest
    
    def _onMotion(self, widget, event):
        """Handle mouse motion for tooltips."""
        x, y = event.x, event.y
        point = self._findNearestPoint(x, y)
        
        if point != self.hoverPoint:
            self.hoverPoint = point
            if point:
                printerName, qty, pricePerCopy = point
                totalCost = qty * pricePerCopy
                if self.priceMode == "total":
                    self.tooltipText = (
                        f"{printerName} | {int(qty)} copies | "
                        f"{self.currencySymbol}{pricePerCopy:.2f}/copy | "
                        f"{self.currencySymbol}{totalCost:.2f} total"
                    )
                else:
                    self.tooltipText = (
                        f"{printerName} | {int(qty)} copies | "
                        f"{self.currencySymbol}{pricePerCopy:.2f}/copy | "
                        f"{self.currencySymbol}{totalCost:.2f} total"
                    )
                # Show tooltip
                widget.set_tooltip_text(self.tooltipText)
            else:
                widget.set_tooltip_text(None)
    
    def _onDraw(self, widget, ctx):
        """Cairo draw callback."""
        self._drawGraph(ctx)
    
    def _onCurvesToggled(self, checkButton):
        """Handle curves checkbox toggle."""
        self.useCurves = checkButton.get_active()
        self.drawingArea.queue_draw()  # Redraw the graph
    
    def show(self):
        """Show the graph in a GTK dialog."""
        self.dialog = Gtk.Dialog(
            title="Multi-Quote Comparison",
            transient_for=self.parentWindow,
            modal=True
        )
        self.dialog.set_default_size(self.width + 40, self.height + 100)
        self.dialog.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        
        content = self.dialog.get_content_area()
        content.set_margin_start(10)
        content.set_margin_end(10)
        content.set_margin_top(10)
        content.set_margin_bottom(10)
        
        # Title label
        title = Gtk.Label()
        title.set_markup("<b>Pricing Comparison Across Printers</b>")
        title.set_halign(Gtk.Align.START)
        content.pack_start(title, False, False, 5)
        
        # COMBINED CONTROLS BOX: Price Mode and Max Budget on same line
        controlsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controlsBox.set_margin_bottom(5)
        
        # Price Mode section
        priceModeLabel = Gtk.Label("Price Mode:")
        priceModeLabel.set_halign(Gtk.Align.START)
        controlsBox.pack_start(priceModeLabel, False, False, 0)
        
        self.priorModePerCopyRadio = Gtk.RadioButton(label="Price per Copy")
        self.priorModePerCopyRadio.set_active(self.priceMode == "perCopy")
        self.priorModePerCopyRadio.connect("toggled", self._onPriceModeChanged)
        controlsBox.pack_start(self.priorModePerCopyRadio, False, False, 0)
        
        self.priceModeTotalRadio = Gtk.RadioButton.new_from_widget(self.priorModePerCopyRadio)
        self.priceModeTotalRadio.set_label("Total Price")
        self.priceModeTotalRadio.set_active(self.priceMode == "total")
        self.priceModeTotalRadio.connect("toggled", self._onPriceModeChanged)
        controlsBox.pack_start(self.priceModeTotalRadio, False, False, 0)
        
        # Add spacer before Max Budget
        spacer = Gtk.Box()
        controlsBox.pack_start(spacer, True, True, 0)  # Expanding spacer
        
        # Max Budget section
        budgetLabel = Gtk.Label("Max Budget:")
        budgetLabel.set_halign(Gtk.Align.START)
        controlsBox.pack_start(budgetLabel, False, False, 0)
        
        # Calculate max possible total from data
        maxPossibleBudget = 0
        for printerName, quantitiesPrices in self.dataDict.items():
            for qty, pricePerCopy in quantitiesPrices.items():
                totalCost = qty * pricePerCopy
                if totalCost > maxPossibleBudget:
                    maxPossibleBudget = totalCost
        
        self.budgetSpinner = Gtk.SpinButton()
        self.budgetSpinner.set_range(0, maxPossibleBudget * 1.5)
        self.budgetSpinner.set_increments(100, 1000)
        self.budgetSpinner.set_value(maxPossibleBudget * 1.1)  # Default to 110% of max
        self.budgetSpinner.set_size_request(100, -1)
        self.budgetSpinner.set_sensitive(True)  # Always enabled
        self.budgetSpinner.connect("value-changed", self._onBudgetChanged)
        controlsBox.pack_start(self.budgetSpinner, False, False, 0)
        
        noBudgetButton = Gtk.CheckButton(label="No limit")
        noBudgetButton.set_active(False)  # Start unchecked - budget filter is ON by default
        noBudgetButton.connect("toggled", self._onNoBudgetToggled)
        controlsBox.pack_start(noBudgetButton, False, False, 0)
        
        # Initialize maxBudget to the spinner value (not None)
        self.maxBudget = self.budgetSpinner.get_value()
        
        content.pack_start(controlsBox, False, False, 0)
        
        # COMBINED PRINTER AND OPTIONS BOX: Printers on left, Curves checkbox on right
        printerOptionsBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        printerOptionsBox.set_margin_bottom(10)
        
        # Printer selection with colored bullets
        printerSelectLabel = Gtk.Label("Show Printers:")
        printerSelectLabel.set_halign(Gtk.Align.START)
        printerOptionsBox.pack_start(printerSelectLabel, False, False, 0)
        
        for index, printerName in enumerate(self.dataDict.keys()):
            color = self._getPrinterColor(printerName, index)
            
            # Create a box for the bullet and label
            bulletBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            
            # Create larger colored bullet using a label with colored background
            bullet = Gtk.Label("●")
            # Convert RGB to hex for CSS
            r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
            cssProvider = Gtk.CssProvider()
            cssProvider.load_from_data(f"label {{ color: #{r:02x}{g:02x}{b:02x}; font-size: 18px; }}".encode())
            bullet.get_style_context().add_provider(cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            bulletBox.pack_start(bullet, False, False, 0)
            
            # Create printer checkbox
            printerButton = Gtk.CheckButton(label=printerName)
            printerButton.set_active(self.printerVisibility.get(printerName, True))
            printerButton.connect("toggled", self._onPrinterToggled, printerName)
            self.printerToggleButtons[printerName] = printerButton
            bulletBox.pack_start(printerButton, False, False, 0)
            
            printerOptionsBox.pack_start(bulletBox, False, False, 0)
        
        # Add spacer before curves checkbox
        spacer2 = Gtk.Box()
        printerOptionsBox.pack_start(spacer2, True, True, 0)  # Expanding spacer
        
        # Curves checkbox on the right
        self.curvesCheckButton = Gtk.CheckButton(label="Show smooth curves")
        self.curvesCheckButton.set_active(self.useCurves)
        self.curvesCheckButton.connect("toggled", self._onCurvesToggled)
        printerOptionsBox.pack_start(self.curvesCheckButton, False, False, 0)
        
        content.pack_start(printerOptionsBox, False, False, 0)
        
        # Drawing area
        self.drawingArea = Gtk.DrawingArea()
        self.drawingArea.set_size_request(self.width, self.height)
        self.drawingArea.connect("draw", self._onDraw)
        self.drawingArea.connect("motion-notify-event", self._onMotion)
        self.drawingArea.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.drawingArea.set_has_tooltip(True)
        
        content.pack_start(self.drawingArea, True, True, 0)
        
        content.show_all()
        self.dialog.run()
        self.dialog.destroy()

