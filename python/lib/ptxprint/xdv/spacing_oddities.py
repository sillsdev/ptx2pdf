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
        self.prev_line = Line(self.v, self.ref, self.curr_font, self.dviratio)
        self.line = Line(self.v, self.ref, self.curr_font, self.dviratio)

    def xglyphs(self, opcode, parm, data):
        start_pos = (self.h, self.v)       
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        glyphs_width = self.topt(width)
        self.update_lines(start_pos)
        pos_points = [[self.topt(n) for n in p] for p in pos]
        # todo: check this conversion, does it work right & should we really convert?
        self.line.add_glyphs(start_pos, glyphs_width, pos_points, glyphs)
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
        self.update_lines((self.h, self.v))
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

    def update_lines(self, startpos):
        if len(self.line.glyph_clusters) == 0:
            # overwrite line if it is empty
            self.line = Line(self.v, self.ref, self.curr_font, self.dviratio)
            self.parent.addxdvline(self.line, self.page_index, self.h, self.v)
            return
        if (self.cursor[1]-startpos[1]) < self.v_line_treshold:
            if (self.cursor[1] - self.line.vstart) < self.v_line_treshold:
                # cursor is at glyph start position and at current line v, or at a verse number of current line
                return
        self.line_collision()
        self.prev_line = self.line
        self.line = Line(startpos[1], self.ref, self.curr_font, self.dviratio)
        self.parent.addxdvline(self.line, self.page_index, self.h, self.v)

    def line_collision(self):
        if self.line.vmin < self.prev_line.vmax:
            self.line.gc_collision(self.prev_line.glyph_clusters)
class Line: 
    def __init__(self, v, ref, font, ratio):
        self.ref = ref
        self.glyph_clusters = [] # list of GlyphCluster objects
        self.vstart = v # v of first glyph
        self.curr_font = font
        self.h_gc_threshold = 1 # space threshold to add glyph to current gc or start new gc
        self.vmin = v
        self.vmax = v
        self.collisions = [] # [xmin, ymin, xmax, ymax] per collision if exists. ymin is top, ymax is bottom.
        self.ratio = ratio

    def change_font(self, h, font):
        self.curr_font = font
        self.glyph_clusters.append(GlyphCluster(h, self.curr_font, self.ratio))
        self.vmin = min(self.vmin, self.glyph_clusters[-1].vmin)
        self.vmax = max(self.vmax, self.glyph_clusters[-1].vmax)

    def add_glyphs(self, startpos, w, pos, g): # in points
        if len(self.glyph_clusters) == 0:
            self.glyph_clusters.append(GlyphCluster(startpos[0], self.curr_font, self.ratio))
        elif startpos[0] - (self.glyph_clusters[-1].hstart + self.glyph_clusters[-1].width) > self.h_gc_threshold:
            # make new gc block only if there is space between glyphs this block and the previous one.
            self.vmin = min(self.vmin, self.glyph_clusters[-1].vmin)
            self.vmax = max(self.vmax, self.glyph_clusters[-1].vmax)
            self.glyph_clusters.append(GlyphCluster(startpos[0], self.curr_font, self.ratio))
        self.glyph_clusters[-1].width += w
        for i in range(len(g)):
            self.glyph_clusters[-1].add_glyph((pos[i][0], startpos[1]), g[i])

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
                width = self.glyph_clusters[i+1].hstart - (self.glyph_clusters[i].hstart + self.glyph_clusters[i].width)
                if width > maxspace:
                    bad_spaces.append([(self.glyph_clusters[i].hstart + self.glyph_clusters[i].width, self.vstart), width, width/fontsize])
        return bad_spaces
    
    def has_collision(self):
        # check collision with glyphclusters
        return self.collisions
    
    def gc_collision(self, prev_gcs):
            i = 0
            j = 0
            while i < len(self.glyph_clusters) and j < len(prev_gcs):
                if self.glyph_clusters[i].vmin <= prev_gcs[j].vmax:
                    # collision on gc level: bottom line gc's vmin is higher on page than top line gc's vmax.
                    glyph_cols = self.glyph_clusters[i].glyph_collision(prev_gcs[j])
                    # todo: find more elegant way to add this.
                    if len(glyph_cols) >0:
                        for c in glyph_cols:
                            self.collisions.append(c)
                if (self.glyph_clusters[i].hstart + self.glyph_clusters[i].width) > (prev_gcs[j].hstart + prev_gcs[j].width):
                    i +=1
                else:
                    j +=1

class GlyphCluster:
    def __init__(self, h, font, ratio):
        # todo: find elegant way to pass ratio, now it needs to be passed often.
        self.hstart = h
        self.font = font 
        self.width = 0
        self.glyphs = [] # list of [hmin, vmin, hmax, vmax] for each glyph. boundary boxes. s
        self.vmin = 0
        self.vmax = 0
        self.ratio = ratio

    def add_glyph(self, pos, g): # pos = (h,v) and g = glyph number
        hmin = pos[0] - self.glyph_topt(g,0)
        vmin = pos[1] - self.glyph_topt(g,3)
        hmax = pos[0] + self.glyph_topt(g,2)
        vmax = pos[1] + self.glyph_topt(g,1)
        self.vmin = min(self.vmin, vmin)
        self.vmax = max(self.vmax, vmax)
        self.glyphs.append([hmin, vmin, hmax, vmax])

    def glyph_topt(self, no, i):
        return (self.font.ttfont.glyphs[no][i] / self.font.ttfont.upem * self.font.points) * self.ratio
    
    def glyph_collision(self, other):
        collisions = []
        i = 0
        j= 0
        while i < len(self.glyphs) and j < len(other.glyphs):
            if self.glyphs[i][1] <= other.glyphs[j][3]:
                # bottom line glyph's vmin is higher on the page than top line glyph's vmax.
                # rectangle drawing takes [xtopleft, ytopleft, width, height]
                xtopleft = max(self.glyphs[i][0], other.glyphs[j][0])
                ytopleft = self.glyphs[i][1] 
                width = min(self.glyphs[i][2], other.glyphs[j][2]) - xtopleft
                height = other.glyphs[j][3] - ytopleft
                collisions.append([xtopleft, ytopleft, width, height])
            if self.glyphs[i][2] < other.glyphs[j][2]:
                i += 1
            else:
                j+=1
        return collisions

def main():
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSG1/local/ptxprint/Default/WSG1_Default_GEN_ptxp.xdv")
    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")    
    #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSGlatin/local/ptxprint/Default/WSGlatin_Default_RUT_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 1:
            break

if __name__ == "__main__":
    main()
