from ptxprint.xdv.xdv import XDViPositionedReader
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, parent = None):
        super().__init__(fname)
        self.ref = None # reference of where we're at, str
        self.cursor = (self.h, self.v) # location of last printed glyph
        self.fontsize = None # in points
        self.v_line_treshold = 4 # vdiff of verse numbers and *s, less than line diff
        self.page_index = 0 
        self.pagediff = self.pageno 
        self.parent = parent
        self.prev_line = None
        self.line = Line(self.v, self.ref, self.fontsize)

    def xglyphs(self, opcode, parm, data):
        start_pos = (self.h, self.v)       
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        glyphs_width = self.topt(width)
        if self.new_line_needed(start_pos):
            self.prev_line = self.line
            self.line = Line(start_pos[1], self.ref, self.fontsize)
            self.parent.addxdvline(self.line, self.page_index, self.h, self.v)
        self.line.add_glyphs(start_pos[0], glyphs_width)
        self.cursor = (self.h, self.v)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf:dest', txt):
            self.ref = re.findall(r'\((.*?)\)', txt)[0]
        return (txt,)

    def xfontdef(self, opcode, parm, data):
        (k, font) = super().xfontdef(opcode, parm, data)
        self.fontsize = font.points
        if self.new_line_needed((self.h, self.v)):
            self.prev_line = self.line
            self.line = Line(self.v, self.ref, self.fontsize)
            self.parent.addxdvline(self.line, self.page_index, self.h, self.v)
        else:
            self.line.change_font(self.h, self.fontsize)
        self.cursor = (self.h,self.v)
        return (k, font)

    def bop(self, opcode, parm, data):
        self.page_index += 1
        return super().bop(opcode, parm, data)

    def new_line_needed(self, startpos):
        if len(self.line.glyph_clusters) == 0:
            self.line = Line(startpos[1], self.ref, self.fontsize)
            self.parent.addxdvline(self.line, self.page_index, self.h, self.v)
            return False
        if (self.cursor[1]-startpos[1]) < self.v_line_treshold:
            if (self.cursor[1] - self.line.v_start) < self.v_line_treshold:
                # cursor is at glyph start position and at current line v, or at a verse number of current line
                return False
        return True          

class Line: 
    def __init__(self, v, ref, fontsize):
        self.ref = ref
        self.glyph_clusters = [] # list of GlyphCluster objects
        self.v_start = v # v of first glyph
        self.curr_fontsize = fontsize
        self.h_gc_threshold = 1 # space threshold to add glyph to current gc or start new gc

    def change_font(self, h, fontsize):
        self.curr_fontsize = fontsize
        self.glyph_clusters.append(GlyphCluster(h, self.curr_fontsize))

    def add_glyphs(self, starth, w): # in points
        if len(self.glyph_clusters) == 0:
            self.glyph_clusters.append(GlyphCluster(starth, self.curr_fontsize))
        elif starth - (self.glyph_clusters[-1].h_start + self.glyph_clusters[-1].width) > self.h_gc_threshold:
            # make new gc block if there is space between glyphs this block and the previous one.
            self.glyph_clusters.append(GlyphCluster(starth, self.curr_fontsize))
        self.glyph_clusters[-1].width += w

    def has_badspace(self, threshold = 4):
        # threshold in ems
        if len(self.glyph_clusters) > 1:
            bad_spaces = []
            fontsize = self.glyph_clusters[0].font_size
            maxspace = fontsize*threshold
            for i in range(0, len(self.glyph_clusters)-1):
                if self.glyph_clusters[i].font_size != fontsize:
                    fontsize = self.glyph_clusters[0].font_size
                    maxspace = fontsize*threshold
                if (self.glyph_clusters[i+1].h_start - (self.glyph_clusters[i].h_start + self.glyph_clusters[i].width)) > maxspace:
                    bad_spaces.append([(self.glyph_clusters[i].h_start + self.glyph_clusters[i].width, self.v_start), self.glyph_clusters[i+1].h_start - (self.glyph_clusters[i].h_start + self.glyph_clusters[i].width)])
            if bad_spaces:
                return bad_spaces
        return None 

class GlyphCluster:
    def __init__(self, h, fontsize):
        self.h_start = h
        self.font_size = fontsize # in points
        self.width = 0

def main():
    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSGlatin/local/ptxprint/Default/WSGlatin_Default_RUT_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 5:
            break

if __name__ == "__main__":
    main()
