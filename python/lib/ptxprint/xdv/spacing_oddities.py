from ptxprint.xdv.xdv import XDViPositionedReader, Font
from ptxprint.font import TTFont
import math
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.curr_ref = None # reference of where we're at, str
        self.lines = [] # list of Line objects
        self.ctol = 0.005 # the absolut difference tolerated to consider v change a difference 

    def curr_hv(self):
        curr_pos = (self.h,self.v)
        return curr_pos

    def parmop(self, opcode, parm, data):
        # note: parmop never contanis opcode <=142 thus no glyphs 
        prev_pos = self.curr_hv()
        result = super().parmop(opcode, parm, data)
        if not math.isclose(prev_pos[1], self.v, abs_tol =self.ctol):
            self.vchange(prev_pos)
        return result

    def simple(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().simple(opcode, parm, data)
        if not math.isclose(prev_pos[1], self.v, abs_tol =self.ctol):
            self.vchange(prev_pos)
        return result
    
    def push(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().push(opcode, parm, data)
        if not math.isclose(prev_pos[1],self.v, abs_tol =self.ctol):
            self.vchange(prev_pos)
        return result

    def pop(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().pop(opcode, parm, data)
        if not math.isclose(prev_pos[1], self.v, abs_tol =self.ctol):
            self.vchange(prev_pos)
        return result
    
    def bop(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        result = super().bop(opcode, parm, data)
        if not math.isclose(prev_pos[1], self.v, abs_tol =self.ctol):
            self.vchange(prev_pos)
        return result 

    def xglyphs(self, opcode, parm, data):
        prev_pos = self.curr_hv()
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        if not math.isclose(prev_pos[0], self.h, abs_tol =self.ctol): # todo: think about a minimum h difference, min width of glyphs
            glyphs_width = self.topt(width)
            if not math.isclose(self.v, self.lines[-1].v_start, abs_tol = self.ctol):
                print("Glyphs are added at a different v than the line starts at.")
            if len(self.lines) == 0:
                self.lines.append(Line(self.curr_hv(), self.curr_ref)) 
            # glyphs start at prev_pos[0] and have width in points glyphs_width
            self.lines[-1].add_glyphs(prev_pos[0], glyphs_width)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf:dest', txt):
            self.curr_ref = re.findall(r'\((.*?)\)', txt)[0]
        return (txt,)

    def xfontdef(self, opcode, parm, data):
        (k, font) = super().xfontdef(opcode, parm, data)
        # font is an xdv Font object. Has .name (filename) and .points (size)
        # for bad spaces, we only need the size. 
        font_size = self.topt(font.points)
        if len(self.lines) == 0:
            self.lines.append(Line(self.curr_hv(), self.curr_ref))
        self.lines[-1].change_font(self.h, font_size)
        # todo: for line collision, check if k is already in font cache
        # todo: if not, create TTFont as attribute of the xdv-font
        # todo: readfont() and add to font cache
        #font.ttfont = TTFont(None, filename = font.name)
        # question: what does the cache in TTFont class do? Since it is within the class, I thought it was an attribute of font object
        # but it adds properties of the font to it in the __init__, so it contains multiiple fonts?
        return (k, font)

    def vchange(self, prevpos):
        # todo: handle negative v-change
        vdiff = self.v - prevpos[1]

        # todo: find elegant way for this if-maze
        if len(self.lines) == 0:
            self.lines.append(Line(self.curr_hv(), self.curr_ref))
        elif len(self.lines[-1].gcs) == 0:
            # current line has no content, so overwrite it
            self.lines[-1] = Line(self.curr_hv(), self.curr_ref)
        else:
            self.lines.append(Line(self.curr_hv(), self.curr_ref))

        
           # return
        #vdiff = self.v - prevpos[1]
        # a diff larger than -100 represents new page
        #if -70 < vdiff < 0:
         #   self.lines[-1].v_up = vdiff
          #  return
        #elif vdiff == self.lines[-1].v_up:
         #   print("Change equal to move up")
        # either new page or normal line change                   
     
        
class Line: 
    def __init__(self, currpos, ref):
        self.ref = ref
        self.gcs = [] # list of GlyphContent objects, index -1 contains current gc
        self.v_start = currpos[1]
        self.h_start = currpos[0]
        self.v_up =0

    def change_font(self, h, fontsize):
        self.add_gc(h, fontsize)

    def needs_new_gc(self, prev_h):
        if len(self.gcs) == 0:
            return True
        elif prev_h - (self.gcs[-1].h_start + self.gcs[-1].width) >1:
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
        # size of glyph won't change, but the boundary box will.
        # fixme: method incomplete.
        #g_no and g_pos are lists of res. numbers and 2-tuples (h,v)
        glyph = self.font.readfont(withglyphs = True)
        # todo: check max en min x en y, update gc vrange
        self.glyphs.append(glyph)
        #self.starts.append(pos)    

def main():
    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSGlatin/local/ptxprint/Default/WSGlatin_Default_RUT_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 5:
            break  
    count = 0
    for l in reader.lines:
        if l.has_badspace(threshold = 4):
            #print(f"Ref = {l.ref}, line starts at v = {l.v_start}")
            count +=1
    print(f"{count} out of {len(reader.lines)} contain bad spaces")

    consecutive =0
    lines_diff = 0
    min_count =0
    for i in range(0, len(reader.lines) -1):
        if reader.lines[i+1].v_start > reader.lines[i].v_start:
            consecutive +=1
        else:
            l_diff = abs(reader.lines[i+1].v_start - reader.lines[i].v_start)
            if l_diff < 200:
                lines_diff += l_diff
                min_count +=1
    print(f"We have {consecutive} lines that are below the previous line on the page")
    print(f"There are {len(reader.lines)} lines in total")
    print(f"For the lines moving up, the average negative distance is {lines_diff/min_count}, page/column changes excluded")


if __name__ == "__main__":
    main()