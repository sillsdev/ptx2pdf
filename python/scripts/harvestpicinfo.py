#!/usr/bin/python3

import sys, os, re, regex, gi
import xml.etree.ElementTree as et
from collections import Counter

_bookslist = """GEN|50 EXO|40 LEV|27 NUM|36 DEU|34 JOS|24 JDG|21 RUT|4 1SA|31 2SA|24 1KI|22 2KI|25 1CH|29 2CH|36 EZR|10 NEH|13
        EST|10 JOB|42 PSA|150 PRO|31 ECC|12 SNG|8 ISA|66 JER|52 LAM|5 EZK|48 DAN|12 HOS|14 JOL|3 AMO|9 OBA|1 JON|4 MIC|7 NAM|3
        HAB|3 ZEP|3 HAG|2 ZEC|14 MAL|4 ZZZ|0
        MAT|28 MRK|16 LUK|24 JHN|21 ACT|28 ROM|16 1CO|16 2CO|13 GAL|6 EPH|6 PHP|4 COL|4
        1TH|5 2TH|3 1TI|6 2TI|4 TIT|3 PHM|1 HEB|13 JAS|5 1PE|5 2PE|3 1JN|5 2JN|1 3JN|1 JUD|1 REV|22
        TOB|14 JDT|16 ESG|10 WIS|19 SIR|51 BAR|6 LJE|1 S3Y|1 SUS|1 BEL|1 1MA|16 2MA|15 3MA|7 4MA|18 1ES|9 2ES|16 MAN|1 PS2|1
        ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 XXA|999 XXB|999 XXC|999 XXD|999 XXE|999 XXF|999 XXG|999 FRT|999 BAK|999 OTH|999 ZZZ|0 ZZZ|0 
        ZZZ|0 ZZZ|0 INT|999 CNC|999 GLO|999 TDX|999 NDX|999 DAG|14 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 ZZZ|0 LAO|1"""
        
bookcodes = dict((b.split("|")[0], "{:02d}".format(i+1)) for i, b in enumerate(_bookslist.split()[:99]) if b != "ZZZ|0")

OTnNTbooks = ("GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH", "EZR", "NEH", "EST",
            "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN", "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM",
            "HAB", "ZEP", "HAG", "ZEC", "MAL", 
            "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH", "1TI", "2TI", "TIT",
            "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV")
            
ptsettings = None
ref2img = {}
img2ref = {}
COUNT = 0
allprojects = []
settings_dir = "C:\My Paratext 9 Projects"

def incPicCnt():
    global COUNT
    COUNT = COUNT+1
    
def getAllBooks(prjid):
    ''' Returns a dict of all books in the project bkid: bookfile_path '''
    if prjid is None:
        return {}
    prjdir = os.path.join(settings_dir, prjid)
    res = {}
    for bk in OTnNTbooks:
        f = getBookFilename(bk, prjid)
        fp = os.path.join(prjdir, f)
        if os.path.exists(fp):
            res[bk] = fp
    return res

def _getPtSettings(prjid=None):
    if prjid is not None:
        ptsettings = parsePTstngs(prjid)
        return ptsettings

def getBookFilename(bk, prjid=None):
    if bk is None or any(x in "./\\" for x in bk):
        return None
    ptsettings = _getPtSettings(prjid)
    if ptsettings is None:
        return None
    fbkfm = ptsettings['FileNameBookNameForm']
    bknamefmt = (ptsettings['FileNamePrePart'] or "") + \
                fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                (ptsettings['FileNamePostPart'] or "")
    fname = bknamefmt.format(bkid=bk, bkcode=bookcodes.get(bk, 0))
    return fname
    
def newBase(fpath):
    doti = fpath.rfind(".")
    f = os.path.basename(fpath[:doti])
    cl = re.findall(r"(?i)_?((?=ab|cn|co|hk|lb|bk|ba|dy|gt|dh|mh|mn|wa|dn|ib)..\d{5})[abcABC]?$", f)
    if cl:
        return cl[0].lower()
    else:
        return re.sub('[()&+,.;: \-]', '_', f.lower())

