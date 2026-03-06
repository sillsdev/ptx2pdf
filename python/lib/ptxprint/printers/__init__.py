import importlib

printerlist = {
    'pretore': ('Pretore', 'l_pr_pretore')
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
