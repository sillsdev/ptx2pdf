from ptxprint.xdv.xdv import XDViPositionedReader
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False, line_callback = None):
        super().__init__(fname, diffable)
        self.curr_ref = None # reference of where we're at, str
        self.lines = [Line(self.v, self.curr_ref, None)] # list of Line objects
        self.cursor = (self.h, self.v) # location of last printed glyph
        self.curr_fontsize = None # in points
        self.v_line_treshold = 4 # vdiff of verse numbers and *s, less than line diff
        self.curr_page_index = 0 
        self.pagediff = self.pageno 
        self.line_callback = line_callback

    def xglyphs(self, opcode, parm, data):
        start_pos = (self.h, self.v)       
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        glyphs_width = self.topt(width)
        if self.new_line_needed(start_pos):
            self.lines.append(Line(start_pos[1],self.curr_ref, self.curr_fontsize))
            self.pass_line(self.x, self.y)
        self.lines[-1].add_glyphs(start_pos[0], glyphs_width)
        self.cursor = (self.h, self.v)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf:dest', txt):
            self.curr_ref = re.findall(r'\((.*?)\)', txt)[0]
        return (txt,)

    def xfontdef(self, opcode, parm, data):
        (k, font) = super().xfontdef(opcode, parm, data)
        self.curr_fontsize = self.topt(font.points)
        if self.new_line_needed((self.h, self.v)):
            self.lines.append(Line(self.v, self.curr_ref, self.curr_fontsize)) 
            self.pass_line(self.x, self.y)
        else:
            self.lines[-1].change_font(self.h, self.curr_fontsize)
        self.cursor = (self.h,self.v)
        return (k, font)

    def new_line_needed(self, startpos):
        if self.pageno > (self.curr_page_index + self.pagediff):
            self.curr_page_index = self.pageno - self.pagediff
        if len(self.lines[-1].glyph_clusters) == 0:
            self.lines[-1] = Line(startpos[1], self.curr_ref, self.curr_fontsize)
            self.pass_line(self.x, self.y)
            return False
        if (self.cursor[1]-startpos[1]) < self.v_line_treshold:
            if (self.cursor[1] - self.lines[-1].v_start) < self.v_line_treshold:
                # cursor is at glyph start position and at current line v, or at a verse number of current line
                return False
        return True          

    def pass_line(self, x, y):
        line_info = {"line" : self.lines[-1],
                    "page_index" : self.curr_page_index,
                    "x" : x,
                    "y" : y}
        if self.line_callback:
            #self.line_callback(line_info)
            print("Works")
        pass

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
            fontsize = self.glyph_clusters[0].font_size
            maxspace = fontsize*threshold
            for i in range(0, len(self.glyph_clusters)-1):
                if self.glyph_clusters[i].font_size != fontsize:
                    fontsize = self.glyph_clusters[0].font_size
                    maxspace = fontsize*threshold
                if (self.glyph_clusters[i+1].h_start - (self.glyph_clusters[i].h_start + self.glyph_clusters[i].width)) > maxspace:
                    return True
        return False

class GlyphCluster:
    def __init__(self, h, fontsize):
        self.h_start = h
        self.font_size = fontsize # in points
        self.width = 0

class line_callback:
    def __init__(self)

def main():
    import sys
    line_function = None
    if sys.argv[2]:
        line_function = "hi"
    reader = SpacingOddities(sys.argv[1], line_function)
    reader.parse() 

    # add option to pass vertical threshold
    # option to pass horizontal threshold
    # option to pass badspacing in ems threshold.

    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    # reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSGlatin/local/ptxprint/Default/WSGlatin_Default_RUT_ptxp.xdv")
    # for (opcode, data) in reader.parse():
    #     if reader.pageno > 5:
    #         break

    # badlines = 0
    # for l in reader.lines:
    #     if l.has_badspace(1):
    #         print(f"Ref {l.ref} at v={l.v_start} contains a badspace.")
    #         badlines += 1
    # print(f"{badlines} out of {len(reader.lines)} lines contain a bad space.")  


if __name__ == "__main__":
    main()