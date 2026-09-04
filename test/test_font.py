#!/usr/bin/python3

import unittest, os, struct, tempfile
from ptxprint.font import TTFont, initFontCache

fontsdir = os.path.join(os.path.dirname(__file__), "fonts")

def mkhead(upem):
    return struct.pack(">18s H 34s", b"\0" * 18, upem, b"\0" * 34)

def mkname(names):
    ''' Build a name table holding Windows US English records for names: {nameID: string} '''
    recs = b""
    strings = b""
    for nid, val in sorted(names.items()):
        dat = val.encode("utf_16_be")
        recs += struct.pack(">HHHHHH", 3, 1, 1033, nid, len(dat), len(strings))
        strings += dat
    return struct.pack(">HHH", 0, len(names), 6 + len(recs)) + recs + strings

def mkttc(faces):
    ''' Build a font collection where each face is a {tag: data} mapping of tables '''
    hdr = struct.pack(">4sLL", b"ttcf", 0x00010000, len(faces))
    diroff = len(hdr) + 4 * len(faces)
    diroffs = []
    for f in faces:
        diroffs.append(diroff)
        diroff += 12 + 16 * len(f)
    dat = b""
    dirs = b""
    for f in faces:
        dirs += struct.pack(">LHHHH", 0x00010000, len(f), 0, 0, 0)
        for tag, tdat in sorted(f.items()):
            dirs += struct.pack(">4sLLL", tag, 0, diroff + len(dat), len(tdat))
            dat += tdat
    return hdr + b"".join(struct.pack(">L", o) for o in diroffs) + dirs + dat

def writettc(faces):
    f = tempfile.NamedTemporaryFile(suffix=".ttc", delete=False)
    f.write(mkttc(faces))
    f.close()
    return f.name


class TestTTCollection(unittest.TestCase):
    ''' macOS ships families like Arial and Courier as collections whose faces carry
        no US English family name, so the family search can never match (#1093). '''

    @classmethod
    def setUpClass(cls):
        initFontCache(nofclist=True)    # these fonts are read by name, not looked up

    def setUp(self):
        self.tmps = []

    def tearDown(self):
        TTFont.cache.clear()
        for f in self.tmps:
            os.unlink(f)

    def mkfont(self, faces, family, style=""):
        fname = writettc(faces)
        self.tmps.append(fname)
        TTFont.cache.clear()
        return TTFont(family, style, filename=fname)

    def test_no_family_names(self):
        faces = [{b"head": mkhead(1000), b"name": mkname({2: "Regular"})},
                 {b"head": mkhead(2048), b"name": mkname({2: "Bold"})}]
        f = self.mkfont(faces, "Courier", "Bold")
        self.assertEqual(f.upem, 1000)
        self.assertEqual(f.family, "Courier")

    def test_family_not_in_collection(self):
        faces = [{b"head": mkhead(1000), b"name": mkname({1: "Avenir", 2: "Regular"})},
                 {b"head": mkhead(2048), b"name": mkname({1: "Avenir", 2: "Bold"})}]
        f = self.mkfont(faces, "Not A Font Family")
        self.assertEqual(f.upem, 1000)

    def test_unknown_family(self):
        ''' TTFontCache.addFontDir reads a file before it knows the family '''
        faces = [{b"head": mkhead(1000), b"name": mkname({1: "Avenir", 2: "Regular"})}]
        f = self.mkfont(faces, None)
        self.assertEqual(f.upem, 1000)
        self.assertEqual(f.family, "Avenir")

    def test_face_without_name_table(self):
        faces = [{b"head": mkhead(1000)},
                 {b"head": mkhead(2048), b"name": mkname({1: "Avenir", 2: "Bold"})}]
        f = self.mkfont(faces, "Avenir", "Bold")
        self.assertEqual(f.upem, 2048)

    def test_matching_family_wins(self):
        faces = [{b"head": mkhead(1000), b"name": mkname({1: "Avenir", 2: "Regular"})},
                 {b"head": mkhead(2048), b"name": mkname({1: "Charis", 2: "Regular"})}]
        f = self.mkfont(faces, "Charis")
        self.assertEqual(f.upem, 2048)

    def test_empty_collection(self):
        f = self.mkfont([], "Avenir")
        self.assertIsNone(f.filename)

    def test_plain_font_unaffected(self):
        TTFont.cache.clear()
        f = TTFont("Charis SIL", "", filename=os.path.join(fontsdir, "CharisSIL-Regular.ttf"))
        self.assertEqual(f.family, "Charis SIL")
        self.assertEqual(f.upem, 2048)


if __name__ == "__main__":
    unittest.main()
