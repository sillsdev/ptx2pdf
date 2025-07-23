from ptxprint.xdv.xdv import XDViPositionedReader
from ptxprint.font import TTFont
import re

def search_collisions( curr, prev):
    i = 0
    j = 0
    while i < len(curr) and j < len(prev):
        if overlap(curr[i], prev[j]):
            yield i,j
        if curr[i][2] < prev[j][2]:
            i +=1
        else:
            j +=1
    while i < len(curr):
        if overlap(curr[i], prev[j-1]):
            yield i,j-1
        i +=1
    while j < len(prev):
        if overlap(curr[i-1], prev[j]):
            yield i-1,j
        j +=1

def overlap( curr, prev):
    if curr[0] <= prev[2] and curr[2] >= prev[0] and curr[1] <= prev[3] and curr[3] >= prev[1]:
        return True
    return False  

class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, parent = None): 
        super().__init__(fname)
        self.ref = None                 # reference of where we're at, str
        self.cursor = (self.h, self.v)  # location of last printed glyp
        self.page_index = 0 
        self.pagediff = self.pageno 
        self.parent = parent
        self.curr_font = None           # font object with .ttfont attribute
        self.prev_line = Line(self.v, self.ref, self.curr_font)
        self.line = Line(self.v, self.ref, self.curr_font)

    def xglyphs(self, opcode, parm, data):
        start_pos = (self.h, self.v) 
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        glyphs_width = self.topt(width)
        self.update_lines(start_pos)
        pos_points = [[self.topt(n) for n in p] for p in pos]
        self.line.add_glyphs(start_pos, glyphs_width, pos_points, glyphs)
        self.cursor = (self.h, self.v)
        return (parm, width, pos, glyphs, txt)

    def xxx(self, opcode, parm, data):
        (txt,) = super().xxx(opcode, parm, data)
        if re.search(r'pdf:dest', txt):
            ref = re.findall(r'\((.*?)\)', txt)
            if ref:
                self.ref = ref[0]
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
        if not hasattr(self.fonts[k], 'ttfont'):
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
            return
        if self.line.vgap_below_threshold(self.cursor, startpos):     
            # cursor is at glyph start position and at current line v, or at a verse number of current line
            return
        self.line.update_bounds()
        self.line.check_line_collisions(self.prev_line)
        self.parent.addxdvline(self.line, self.page_index)
        self.prev_line = self.line
        self.line = Line(startpos[1], self.ref, self.curr_font)
class Line: 
    def __init__(self, v, ref, font):
        self.ref = ref
        self.glyph_clusters = []    # list of GlyphCluster objects
        self.vstart = v             # v of first glyph
        self.curr_font = font
        self.vmin = v
        self.vmax = v
        self.collisions = set()        # [xmin, ymin, xmax, ymax] per collision if exists. ymin is top, ymax is bottom.
        if self.curr_font == None:
            self.v_threshold = 4
        else:
            
            self.v_threshold = 0.5 * self.curr_font.points

    def check_line_collisions(self, prev_line):
        if (self.vmin <= prev_line.vmax):
            curr_clusterpos = [c.boundary_box() for c in self.glyph_clusters]
            prev_clusterpos = [c.boundary_box() for c in prev_line.glyph_clusters]   
            for i,j in search_collisions(curr_clusterpos, prev_clusterpos):
                for g, p in self.glyph_clusters[i].collision(prev_line.glyph_clusters[j]):
                    self.add_collision(g, p)

    def change_font(self, h, font):
        self.curr_font = font
        self.update_gcs((h, self.vstart), True)

    def update_bounds(self):
        if self.glyph_clusters[-1].width == 0:
            self.glyph_clusters.pop()
        self.vmin = min(self.vmin, self.glyph_clusters[-1].vmin)
        self.vmax = max(self.vmax, self.glyph_clusters[-1].vmax)
        self.v_threshold = self.vmax- self.vstart
        #print(f"threshold now {self.v_threshold}")
        #self.v_threshold = self.vmax - self.vmin

    def add_glyphs(self, startpos, w, pos, g): # in points
        self.update_gcs(startpos, False)
        self.glyph_clusters[-1].width += w
        for i in range(len(g)):
            self.glyph_clusters[-1].add_glyph((startpos[0]+pos[i][0], startpos[1]+pos[i][1]), g[i])
            
    def update_gcs(self, startpos, font_change):
        if len(self.glyph_clusters) == 0:
            self.glyph_clusters.append(GlyphCluster(startpos, self.curr_font))
            return
        if self.glyph_clusters[-1].is_empty():
            self.glyph_clusters[-1] = GlyphCluster(startpos, self.curr_font)
            return
        if self.glyph_clusters[-1].gap_too_big(startpos) or font_change:
            self.update_bounds()
            self.glyph_clusters.append(GlyphCluster(startpos, self.curr_font))

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

    def add_collision(self, curr, prev):
        xtopleft = max(curr[0], prev[0]) - 0.3* self.curr_font.points
        ytopleft = min(curr[1], prev[3]) - 0.3 * self.curr_font.points
        width = self.curr_font.points
        height = self.curr_font.points
        self.collisions.add((xtopleft, ytopleft, width, height)) 

    def has_collisions(self):
        return self.collisions   
    
    def vgap_below_threshold(self, cursor, startpos):
        return abs(cursor[1]-startpos[1]) < self.v_threshold and abs(cursor[1]-self.vstart) < self.v_threshold

