from ptxprint.xdv.xdv import XDViPositionedReader
from ptxprint.font import TTFont
import re
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, parent = None):
        super().__init__(fname)
        self.ref = None # reference of where we're at, str
        self.cursor = (self.h, self.v) # location of last printed glyph
        self.v_line_threshold = 4 # vdiff of verse numbers and *s, less than line diff
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
        #print(f"{{\"name\": \"Xlgyphs run\", \"coords\": [{start_pos[0]}, {start_pos[1]}, {self.h}, {self.v}]}},")
        self.update_lines(start_pos)
        # pos need to be converted to points!
        pos_points = [[self.topt(n) for n in p] for p in pos]
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
        self.v_line_threshold = self.curr_font.points * 0.3
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
            self.line = Line(self.v, self.ref, self.curr_font)
            self.parent.addxdvline(self.line, self.page_index, startpos[0], startpos[1])
            return
        if abs(self.cursor[1]-startpos[1]) < self.v_line_threshold:
            if abs(self.cursor[1] - self.line.vstart) < self.v_line_threshold:
                # cursor is at glyph start position and at current line v, or at a verse number of current line
                return
        self.line.update_bounds()
        self.line_collision()
        self.bounds_checking()
        #print(f"{{\"name\": \"line\", \"coords\": [{self.line.glyph_clusters[0].hstart}, {self.line.vmin}, {self.line.glyph_clusters[-1].hstart + self.line.glyph_clusters[-1].width}, {self.line.vmax}]}},")
        #for gc in self.line.glyph_clusters:
       #                 print(f"{{\"name\": \"gc\", \"coords\": [{gc.hstart}, {gc.vmin}, {gc.hstart + gc.width}, {gc.vmax}]}},")
        self.prev_line = self.line
        self.line = Line(startpos[1], self.ref, self.curr_font)
        self.parent.addxdvline(self.line, self.page_index, startpos[0], startpos[1])

    def line_collision(self):
        # todo: think about whether a collision can happen with lines before the previous line.
        if (self.line.vmin <= self.prev_line.vmax) :
            self.line.gc_collision(self.prev_line.glyph_clusters)
            
    def bounds_checking(self):
        if (self.line.vmin < self.prev_line.vmax):
            self.line.check_bounds(self.prev_line.glyph_clusters, self.prev_line.vmax)
class Line: 
    def __init__(self, v, ref, font):
        self.ref = ref
        self.glyph_clusters = [] # list of GlyphCluster objects
        self.vstart = v # v of first glyph
        self.curr_font = font
        self.h_gc_threshold = 1 # space threshold to add glyph to current gc or start new gc
        self.vmin = v
        self.vmax = v
        self.collisions = [] # [xmin, ymin, xmax, ymax] per collision if exists. ymin is top, ymax is bottom.

    def change_font(self, h, font):
        self.curr_font = font
        if len(self.glyph_clusters) >0:
            self.update_bounds()
        self.glyph_clusters.append(GlyphCluster((h, self.vstart), self.curr_font))

    def update_bounds(self):
        self.vmin = min(self.vmin, self.glyph_clusters[-1].vmin)
        self.vmax = max(self.vmax, self.glyph_clusters[-1].vmax)

    def add_glyphs(self, startpos, w, pos, g): # in points
        if len(self.glyph_clusters) == 0:
            self.glyph_clusters.append(GlyphCluster(startpos, self.curr_font))
        elif startpos[0] - (self.glyph_clusters[-1].hstart + self.glyph_clusters[-1].width) > self.h_gc_threshold:
            # make new gc block only if there is space between glyphs this block and the previous one.
            self.update_bounds()
            self.glyph_clusters.append(GlyphCluster(startpos, self.curr_font))
        self.glyph_clusters[-1].width += w
        for i in range(len(g)):
            self.glyph_clusters[-1].add_glyph((startpos[0] +pos[i][0], startpos[1]+pos[i][1]), g[i])
            #self.glyph_clusters[-1].add_glyph((startpos[0], startpos[1]), g[i])

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

    def gc_collision(self, prev_gcs):            
        for gc in self.glyph_clusters:
            i = 0
            while i < len(prev_gcs):
                c = [gc.hstart, gc.vmin, gc.glyphs[-1][2], gc.vmax]
                p = [prev_gcs[i].hstart, prev_gcs[i].vmin, prev_gcs[i].glyphs[-1][2], prev_gcs[i].vmax]
                if c[0] <= p[2] and c[2] >= p[0] and c[1] <= p[3] and c[3] >= p[1]:
                    glyph_cols = gc.glyph_collision(prev_gcs[i])
                    if len(glyph_cols) > 0:
                        for c in glyph_cols:
                            self.collisions.append(c)
                i +=1
        new = []
        for val in self.collisions:
            if val not in new:
                new.append(val)
        self.collisions = new

    def check_bounds(self, prev_gcs, prev_vmax):
        for gc in self.glyph_clusters:
            i = 0
            while i < len(prev_gcs):
                if gc.vmin <= prev_vmax or prev_gcs[i].vmax >= self.vmin:
                    glyph_cols = gc.crossing_line_bounds(prev_gcs[i], self.vmin, prev_vmax)
                    if len(glyph_cols) > 0:
                        for c in glyph_cols:
                            self.collisions.append(c)
                i +=1
        new = []
        for val in self.collisions:
            if val not in new:
                new.append(val)
        self.collisions = new
        

    def has_collisions(self):
        return self.collisions                

