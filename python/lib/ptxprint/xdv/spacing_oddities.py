from ptxprint.xdv.xdv import XDViPositionedReader, Font
from ptxprint.font import TTFont
import math
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.curr_ref = None # reference of where we're at, str
        self.lines = [Line((self.h, self.v), self.curr_ref)] # list of Line objects
        self.cursor = (0,0) # location of last printed glyph
        self.ctol = 0.0001 # the absolut difference tolerated to consider v change a difference 
    
    def bop(self, opcode, parm, data):
        result = super().bop(opcode, parm, data)
        return result 

    def xglyphs(self, opcode, parm, data):
        prev_pos = (self.h, self.v)
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        
            
        if self.new_line_needed(prev_pos):
            self.lines.append(Line(prev_pos, self.curr_ref))
       # else:
        #    if not math.isclose(prev_pos[1], self.cursor[1], abs_tol = self.ctol):
         #       print(f"No new line added for change of {prev_pos[1]- self.cursor[1]}, self v is {self.v}")
        glyphs_width = self.topt(width)               
        self.lines[-1].add_glyphs(prev_pos[0], glyphs_width)
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
            self.lines.append(Line((self.h, self.v), self.curr_ref))
        self.lines[-1].change_font(self.h, font_size)
        self.cursor = (self.h, self.v)

        # todo: for line collision, check if k is already in font cache
        # todo: if not, create TTFont as attribute of the xdv-font
        # todo: readfont() and add to font cache
        #font.ttfont = TTFont(None, filename = font.name)
        # question: what does the cache in TTFont class do? Since it is within the class, I thought it was an attribute of font object
        # but it adds properties of the font to it in the __init__, so it contains multiiple fonts?
        return (k, font)

    def new_line_needed(self, startpos):
        if not math.isclose(startpos[0], self.cursor[0], abs_tol = self.ctol):
            # h changed 
            if startpos[0] < self.cursor[0]:
                #h moved backward
                if not math.isclose(startpos[1], self.cursor[1], abs_tol = self.ctol) and startpos[1] > self.cursor[1]:
                    # v changed and got bigger, moved down on page
                    return True
            elif startpos[0] > self.cursor[0]:
                # h moved forward
                if not math.isclose(startpos[1], self.cursor[1], abs_tol = self.ctol) and (self.cursor[1] - startpos[1]) > 20:
                    # v moved up the page by min. 20 points.
                    return True
        elif math.isclose(startpos[0], self.cursor[0], abs_tol = self.ctol):
            print(f"h stayed the same {startpos[0]-self.cursor[0]} and v moved {startpos[1] - self.cursor[1]}")
        return False                   
class Line: 
    def __init__(self, pos, ref):
        self.ref = ref
        self.gcs = [] # list of GlyphContent objects, index -1 contains current gc
        self.startpos = pos[:2]

    def change_font(self, h, fontsize):
        self.gcs.append(GlyphContent(h, fontsize))

    def add_glyphs(self, prev_h, w): # in points
        if len(self.gcs) == 0:
            self.gcs.append(GlyphContent(prev_h, None))
            # can we use if or above? or will it give error since out of bounds.
        elif prev_h - (self.gcs[-1].h_start + self.gcs[-1].width) >1:
            # make new gc block if there is space between glyphs this block and the previous one.
            self.gcs.append(GlyphContent(prev_h, self.gcs[-1].font_size))
        self.gcs[-1].width += w

    def has_badspace(self, threshold = 4):
        # We don't count spaces at the start or end of a line.yes 
        if len(self.gcs) >1:
            for i in range (0, len(self.gcs)-1):
                if self.gcs[i+1].h_start - (self.gcs[i].h_start + self.gcs[i].width) > threshold:
                    return True
        return False

class GlyphContent:
    def __init__(self, h, fontsize):
        self.h_start = h
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
        if reader.pageno > 5:
            break  

    print(f"There are {len(reader.lines)} lines.")

    #for l in reader.lines:
     #   print(f"{l.ref} at {l.startpos} has {len(l.gcs)} gcs")


    
    # count = 0
    # for l in reader.lines:
    #     if l.has_badspace(threshold = 4):
            
    #         print(f"Ref = {l.ref}, line starts at v = {l.startpos}")
    #         count +=1
    # print(f"{count} out of {len(reader.lines)} contain bad spaces")

if __name__ == "__main__":
    main()