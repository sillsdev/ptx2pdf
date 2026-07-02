r"""Snowfall Press (USA) — placeholder until a pricing model is built."""

from ptxprint.printers.base import PrinterBase


class Snowfall(PrinterBase):
    pid = "snowfall"
    displayName = "Snowfall Press"
    country = "US"
    countryName = "United States"
    homeCurrency = "USD"
    url = "https://www.snowfallpress.com/"
    description = ("No pricing model has been built for this printer yet, "
                   "so it is excluded from price comparisons. "
                   "Use the website link above to get a quotation directly.")
