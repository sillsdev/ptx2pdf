from ptxprint.xdv.xdv import XDViPositionedReader, Font
from ptxprint.font import TTFont
import math
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.curr_ref = None # reference of where we're at, string
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
            if len(self.lines) == 0:
                self.lines.append(Line(prev_pos[1], self.curr_ref))
            self.lines[-1].add_glyphs(prev_pos[0], glyphs_width)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf:dest', txt):
            self.curr_ref = re.findall(r'\((.*?)\)', txt)[0]
        return (txt,)
        # todo: make into sensible string

    def xfontdef(self, opcode, parm, data):
        (k, font) = super().xfontdef(opcode, parm, data)
        # font is an xdv Font object. Has .name (filename) and .points (size)
        # for bad spaces, we only need the size. 
        font_size = self.topt(font.points)
        if len(self.lines) == 0:
            self.lines.append(Line(self.v, self.curr_ref))
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
        # fixme: find more elegant way to do this.
        if len(self.lines) != 0:
            if len(self.lines[-1].gcs) == 0:
                self.lines[-1] = newline
            else:
                self.lines.append(newline)
        elif len(self.lines) == 0:
            self.lines.append(newline)
class Line: 
    def __init__(self, v, ref):
        self.ref = ref
        self.gcs = [] # list of GlyphContent objects, index -1 contains current gc
        self.v_start = v

    def change_font(self, h, fontsize):
        self.add_gc(h, fontsize)

    def needs_new_gc(self, prev_h):
        if len(self.gcs) == 0:
            return True
        elif abs(prev_h - (self.gcs[-1].h_start + self.gcs[-1].width)) >1:
            return True 
        return False
    
    def add_gc(self, h, fontsize):
        gc = GlyphContent(h, fontsize)
        self.gcs.append(gc)
        # todo: make sure that spaces between gc blocks are in the font of the previous block.

    def add_glyphs(self, prev_h, width): # in points
        # check if there's a space before the glyphs.
        if self.needs_new_gc(prev_h):
            self.add_gc(prev_h, self.gcs[-1].font_size if len(self.gcs)!= 0 else None)
        # if there is no space between current gc and new glyphs: add glyphs to current gc.
        self.gcs[-1].width += width 

    def has_badspace(self):
        # question: should we take lines with only 1 gc into account? 
        # if so, need to save the start and end h of the line (or start h and width) so we can determine space on both ends of gc.            
        if len(self.gcs) > 1:
            for i in range (0, len(self.gcs)-1):
                # question: why are we not getting index out of bound error for len(gcs) == 1 and i = 0? 
                if abs(self.gcs[i+1].h_start - (self.gcs[i].h_start + self.gcs[i].width)) > 6:
                    return True
        return False

class GlyphContent:
    def __init__(self, h, fontsize):
        self.h_start = h
        self.font_size = fontsize # in points
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
        if reader.pageno > 10:
            break
        pass
    count =0
    for l in reader.lines:
        if l.has_badspace():
            print(f"Ref = {l.ref}, amount of gcs = {len(l.gcs)}, line starts at v = {l.v_start}.")
            count +=1

    print(f"{count} out of {len(reader.lines)} contain bad spaces")

if __name__ == "__main__":
    main()

    # question: I see consecutive lines with for example v_start = 1692.16529... and v_start = 1692.16548...
    # But they are registered as separate lines, should this happen? They would be interfering right?
    
