from xdv import XDViPositionedReader 
import math
class SpacingOddities(XDViPositionedReader):
    # todo: add optional parameter for max and min space.
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.lines = [] 
        self.currline = Line([0,0]) # fixme: add right positions for the first line.
        
    def currpos(self):
        # fixme: do we really need to save all, or just h and v enough?
        curr_pos = (self.h,self.v, self.w,self.x,self.y,self.z)
        return curr_pos

    def parmop(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().parmop(opcode, parm, data) 
        self.check_changes(prev_pos, opcode)
        if opcode <= 142:
            itype = 3 #glyph
        else:
            itype = 4 # space=

    def simple(self, opcode, parm, data):
        prev_pos = self.currpos()
        itype = 4 # FIXME: is this really always a space?
        super().simple(opcode, parm, data)
        self.check_changes(prev_pos, opcode)

    def xglyphs(self, opcode, parm, data):
        prev_pos = self.currpos()
        itype = 3     # glyph
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
            # fixme: should i pass opcode or decide here whether it is glyph or space?
            self.currline.add_item(prevpos, self.currpos(), opcode)
class Line:
    # fixme: should this be a subclass of list?
    def __init__(self, startpos):
        self.starth = 0
        self.startv = startpos[1]
        self.width = 0
        self.order = [] # glyph, space widths
        self.ref = 0
        self.glyphs = []
        self.gstart = 0 # start h-pos of glyph
        self.prevline = None # keep track of previous line
        

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


def main():
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 10:
            break
        pass
    print(len(reader.lines))



if __name__ == "__main__":
    main()