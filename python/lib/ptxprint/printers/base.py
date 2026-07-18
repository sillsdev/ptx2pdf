r"""Common printer abstractions for the Printers tab.

Every print house is a PrinterBase subclass that declares its identity,
its printer-specific options (rendered by panel.py — no Glade editing) and
implements estimate() over a shared JobSpec. Adding a new printer means
adding one module here and listing it in printers/__init__.py.
"""

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Shared binding classes offered in the job specification strip.
# Each printer maps these onto its own catalogue (or warns when unsupported).
BINDING_SOFT   = "soft"
BINDING_HARD   = "hard"
BINDING_SADDLE = "saddle"


@dataclass
class JobSpec:
    """The printer-independent description of the print job."""
    pages: int = 0
    widthMm: float = 148.0
    heightMm: float = 210.0
    copies: int = 0
    color: bool = False         # full-colour interior (else B&W)
    binding: str = BINDING_SOFT
    currency: str = "EUR"       # display currency for the UI

    def key(self):
        """Hashable identity, used to detect stale cached quotes."""
        return (self.pages, round(self.widthMm, 1), round(self.heightMm, 1),
                self.copies, self.color, self.binding)


@dataclass
class Choice:
    """A printer-specific combo option. items is a list of (id, label)."""
    wid: str
    label: str
    items: list
    default: str = None
    tip: str = None


@dataclass
class Spin:
    """A printer-specific numeric option."""
    wid: str
    label: str
    lower: float = 0
    upper: float = 100
    step: float = 1
    default: float = 0
    tip: str = None
    width: int = None           # narrow the widget to this many chars, if set


@dataclass
class Output:
    """A read-only result row (label + value) in the detail panel."""
    wid: str
    label: str
    bold: bool = False


class PrinterBase:
    pid = None                  # stable id: settings keys, graph colours
    displayName = ""
    country = ""                # ISO code shown in the printer list
    countryName = ""
    homeCurrency = "USD"
    url = None
    description = None          # optional note shown at the top of the panel
    supportsOrders = False
    options = []                # Choice/Spin declarations
    outputs = []                # Output declarations (cost breakdown rows)

    def __init__(self, view):
        self.view = view

    def get(self, wname, **kw):
        return self.view.get(wname, **kw)

    def set(self, wname, val, **kw):
        return self.view.set(wname, val, **kw)

    def prepare(self):
        """Called when this printer's panel becomes visible."""
        pass

    def warnings(self, job):
        """List of constraint warnings for this job, in the user's terms."""
        return []

    def billedCopies(self, job):
        """Copies actually invoiced for job.copies (accounts for printer-
        specific rounding, e.g. print runs sold in pairs). Default: none."""
        return max(job.copies, 1)

    def estimate(self, job, quantities):
        """{quantity: perCopy} in homeCurrency, or None when unavailable.

        Local pricing models compute directly; API printers return their
        cached quote when it still matches job.key(), else None (the UI
        then offers estimateAsync via the panel's quote workflow).
        """
        return None

    def estimateAsync(self, job, quantities, callback):
        """Fetch estimates asynchronously; callback({qty: perCopy} or None)
        must run on the GTK main loop. Default: wrap estimate()."""
        callback(self.estimate(job, quantities))

    def update(self, job):
        """Refresh this printer's output rows (cost breakdown, warnings)."""
        pass

    def thicknessText(self, job):
        """Formatted spine/book thickness for this job, or None if this
        printer doesn't model it. Shown in the shared job spec strip
        whenever this printer's panel is the one visible."""
        return None

    def panelExtras(self, panel):
        """Hook for custom panel content (e.g. an ordering workflow).

        panel is the PrinterPanel being built; use panel.addRow()/panel.box
        to extend it.
        """
        pass
