from ptxprint.xdv.xdv import XDViPositionedReader, Font
from ptxprint.font import TTFont
import math
import re

# todo: check if we're consistent with adding gc and line objects: is currgc always -1 index?
class SpacingOddities(XDViPositionedReader, ems = 1.2):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.currline = None
        self.currgc = None
        self.ref = None

    def curr_hv(self):
        curr_pos = (self.h,self.v)
        return curr_pos

    def parmop(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().parmop(opcode, parm, data) 
        self.handle_hv_changes(prev_pos, opcode)
        return result

    def simple(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().simple(opcode, parm, data)
        self.handle_hv_changes(prev_pos, opcode)
        return result

    def xglyphs(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        self.handle_hv_changes(prev_pos, opcode, gno = glyphs, gpos = pos)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        pat = r'\((.*?)\)'
        self.ref= re.findall(pat, txt)
        #super().xxx(opcode, parm, data)
        return (txt,)

    def xfontdef(self, opcode, parm, data):
        (k, points, flags) = data
        # points is huge number rn.
        # convert points to ems
        # save ems as the space thingie for the curr glyphcontent obj
        (k, font) = super().xfontdef(opcode, parm, data)
        font_size = self.fonts[k].points
        # set fontsize for current gc block
        self.currline.content[-1].fontsize = font_size
        print(f"size of {self.fonts[k].name} is {self.topt(font_size)}")
        
        return (k, font)
        # question: should we save the h when starting new gc block, or enter first hpos when adding new glyph?
        # so: is the hpos at start of new block same as end prev block, or is there space between blocks?
        # and if so, under whose jurisdiction do they fall? old or new font?
        #super().xfontdef(opcode, parm, data)

    def handle_hv_changes(self, prevpos, opcode, gno = None, gpos = None):
        # check vertical movement
        if self.v != prevpos[1]:
            # check if line is empty (then first gc has no elements)
            if self.currline != None:
                if len(self.currline.content[-1].glyphs) <1:
                    # reuse line, font stays the same, update ref
                    self.currline.ref = self.ref
                else:
                    self.currline.report_badspaces(ems)
                    self.currline.prevline = None
                    self.currline = Line(self.ref, self.currline)
                    self.currline.add_gc(self.font)
            else:
                # this will be the first line
                self.currline = Line(self.ref, Line(self.ref, None))
                gc = GlyphContent(self.font)
                self.currline.content.append(gc)
        # check horizontal movement
        if self.h != prevpos[0]:
            # check glyph
            if opcode < 142:
                self.currline.content[-1].add_glyph(gno, gpos)

            
class Line: 
    def __init__(self, ref, line):
        self.ref = ref
        self.content = [] # list of GlyphContent objects, index -1 contains current gc
        self.prevline = line
        self.vstart = 0
        self.vrange = [0,0] # upper (min) and lower (max) v-pos of Line

    def fontchange(self, font):
        # update line vrange based on previous gc vrange
        self.vrange[0] = min(self.vrange[0], self.content[-1].vrange[0])
        self.vrange[1] = max(self.vrange[1], self.content[-1].vrange[1])
        # create new gc obj with new font and add it to this line
        gc = GlyphContent(font)
        self.content.append(gc)

    def report_badspaces(self, ems, diff = .1):
        # needs to be per gc, since font affects max space.
        for gc_block in self.content:
            if gc_block.find_badspaces():
                print(f"The line with reference {self.ref} starting at {self.get_pos()} contains badspaces")
                break

    def get_pos(self):
        hstart = self.content[0].starts[0]
        return (hstart, self.vstart)

class GlyphContent:
    def __init__(self, font):
        # make ttfont with name none.
        # todo: let fontsize be determined in one go, not save self.font
        self.font = TTFont(None)
        self.fontsize = 0 # in pt
        self.glyphs = []
        self.starts = []
        self.vrange = (0,0) # upper and lower v of gc block 

    def add_glyph(self, g_no, g_pos):
        # fixme: method incomplete.
        #g_no and g_pos are lists of res. numbers and 2-tuples (h,v)
        glyph = self.font.readfont(withglyphs = True)
        # can ask 
        # get 
        # todo: check max en min x en y, update gc vrange
        self.glyphs.append(glyph)
        #self.starts.append(pos)

    def find_badspaces(self, ems, diff = .1):
        smin, smax = self.set_slimits(ems) 
        for i in range(len(self.starts)-2):
            sratio = self.starts[i+1] - self.starts[i]
            s_vs_ems = abs(sratio - ems) / ems
            if s_vs_ems > diff:
                return True
        return False

def main():
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 3:
            break
        pass

if __name__ == "__main__":
    main()