def read_sfm(bk, fname):
    with universalopen(fname) as inf:
        dat = inf.read()
        blocks = ["0"] + re.split(r"\\c\s+(\d+)", dat)
        for c, t in zip(blocks[0::2], blocks[1::2]):
            for v in re.findall(r"(?s)(?<=\\v )(\d+[abc]?(?:[,-]\d+?[abc]?)?) ((?:.(?!\\v ))+)", t):
                lastv = v[0]
                s = v[1]
                r = "{}{}".format(bk, c)   #  or   "{} {}.{}".format(bk, c, lastv)
                key = None
                m = regex.findall(r"(?ms)\\fig (.*?)\|(.+?\.....?)\|(....?)\|([^\\]+?)?\|([^\\]+?)?"
                               r"\|([^\\]+?)?\|([^\\]+?)?\\fig\*", s)
                if len(m):
                    for f in m:     # usfm 2
                        incPicCnt()
                        nbf = newBase(f[1])
                        # print(r, nbf, f[1])
                        try:
                            ref2img[r] += [nbf]
                        except KeyError:
                            ref2img[r] = [nbf]
                        try:
                            img2ref[nbf] += [r]
                        except KeyError:
                            img2ref[nbf] = [r]
                else:
                    m = regex.findall(r'(?ms)\\fig ([^\\]*?)\|([^\\]+)*src=[\'"]([^\\]+?)[\'"]([^\\]+)\\fig\*', s)
                    if len(m):
                        for f in m:     # usfm 3
                            incPicCnt()
                            nbf = newBase(f[2])
                            # print(r, nbf, f[2])
                            try:
                                ref2img[r] += [nbf]
                            except KeyError:
                                ref2img[r] = [nbf]
                            try:
                                img2ref[nbf] += [r]
                            except KeyError:
                                img2ref[nbf] = [r]

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
            return None
    fh.seek(0)
    return fh

def parsePTstngs(prjid):
    ptstngs = {}
    path = os.path.join(settings_dir, prjid, "Settings.xml")
    if os.path.exists(path):
        doc = et.parse(path)
        for c in doc.getroot():
            ptstngs[c.tag] = c.text
    else:
        inferValues()
    return ptstngs

def get(key, default=None):
    res = ptstngs.get(key, default)
    if res is None:
        return default
    return res

def inferValues():
    print("--infering setting values")
    path = os.path.join(settings_dir, prjid)
    sfmfiles = [x for x in os.listdir(path) if x.lower().endswith("sfm")]
    for f in sfmfiles:
        m = re.search(r"(\d{2})", f)
        if not m:
            continue
        bk = allbooks[int(m.group(1))-1]
        bki = f.lower().find(bk.lower())
        if bki < 0:
            continue
        numi = m.start(1)
        s = min(bki, numi)
        e = max(bki+3, numi+2)
        (pre, main, post) = f[:s], f[s:e], f[e:]
        ptstngs['FileNamePrePart'] = pre
        ptstngs['FileNamePostPart'] = post
        main = main[:numi-s] + "41" + main[numi-s+2:]
        main = main[:bki-s] + "MAT" + main[bki-s+3:]
        ptstngs['FileNameBookNameForm'] = main
        break

    ptstngs['DefaultFont'] = ""
    ptstngs['Encoding'] = 65001
    
    fbkfm = ptstngs['FileNameBookNameForm']
    bknamefmt = get('FileNamePrePart', "") + \
                fbkfm.replace("MAT","{bkid}").replace("41","{bkcode}") + \
                get('FileNamePostPart', "")
    bookspresent = [0] * len(allbooks)
    for k, v in books.items():
        if os.path.exists(os.path.join(path, bknamefmt.format(bkid=k, bkcode=v))):
            bookspresent[v-1] = 1
    ptstngs['BooksPresent'] = "".join(str(x) for x in bookspresent)

for d in os.listdir(settings_dir):
    p = os.path.join(settings_dir, d)
    if not os.path.isdir(p):
        continue
    try:
        if os.path.exists(os.path.join(p, 'Settings.xml')) \
                or any(x.lower().endswith("sfm") for x in os.listdir(p)):
            # if d in ["WSG", "WSGdev", "aArp", "VASV", "VNT", "U01", "SGAH", "RWB"]:
            if d is not None and d not in ["KEY-L", "KEY-F"]:
                COUNT = 0
                allprojects.append(d)
                try:
                    pts = _getPtSettings(d)
                except:
                    continue
                if pts is not None:
                    bks = getAllBooks(d)
                    for bk in bks.keys():
                        if bk in OTnNTbooks:
                            read_sfm(bk, bks[bk])
                if COUNT != 0:
                    print("{}  {} pics".format(d, COUNT))
                else:
                    print(d)
    except OSError:
        pass

print('-'*40)
for ref in sorted(ref2img.keys()):
    i = ref2img[ref]
    d = {x:i.count(x) for x in i}
    print(ref, d)

print('-'*40)

for img in sorted(img2ref.keys()):
    i = img2ref[img]
    d = {x:i.count(x) for x in i}
    print(img, d)
