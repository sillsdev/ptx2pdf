from ptxprint.xdv.xdv import XDViPositionedReader
from ptxprint.font import TTFont
import re

def search_collisions(curr, prev, threshold):
    i = 0
    j = 0
    while i < len(curr) and j < len(prev):
        if overlap(curr[i], prev[j], threshold):
            yield i,j
        if curr[i][2] < prev[j][2]:
            i +=1
        else:
            j +=1
    while i < len(curr):
        if overlap(curr[i], prev[j-1], threshold):        
            yield i,j-1
        i +=1
    while j < len(prev):
        if overlap(curr[i-1], prev[j], threshold):
            yield i-1,j
        j +=1

def overlap(curr, prev, t):
    return (curr[0] <= prev[2] and curr[2] >= prev[0] and curr[1] <= prev[3]+t and curr[3] +t >= prev[1])


class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, parent = None, collision_threshold = 0.5, fontsize=10): 
        super().__init__(fname)
        self.ref = ''                 # reference of bible verse
        self.cursor = (self.h, self.v)  # location of last printed glyph
        self.page_index = 0 
        self.pagediff = self.pageno 
        self.parent = parent
        self.curr_font = None           # font object with .ttfont attribute
        self.prev_line = None
        self.line = None
        self.fontsize = fontsize
        self.v_threshold = 0.7*self.fontsize
        self.collision_threshold = collision_threshold
        
        
    def xglyphs(self, opcode, parm, data):
        start_pos = (self.h, self.v) 
        (parm, width, pos, glyphs, txt) = super().xglyphs(opcode, parm, data)
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
        if abs(self.fonts[k].points - self.fontsize) < 1:
            self.curr_font = self.fonts[k] 
        #self.v_threshold = 0.7*self.curr_font.points
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
        self.line = None
        self.prev_line = None
        return super().bop(opcode, parm, data)
    
    def update_lines(self, startpos, rect):
        if  self.line == None:
            self.line = Line(startpos[1], self.ref, self.curr_font, rect)
            return
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
        if self.prev_line != None:
            if not self.prev_line.is_empty():
                self.line.check_line_collisions(self.prev_line, self.collision_threshold)
        self.parent.addxdvline(self.line, self.page_index, self.line.inrect)
        self.prev_line = self.line
        self.line = Line(startpos[1], self.ref, self.curr_font, rect)
    
    def get_rect(self, pos):
        v_rects = self.parent.getyrects(self.page_index, pos[1])
        for r in v_rects:
            if r.xstart <= pos[0] <= r.xend:
                return r
            if abs(pos[0] - r.xstart) < self.curr_font.points and pos[0] <= r.xend:
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
        if not self.gcs_change(startpos[1]):
            self.update_bounds()
            if self.glyph_clusters[-1].hgap_too_big(startpos):
                self.glyph_clusters.append(GlyphCluster(self.vstart, self.curr_font))
        for i in range(len(g)):
            self.glyph_clusters[-1].add_glyph((startpos[0]+pos[i][0], startpos[1]+pos[i][1]), g[i])    

    def add_collision(self, curr, prev):
        # move left top point to left top to get collision in middle of highlight.
        xtopleft = max(curr[0], prev[0]) - 0.2* self.curr_font.points
        ytopleft = min(curr[1], prev[3]) - 0.3 * self.curr_font.points
        width = 0.8*self.curr_font.points
        height = 0.8*self.curr_font.points
        self.collisions.add((xtopleft, ytopleft, width, height))
        # self.collisions.add((curr[0], curr[1], curr[2]-curr[0], curr[3]-curr[1]))       # to highlight both glyph boxes
        # self.collisions.add((prev[0], prev[1], prev[2]-prev[0], prev[3]-prev[1]))        
        
    def check_line_collisions(self, prev_line, threshold):
        if (self.vmin <= prev_line.vmax):
            curr_clusterpos = [c.get_boundary_box() for c in self.glyph_clusters]
            prev_clusterpos = [c.get_boundary_box() for c in prev_line.glyph_clusters]   
            for i,j in search_collisions(curr_clusterpos, prev_clusterpos, threshold):
                for g, p in self.glyph_clusters[i].collision(prev_line.glyph_clusters[j], threshold):
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
    
    def is_empty(self):
        return len(self.glyph_clusters) == 0

