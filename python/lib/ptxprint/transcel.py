
import os
import xml.etree.ElementTree as et
from ptxprint.reference import Reference, RefRange

class NoBook:
    @classmethod
    def getLocalBook(cls, s, level=0):
        return ""

def transcel(triggers, bk, prjdir, lang):
    tfile = os.path.join(prjdir, "pluginData", "Transcelerator", "Transcelerator",
                         "Translated Checking Questions for {}.xml".format(bk))
    if not os.path.exists(tfile):
        return triggers
    tdoc = et.parse(tfile)
    for q in tdoc.findall('.//Question'):
        ref = Reference(bk, int(q.get("startChapter", 0)), int(q.get("startVerse", 0)))
        ev = int(q.get("endVerse", 0))
        if ev != 0:
            ref = RefRange(ref, Reference(ref.book. ref.chap, ev))
        txt = q.findtext('Q/StringAlt[@{{}}:lang="{}"]'.format(lang))
        if txt is not None and len(txt):
            entry = "\\fe - \\fr {} \\ft {}\\fe*".format(ref.str(context=NoBook), txt)
            triggers[ref.first] = triggers.get(ref.first, "") + entry
    return triggers

def outtriggers(triggers, bk, outpath):
    with open(outpath, "w", encoding="utf-8") as outf:
        for k, v in [x for x in sorted(triggers.items()) if x[0].book == bk]:
            outf.write("\\AddTrigger {}{}.{}\n{}\n\\EndTrigger\n".format(k.book, k.chap, k.verse, v))


