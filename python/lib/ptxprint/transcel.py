
import os
import xml.etree.ElementTree as et
from ptxprint.reference import Reference, RefRange, RefSeparators
import logging

logger = logging.getLogger(__name__)

class NoBook:
    @classmethod
    def getLocalBook(cls, s, level=0):
        return ""

def transcel(triggers, bk, prjdir, lang, overview, boldover, numberedQs, showRefs, usfm=None):
    tfile = os.path.join(prjdir, "pluginData", "Transcelerator", "Transcelerator",
                         "Translated Checking Questions for {}.xml".format(bk))
    logger.debug(f"Importing transcelerator data from {tfile}")
    if not os.path.exists(tfile):
        logger.debug(f"Transcelerator file missing: {tfile}")
        return triggers
    if usfm is not None:
        usfm.addorncv()
    tdoc = et.parse(tfile)
    n = 0
    for q in tdoc.findall('.//Question'):
        ovqs = q.get("overview", "") == "true"
        if not overview and ovqs:
            continue
        ref = Reference(bk, int(q.get("startChapter", 0)), int(q.get("startVerse", 0)))
        ev = int(q.get("endVerse", 0))
        # print(f"{ev=}")
        if ev != 0:
            ref = RefRange(ref, Reference(ref.book, ref.chap, ev))
        # print(f"{ref=}")
        if usfm is not None:
            ref = usfm.bridges.get(ref.first, ref.first)
        txt = q.findtext('./Q/StringAlt[@{{http://www.w3.org/XML/1998/namespace}}lang="{}"]'.format(lang))
        
        if txt is not None and len(txt):
            n += 1
            txt = "\\bd " + txt + "\\bd*" if ovqs and boldover else txt
            r = ref.str(context=NoBook) 
            fr = ""
            if numberedQs and showRefs:
                fr = f"\\fr {n}. ({r}) "
            elif numberedQs:
                fr = f"\\fr {n}. " if numberedQs else r
            elif showRefs:
                fr = f"\\fr {r} "
            entry = f"\\ef - {fr}\\ft {txt}\\ef*"
            triggers[ref] = triggers.get(ref, "") + entry
    return triggers

def outtriggers(triggers, bk, outpath):
    dotsep = RefSeparators(cv=".", onechap=True)
    with open(outpath, "w", encoding="utf-8") as outf:
        for k, v in [x for x in sorted(triggers.items()) if x[0].first.book == bk]:
            outf.write("\n\\AddTrigger {}{}\n{}\n\\EndTrigger\n".format(k.first.book, k.str(context=NoBook, addsep=dotsep), v))
