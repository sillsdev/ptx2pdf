from xdv import XDViPositionedReader 
import math
import re
class SpacingOddities(XDViPositionedReader):
    # todo: add optional parameter for max and min space.
    def __init__(self, fname, diffable = False, slimits = (2,4)):
        super().__init__(fname, diffable)
        self.lines = [] 
        self.currline = Line([0,0], 'first line') # fixme: add right positions for the first line.
        # fixme: perhaps convert to pt depending on input type, will most likely be input.
        self.smin = slimits[0]
        self.smax = slimits[1]
        
    def currpos(self):
        curr_pos = (self.h,self.v)
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

    def xxx(self, opcode, parm, data):
        ref = self.readbytes(data[0])
        ref2 = ref.decode("utf-8")
        pat = r'\((.*?)\)'
        ref3= re.findall(pat, ref2)
        if ref3:
            self.currline.ref = ref3[0]
        return (ref2,)

    def check_changes(self, prevpos, opcode):
        if self.v != prevpos[1]:
            # if the current line contains min. 1 item, save endpos and add to lines list
            if not self.currline.isEmpty():
                self.currline.finish(self.currpos())
                self.lines.append(self.currline)
            self.currline = Line(self.currpos(), self.currline.ref)
        if self.h != prevpos[0]:
            self.currline.add_item(prevpos, self.currpos(), opcode)

    def report_bad_spaces(self):
        bad_lines = 0
        for l in self.lines:
            bspaces = l.find_badspaces((self.smin, self.smax))
            if len(bspaces) >0:
                print(f"A line in {l.ref} contains {len(bspaces)} bad spaces.")
                bad_lines += 1
        print(f"A total of {len(self.lines)} lines was checked. {bad_lines} lines contained bad spaces.")

    def get_badspaces(self):
        # fixme: depending on how we handle spaces, this method is unnecessary and we can just call 
        # the badspaces function per line from another place.
        badspace_lines = []
        for l in self.lines:
            bspaces = l.find_badspaces((self.smin, self.smax))
            if len(bspaces) >0:
                badspace_lines.append(bspaces) 
        return badspace_lines

class Line:
    def __init__(self, startpos, ref):
        self.starth = 0
        self.startv = startpos[1]
        self.width = 0
        self.order = [] # glyph, space widths
        self.glyphs = [] # todo: implement
        self_gcount = 0 # todo: implement
        self.gstart = 0 # start h-pos of glyph #todo: implement
        self.prevline = None # keep track of previous line # todo: implement
        self.ref = ref # todo: implement 

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
        badspaces = []
        for i in range(1, len(self.order), 2):
            if slimits[0] <= self.order[i] <= slimits[1]:
                pass
            else:
                # get startpos of space by startpos line + sum of item widths up to space
                badspaces.append((self.starth + sum(self.order[:i-1]), self.order[i]))
        return badspaces

def main():
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 10:
            break
        pass
    reader.report_bad_spaces()
    

if __name__ == "__main__":
    main()