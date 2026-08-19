r"""Shared currency services for all printers: exchange rates, price
formatting and the standard quotation quantity ladder.

Exchange rates are fetched once per session from frankfurter.dev (EUR base)
and shared by every printer, so a local INR calculator and a live EUR quote
can both be displayed in the user's chosen currency.
"""

import json, threading, urllib.request, logging

logger = logging.getLogger(__name__)

allcurrencies = {
    "AFN":  "؋",
    "AMD":  "֏",
    "AOA":  "Kz",
    "ARS":  "$",
    "AUD":  "A$",
    "AZN":  "₼",
    "BAM":  "KM",
    "BBD":  "$",
    "BDT":  "৳",
    "BMD":  "$",
    "BND":  "$",
    "BOB":  "Bs",
    "BRL":  "R$",
    "BSD":  "$",
    "BWP":  "P",
    "BZD":  "$",
    "CAD":  "CA$",
    "CLP":  "$",
    "CNY":  "CN¥",
    "COP":  "$",
    "CRC":  "₡",
    "CUC":  "$",
    "CUP":  "$",
    "CZK":  "Kč",
    "DKK":  "kr",
    "DOP":  "$",
    "EGP":  "E£",
    "ESP":  "₧",
    "EUR":  "€",
    "FJD":  "$",
    "FKP":  "£",
    "GBP":  "£",
    "GEL":  "₾",
    "GHS":  "GH₵",
    "GIP":  "£",
    "GNF":  "FG",
    "GTQ":  "Q",
    "GYD":  "$",
    "HKD":  "HK$",
    "HNL":  "L",
    "HRK":  "kn",
    "HUF":  "Ft",
    "IDR":  "Rp",
    "ILS":  "₪",
    "INR":  "₹",
    "ISK":  "kr",
    "JMD":  "$",
    "JPY":  "JP¥",
    "KGS":  "⃀",
    "KHR":  "៛",
    "KMF":  "CF",
    "KPW":  "₩",
    "KRW":  "₩",
    "KYD":  "$",
    "KZT":  "₸",
    "LAK":  "₭",
    "LBP":  "L£",
    "LKR":  "Rs",
    "LRD":  "$",
    "LTL":  "Lt",
    "LVL":  "Ls",
    "MGA":  "Ar",
    "MMK":  "K",
    "MNT":  "₮",
    "MUR":  "Rs",
    "MXN":  "MX$",
    "MYR":  "RM",
    "NAD":  "$",
    "NGN":  "₦",
    "NIO":  "C$",
    "NOK":  "kr",
    "NPR":  "Rs",
    "NZD":  "NZ$",
    "PHP":  "₱",
    "PKR":  "Rs",
    "PLN":  "zł",
    "PYG":  "₲",
    "RON":  "lei",
    "RUB":  "₽",
    "RWF":  "RF",
    "SAR":  "⃁",
    "SBD":  "$",
    "SEK":  "kr",
    "SGD":  "$",
    "SHP":  "£",
    "SRD":  "$",
    "SSP":  "£",
    "STN":  "Db",
    "SYP":  "£",
    "THB":  "฿",
    "TOP":  "T$",
    "TRY":  "₺",
    "TTD":  "$",
    "TWD":  "NT$",
    "UAH":  "₴",
    "USD":  "US$",
    "UYU":  "$",
    "VEF":  "Bs",
    "VND":  "₫",
    "XAF":  "FCFA",
    "XCD":  "EC$",
    "XCG":  "Cg.",
    "XOF":  "F CFA",
    "XPF":  "CFPF",
    "XXX":  "¤",
    "ZAR":  "R",
    "ZMW":  "ZK",
}

# Currencies conventionally grouped in the Indian 2,2,3 digit pattern
_indianGrouping = ("INR", "NPR", "PKR", "LKR", "BDT")

# Standard quantity ladder used for multi-point quotations and graphs
standardQuantities = [50, 100, 250, 500, 1000]


def quoteQuantities(copies=None):
    """The standard quantity ladder, with the user's own quantity merged in."""
    quantities = set(standardQuantities)
    if copies:
        quantities.add(int(copies))
    return sorted(quantities)


def formatCurrency(amount, code):
    """Format an amount with its currency symbol and locale digit grouping."""
    symbol = allcurrencies.get(code, code)
    minor = round(amount * 100)
    if minor < 0:
        sign, minor = "-", -minor
    else:
        sign = ""
    intStr = str(minor // 100)
    if code in _indianGrouping:
        if len(intStr) > 3:
            parts = [intStr[-3:]]
            intStr = intStr[:-3]
            while intStr:
                parts.append(intStr[-2:])
                intStr = intStr[:-2]
            intStr = ",".join(reversed(parts))
    else:
        intStr = "{:,}".format(int(intStr))
    return "{}{}{}.{:02d}".format(sign, symbol, intStr, minor % 100)


class ExchangeRates:
    """Session-wide exchange rate table, EUR based, fetched in a worker thread.

    GTK-free by design: callers needing UI updates should wrap their callback
    with GLib.idle_add themselves.
    """

    _url = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=" + \
           ",".join(sorted(allcurrencies.keys()))

    def __init__(self):
        self.rates = {}
        self.thread = None
        self._lock = threading.Lock()
        self._callbacks = []

    @property
    def ready(self):
        return len(self.rates) > 0

    def startFetch(self, onDone=None, force=False):
        """Fetch rates in a daemon thread. onDone(rates) runs on that thread."""
        with self._lock:
            if onDone is not None:
                self._callbacks.append(onDone)
            if self.ready and not force:
                pass
            elif self.thread is None or not self.thread.is_alive():
                self.thread = threading.Thread(target=self._fetch, args=(force,))
                self.thread.daemon = True
                self.thread.start()
                return
            elif not self.ready:
                return          # a fetch is already under way
        self._notify()

    def wait(self, timeout=10):
        """Block until rates are available or the timeout expires."""
        t = self.thread
        if t is not None and t.is_alive():
            t.join(timeout)
        return self.ready

    def _fetch(self, force=False):
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 11.0; Win64; x64)"}
        try:
            req = urllib.request.Request(self._url, headers=headers)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    rates = data.get('rates', {})
                    rates["EUR"] = 1.0
                    self.rates = rates
                else:
                    logger.warning(f"Exchange rate response code: {response.getcode()}")
        except Exception as e:
            logger.warning(f"Exchange rate fetch failed: {e}")
        self._notify()

    def _notify(self):
        with self._lock:
            callbacks, self._callbacks = self._callbacks, []
        for cb in callbacks:
            try:
                cb(self.rates)
            except Exception as e:
                logger.warning(f"Exchange rate callback failed: {e}")

    def rate(self, code):
        """Units of code per EUR, or None if unknown/not yet fetched."""
        return self.rates.get(code, None)

    def convert(self, amount, fromCode, toCode):
        """Convert between currencies; returns None if a rate is missing."""
        if fromCode == toCode:
            return amount
        fromRate = self.rates.get(fromCode, None)
        toRate = self.rates.get(toCode, None)
        if fromRate is None or toRate is None or fromRate == 0:
            return None
        return amount / fromRate * toRate


_exchangeRates = None

def getExchangeRates():
    """The session-wide ExchangeRates singleton."""
    global _exchangeRates
    if _exchangeRates is None:
        _exchangeRates = ExchangeRates()
    return _exchangeRates
