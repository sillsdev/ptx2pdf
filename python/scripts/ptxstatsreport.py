import sys
from math import log10
from simpleapp import *
current_module = sys.modules[__name__]

def process(js, args, afns, rfns):
    results = {}
    # breakpoint()
    for s in js:
        for fn in afns:
            fn(results, s)
    
    report = [fn(results) for fn in rfns]
    return "\n\n".join(report)

def duck(*args):
    return ""
    
def cfgCount_analyze(results, stat):
    results.setdefault("numConfigs", []).append(stat["ptxPrint.numberOfConfigurations"])
    
def cfgCount_results(results):
    res = ["numConfigs"]
    res.append(histogram(results["numConfigs"], indent=4, zoom=(0.02, 0.3), bins=18, width=50))
    return "\n".join(res)
    
def usage_analyze(results, stat):
    results.setdefault("usage", []).append(stat["ptxPrint.usage"])
    
def usage_results(results):
    res = ["usage"]
    res.append(histogram(results["usage"], indent=4, zoom=(0.01, 0.12), bins=15, width=50))
    return "\n".join(res)
    
def font_analyze(results, stat):
    fonts = stat.get("fonts", stat.get("ptxPrint.fonts", []))
    resf = results.setdefault("fonts", {})
    for f in fonts:
        if len(f) < 5:
            continue
        resf[f] = resf.get(f, 0) + 1
        
def font_results(results):
    res = ["fonts"]
    for k, v in sorted(results["fonts"].items(), key=lambda x: (-x[1], x[0])): # [:20]:
        res.append(f"    {k}: {v}")
    return "\n".join(res)
    
def org_analyze(results, stat):
    if "ownerName" not in results:
        results["ownerName"] = {}
    reso = results["ownerName"]
    orgs = stat["ownerName"]
    reso[orgs] = reso.get(orgs, 0) + 1
        
def org_results(results):
    res = ["ownerName"]
    count = 0 
    for k, v in sorted(results["ownerName"].items(), key=lambda x: (-x[1], x[0])): # [:20]:
        res.append(f"    {k}: {v}")
        count += v
    res.append(f"Number of Organisations: {len(results['ownerName'])}")
    res.append(f"Projects Total: {count}")
    return "\n".join(res)
        
def intlin_analyze(results, stat):
    resf = results.setdefault("interlinear", 0)
    inum = stat["interlinear"]["number"]
    if inum > 0:
        results["interlinear"] = resf + 1
        
def intlin_results(results):
    return (f"Projects with interlinear: {results['interlinear']}")
        
def confName_analyze(results, stat):
    if "configurations" not in results:
        results["configurations"] = {}
    reso = results["configurations"]
    cfgs = set(stat["configurations"])
    for c in cfgs:
        reso[c] = reso.get(c, 0) + 1
        
def confName_results(results):
    res = ["configurations"]
    count = 0
    for k, v in sorted(results["configurations"].items(), key=lambda x: (-x[1], x[0])): # [:20]:
        res.append(f"    {k}: {v}")
        count += v
    res.append(f"Configurations Total: {count}")
    return "\n".join(res)
    
def histogram(data, indent=0, zoom=(0,1), bins=10, width=40):
    res = []
    mean = sum(data) / len(data)
    data = sorted(data)
    median = data[len(data)//2]
    maxval = max(data)
    res.append(" "*indent + "Total: {}".format(sum(data)))
    res.append(" "*indent + "Number: {}".format(len(data)))
    res.append(" "*indent + "Mean: {:.2f}".format(mean))
    res.append(" "*indent + "Median: {:.2f}".format(median))
    res.append(" "*indent + "Maximum: {}".format(maxval))
    hist = [0] * bins
    mult = bins / (zoom[1] - zoom[0]) / maxval
    lx = mx = 0
    for d in data:
        x = (d * mult) - bins * zoom[0] / (zoom[1] - zoom[0])
        if x < 0:
            lx += 1
        elif x >= bins:
            mx += 1
        else:
            hist[int(x)] += 1
    if lx > 0:
        res.append(" "*indent + "Below {}%: {}".format(int(zoom[0] * 100), lx))
    maxhist = max(hist)
    vwidth = int(log10(maxhist)) + 1
    lwr = zoom[0]
    iwidth = int(log10(zoom[1] * maxval)) + 1
    for i in range(bins):
        m = ((i + 1) / bins * (zoom[1] - zoom[0])) + zoom[0]
        res.append(" "*indent + f"{{:2}}% ({{:-{iwidth}}}-{{:{iwidth}}}) {{:-{vwidth}}}: ".format(int(m * 100), 
                   int(lwr * maxval), int(maxval * m - 1), hist[i]) + "*"*int(hist[i]/maxhist * width))
        lwr = m
    if mx > 0:
        res.append(" "*indent + "Above {}%: {}".format(int(zoom[1] * 100), mx))
    return "\n".join(res)
    
def main(argv=None):
    parser = ArgumentParser(prog="something")
    parser.add_argument("infile",help="Input file",default="stats/ptxPrintStats.txt")
    parser.add_argument("-o","--outfile",help="Output file",default="stats/report.txt")
    parser.add_argument("-f","--find",help="What to report on",action="append")
    
    args = parser.parse_args(argv)

    afns = [getattr(current_module, f+"_analyze", duck) for f in args.find]
    rfns = [getattr(current_module, f+"_results", duck) for f in args.find]

    Pipeline(args, jsoninfile, f_(process, afns, rfns), textoutfile)

if __name__ == "__main__":
    main()

