from ptxprint.xdv.xdv import XDViPositionedReader, Font
from ptxprint.font import TTFont
import math
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.curr_ref = None # reference of where we're at, str
        self.lines = [Line(self.v, self.curr_ref)] # list of Line objects
        self.cursor = (self.h, self.v) # location of last printed glyph
        self.ctol = 0.01 # the absolut difference tolerated to consider v change a difference

    def bop(self, opcode, parm, data):
        result = super().bop(opcode, parm, data)
        return result 

    def xglyphs(self, opcode, parm, data):
        prev_pos = (self.h, self.v)        
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        if not math.isclose((self.h-prev_pos[0]), 0, abs_tol = self.ctol):
            # glyphs have some width
            glyphs_width = self.topt(width)
            if self.new_line_needed(prev_pos):
                self.lines.append(Line(prev_pos[1],self.curr_ref))
            self.lines[-1].add_glyphs(prev_pos, glyphs_width)
        self.cursor = (self.h, self.v)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf:dest', txt):
            self.curr_ref = re.findall(r'\((.*?)\)', txt)[0]
        return (txt,)

    def xfontdef(self, opcode, parm, data):
        # this method does not change pos
        (k, font) = super().xfontdef(opcode, parm, data)
        font_size = self.topt(font.points)
        if self.new_line_needed((self.h, self.v)):
            self.lines.append(Line(self.v, self.curr_ref))        
        self.lines[-1].change_font((self.h, self.v), font_size)
        self.cursor = (self.h,self.v)
        return (k, font)
        # todo: for line collision, check if k is already in font cache
        # todo: if not, create TTFont as attribute of the xdv-font
        # todo: readfont() and add to font cache font.ttfont = TTFont(None, filename = font.name)
        # question: what does the cache in TTFont class do? Since it is within the class, I thought it was an attribute of font object but it adds properties of the font to it in the __init__, so it contains multiiple fonts?

    def new_line_needed(self, startpos):
        if len(self.lines[-1].gcs) == 0:
            # overwrite current line if it was empty.
            self.lines[-1] = Line(startpos[1], self.curr_ref)
            return False
        if math.isclose(self.cursor[1], startpos[1], abs_tol = self.ctol):
            if math.isclose(self.cursor[1], self.lines[-1].v_start, abs_tol = self.ctol):
                # cursor is at glyph start position and at current line v. No need for new line.
                return False
        return True

        # if not math.isclose(startpos[1], self.cursor[1], abs_tol = self.ctol):
        #     vdiff = self.cursor[1] - startpos[1]
        #     if vdiff < 0:
        #         if not math.isclose(startpos[0], self.cursor[0], abs_tol = self.ctol) and self.cursor[0] > startpos[0]:
        #             # v higher, h smaller: new pos move cursor down and left on page
        #             return True
        #     if vdiff > 12:
        #         #if not math.isclose(startpos[0], self.cursor[0], abs_tol = self.ctol) and self.cursor[0] < startpos[0]:
        #             # v smaller, h bigger: new pos move cursor up and right on page
        #         return True
        # if not math.isclose(self.lines[-1].v_start, self.cursor[1], abs_tol = self.ctol):
        #     linediff = abs(self.cursor[1] - self.lines[-1].v_start)
        #     print(f"Line and cursor mismatch by {linediff}")
        #     if linediff >4:
        #         return True
        # return False                   
class Line: 
    def __init__(self, v, ref):
        self.ref = ref
        self.gcs = [] # list of GlyphContent objects, index -1 contains current gc
        self.v_start = v
        self.curr_font = 0

    def change_font(self, pos, fontsize):
        self.gcs.append(GlyphContent(pos, fontsize))
        self.curr_font = fontsize

    def add_glyphs(self, prevpos, w): # in points
        if len(self.gcs) == 0:
            self.gcs.append(GlyphContent(prevpos, self.curr_font))
        elif prevpos[0] - (self.gcs[-1].h_start + self.gcs[-1].width) >1:
            # make new gc block if there is space between glyphs this block and the previous one.
            self.gcs.append(GlyphContent(prevpos, self.curr_font))
        self.gcs[-1].width += w

    def has_badspace(self, threshold = 4):
        # We don't count spaces at the start or end of a line
        # todo: define space boundary based on fontsize of blocks, spaces take size of preceding block.
        # todo: return start and width of space 
        if len(self.gcs) >1:
            for i in range (0, len(self.gcs)-1):
                if self.gcs[i+1].h_start - (self.gcs[i].h_start + self.gcs[i].width) > threshold:
                    return True
        return False

class GlyphContent:
    def __init__(self, pos, fontsize):
        self.h_start = pos[0]
        self.font_size = fontsize # in points
        self.width = 0

    def add_glyph(self, g_no, g_pos):
        # note: to be implemented still
        # todo: for every glyph, find what x&y cooridnat is relative to start of line, resolve to actual position.
        # todo: need the y of every glyph, for calculating when things change. top of line is ymax + the offset. 
        # size of glyph won't change, but the boundary box will. g_no and g_pos are lists of res. numbers and 2-tuples (h,v)
        glyph = self.font.readfont(withglyphs = True)
        # todo: check max en min x en y, update gc vrange

def main():
    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSGlatin/local/ptxprint/Default/WSGlatin_Default_RUT_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 1:
            break  
    
    for l in reader.lines:
        print(f"Start line: {l.v_start}")
    print(f"There are {len(reader.lines)} lines in total.")  


if __name__ == "__main__":
    main()