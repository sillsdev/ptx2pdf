from ptxprint.xdv.xdv import XDViPositionedReader
from ptxprint.font import TTFont
import re

def search_collisions(curr, prev):
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
    def __init__(self, fname, parent = None, line_spacing = 12): #line spacing in points
        super().__init__(fname)
        self.ref = ''                 # reference of where we're at, str
        self.cursor = (self.h, self.v)  # location of last printed glyph
        self.page_index = 0 
        self.pagediff = self.pageno 
        self.parent = parent
        self.curr_font = None           # font object with .ttfont attribute
        self.prev_line = Line(self.v, self.ref, self.curr_font, None)
        self.line = Line(self.v, self.ref, self.curr_font, None)
        self.v_threshold = 0.7* line_spacing
       # self.active_lines = []      # complete lines that have not been compared to the line below them.
        #self.rivers = Rivers()s

    def xglyphs(self, opcode, parm, data):
        start_pos = (self.h, self.v) 
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
        # get rect of pos. if none, could be that glyphs are actually in box? nahh. if none, don't process. 
        curr_rect = self.get_rect(start_pos)
        if curr_rect:
            self.update_lines(start_pos, curr_rect)
            pos_points = [[self.topt(n) for n in p] for p in pos]
            self.line.add_glyphs(start_pos, pos_points, glyphs)
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
        self.v_threshold = 0.7*self.curr_font.points
        curr_rect = self.get_rect((self.h, self.v))
        if curr_rect:
            self.update_lines((self.h, self.v), curr_rect)
            self.line.change_font(self.curr_font)
            self.cursor = (self.h,self.v)
        return (k,)

    def xfontdef(self, opcode, parm, data):
        (k, font) = super().xfontdef(opcode, parm, data)
        if not hasattr(self.fonts[k], 'ttfont'):
            self.fonts[k].ttfont = TTFont(None, filename = font.name)    
            self.fonts[k].ttfont.readfont(withglyphs=True)
        return (k, font)

    def bop(self, opcode, parm, data):
        curr_rect  = self.get_rect((self.h, self.v))
        self.update_lines((self.h,self.v), curr_rect)
        self.cursor = (self.h, self.v)
        self.page_index += 1
       # self.active_lines = []
        return super().bop(opcode, parm, data)
    
    def update_lines(self, startpos, rect):
        if self.line.is_empty():
            self.line = Line(startpos[1], self.ref, self.curr_font, rect)
            return
        if abs(self.cursor[1]-startpos[1]) < self.v_threshold and abs(self.cursor[1]-self.line.vstart) < self.v_threshold :
            # v might be right, but we need to check the h in case of a diglot, since it's printed horizontally
            if rect == self.line.inrect:
                return
        if self.line.glyph_clusters[-1].is_empty():
            self.line.glyph_clusters.pop()
        self.line.update_bounds()
        # iterate over active lines to find the line above curr line.
        # prev_line = None
        # for l in self.active_lines:
        #     if l.inrect.ystart >= self.line.inrect.ystart:
        #         # same rect or l is in rect above self.line
        #         if l.inrect.xstart == self.line.inrect.xstart:
        #             prev_line = l
        #             break
                # if l.inrect == self.line.inrect:
                    # l is at same hpos as current line
                    # prev_line = l
                #     break
                # elif abs(l.glyph_clusters[0].glyphs[0][0] - self.line.glyph_clusters[0].glyphs[0][0]) <= 100:
                #     prev_line = l
                #     break
                # also check h overlap in another way to catch the last line of prev rect with first line of new rect collision
        # if line is found, check collisions.
        # if prev_line:
        #     self.line.check_line_collisions(prev_line)
        #     self.active_lines.remove(prev_line)
        # self.line.mark_starts()
        
        if not self.prev_line.is_empty():
            self.line.check_line_collisions(self.prev_line)
       # self.active_lines.append(self.line)
        self.parent.addxdvline(self.line, self.page_index, self.line.inrect)
        # self.rivers.add_line(self.line)
        self.prev_line = self.line
        self.line = Line(startpos[1], self.ref, self.curr_font, rect)
        
    def get_rect(self, pos):
        v_rects = self.parent.getyrects(self.page_index, pos[1])
        # if len(v_rects) ==1:
        #     return v_rects[0]
        for r in v_rects:
            # assuming rects are ordered and the program prints horizontally left to right:
            # if r.xstart - 0.05 <= pos[0] <= r.xend:
            if pos[0] <= r.xend:
                return r

