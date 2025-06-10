

from xdv import XDViPositionedReader 
import numpy as np

class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.lines = [[]] # numpy array of lines 
        self.currline = 0 # index of current line
        

    def currpos(self):
        # Returns a tuple of the coordinates of the current position: h,v,w,x,y,z
        curr_pos = (self.h,self.v, self.w,self.x,self.y,self.z)
        return curr_pos
    
    def parmop(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().parmop(opcode, parm, data)
        # value change of v indicites a new line
        if self.v != prev_pos[1]:
            # save the end position of the previous line
            self.lines[self.currline].append(prev_pos)
            # add new line
            self.add_line(self.currpos())

        
    def simple(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().simple(opcode, parm, data)
        if self.v  != prev_pos[1]:
            # save endpos of previous line
            self.lines[self.currline].append(prev_pos)
            # add new line
            self.add_line(self.currpos())

    # TODO check what push does with v since it includes positions
    
    # TODO check what pop does with v since it includes positions
    
    # TODO check what bop does with psitions 

    def add_line(self, startpos):
        self.lines.append([startpos])
        self.currline = len(self.lines) - 1
        # TODO: handle size problems of np array, resize if necessary.



     
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
    for l in reader.lines:
        print(l)
    print(f"Dimensions of array are {len(reader.lines)}")
    print(f"coordinate is a {type(reader.v)}")
    

if __name__ == "__main__":
    main()
    
   
