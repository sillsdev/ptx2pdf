from xdv import XDViPositionedReader 
import math
class SpacingOddities(XDViPositionedReader):
    # todo: add optional parameter for max and min space.
    def __init__(self, fname, diffable = False, slimits = (2,4)):
        super().__init__(fname, diffable)
        self.lines = [] 
        self.currline = Line([0,0]) # fixme: add right positions for the first line.
        # perhaps convert to pt depending on input type
        self.smin = slimits[0]
        self.smax = slimits[1]
        
    def currpos(self):
        # fixme: do we really need to save all, or just h and v enough?
        curr_pos = (self.h,self.v, self.w,self.x,self.y,self.z)
        return curr_pos

    def parmop(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().parmop(opcode, parm, data) 
        self.check_changes(prev_pos, opcode)

    def simple(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().simple(opcode, parm, data)
        self.check_changes(prev_pos, opcode)

    def xglyphs(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().xglyphs(opcode, parm, data)
        self.check_changes(prev_pos, opcode)

    def check_changes(self, prevpos, opcode):
        if self.v != prevpos[1]:
            # if the current line contains min. 1 item, save h-pos and add to lines list
            if not self.currline.isEmpty():
                self.currline.finish(self.currpos())
                self.lines.append(self.currline)
            self.currline = Line(self.currpos())
        if self.h != prevpos[0]:
            self.currline.add_item(prevpos, self.currpos(), opcode)

    def get_badspaces(self):
        badspace_lines = []
        for l in self.lines:
            l.find_badspaces((self.smin, self.smax))
            if len(l.badspaces) >0:
                badspace_lines.append(l)
        return badspace_lines

class Line:
    def __init__(self, startpos):
        self.starth = 0
        self.startv = startpos[1]
        self.width = 0
        self.order = [] # glyph, space widths
        self.glyphs = []
        self_gcount = 0
        self.gstart = 0 # start h-pos of glyph
        self.prevline = None # keep track of previous line
        self.ref = 0
        self.badspaces = []

    def isEmpty(self):
        if len(self.order) >0:
            return False
        return True

    def add_item(self, prevpos, newpos, opcode):
        if opcode <143:
            itype = 'glyph'
        else:
            itype = 'space'
        if self.isEmpty():
            self.starth = prevpos[0]
        # fixme: there are glyphs without width, so should be added without checking width?
        if prevpos[0] != newpos[0]:
            iwidth = abs(newpos[0] - prevpos[0])
            self.order.append(iwidth)
        # todo: handle type, so save to glyphs or spaces depending on the type. See opcodes.

    def finish(self, endpos):
        self.width = abs(endpos[0] - self.starth)

    def find_badspaces(self, slimits):
        for i in range(1, len(self.order), 2):
            if slimits[0] <= self.order[i] <= slimits[1]:
                pass
            else:
                # get startpos of space by startpos line + sum of item widths up to space
                self.badspaces.append((self.starth + sum(self.order[:i-1]), self.order[i]))

def main():
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 10:
            break
        pass
    print(len(reader.lines))
    print(reader.smin)
    print(reader.smax)
    bspace_lines = reader.get_badspaces()
    for l in bspace_lines:
        print(f"Reference {l.ref} contains badspaces at locations {[loc for (loc, w) in l.badspaces]}")


if __name__ == "__main__":
    main()