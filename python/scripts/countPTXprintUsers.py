#!/usr/bin/python3
# Script to extract anonymous PTXprint usage statistics from a folder of Paratext projects
# by Mark Penny, Feb 2023

import sys, os, re
import datetime as dt
import xml.etree.ElementTree as et
import json, argparse

ptsettings = None
ptxpusers = {}
pdftypes = {}
pdfsizes = {}
cfgage = {}
pdfage = {}
lastuse = {}
cfgnames = {}
prjtypes = {}
picnopic = {}
indicScripts = {}
COUNT = 0
counts = {}

def incHashRef(d, *a):
    for i, k in enumerate(a):
        if k not in d:
            d[k] = {} if i < len(a) - 1 else 0
        if i < len(a) - 1:
            d = d[k]
        else:
            d[k] += 1

def universalopen(fname, cp=65001):
    """ Opens a file with the right codec from a small list and perhaps rewrites as utf-8 """
    encoding = "cp{}".format(cp) if str(cp) != "65001" else "utf-8"
    fh = open(fname, "r", encoding=encoding)
    try:
        fh.readline()
        fh.seek(0)
        return fh
    except ValueError:
        pass
    try:
        fh = open(fname, "r", encoding="utf-16")
        fh.readline()
        failed = False
    except UnicodeError:
        failed = True
    if failed:
        try:
            fh = open(fname, 'r', encoding="cp1252")
            fh.readline()
            failed = False
        except UnicodeError:
            print("Failed to open with various encodings!")
            return None
    fh.seek(0)
    return fh

def parsePTstngs(prjdir):
    ptstngs = {}
    path = os.path.join(prjdir, "Settings.xml")
    if os.path.exists(path):
        doc = et.parse(path)
        for c in doc.getroot():
            ptstngs[c.tag] = c.text or ""
    else:
        ptstngs = None
    return ptstngs

def get(key, default=None):
    res = ptstngs.get(key, default)
    if res is None:
        return default
    return res

def writeFile(outfile, **kw):    
    with open(outfile, "w", encoding="utf-8") as outf:
        json.dump(kw, outf, indent=2, separators=(',', ': '))  # sort_keys=True, indent=4)
        
def age(filepath):
    try:
        info = os.lstat(filepath)
    except FileNotFoundError:
        # print(f"FILE NOT FOUND: {str(filepath)}")
        return 9999
    created = dt.datetime.fromtimestamp(info.st_mtime)
    ageInDays = (now-created).days
    # print(f"{filepath} {ageInDays}")
    return ageInDays

def categorizeByAge(filepath, countdict):
    a = age(filepath)
    if a < 8:
        incHashRef(countdict, "1. within the last week")
    elif a < 31:
        incHashRef(countdict, "2. within the last month")
    elif a < 91:
        incHashRef(countdict, "3. within the last quarter")
    elif a < 181:
        incHashRef(countdict, "4. within the half a year")
    elif a < 366:
        incHashRef(countdict, "5. within the last year")
    elif a < 731:
        incHashRef(countdict, "6. within the last 2 years")
    else:
        incHashRef(countdict, "7. more than 2 years ago")

def categorizeBySize(filepath, sizedict):
    sz = int(os.path.getsize(filepath)/1024)
    if sz < 256: #KB
        incHashRef(sizedict, "1. Tiny (< 256 KB)")
    elif sz < 512: #KB
        incHashRef(sizedict, "2. Normal (< 512 KB)")
    elif sz < 2024: #2MB
        incHashRef(sizedict, "3. Large (< 2 MB)")
    elif sz < 10240: #10MB
        incHashRef(sizedict, "4. Very large (< 10 MB)")
    elif sz < 51200: #50MB
        incHashRef(sizedict, "5. Massive (< 50 MB)")
    else:
        incHashRef(sizedict, "6. Probaby a _diff file (> 50 MB)")
    return sz

# -------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indir", default="C:/My Paratext 9 Projects", help="Path to Paratext project tree")
parser.add_argument("-o", "--outfile", default="PTxprintUsageStats.json", help="Output JSON file")
parser.add_argument("-a", "--all", action="store_true", help="Process ALL projects, not just Standard translation type")
parser.add_argument("-p", "--pdfs", action="store_true", help="Also count how many PDFs were produced (only possible if Local)")
parser.add_argument("-v", "--byverse", action="store_true", help="Verse-level granularity instead of by chapter")
# parser.add_argument("-s", "--scripts", action="store_true", help="Also produce count of the 10 Indic scripts")
args = parser.parse_args()
# -------------------------------------------------------------------------------------------
# This is where the main work is done - cycle through all the folders looking for valid projects
now = dt.datetime.today()
print(now)

