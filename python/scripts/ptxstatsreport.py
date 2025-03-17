import sys
from math import log10
from simpleapp import *
current_module = sys.modules[__name__]

# data from metrics.paratext.org
# run from commandline with something like this:
python python/scripts/ptxstatsreport.py -f projectAge -f cfgCount -f first_last_used -f intlin -f hasOT -f org -f font

# --------------------------- snip ------------------------------

from datetime import datetime, timedelta
from collections import defaultdict

def convert_to_month(timestamp):
    """Convert UNIX timestamp to 'YYYY-MM' format."""
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m")

def filter_n_months(data):
    """Filter data to keep only the last 60 months."""
    current_date = datetime.utcnow()
    cutoff_date = current_date - timedelta(days=5 * 365)  # 5 years
    return {month: count for month, count in data.items() if datetime.strptime(month, "%Y-%m") >= cutoff_date}

def first_last_used_analyze(results, stat):
    """Analyze firstUsed and lastUsed, aggregating counts by month."""
    first_used = stat.get("ptxPrint", {}).get("firstUsed")
    last_used = stat.get("ptxPrint", {}).get("lastUsed")

    if first_used:
        month = convert_to_month(first_used)
        results.setdefault("firstUsed", defaultdict(int))[month] += 1

    if last_used:
        month = convert_to_month(last_used)
        results.setdefault("lastUsed", defaultdict(int))[month] += 1

def first_last_used_results(results):
    """Generate histogram of firstUsed and lastUsed per month."""
    res = ["First Used Histogram"]
    first_used_data = filter_n_months(results.get("firstUsed", {}))
    res.append(histogram_from_dict(first_used_data, indent=4, width=50))

    res.append("\nLast Used Histogram")
    last_used_data = filter_n_months(results.get("lastUsed", {}))
    res.append(histogram_from_dict(last_used_data, indent=4, width=50))

    return "\n".join(res)

def histogram_from_dict(data, indent=0, width=50):
    """Generate a histogram from a dictionary where keys are months and values are counts."""
    if not data:
        return " " * indent + "No data available."

    max_count = max(data.values()) if data else 1
    res = []
    for month, count in sorted(data.items()):
        bar = "*" * int((count / max_count) * width)
        res.append(" " * indent + f"{month}: {count} {bar}")
    return "\n".join(res)
# --------------------------- snip ------------------------------

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
    results.setdefault("numConfigs", []).append(stat.get("ptxPrint", {}).get("numberOfConfigurations"))
    
def cfgCount_results(results):
    res = ["numConfigs"]
    res.append(histogram(results["numConfigs"], indent=4, zoom=(0.02, 0.3), bins=18, width=50))
    return "\n".join(res)
    
def usage_analyze(results, stat):
    results.setdefault("usage", []).append(stat.get("ptxPrint", {}).get("usage"))
    
def usage_results(results):
    res = ["usage"]
    res.append(histogram(results["usage"], indent=4, zoom=(0.01, 0.12), bins=15, width=50))
    return "\n".join(res)
    
def projectAge_analyze(results, stat):
    """Extracts project ages based on duration and stores them for histogram plotting."""
    duration = stat.get("duration")
    if duration is not None:
        # Convert duration from milliseconds to years
        age_in_years = duration / (60 * 60 * 24 * 365)  # Convert seconds → years
        results.setdefault("projectAges", []).append(age_in_years)

def projectAge_results(results):
    """Generates a histogram of project ages."""
    res = ["Project Age Distribution (Years)"]
    res.append(histogram(results["projectAges"], indent=4, zoom=(0, 1), bins=16, width=50))
    return "\n".join(res)
    
    
def hasOT_analyze(results, stat):
    resf = results.setdefault("hasOT", 0)
    results["hasOT"] = resf + stat["hasOT"]   
    
def hasOT_results(results):
    return (f"Projects with OT: {results['hasOT']}")
    
def font_analyze(results, stat):
    fonts = stat.get("fonts", stat.get("ptxPrint", {}).get("fonts", []))
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
    res.append(f"Number of Organisations: {len(results['ownerName'])}")
    for k, v in sorted(results["ownerName"].items(), key=lambda x: (-x[1], x[0])): # [:20]:
        res.append(f"    {k}: {v}")
        count += v
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
    cfgs = set(stat["ptxPrint"]["configurations"])
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
    parser.add_argument("-f","--find",help="What to report on",action="append",default=["usage"])

    args = parser.parse_args(argv)

    afns = [getattr(current_module, f+"_analyze", duck) for f in args.find]
    rfns = [getattr(current_module, f+"_results", duck) for f in args.find]

    Pipeline(args, jsoninfile, f_(process, afns, rfns), textoutfile)

if __name__ == "__main__":
    main()

