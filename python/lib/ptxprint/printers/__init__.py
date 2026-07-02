import importlib

from ptxprint.printers.currency import allcurrencies      # noqa: F401 (re-export)

printerlist = {
    'pretore':       ('Pretore',      'l_pr_pretore'),
    'print_gallery': ('PrintGallery', 'l_pr_print_gallery'),
    'pothi':         ('Pothi',        'l_pr_pothi'),
}

def init_printers(view):
    res = {}
    for k, v in printerlist.items():
        module = importlib.import_module("ptxprint.printers."+k)
        c = getattr(module, v[0])
        res[k] = c(view)
    return res

def printer_from_label(lid):
    for k, v in printerlist.items():
        if v[1] == lid:
            return k
    return None

def comparePrinterPrices(view):
    """Show the multi-printer price comparison graph.

    Collects per-copy price curves from every participating printer: local
    pricing models are computed directly; printers with a live API (Pretore)
    are queried only when usable (account + job fields present). All prices
    are converted into one display currency, so the graph works with any
    combination of printers.
    """
    from ptxprint.printers.currency import getExchangeRates, quoteQuantities, allcurrencies
    from ptxprint.printers.pricing_graph import PricingGraphViewer

    printers = getattr(view, 'printers', {})
    rates = getExchangeRates()
    rates.startFetch()
    try:
        copies = int(float(view.get("s_prnl_copies") or 0))
    except (TypeError, ValueError):
        copies = 0
    quantities = quoteQuantities(copies)
    pretore = printers.get("pretore")
    displayCurrency = pretore.currency if pretore is not None else "EUR"

    localData = {}      # displayName: (perCopyDict, homeCurrency)
    for printer in printers.values():
        if not hasattr(printer, 'getEstimate'):
            continue
        compareWidget = getattr(printer, 'compareWidget', None)
        if compareWidget and not view.get(compareWidget):
            continue
        data = printer.getEstimate(quantities)
        if data:
            localData[printer.displayName] = (data, printer.homeCurrency)

    def convertSeries(data, home):
        if home == displayCurrency:
            return data
        out = {}
        for q, p in data.items():
            c = rates.convert(p, home, displayCurrency)
            if c is None:
                return None
            out[q] = c
        return out

    def showGraph(pretoreData):
        allData = {}
        if pretoreData:
            converted = convertSeries(pretoreData, pretore.homeCurrency)
            if converted is not None:
                allData[pretore.displayName] = converted
        for name, (data, home) in localData.items():
            converted = convertSeries(data, home)
            if converted is None:
                print(f"No exchange rate for {home}; {name} excluded from comparison")
            else:
                allData[name] = converted
        if not len(allData):
            print("No printer pricing available to compare")
            return
        viewer = PricingGraphViewer(allData, parentWindow=view.mainapp.win,
                currencySymbol=allcurrencies.get(displayCurrency, displayCurrency))
        viewer.show()

    if pretore is not None:
        pretore.getEstimateAsync(quantities, showGraph)
    else:
        showGraph(None)