class Line: 
    def __init__(self, v, ref, font, rect):
        self.ref = ref
        self.vstart = v             # v of first glyph
        self.curr_font = font
        self.vmin = v
        self.vmax = v
        self.glyph_clusters = []    # list of GlyphCluster objects
        self.collisions = set()        # [xmin, ymin, xmax, ymax] per collision if exists. ymin is top, ymax is bottom.
        self.inrect = rect
        
    def gcs_change(self, v):
        if self.is_empty():
            self.glyph_clusters.append(GlyphCluster(v, self.curr_font))
            return True
        if self.glyph_clusters[-1].is_empty():
            self.glyph_clusters[-1] = GlyphCluster(v, self.curr_font)
            return True
        return False
    
    def update_bounds(self):
        self.vmin = min(self.vmin, self.glyph_clusters[-1].vmin)
        self.vmax = max(self.vmax, self.glyph_clusters[-1].vmax)  

    def change_font(self, font):
        self.curr_font = font
        gcs_changed = self.gcs_change(self.vstart) 
        if not gcs_changed:
            self.update_bounds()
            self.glyph_clusters.append(GlyphCluster(self.vstart, self.curr_font))

    def add_glyphs(self, startpos, pos, g): # in points
        gcs_changed = self.gcs_change(startpos[1])
        if not gcs_changed:
            self.update_bounds()
            if self.glyph_clusters[-1].hgap_too_big(startpos):
                self.glyph_clusters.append(GlyphCluster(self.vstart, self.curr_font))
        for i in range(len(g)):
            self.glyph_clusters[-1].add_glyph((startpos[0]+pos[i][0], startpos[1]+pos[i][1]), g[i])    

    def add_collision(self, curr, prev):
        # move left top point to left top to get collision in middle of highlight.
        # xtopleft = max(curr[0], prev[0]) - 0.2* self.curr_font.points
        # ytopleft = min(curr[1], prev[3]) - 0.3 * self.curr_font.points
        # width = 0.8*self.curr_font.points
        # height = 0.8*self.curr_font.points
        # self.collisions.add((xtopleft, ytopleft, width, height))
        self.collisions.add((curr[0], curr[1], curr[2]-curr[0], curr[3]-curr[1]))       # to highlight both glyph boxes
        self.collisions.add((prev[0], prev[1], prev[2]-prev[0], prev[3]-prev[1]))        
        
    def check_line_collisions(self, prev_line):
        if (self.vmin <= prev_line.vmax):
            curr_clusterpos = [c.get_boundary_box() for c in self.glyph_clusters]
            prev_clusterpos = [c.get_boundary_box() for c in prev_line.glyph_clusters]   
            for i,j in search_collisions(curr_clusterpos, prev_clusterpos):
                for g, p in self.glyph_clusters[i].collision(prev_line.glyph_clusters[j]):
                    self.add_collision(g, p)        
            
    def has_badspace(self, threshold = 4):
        # threshold in ems
        bad_spaces = []
        if len(self.glyph_clusters) > 1:
            fontsize = self.glyph_clusters[0].font.points
            maxspace = fontsize*threshold
            for i in range(len(self.glyph_clusters)-1):
                if self.glyph_clusters[i].font.points != fontsize:
                    fontsize = self.glyph_clusters[i].font.points
                    maxspace = fontsize*threshold
                gc_box1 = self.glyph_clusters[i].get_boundary_box()
                gc_box2 = self.glyph_clusters[i+1].get_boundary_box()
                width = abs(gc_box2[0] - gc_box1[2])
                if width > maxspace:
                    bad_spaces.append([(gc_box1[2], self.vstart), width, width/fontsize])
        return bad_spaces        
    
    def has_collisions(self):
        return self.collisions   
    
    def mark_starts(self):  # to mark the start of every line, perform this method instead of check_collisions methods in spacingoddities update_lines
        # box = self.glyph_clusters[0].get_boundary_box()
        # self.collisions.add((box[0], box[1], box[2] - box[0], box[3]-box[1]))
        # box2 = self.glyph_clusters[-1].get_boundary_box()
        # self.collisions.add((box2[0], box2[1], box2[2] - box2[0], box2[3]-box2[1]))
        start_glyph = self.glyph_clusters[0].glyphs[0]
        end_glyph = self.glyph_clusters[-1].glyphs[-1]
        self.collisions.add((start_glyph[0], start_glyph[1], start_glyph[2]-start_glyph[0], start_glyph[3]-start_glyph[1]))
        self.collisions.add((end_glyph[0], end_glyph[1], end_glyph[2]-end_glyph[0], end_glyph[3]-end_glyph[1]))
    
    def is_empty(self):
        return len(self.glyph_clusters) == 0

