

from xdv import XDViPositionedReader 
import numpy as np

class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.lines = np.empty([205,15]) # numpy array of lines 
        self.currline = 0 # index of current line
        self.currindex = 0 # index of current item in line
        

    def currpos(self):
        # Returns a tuple of the coordinates of the current position: h,v,w,x,y,z
        curr_pos = (self.h,self.v, self.w,self.x,self.y,self.z)
        return curr_pos
    
    def parmop(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().parmop(opcode, parm, data)

        # value change of h indicates new glyph / space
        if self.h != prev_pos[0]:
            # add the width of item to current line
            self.add_item(prev_pos)
            
        # value change of v indicates a new line
        if self.v != prev_pos[1]:
            # save the width of the previous line
            self.lines[self.currline, 2] = prev_pos[0] - self.lines[self.currline, 0]
            
            # add new line with starting positions
            self.add_line()

        
    def simple(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().simple(opcode, parm, data)
        # value change of h indicates new glyph / space
        if self.h != prev_pos[0]:
            # add the width of item to current line
            self.add_item(prev_pos)
        if self.v  != prev_pos[1]:
            self.lines[self.currline, 2] = prev_pos[0] - self.lines[self.currline, 0] # width of line
            # add new line
            self.add_line()

    # TODO: check what push does with v since it includes positions
    
    # TODO: check what pop does with v since it includes positions
    
    # TODO: check what bop does with positions 

    # FIXME: is the topt method of positioned reader actually used?

    def add_line(self):
        self.currline += 1
        self.lines[self.currline,0] = self.h
        self.lines[self.currline,1] = self.v
        self.currindex = 3
        # FIXME: handle size problems of np array, resize if necessary.
    
    def add_item(self, prev_pos):
        # add width of item at current position
        self.lines[self.currline, self.currindex] = self.h - prev_pos[0]
        self.currindex += 1
        # FIXME: handle outofbound error of np array, resize if necessary.



     
class Line:
    # not in use atm.
    def __init__(self, startpos):
        self.startpos = startpos
        self.book = str()
        self.chapter = str()
        self.verse = str()
        self.glyphs = 0
        self.endpos = 0
        self.ratio = 0
        self.width = 0


def main():
   # import sys
    #if len(sys.argv) < 3:
     #   print("Don't really know what is happening but it looks cool.")
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno>2:
            break
        pass
    # if pageno gets to x, stop. to avoid overload haha.
    #for l in reader.lines:
     #   print(l)
    

if __name__ == "__main__":
    main()
    
   