class GlyphCluster:
    def __init__(self, startpos, font):
        # todo: find elegant way to pass ratio, now it needs to be passed often.
        self.hstart = startpos[0]
        self.font = font 
        self.width = 0
        self.glyphs = [] # list of [hmin, vmin, hmax, vmax] for each glyph. boundary boxes. s
        self.vmin = startpos[1]
        self.vmax = startpos[1]

    def add_glyph(self, pos, g): # pos = (h,v) and g = glyph number
        hmin = pos[0] + self.glyph_topt(g,0)
        vmin = pos[1] - self.glyph_topt(g,3)
        hmax = pos[0] + self.glyph_topt(g,2)
        vmax = pos[1] - self.glyph_topt(g,1)
        #print(f"{{\"name\": \"glyph\", \"coords\": [{hmin}, {vmin}, {hmax}, {vmax}]}},")
        self.vmin = min(self.vmin, vmin)
        self.vmax = max(self.vmax, vmax)
        self.glyphs.append([hmin, vmin, hmax, vmax])

    def glyph_topt(self, no, i):
        a = self.font.ttfont.glyphs[no][i]
        b = self.font.ttfont.upem
        c = self.font.points
        return (self.font.ttfont.glyphs[no][i] / self.font.ttfont.upem * self.font.points)

    def glyph_collision(self, other):
        collisions = []
        for c in self.glyphs:
            i=0
            while i < len(other.glyphs):
                p = other.glyphs[i]
                if c[0] <= p[2] and c[2] >= p[0] and c[1] <= p[3] and c[3] >= p[1]:
                    # rectangle drawing takes [xtopleft, ytopleft, width, height]
                    xtopleft = max(c[0], p[0]) 
                    ytopleft = min(c[1], p[3]) 
                    width = 10
                    height = 10
                    collisions.append([[xtopleft, ytopleft, width, height], (1.0,0,0.2,0.5)])
                    # xtopleft = min(c[0], p[0])
                    # ytopleft = min(c[1], p[1])
                    # width = max(c[2], p[2]) - xtopleft 
                    # height = max(c[3],p[3]) - ytopleft
                    # collisions.append([xtopleft, ytopleft, width, height])
                i +=1
        return collisions
    
    def crossing_line_bounds(self, other, bottomvmin, topvmax):
        collisions = []
        for c in self.glyphs:
            if c[1] < topvmax:
                collisions.append([[c[0], c[1], c[2]-c[0], c[3]-c[1]], (4,0,4,0.5)])
        for p in other.glyphs:
            if p[3] > bottomvmin:
                collisions.append([[p[0], p[1], p[2]-p[0], p[3]-p[1]], (180,150, 0, 0.5)])
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
