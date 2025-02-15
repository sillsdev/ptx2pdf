#!/usr/bin/python3

import unittest, re
from ptxprint.usfmutils import Usfm, Sheets
from ptxprint.reference import RefList

testmode = ("usfm", "usx")[0]
if testmode == "usx":
    from ptxprint.usxutils import Usfm as Usx

testdatpath = "projects/WSGBTpub/44JHNWSGBTpub.SFM"

class MockHyphen:
    def hyphenate(self, txt, hyphenchar):
        hphar = "pha-ri-see".replace("-", hyphenchar)
        return txt.replace("pharisee", hphar)
    def get_hyphen_char(self):
        return "-"

class MockStrongs:
    def __init__(self):
        self.regexes = {"G25": r"(lov(ing|ed|e))"}
    def addregexes(self, st):
        pass
    def getstrongs(self, ref):
        if ref.first.chap==3 and ref.first.verse==16:
            return ["G25"]
        else:
            return []

class TestUSFMClass(unittest.TestCase):
    mode = testmode

    def setUp(self):
        if self.mode == "usfm":
            self.sheets = Sheets()
            with open(testdatpath, encoding="utf-8") as inf:
                txtlines = inf.readlines()
            self.usfmdoc = Usfm(txtlines, self.sheets)
        elif self.mode == "usx":
            self.usfmdoc = Usx.readfile(testdatpath)

    def test_readnames(self):
        self.usfmdoc.readnames()
        self.assertTrue(hasattr(self.usfmdoc, 'tocs'))
        self.assertEqual(len(self.usfmdoc.tocs), 3)
        self.assertEqual(self.usfmdoc.tocs[0], "The Good News That John Wrote")
        self.assertEqual(self.usfmdoc.tocs[1], "John")
        self.assertEqual(self.usfmdoc.tocs[2], "John")

    def test_getwords(self):
        words = self.usfmdoc.getwords(constrain=["book"], lowercase=True)
        self.assertEqual(words["book"], 4)

    def test_getmarkers(self):
        markers = self.usfmdoc.getmarkers()
        markers.add("id")
        self.assertEqual(len(markers), 38, " ".join(sorted(markers)))
        self.assertIn("p", markers)

    def test_hyphenate(self):
        mock = MockHyphen()
        self.usfmdoc.hyphenate(mock, False)
        # and test it somehow

    def test_stripintro(self):
        if self.mode == "usx":
            before = len(self.usfmdoc.get_root())
            self.usfmdoc.stripIntro()
            self.assertEqual(len(self.usfmdoc.get_root()), 298, f"{before=} < {len(self.usfmdoc.get_root())}")
        else:
            pass

    def test_subdoc(self, res=None):
        if res is None:
            res = "\u201CDue to God loving the people"
        refrange = RefList.fromStr("JHN 3:16")
        subdoc = self.usfmdoc.subdoc(refrange, addzsetref=False)
        t = str(subdoc[0][0][0])[9:9+len(res)] if self.mode == "usfm" else subdoc[0][0].tail[:len(res)]
        self.assertEqual(t, res)

    def test_transform(self):
        self.usfmdoc.addorncv()
        def testref(e):
            return e.pos is not None and hasattr(e.pos, 'ref') and e.pos.ref.first.chap == 3 and e.pos.ref.first.verse == 16
        self.usfmdoc.transform_text((testref, re.compile("(the people)"), r"all \1"))
        self.test_subdoc(res="\u201CDue to God loving all the people")

    def test_emptycvs(self):
        self.usfmdoc.stripEmptyChVs()

    def test_strongs(self):
        #breakpoint()
        aStrongs = MockStrongs()
        self.usfmdoc.addStrongs(aStrongs, True)
        refrange = RefList.fromStr("JHN 3:16")
        if self.mode == "usfm":
            res = '\u201CDue to God \u200B\\xts|strong="25" align="r"\\*\\nobreak loving'
        else:
            res = "\u201CDue to God \u200b"
        subdoc = self.usfmdoc.subdoc(refrange, addzsetref=False)
        t = str(subdoc[0][0][0])[9:9+len(res)] if self.mode == "usfm" else subdoc[0][0].tail[:len(res)]
        self.assertEqual(t, res)

if __name__ == "__main__":
    unittest.main()