class GlyphCluster:
    def __init__(self, v, font):
        self.font = font 
        self.glyphs = []            # list of [hmin, vmin, hmax, vmax] for each glyph. boundary boxes. 
        self.h_threshold = 0.05*font.points  if font != None else 0.001
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
        return (self.font.ttfont.glyphs[no][i] / self.font.ttfont.upem * self.font.points) 
    
    def collision(self, prev_gc, threshold):
        for i,j in search_collisions(self.glyphs, prev_gc.glyphs, threshold):
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
    
class Rivers:
    def __init__(self, max_v_gap = 0.7, min_h = 0.4, minmax_h = 1, total_width = 3):
        self.final_rivers = []
        self.active_rivers = []
        self.max_v_gap = max_v_gap
        self.min_h = min_h
        self.minmax_h = minmax_h
        self.total_width = total_width

    def add_line(self, line):   # check vertical gap and finish river, then add spaces
        spaces_info = self.get_line_spaces(line)   
        if len(spaces_info) == 0:
            return
        if len(self.active_rivers) == 0:
            for space, fontsize in spaces_info:
                self.active_rivers.append(River())   
                self.active_rivers[-1].add(space)
            return
        for river in self.active_rivers.copy():
            if river.vdiff(line.vmin) > self.max_v_gap*line.curr_font.points:
                self.finish_active_river(river, self.minmax_h*line.curr_font.points, self.total_width*line.curr_font.points)
        for space, fontsize in spaces_info:
            space_in_river = False
            for river in self.active_rivers.copy():
                if river.accepts(space, self.max_v_gap*fontsize, self.min_h*fontsize):
                    river.add(space)
                    space_in_river = True
            if not space_in_river:
                self.active_rivers.append(River())   
                self.active_rivers[-1].add(space)
        
    def get_line_spaces(self, line):
        spaces = []
        for i in range(len(line.glyph_clusters)-1):
            gc1_box = line.glyph_clusters[i].get_boundary_box()
            gc2_box = line.glyph_clusters[i+1].get_boundary_box()
            space = [gc1_box[2], line.vmin, gc2_box[0]-gc1_box[2], line.vmax - line.vmin]                              
            if space[2] > self.min_h*line.glyph_clusters[i].font.points:
                spaces.append((space, line.glyph_clusters[i].font.points))
        return spaces
        
    def finish_active_river(self, river, h_threshold, total_threshold): 
        if river.is_valid(h_threshold, total_threshold):
            self.final_rivers.append(river)
        self.active_rivers.remove(river)
        
    def print_all(self):
        for r in self.final_rivers:
            print(r.spaces)
            
    def all_rivers(self):
        return self.final_rivers
class River:
    def __init__(self):
        self.spaces = []
        self.width = 0
        
    def vdiff(self, v):
        if len(self.spaces) <1:
            return 100  # just some big number
        return v - (self.spaces[-1][1]+self.spaces[-1][3]) 
        
    def accepts(self, space, vmaxgap, hminoverlap):
        if len(self.spaces) <1:
            return True
        if (space[1] - (self.spaces[-1][1]+self.spaces[-1][3])) > vmaxgap:
            return False
        h_overlap = min(space[0]+space[2], self.spaces[-1][0]+self.spaces[-1][2]) - max(space[0], self.spaces[-1][0])
        if h_overlap > hminoverlap:
            return True
        return False
    
    def add(self, space):
        if len(self.spaces) >0:
            gap = space[1] - (self.spaces[-1][1]+self.spaces[-1][3])
            if gap >0:
                extended_topspace = [self.spaces[-1][0], self.spaces[-1][1], self.spaces[-1][2], self.spaces[-1][3] + gap/2]
                extended_bottomspace = [space[0], space[1] - gap/2, space[2], space[3] + gap/2]
                self.spaces[-1] = extended_topspace
                self.spaces.append(extended_bottomspace)
        else:
            self.spaces.append(space)
        
    def is_valid(self, h_threshold, total_threshold):
        if len(self.spaces) > 2:
            total_width = sum([s[2] for s in self.spaces])
            if total_width > total_threshold:
                for s in self.spaces:
                    if s[2] > h_threshold:
                        self.width = total_width
                        return True
        return False
    
    def is_empty(self):
        if len(self.spaces) >0:
            return False
        return True