class GlyphCluster:
    def __init__(self, startpos, font):
        self.hstart = startpos[0]
        self.font = font 
        self.width = 0
        self.glyphs = []            # list of [hmin, vmin, hmax, vmax] for each glyph. boundary boxes. 
        self.vmin = startpos[1]
        self.vmax = startpos[1]
        self.h_threshold = 1

    def add_glyph(self, pos, g):    # pos = (h,v) and g = glyph number
        hmin = pos[0] + self.glyph_topt(g,0)
        vmin = pos[1] - self.glyph_topt(g,3)
        hmax = pos[0] + self.glyph_topt(g,2)
        vmax = pos[1] - self.glyph_topt(g,1)
        self.vmin = min(self.vmin, vmin)
        self.vmax = max(self.vmax, vmax)
        self.glyphs.append([hmin, vmin, hmax, vmax])
    
    def glyph_topt(self, no, i):
        return (self.font.ttfont.glyphs[no][i] / self.font.ttfont.upem * self.font.points)
    
    def collision(self, prev_gc):
        for i,j in search_collisions(self.glyphs, prev_gc.glyphs):
            yield self.glyphs[i], prev_gc.glyphs[j]
    
    def boundary_box(self):
        if len(self.glyphs) <1:
            print(f"glyphs: {self.glyphs}")
            print(f"vmin: {self.vmin}, vmax: {self.vmax}, hstart: {self.hstart} width: {self.width}")
        return [self.hstart, self.vmin, self.glyphs[-1][2], self.vmax]
    
    def gap_too_big(self, startpos):
        if startpos[0] -(self.hstart + self.width) > self.h_threshold:
            return True
        return False
    
    def is_empty(self):
        return self.width == 0

# class Rivers:
#     def __init__(self, max_v_gap = 0.8, min_h_overlap = 0.3):
#         self.final_rivers = []
#         self.active_river = River()
#         self.max_v_gap = max_v_gap
#         self.min_h_overlap = min_h_overlap
#         self.last_v = 0

#     def add_line(self, line):   # check vertical gap and finish river, then add spaces
#         if line.vmin - self.last_v > self.max_v_gap * line.curr_font.points:
#             self.finish_active_river()
#         self.check_spaces(line.glyph_clusters)
#         self.last_v = line.vmax
#         pass
    
#     def finish_active_river(self):  # add river to final_rivers if >3 lines, create new River.
#         if self.active_river.is_valid():
#             self.final_rivers.append(self.active_river)
#         self.active_river = River()
#         pass

#     def check_spaces(self, gcs):    # iterate over space and check river acceptance, add
#         for i in range(0, len(gcs)-1):
#             space = (gcs[i].glyphs[-1][2], gcs[i+1].hstart)
#             if space[1]-space[0] > self.min_h_overlap:
#                 if self.active_river.accepts(space, self.min_h_overlap*gcs.font.points):
#                     self.active_river.add(space)
#                     return          # because for now we will only track one river
#         self.finish_active_river()
# class River:
#     def __init__(self):
#         self.spaces = []
#         self.covered_regions = []

#     def accepts(self, space, threshold):
#         if len(self.spaces) <1:
#             return True
#         overlap = min(self.spaces[-1][1], space[1]) - max(self.spaces[-1][0], space[0])
#         if overlap > threshold:
#             return True
#         return False

#     def add(self, space):
#         self.spaces.append(space)
#         # adds space to river
#         # updates covered regions
#         pass

#     def is_valid(self):
#         if len(self.spaces) > 2:
#             return True
#         return False
    
#     def is_empty(self):
#         if len(self.spaces) >0:
#             return False
#         return True

# def main():
#     # CR: You don't want this in here now
#     reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSG1/local/ptxprint/Default/WSG1_Default_GEN_ptxp.xdv")
#     #reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/WSGlatin/local/ptxprint/Default/WSGlatin_Default_RUT_ptxp.xdv")
#     for (opcode, data) in reader.parse():
#         if reader.pageno > 1:
#             break

# if __name__ == "__main__":
#     main()
