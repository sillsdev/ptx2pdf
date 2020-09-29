
import re

_units = {'pt': 1, 'in': 72.27, 'mm': 72.27/25.4}

class Dimension:
    def __init__(self, val="0", units=None):
        s = str(val)
        print(s)
        m = re.match(r"^(-?\d+(?:\.\d+)?)\s*(\S*)$", s)
        if m:
            val = float(m.group(1))
            units = m.group(2) or units
        if units is None:
            units = "pt"
        self.val = val * _units.get(units, 1.)

    def asunits(self, units="pt"):
        return self.val / _units.get(units, 1.)