class GlyphCluster:
    def __init__(self, v, font):
        self.font = font 
        self.glyphs = []            # list of [hmin, vmin, hmax, vmax] for each glyph. boundary boxes. 
        self.h_threshold = 0.05*font.points  # this was 1.
        self.vmin = v
        self.vmax = v
    
    def add_glyph(self, pos, g):    # pos = (h,v) and g = glyph number
        hmin = pos[0] + self.glyph_topt(g,0)
        vmin = pos[1] - self.glyph_topt(g,3)
        hmax = pos[0] + self.glyph_topt(g,2)
        vmax = pos[1] - self.glyph_topt(g,1)
        self.vmin = min(self.vmin, vmin)
        self.vmax = max(self.vmax, vmax)
        self.glyphs.append([hmin, vmin, hmax, vmax])
    
    def glyph_topt(self, no, i):
        a = self.font.ttfont.glyphs[no][i]
        b  = self.font.ttfont.upem
        c = self.font.points
        return (self.font.ttfont.glyphs[no][i] / self.font.ttfont.upem * self.font.points) 
    
    def collision(self, prev_gc):
        for i,j in search_collisions(self.glyphs, prev_gc.glyphs):
            yield self.glyphs[i], prev_gc.glyphs[j]
    
    def get_boundary_box(self):
        if len(self.glyphs) ==0:
            return [0, self.vmin, 0, self.vmax]
        else:
            return [self.glyphs[0][0], self.vmin, self.glyphs[-1][2], self.vmax]
    
    def is_empty(self):
        return len(self.glyphs) == 0
    
    def hgap_too_big(self, startpos):
        if abs(startpos[0] - self.glyphs[-1][2]) > self.h_threshold:
            return True
        return False

# class Rivers:
#     def __init__(self, max_v_gap = 0.8, min_h_overlap = 0.1):
#         self.final_rivers = []
#         self.active_rivers = [River()]
#         self.max_v_gap = max_v_gap
#         self.min_h_overlap = min_h_overlap

#     def add_line(self, line):   # check vertical gap and finish river, then add spaces
#         for river in self.active_rivers:
#             if river.vdiff(line.vmin) > self.max_v_gap*line.curr_font.points:
#                 self.finish_active_river(river)
#         self.check_spaces(line.glyph_clusters)
        
#     def finish_active_river(self, river):  # add river to final_rivers if >3 lines, create new River.
#         if river.is_valid():
#             self.final_rivers.append(river)
#         self.active_rivers.remove(river)
        
#     def check_spaces(self, gcs):    # iterate over space and check river acceptance, add
#         for i in range(len(gcs)-1):
#             gc1_box = gcs[i].get_boundary_box()
#             gc2_box = gcs[i+1].get_boundary_box()
#             space = [gc1_box[2], min(gc1_box[1], gc2_box[1]), abs(gc2_box[0]-gc1_box[2]), abs(max(gc1_box[3], gc2_box[3])- min(gc1_box[1], gc2_box[1]))]
#             if space[2] > self.min_h_overlap*gcs[i].font.points:  # since space between gcs takes the font of the previous gc
#                 acce
#                 for river in self.active_rivers:
#                     if river.accepts(space, self.min_h_overlap*gcs[i].font.points):
#                         river.add(space)
#                         break       # todo: what if a space should be added to multiple active rivers because it's for example a bad space?

#         self.finish_active_river()
# class River:
#     def __init__(self):
#         self.spaces = []
#         self.covered_regions = []
        
#     def vdiff(self, v):
#         if len(self.spaces) <1:
#             return 100
#         return abs(self.spaces[-1][3] - v)
        
#     def accepts(self, space, threshold):
#         if len(self.spaces) <1:
#             return True
#         overlap = abs(min(self.spaces[-1][0] + self.spaces[-1][2], space[0]+space[2]) - max(self.spaces[-1][0], space[0]))
#         if overlap > threshold:
#             return True
#         return False
    
#     def add(self, space):
#         self.spaces.append(space)
#         # todo: updates covered regions
        
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
