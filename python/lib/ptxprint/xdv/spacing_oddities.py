from ptxprint.xdv.xdv import XDViPositionedReader
from ptxprint.font import TTFont
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, parent = None):
        super().__init__(fname)
        self.ref = None # reference of where we're at, str
        self.cursor = (self.h, self.v) # location of last printed glyph
        self.v_line_treshold = 4 # vdiff of verse numbers and *s, less than line diff
        self.page_index = 0 
        self.pagediff = self.pageno 
        self.parent = parent
        self.curr_font = None # TTFont object
        self.prev_line = Line(self.v, self.ref, self.curr_font)
        self.line = Line(self.v, self.ref, self.curr_font)

    def xglyphs(self, opcode, parm, data):
        start_pos = (self.h, self.v)       
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        glyphs_width = self.topt(width)
        if self.new_line_needed(start_pos):
            self.add_line(start_pos[1])
            #self.parent.addxdvline(self.line, self.page_index, self.h, self.v)
        self.line.add_glyphs(start_pos, glyphs_width, pos, glyphs)
        self.cursor = (self.h, self.v)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf:dest', txt):
            self.ref = re.findall(r'\((.*?)\)', txt)[0]
        return (txt,)
    
    def font(self, opcode, parm, data):
        (k, ) = super().font(opcode, parm, data)
        self.curr_font = self.fonts[k]
        if self.new_line_needed((self.h, self.v)):
            self.add_line(self.v)
            #self.parent.addxdvline(self.line, self.page_index, self.h, self.v)
        else:
            self.line.change_font(self.h, self.curr_font)
        self.cursor = (self.h,self.v)
        return (k,)

    def xfontdef(self, opcode, parm, data):
        (k, font) = super().xfontdef(opcode, parm, data)
        self.fonts[k].ttfont = TTFont(None, filename = font.name)
        self.fonts[k].ttfont.readfont(withglyphs=True)
        return (k, font)

    def bop(self, opcode, parm, data):
        self.page_index += 1
        return super().bop(opcode, parm, data)

    def new_line_needed(self, startpos):
        if len(self.line.glyph_clusters) == 0:
            self.line = Line(startpos[1], self.ref, self.curr_font)
            #self.parent.addxdvline(self.line, self.page_index, self.h, self.v)
            return False
        if (self.cursor[1]-startpos[1]) < self.v_line_treshold:
            if (self.cursor[1] - self.line.vstart) < self.v_line_treshold:
                # cursor is at glyph start position and at current line v, or at a verse number of current line
                return False
        return True 

    def add_line(self, v):
        # check vertical line collision
        if self.prev_line.maxpos[1] > self.line.minpos[1]:
            # check if collision occurs in same horizontal space
            if (max(0, min(self.prev_line.maxpos[2], self.line.minpos[2]) - max(self.prev_line.maxpos[0], self.line.minpos[0]))) >0:
                print(f"Collision detected: {self.prev_line.maxpos[1]} > {self.line.minpos[1]} at ref {self.ref}")
        self.prev_line = self.line
        self.line = Line(v, self.ref, self.curr_font)
class Line: 
    def __init__(self, v, ref, font):
        self.ref = ref
        self.glyph_clusters = [] # list of GlyphCluster objects
        self.vstart = v # v of first glyph
        self.curr_font = font
        self.h_gc_threshold = 1 # space threshold to add glyph to current gc or start new gc
        self.minpos = [0,v,0] # [hmin, vmin, hmax]
        self.maxpos = [0,v,0] # [hmin, vmax, hmax]

    def change_font(self, h, font):
        self.curr_font = font
        self.glyph_clusters.append(GlyphCluster(h, self.curr_font))

    def add_glyphs(self, startpos, w, pos, glyphs): # in points
        if len(self.glyph_clusters) == 0:
            self.glyph_clusters.append(GlyphCluster(startpos[0], self.curr_font))
        elif startpos[0] - (self.glyph_clusters[-1].h_start + self.glyph_clusters[-1].width) > self.h_gc_threshold:
            # make new gc block only if there is space between glyphs this block and the previous one.
            self.glyph_clusters.append(GlyphCluster(startpos[0], self.curr_font))
        self.glyph_clusters[-1].width += w
        for i in range(len(glyphs)-1):
            g_vmin = startpos[1] - ((self.curr_font.ttfont.glyphs[i][3] /self.curr_font.ttfont.upem) * self.curr_font.points)
            g_vmax = startpos[1] + ((self.curr_font.ttfont.glyphs[i][1] /self.curr_font.ttfont.upem) * self.curr_font.points)
            # compare glyph bounds to line bounds and update line values if necessary
            if g_vmin < self.minpos[1]:
                # get hmin and max
                self.minpos[0] = startpos[0] - ((self.curr_font.ttfont.glyphs[i][0]/ self.curr_font.ttfont.upem) * self.curr_font.points)
                self.minpos[1] = g_vmin
                self.minpos[2] = startpos[0] + ((self.curr_font.ttfont.glyphs[i][2] / self.curr_font.ttfont.upem)* self.curr_font.points)
            if g_vmax > self.maxpos[1]:
                self.maxpos[0] = startpos[0] - ((self.curr_font.ttfont.glyphs[i][0]/ self.curr_font.ttfont.upem) * self.curr_font.points)
                self.maxpos[1] = g_vmax
                self.maxpos[2] = startpos[0] + ((self.curr_font.ttfont.glyphs[i][2] / self.curr_font.ttfont.upem)* self.curr_font.points)

    def has_badspace(self, threshold = 4):
        # threshold in ems
        bad_spaces = []
        if len(self.glyph_clusters) > 1:
            fontsize = self.glyph_clusters[0].font.points
            maxspace = fontsize*threshold
            for i in range(0, len(self.glyph_clusters)-1):
                if self.glyph_clusters[i].font.points != fontsize:
                    fontsize = self.glyph_clusters[0].font.points
                    maxspace = fontsize*threshold
                width = self.glyph_clusters[i+1].h_start - (self.glyph_clusters[i].h_start + self.glyph_clusters[i].width)
                if width > maxspace:
                    bad_spaces.append([(self.glyph_clusters[i].h_start + self.glyph_clusters[i].width, self.v_start), width, width/fontsize])
        return bad_spaces

class GlyphCluster:
    def __init__(self, h, font):
        self.h_start = h
        self.font = font # in points
        self.width = 0

    # def add_glyph

def main():
    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/my_judson/local/ptxprint/Default/my_judson_Default_ROM_ptxp.xdv")
    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")    
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSGlatin/local/ptxprint/Default/WSGlatin_Default_RUT_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 1:
            break

if __name__ == "__main__":
    main()