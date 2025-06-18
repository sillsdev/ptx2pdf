from ptxprint.xdv.xdv import XDViPositionedReader, Font
from ptxprint.font import TTFont
import math
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.curr_ref = None # reference of where we're at
        self.lines = [] # list of Line objects 

    def curr_hv(self):
        curr_pos = (self.h,self.v)
        return curr_pos

    def parmop(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().parmop(opcode, parm, data)
        # question: does h change need to be handled here? It cannot be a glyph right? 
        if self.v != prev_pos[1]:
            self.vchange()
        return result

    def simple(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().simple(opcode, parm, data)
        if self.v!= prev_pos[1]:
            self.vchange()
        return result

    def xglyphs(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        if self.h != prev_pos[0]: # todo: think about a minimum h difference, min width of glyphs
            glyphs_width = self.topt(width)
            self.lines[-1].add_glyphs(prev_pos, glyphs_width)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf\: dest', txt):
            self.curr_ref = re.findall(r'\((.*?)\)', txt)
            print(f"reference is now {self.curr_ref}")
        return (txt,)
        # todo: make into sensible string

    def xfontdef(self, opcode, parm, data):
        (k, points, flags) = data
        (k, font) = super().xfontdef(opcode, parm, data)
        # font is an xdv Font object. Has .name (filename) and .points (size)
        # for bad spaces, we only need the size. 
        font_size = self.topt(font.points)
        self.lines[-1].change_font(self.h, font_size)
        # todo: for line collision, check if k is already in font cache
        # todo: if not, create TTFont as attribute of the xdv-font
        # todo: readfont() and add to font cache
        #font.ttfont = TTFont(None, filename = font.name)
        # question: what does the cache in TTFont class do? Since it is within the class, I thought it was an attribute of font object
        # but it adds properties of the font to it in the __init__, so it contains multiiple fonts?
        return (k, font)

    def vchange(self):
        # todo: handle empty lines. should we add gc now or later?
        newline = Line(self.v, self.curr_ref)
        self.lines.append(newline)
class Line: 
    def __init__(self, v, ref):
        self.ref = ref
        self.gcs = [] # list of GlyphContent objects, index -1 contains current gc
        self.v_start = v
        self.prev_glyph_h = 0 # to determine spaces
        print("new line")

    def change_font(self, h, fontsize):
        self.add_gc(h, fontsize)

    def needs_new_gc(self, prev_h, width):
        if self.prev_glyph_h + width + 1 < prev_h + width:
            # this is a space
            return True
        return False
    
    def add_gc(self, h, fontsize):
        gc = GlyphContent(h, fontsize)
        self.gcs.append(gc)
        # todo: make sure that spaces between gc blocks are in the font of the previous block.

    def add_glyphs(self, prevpos, width): # in points
        # check if there's a space before the glyphs.
        if abs(prevpos[0] - self.prev_glyph_h) > 1:
            print(f"Length of gcs is now {len(self.gcs)}")
            if len(self.gcs) !=0:
                self.add_gc(prevpos[0], self.gcs[-1].font_size)
            else:
                self.add_gc(prevpos[0], None)
        self.gcs[-1].width += width 
        self.prev_glyph_h = prevpos[0] + width
        # question: better way to calculate this?

    def has_badspace(self):
        for i in range (0, len(self.gcs)-1):
            if abs(self.gcs[i+1].start_h - (self.gcs[i].start_h + self.gcs[i].width)) > 4:
                return True
        return False

class GlyphContent:
    # todo: just represents black from h to h, or width.
    def __init__(self, h, fontsize):
        self.start_h = h
        self.font_size = fontsize 
        self.width = 0

    def add_glyph(self, g_no, g_pos):
        # note: this method is not in use rn
        # todo: for every glyph, find what x&y cooridnat is relative to start of line, resolve to actual position.
        #todo: need the y of every glyph, for calculating when things change. top of line is ymax + the offset. 
        # size of glyph won't change, but the boundary box will.
        # fixme: method incomplete.
        #g_no and g_pos are lists of res. numbers and 2-tuples (h,v)
        glyph = self.font.readfont(withglyphs = True)
        # can ask 
        # get 
        # todo: check max en min x en y, update gc vrange
        self.glyphs.append(glyph)
        #self.starts.append(pos)    

def main():
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 3:
            break
        pass

if __name__ == "__main__":
    main()