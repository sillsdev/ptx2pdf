
import os
import xml.etree.ElementTree as et
from ptxprint.reference import Reference, RefRange, RefSeparators
import logging

logger = logging.getLogger(__name__)

class NoBook:
    @classmethod
    def getLocalBook(cls, s, level=0):
        return ""

def transcel(triggers, bk, prjdir, lang, usfm=None):
    tfile = os.path.join(prjdir, "pluginData", "Transcelerator", "Transcelerator",
                         "Translated Checking Questions for {}.xml".format(bk))
    logger.debug(f"Importing transcelerator data from {tfile}")
    if not os.path.exists(tfile):
        return triggers
    if usfm is not None:
        usfm.addorncv()
    tdoc = et.parse(tfile)
    for q in tdoc.findall('.//Question'):
        ref = Reference(bk, int(q.get("startChapter", 0)), int(q.get("startVerse", 0)))
        ev = int(q.get("endVerse", 0))
        if ev != 0:
            ref = RefRange(ref, Reference(ref.book, ref.chap, ev))
        if usfm is not None:
            ref = usfm.bridges.get(ref.first, ref.first)
        txt = q.findtext('./Q/StringAlt[@{{http://www.w3.org/XML/1998/namespace}}lang="{}"]'.format(lang))
        if txt is not None and len(txt):
            entry = "\\ef - \\fr {} \\ft {}\\ef*".format(ref.str(context=NoBook), txt)
            triggers[ref] = triggers.get(ref.first, "") + entry
    return triggers

def outtriggers(triggers, bk, outpath):
    dotsep = RefSeparators(cv=".", onechap=True)
    with open(outpath, "w", encoding="utf-8") as outf:
        for k, v in [x for x in sorted(triggers.items()) if x[0].first.book == bk]:
            outf.write("\n\\AddTrigger {}{}\n{}\n\\EndTrigger\n".format(k.first.book, k.str(context=NoBook, addsep=dotsep), v))


