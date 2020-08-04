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
    def __init__(self, filename=None):
        self.filename = filename
        self.stack = []
        self.pos = [0, 0, 0, 0, 0, 0] # (h,v,w,x,y,z)
        self.pageno = 0
        self.page = Page()
    
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
        pass#print(self.page.glyphs)
        #input(False)
    
    def font(self):
        pass
    
    def xfontdef(self):
        pass
    
    def pre(self):
        pass
    
    def special(self):
        pass
    
    def setrule(self, data):
        pass
    
    def post(self, *a):
        pass
    
    def postpost(self, *a):
        pass

class Page:
    def __init__(self, pageno=0):
        self.pageno = pageno
        self.glyphs = []
        self.fonts = []
   
        

class XDviType:
    def __init__(self, fname, gname, q=False):
        self.fonts = {}
        self.f = open(fname, "rb")
        self.g = open(gname, "rb")
        self.files = [self.f, self.g]
        self.pageno = 0
        self.fcursor = Cursor()
        self.gcursor = Cursor()
        self.cursors = [self.fcursor, self.gcursor]
        self.switch = 0
        self.q = q
    
    def compare(self, fcursor, gcursor):
        fpage = fcursor.page
        gpage = gcursor.page
        fpage.glyphs.sort(key=lambda x:(x[0], x[1]))
        gpage.glyphs.sort(key=lambda x:(x[0], x[1]))
        for i in range(len(fpage.glyphs)):
            pass#print(fpage.glyphs[i], gpage.glyphs[i])
        #print(fpage.glyphs)
        #print(gpage.glyphs)
        print("Page {} equivalent: {}".format(self.pageno, fpage.glyphs == gpage.glyphs))
        fcursor.page = Page()
        gcursor.page = Page()
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
        lastparm = None
        while lastparm != "postpost":
            op = self.readval(1, uint=True)
            opc = opcodes[op]
            data = [self.readval((x if x>0 else -x), uint=x>0) for x in opc[1]]
            lastparm = opc[2]
            #print(self.cursors[self.switch].pos)
            getattr(self, opc[0])(op, lastparm, data)
            if opc[2] == "eop":
                #input(self.switch)#self.cursor = self.cursors[self.switch]
                if self.switch:
                    self.compare(*self.cursors)
                self.switch = not self.switch
            

    def out(self, txt):
        if not self.q:
            print(("file[{}] pg[{}] ".format(self.switch, self.pageno) + txt).encode("utf-8"))
        
    def setchar(self, opcode, parm, data):
        self.out("setchar({})".format(opcode))

    def multiparm(self, opcode, parm, data):
        self.out("{}({}) {}".format(parm, opcode, data))
        getattr(self.cursors[self.switch], parm)(data)

    def parmop(self, opcode, parm, data):
        self.out("{}({}) [{}]".format(parm, opcode, data[0]))
        getattr(self.cursors[self.switch], parm)(data[0])

    def simple(self, opcode, parm, data):
        self.out("{}".format(parm))
        getattr(self.cursors[self.switch], parm)()

    def bop(self, opcode, parm, data):
        self.pageno = data[0]
        self.out("{}({}) [{}]".format(parm, opcode, data[0]))

    def font(self, opcode, parm, data):
        if parm is not None:
            data = [parm]
        self.out("font [{:04x}]".format(self.fonts[data[0]][0]))

    def xxx(self, opcode, parm, data):
        txt = self.readbytes(data[0])
        self.out('special({}) "{}"'.format(opcode, txt.decode("utf-8")))

    def fontdef(self, opcode, parm, data):
        (k, c, s, d, a, l) = data
        n = self.readbytes(a+l).decode("utf-8")
        # the k to c mapping may vary across 'identical' files
        self.out("fontdef({}) checksum={:04x} sf={:f} name=\"{}\"".format(opcode, c, s / 1000. / d, n))
        self.fonts[k] = (c, n)

    def pre(self, opcode, parm, data):
        (i, n, d, m, k) = data
        x = self.readbytes(k)
        self.out("pre num={}, den={}, mag={}".format(n, d, m))

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
        self.fonts[k]=(ident, font_name)
        self.out('xfontdef[{}] "{}", size={}, flags={:04X}, color={:08X}, vars={}, ext={}, slant={}, embolden={}'.format(
                ident, font_name, points, flags, color, variations, ext, slant, embolden))

    def xglyphs(self, opcode, parm, data):
        width = self.readval(4)
        slen = self.readval(2, uint=True)
        if parm:
            pos = [(self.readval(4), self.readval(4)) for i in range(slen)]
        else:
            pos = [(self.readval(4), 0) for i in range(slen)]
        glyphs = [self.readval(2) for i in range(slen)]
        res = ["{}@({},{})".format(glyphs[i], *pos[i]) for i in range(slen)]
        self.out("xglyphs: {}".format(res))
        curs = self.cursors[self.switch]
        curs.page.glyphs += [(pos[i][0] + curs.pos[1], pos[i][1] + curs.pos[0], glyphs[i]) for i in range(slen)] ########## This needs checking; does xglyphs move the cursor at all?

    def xpic(self, opcode, parm, data):
        box = data.pop(0)
        length = data.pop()
        pageno = data.pop()
        matrix = data[:]
        path = self.readbytes(length).decode("utf-8")
        self.out('xpic "{}"@{} pageno={}, box={}'.format(path, matrix, pageno, box))

parser = argparse.ArgumentParser()
parser.add_argument("projectfile",help="Input xdvi file (project)")
parser.add_argument("standardfile",help="Input xdvi file (standard)")
parser.add_argument("-q","--quiet",action="store_true",help="Output a diffable structure")
args = parser.parse_args()

dviparser = XDviType(args.projectfile, args.standardfile, args.quiet)
dviparser.parse()
