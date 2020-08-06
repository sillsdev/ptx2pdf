#!/usr/bin/python3

# Reads xdvi files and outputs a version that can be diffed.

import argparse, os
from struct import unpack


opcodes = [("setchar", [], i) for i in range(128)]
opcodes += [
    ("parmop", [1], "setcode"),
    ("parmop", [2], "setcode"),
    ("parmop", [3], "setcode"),
    ("parmop", [-4], "setcode"),
    ("multiparm", [-4]*2, "setrule"),
    ("parmop", [1], "setcode"),
    ("parmop", [2], "setcode"),
    ("parmop", [3], "setcode"),
    ("parmop", [-4], "setcode"),
    ("multiparm", [-4]*2, "setrule"),
    ("simple", [], "nop"),
    ("bop", [4]*11, "bop"),
    ("simple", [], "eop"),       # code 140
    ("simple", [], "push"),
    ("simple", [], "pop"),
    ("parmop", [-1], "right"),
    ("parmop", [-2], "right"),
    ("parmop", [-3], "right"),
    ("parmop", [-4], "right"),
    ("simple", [], "w"),
    ("parmop", [-1], "w"),
    ("parmop", [-2], "w"),
    ("parmop", [-3], "w"),         # code 150
    ("parmop", [-4], "w"),
    ("simple", [], "x"),
    ("parmop", [-1], "x"),
    ("parmop", [-2], "x"),
    ("parmop", [-3], "x"),
    ("parmop", [-4], "x"),
    ("parmop", [-1], "down"),
    ("parmop", [-2], "down"),
    ("parmop", [-3], "down"),
    ("parmop", [-4], "down"),
    ("simple", [], "y"),
    ("parmop", [-1], "y"),
    ("parmop", [-2], "y"),
    ("parmop", [-3], "y"),
    ("parmop", [-4], "y"),
    ("simple", [], "z"),
    ("parmop", [-1], "z"),
    ("parmop", [-2], "z"),
    ("parmop", [-3], "z"),
    ("parmop", [-4], "z")]         # code 170
opcodes += [("font", [], i) for i in range(64)]
opcodes += [
    ("font", [1], None),
    ("font", [2], None),
    ("font", [3], None),
    ("font", [4], None),
    ("xxx", [1], None),
    ("xxx", [2], None),
    ("xxx", [3], None),
    ("xxx", [4], None),
    ("fontdef", [1, 4, 4, 4, 1, 1], None),
    ("fontdef", [2, 4, 4, 4, 1, 1], None),
    ("fontdef", [3, 4, 4, 4, 1, 1], None),
    ("fontdef", [4, 4, 4, 4, 1, 1], None),
    ("pre", [1, 4, 4, 4, 1], None),
    ("multiparm", [4]*6 + [2,2], "post"),
    ("multiparm", [4, 1], "postpost"),
    ("unknown", [], None),   # code 250
    ("xpic", [1, 4, 4, 4, 4, 4, 4, 2, 2], None),
    ("xfontdef", [4, 4, 2], None),
    ("xglyphs", [], 1),
    ("xglyphs", [], 0),
    ("parmop", [1], "direction")]

packings = ("bhxi", "BHxI")

class Cursor:
    def __init__(self, name=None):
        self.name = name
        self.stack = []
        self.pos = [0, 0, 0, 0, 0, 0] # (h,v,w,x,y,z)
        self.pageno = 0
        self.pages = []
        self.page = Page(0)
        self.prevals = None
        self.postvals = None # unused at time of writing
        self.fonts = {} # map k: common id
        self.activefont = None
    
    def summarise(self):
        print(self.name)
        for font in self.fonts:
            print("Font {}: common ID {}".format(font, self.fonts[font]))
    
    def getpage(self):
        return self.page # sorted at eop
    
    def newpage(self):
        self.pages.append(self.page)
        self.page = Page(self.pageno)
    
    def right(self, dist):
        self.pos[0] = self.pos[0] + dist
    
    def down(self, dist):
        self.pos[1] = self.pos[1] + dist
        
    def w(self, dist=None):
        if dist is not None:
            self.pos[2] = dist
        self.right(self.pos[2])
        
    def x(self, dist=None):
        if dist is not None:
            self.pos[3] = dist
        self.right(self.pos[3])

    def y(self, dist=None):
        if dist is not None:
            self.pos[4] = dist
        self.down(self.pos[4])
        
    def z(self, dist=None):
        if dist is not None:
            self.pos[5] = dist
        self.down(self.pos[5])
        
    def push(self):
        self.stack.append(self.pos.copy())
    
    def pop(self):
        self.pos = self.stack.pop(-1)
    
    def bop(self):
        self.stack = []
        self.pos = [0, 0, 0, 0, 0, 0]
    
    def eop(self):
        self.page.glyphs.sort(key=lambda x:(x[0], x[1]))
    
    def setrule(self, data):
        pass # may want something implemented here?
    
    def post(self, data):
        self.postvals = data
    
    def postpost(self, *a):
        print(self.name, "xdv reading complete")  


