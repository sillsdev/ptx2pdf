#!/usr/bin/python3

import unittest, re
from ptxprint.usfmutils import Usfm, Sheets
from ptxprint.reference import RefList
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
    mode = "usfm"

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
        self.assertEqual(len(self.usfmdoc.tocs), 4)
        self.assertEqual(self.usfmdoc.tocs[0], "The Good News That John Wrote")
        self.assertEqual(self.usfmdoc.tocs[1], "John")
        self.assertEqual(self.usfmdoc.tocs[2], "John")

    def test_getwords(self):
        words = self.usfmdoc.getwords(constrain=["jesus"], lowercase=True)
        self.assertEqual(words["jesus"], 518)

    def test_getmarkers(self):
        markers = self.usfmdoc.getmarkers()
        self.assertEqual(len(markers), 37)
        self.assertIn("p", markers)

    def test_hyphenate(self):
        mock = MockHyphen()
        self.usfmdoc.hyphenate(mock, False)
        # and test it somehow

    def test_subdoc(self, res=None):
        refrange = RefList.fromStr("JHN 3:16")
        subdoc = self.usfmdoc.subdoc(refrange, addzsetref=False)
        if res is None:
            t = str(subdoc[0][0][0])[10:38]
            self.assertEqual(t, "Due to God loving the people")
        else:
            t = str(subdoc[0][0][0])[10:10+len(res)]
            self.assertEqual(t, res)

    def test_transform(self):
        self.usfmdoc.addorncv()
        def testref(e):
            return e.pos.ref.first.chap == 3 and e.pos.ref.first.verse == 16
        self.usfmdoc.transform_text((testref, re.compile("(the people)"), r"all \1"))
        self.test_subdoc(res="Due to God loving all the people")

    def test_emptycvs(self):
        self.usfmdoc.stripEmptyChVs()

    def test_strongs(self):
        aStrongs = MockStrongs()
        self.usfmdoc.addStrongs(aStrongs, True)
        refrange = RefList.fromStr("JHN 3:16")
        subdoc = self.usfmdoc.subdoc(refrange, addzsetref=False)
        t = str(subdoc[0][0][0])[10:65]
        self.assertEqual(t, 'Due to God \u200B\\xts|strong="25" align="r"\\*\\nobreak loving')

if __name__ == "__main__":
    unittest.main()