for d in os.listdir(args.indir):
    # try:
    p = os.path.join(args.indir, d)
    if not os.path.isdir(p):
        continue
    if not os.path.exists(os.path.join(p, 'Settings.xml')) \
            and not any(x.lower().endswith("sfm") for x in os.listdir(p)):
        continue
    if d.lower().startswith("z"):
        incHashRef(prjtypes, "ignored", "Resource, Temp, Training projects")
        continue
    totalCOUNT = 0
    try:
        pts = parsePTstngs(p)
    except NameError:
        continue
    if pts is None:
        # This happens for Resource projects
        incHashRef(prjtypes, "ignored", "Resource, Temp, Training projects")
        continue
    # Read the project description to see if it contains "test" or "train"ing - and if so, ignore it
    pdesc = pts.get("FullName", "").lower()
    if "test" in pdesc or "train" in pdesc:
        incHashRef(prjtypes, "ignored", "Resource, Temp, Training projects")
        continue
    # Read the 'Project type' so that we only look at 'Standard' projects (unless -a = all was passed in)
    ptype = pts.get("TranslationInfo", "").split(":")[0]
    if not args.all and not ptype.startswith("Standard"):
        incHashRef(prjtypes, "ignored", ptype)
        continue
    foundScr = False
    # Search for evidence of PTXprint being used
    shrptxp = os.path.join(p, 'shared','ptxprint')
    if not os.path.exists(shrptxp):
        incHashRef(prjtypes, "Counted (but don't use PTXprint)", ptype)
        incHashRef(ptxpusers, "Never used")
    else:
        totalPDFsize = 0
        # totalPages = 0
        cfgCount = 0
        # Initialize the "latest" file so there is something to compare with
        # latestConfig = args.indir
        latestConfig = os.path.join(args.indir, "eng.vrs")
        incHashRef(ptxpusers, "Using PTXprint")
        for cfg in os.listdir(shrptxp):
            if os.path.isdir(os.path.join(shrptxp, cfg)):
                # print(cfg)
                incHashRef(cfgnames, cfg)
                categorizeByAge(os.path.join(shrptxp, cfg), cfgage)
                # try:
                cfgSettings = os.path.join(shrptxp, cfg, "ptxprint.cfg")
                try:
                    if age(cfgSettings) < age(latestConfig):
                        latestConfig = cfgSettings
                    cfgCount += 1
                except:
                    print("No ptxprint.cfg file found")
        categorizeByAge(latestConfig, lastuse)
        if args.pdfs:                
            locptxp = os.path.join(p, 'local','ptxprint')
            if os.path.exists(locptxp):
                for f in os.listdir(locptxp):
                    fn = os.path.join(locptxp, f)
                    if fn.endswith(".pdf"):
                        # print("Pages: ", pdfpagenumber.extractPdfPageCount(fn))
                        # reader = PdfReader(fn)
                        # totalPages += len(reader.pages)
                        totalPDFsize += categorizeBySize(fn, pdfsizes)
                        categorizeByAge(fn, pdfage)
                        incHashRef(pdftypes, "Total count of PDFs")
                        if fn.endswith("diff.pdf"):
                            incHashRef(pdftypes, "_diff.pdf")
                        elif fn.endswith("_1.pdf"):
                            incHashRef(pdftypes, "_1.pdf")
                        elif fn.endswith("ptxp.pdf"):
                            incHashRef(pdftypes, "ptxp.pdfs")
                        elif "ptxprint-" in fn:
                            incHashRef(pdftypes, "(old)ptxprint-.pdf")
                        else:
                            incHashRef(pdftypes, "unknown pdf")
        if totalPDFsize:
            avgPDFsize = int(totalPDFsize/cfgCount/1024)
            print(f"{d} {cfgCount=} totalPDFsize={int(totalPDFsize/1024/1024)}MB {avgPDFsize=}KB ")
            # avgPageCount = int(totalPages/cfgCount)
            # print(f"{p} {cfgCount=} {totalPages=} {avgPageCount=} ")
        incHashRef(prjtypes, "Counted (using PTXprint)", ptype)
    # except: OSError:
        # pass

# To flip the structure to be ref-based instead of img-based
# for pic, dat in img2ref.items():
    # for k, v in dat.items():
        # ref2img.setdefault(k, {})[pic]=v
        
print("\nWriting JSON file:", args.outfile)
writeFile(args.outfile, NumberOfProjects=ptxpusers, projectypes=prjtypes, PDFtypes=pdftypes, PDFsizes=pdfsizes, PDFages=pdfage, ConfigAge=cfgage, LastUse=lastuse)
print("Done harvesting PTXprint Usage statistics.")
print("\n")
print("\nHow many projects have used PTXprint?")
print(ptxpusers)
print("\nWhen were the Configs created?")
print(cfgage)
print("\nWhen was PTXprint last used by each project?")
print(lastuse)
if args.pdfs:
    print("\n")
    print(pdftypes)
    print("\nWhen were the PDFs created?")
    print(pdfage)
    print("\nWhat size were the created PDFs?")
    print(pdfsizes)
# print("\n")
# print(cfgnames)
print("\n")
print(prjtypes)

# How many are diglots?
# How many are interlinear?
