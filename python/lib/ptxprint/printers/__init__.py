import importlib

from ptxprint.printers.currency import allcurrencies      # noqa: F401 (re-export)

# module name: PrinterBase subclass. Adding a printer = one module + one line.
printerlist = {
    'pretore':       'Pretore',
    'print_gallery': 'PrintGallery',
    'pothi':         'Pothi',
    'snowfall':      'Snowfall',
}

def init_printers(view):
    res = {}
    for k, v in printerlist.items():
        module = importlib.import_module("ptxprint.printers."+k)
        c = getattr(module, v)
        res[k] = c(view)
    return res

def comparePrinterPrices(view):
    """Show the multi-printer price comparison graph.

    Collects per-copy price curves from every printer ticked in the printer
    list: local pricing models are computed directly; printers with a live
    API (Pretore) are queried when usable (account + job fields present).
    All prices are converted into the display currency, so the graph works
    with any combination of printers.
    """
    from ptxprint.printers.currency import getExchangeRates, quoteQuantities, allcurrencies
    from ptxprint.printers.pricing_graph import PricingGraphViewer

    tab = getattr(view, 'printerTab', None)
    if tab is None:
        return
    job = tab.jobSpec()
    quantities = quoteQuantities(job.copies)
    rates = getExchangeRates()
    rates.startFetch()

    results = {}        # displayName: (perCopyDict, homeCurrency)
    liveQueue = []      # printers that must be queried asynchronously
    for pid, printer in view.printers.items():
        if not tab.isCompared(pid):
            continue
        data = printer.estimate(job, quantities)
        if data:
            results[printer.displayName] = (data, printer.homeCurrency)
        elif getattr(printer, 'liveQuotes', False):
            liveQueue.append(printer)

    def convertSeries(data, home):
        if home == job.currency:
            return data
        out = {}
        for q, p in data.items():
            c = rates.convert(p, home, job.currency)
            if c is None:
                return None
            out[q] = c
        return out

    def showGraph():
        allData = {}
        for name, (data, home) in results.items():
            converted = convertSeries(data, home)
            if converted is None:
                print(f"No exchange rate for {home}; {name} excluded from comparison")
            else:
                allData[name] = converted
        if not len(allData):
            print("No printer pricing available to compare")
            return
        viewer = PricingGraphViewer(allData, parentWindow=view.mainapp.win,
                currencySymbol=allcurrencies.get(job.currency, job.currency))
        viewer.show()
        tab.updateAll()     # live quotes fetched here may now be cached

    if liveQueue:
        remaining = [len(liveQueue)]
        def makeCallback(printer):
            def _cb(data):
                if data:
                    results[printer.displayName] = (data, printer.homeCurrency)
                remaining[0] -= 1
                if remaining[0] == 0:
                    showGraph()
            return _cb
        for printer in liveQueue:
            printer.estimateAsync(job, quantities, makeCallback(printer))
    else:
        showGraph()