class Page:
    def __init__(self, pageno=0):
        self.pageno = pageno
        self.glyphs = []
        #self.fonts = []
        self.summaryvals = None
   
        

class XDviType:
    def __init__(self, fname, gname, q=False):
        self.fonts = {} # (font parameter tuple): common ID
        self.q = q
        self.files = [open(fname, "rb"), open(gname, "rb")]
        self.pageno = 0
        if "project" in fname and "standard" in gname:
            fcurname, gcurname = "Project", "Standard"
        elif "project" in gname and "standard" in fname:
            gcurname, fcurname = "Project", "Standard"
        else:
            fcurname, gcurname = "Xdv 1", "Xdv 2"
        self.cursors = [Cursor(fcurname), Cursor(gcurname)]
        self.switch = 0
        self.cursor = self.cursors[self.switch]
        self.prevals = None
        self.mmtolerance = 10
        self.mmboxtolerance = (15, 15)
        self.pages = []
        self.allowfontmismatch = False
        self.fontid = -1
        
    def summary(self):
        print("Percentage matches:", ", ".join(["{:.1f}%".format((page[2] * 100)/(max(page[0], page[1]))) for page in self.pages]))
        
        for parm in self.fonts:
            #fontparam = (font_name, "{:.2f}mm".format(self.pointstomm(points)), "{:08X}".format(color), "{:04X}".format(flags), *variations, ext, slant, embolden)
            print("{}: {} at size {:.2f}mm, colour {:08X}, flags {:04X}, ext {}, slant {}, embolden {}".format(self.fonts[parm], parm[0], self.pointstomm(parm[1]), *parm[2:]))
        
    def glyphdistance(self, a, b):
        return a[2] == b[2] and (not self.allowfontmismatch or a[3]==b[3]) and (a[0]-b[0])**2 + (a[1]-b[1])**2 < self.sqdistance
    
    def glyphdistance2(self, a, b):
        if a[2] != b[2]:
            return None
        return abs(a[0] - b[0]) < self.boxtol[0] and abs (a[1] - b[1]) < self.boxtol[1]
        
    def locateglyph(self, aglyph, startindex, bglyphs):
        index = startindex
        flip = True
        blen = len(bglyphs)
        for i in range(2*max(blen-startindex, startindex)):
            index += i * (-1 if flip else 1)
            flip = not flip
            
            if 0 <= index and index <= blen-1 and self.glyphdistance(aglyph, bglyphs[index]):
                return True
        else:
            return False
    
    def compare(self, fcursor, gcursor):
        fpage, gpage = fcursor.page, gcursor.page
        
        count = 0        
        for i in range(len(fpage.glyphs)):
            try:
                count += self.locateglyph(fpage.glyphs[i], i, gpage.glyphs)
            except IndexError:
                pass
        page = (len(fpage.glyphs), len(gpage.glyphs), count)
        self.pages.append(page)
        if "postpost" in self.lastparm and self.lastparm != ["postpost"]*2:
            curs = self.cursors[not self.lastparm.index("postpost")]
            print("Mismatch in pages // glyphs: {} page {}: {} // no match possible".format(curs.name, self.pageno, len(curs.page.glyphs)))
        else:
            print("Page {}: {} // glyphs: {}: {}, {}: {} // {} ({:.1f}%) match".format(self.pageno, "Perfect" if fpage.glyphs == gpage.glyphs else "Imperfect", fcursor.name, len(fpage.glyphs), gcursor.name, len(gpage.glyphs), count, (page[2] * 100)/(max(page[0], page[1]))))
        #print("{}: {} glyphs found; {}: {} glyphs found; {} matched successfully".format())
        
    def readbytes(self, num):
        return self.files[self.switch].read(num)

    def readval(self, size, uint=False):
        d = self.readbytes(size)
        if size == 3:
            if uint:
                s = unpack(">"+packings[1][1]+packings[1][0], d)
                res = s[0] * 256 + s[1]
            else:
                s = unpack(">"+packings[0][1]+packings[1][0], d)
                res = s[0] * 256 + (s[1] if s[0] > 0 else -s[1])
        else:
            res = unpack(">"+packings[1 if uint else 0][size-1], d)[0]
        return res

    def parse(self):
        if True:
            print("Comparing {} and {} with {}mm tolerance, font mismatching is {}allowed".format(
                *[c.name for c in self.cursors], self.mmtolerance, "" if self.allowfontmismatch else "not "))
        
        self.lastparm = [None, None]
        while self.lastparm != ["postpost"]*2:
            op = self.readval(1, uint=True)
            opc = opcodes[op]
            data = [self.readval((x if x>0 else -x), uint=x>0) for x in opc[1]]
            self.lastparm[self.switch] = opc[2]
            getattr(self, opc[0])(op, opc[2], data)
            if opc[2] == "eop" or opc[2] == "postpost":
                if self.switch and self.lastparm != ["postpost"]*2:
                    self.compare(*self.cursors)
                    [cursor.newpage() for cursor in self.cursors]
                if self.lastparm[not self.switch] != "postpost":
                    self.switch = not self.switch
                    self.cursor = self.cursors[self.switch]
            elif opc[0] == "pre":
                if self.switch:
                    assert self.cursors[0].prevals[:4] == self.cursors[1].prevals[:4]
                    self.prevals = self.cursors[0].prevals
                    self.sqdistance = self.mmtopoints(self.mmtolerance)**2
                    self.boxtol = self.mmtopoints(self.mmboxtolerance[0]), self.mmtopoints(self.mmboxtolerance[1])
                self.switch = not self.switch
                self.cursor = self.cursors[self.switch]
        [curs.summarise() for curs in self.cursors]
        self.summary()

            

    def out(self, txt):
        if not self.q:
            print(("file[{}] pg[{}] ".format(self.switch, self.pageno) + txt).encode("utf-8"))
        
    def setchar(self, opcode, parm, data):
        self.out("setchar({})".format(opcode))

    def multiparm(self, opcode, parm, data):
        self.out("{}({}) {}".format(parm, opcode, data))
        getattr(self.cursor, parm)(data)

    def parmop(self, opcode, parm, data):
        self.out("{}({}) [{}]".format(parm, opcode, data[0]))
        getattr(self.cursor, parm)(data[0])

    def simple(self, opcode, parm, data):
        self.out("{}".format(parm))
        getattr(self.cursor, parm)()

    def bop(self, opcode, parm, data):
        self.pageno = data[0]
        for cursor in self.cursors:
            cursor.page.pageno = data[0] ######### This is wrong
        self.out("{}({}) [{}]".format(parm, opcode, data[0]))

    def font(self, opcode, parm, data):
        if parm is not None:
            data = [parm]
        #self.out("font [{:04x}]".format(self.fonts[data[0]][0]))
        self.cursor.activefont = self.cursor.fonts[data[0]]
        #print("Switch to font [{}] on cursor {}, font found {}successfully".format(data[0], self.cursor.name, "un" if data[0] not in self.cursor.fonts else ""))

    def xxx(self, opcode, parm, data):
        txt = self.readbytes(data[0])
        self.out('special({}) "{}"'.format(opcode, txt.decode("utf-8")))

    def fontdef(self, opcode, parm, data):
        (k, c, s, d, a, l) = data
        n = self.readbytes(a+l).decode("utf-8")
        # the k to c mapping may vary across 'identical' files
        self.out("fontdef({}) checksum={:04x} sf={:f} name=\"{}\"".format(opcode, c, s / 1000. / d, n))
        self.cursor.fonts[k] = (c, n)

    def pre(self, opcode, parm, data):
        (i, n, d, m, k) = data
        x = self.readbytes(k)
        print("{} pre num={}, den={}, mag={}".format(self.cursor.name, n, d, m))
        self.cursor.prevals = data

    def xfontdef(self, opcode, parm, data):
        (k, points, flags) = data
        plen = self.readval(1, uint=True)
        font_name = self.readbytes(plen).decode("utf-8")
        font_name = os.path.basename(font_name)
        color = self.readval(4) if flags & 0x200 else 0xFFFFFFFF
        if flags & 0x800:       # variations
            nvars = self.readval(2)
            variations = [self.readval(4) for i in range(nvars)]
        else:
            variations = []
        ext = self.readval(4) if flags & 0x1000 else 0
        slant = self.readval(4) if flags & 0x2000 else 0
        embolden = self.readval(4) if flags & 0x4000 else 0
        ident = self.readval(4)
        
        #fontparam = (font_name, "{:.2f}mm".format(self.pointstomm(points)), "{:08X}".format(color), "{:04X}".format(flags), *variations, ext, slant, embolden)
        
        fontparam = (font_name, points, color, flags, *variations, ext, slant, embolden)
        
        if fontparam not in self.fonts:
            self.fontid += 1
            self.fonts[fontparam] = self.fontid
        
        if k not in self.cursor.fonts:
            self.cursor.fonts[k] = self.fonts[fontparam]
        
        #print('{} xfontdef k{} [{}] "{}", size={:.2f}mm, flags={:04X}, color={:08X}, vars={}, ext={}, slant={}, embolden={}'.format(self.cursor.name, k,
                #ident, font_name, self.pointstomm(points), flags, color, variations, ext, slant, embolden))

    def xglyphs(self, opcode, parm, data):
        width = self.readval(4)
        slen = self.readval(2, uint=True)
        if parm:
            pos = [(self.readval(4), self.readval(4)) for i in range(slen)]
        else:
            pos = [(self.readval(4), 0) for i in range(slen)]
        glyphs = [self.readval(2) for i in range(slen)]
        #res = ["{}@({},{})".format(glyphs[i], *pos[i]) for i in range(slen)]
        #self.out("xglyphs: {}".format(res))
        curs = self.cursor
        curs.page.glyphs += [(pos[i][0] + curs.pos[1], pos[i][1] + curs.pos[0], glyphs[i], curs.activefont) for i in range(slen)] ########## This needs checking; does xglyphs move the cursor at all?

    def xpic(self, opcode, parm, data):
        box = data.pop(0)
        length = data.pop()
        pageno = data.pop()
        matrix = data[:]
        path = self.readbytes(length).decode("utf-8")
        self.out('xpic "{}"@{} pageno={}, box={}'.format(path, matrix, pageno, box))
    
    def pointstomm(self, dist):
        # (i, n, d, m, k)
        if self.prevals is None:
            raise NameError("Preamble values have not yet been read")
        return (dist * self.prevals[1] * self.prevals[3]) / (self.prevals[2] * 10**7)
    
    def mmtopoints(self, mm):
        # (i, n, d, m, k)
        if self.prevals is None:
            raise NameError("Preamble values have not yet been read")
        return (mm * self.prevals[2] * 10**7) /(self.prevals[1] * self.prevals[3]) 


parser = argparse.ArgumentParser()
parser.add_argument("projectfile",help="Input xdvi file (project)")
parser.add_argument("standardfile",help="Input xdvi file (standard)")
parser.add_argument("-q","--quiet",action="store_true",help="Run quietly")
args = parser.parse_args()

dviparser = XDviType(args.projectfile, args.standardfile, args.quiet)
dviparser.parse()

'''
Points for discussion:
    - What's the most efficient way to check whether a glyph matches? Currently takes a long time to exclude possibilities
        Maybe using a dictionary by glyph id, or arranging into a list matrix and only searching rows within a feasible distance?
    - Do the flags affect the slant/boldness of a font, or do they just specify whether or not there is a value to be read?


'''