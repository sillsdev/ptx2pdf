from xdv import XDViPositionedReader 
import numpy as np

itypes = {0: 'h', 1: 'v', 2: 'width', 3: 'glyph', 4: 'space'}
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.lines = np.empty([205,30, 2]) # numpy array of lines 
        self.currline = 0 # index of current line, np array row
        self.currindex = 0 # index of current item in line, np array column
        
    def currpos(self):
        # Returns a tuple of the coordinates of the current position: h,v,w,x,y,z
        curr_pos = (self.h,self.v, self.w,self.x,self.y,self.z)
        return curr_pos

    def parmop(self, opcode, parm, data):
        prev_pos = self.currpos()
        itype = 5 #FIXME: find out what this is: space or glyph? and assign right itype
        super().parmop(opcode, parm, data)

        # value change of h indicates new glyph / space
        if self.h != prev_pos[0]:
            # add the width of item to current line
            self.add_item(prev_pos, itype)
            
        # value change of v indicates a new line
        if self.v != prev_pos[1]:            
            # add new line 
            self.add_line(prev_pos)
            # FIXME: this operates on self now, but it modifies the line array. 
            # should i make a class for the line array and call the methods on the object itself?

    def simple(self, opcode, parm, data):
        prev_pos = self.currpos()
        itype = 4 # FIXME: is this really always a space?s
        super().simple(opcode, parm, data)
        if self.h != prev_pos[0]:
            self.add_item(prev_pos, itype)
        if self.v  != prev_pos[1]:
            self.add_line(prev_pos)

    def xglyphs(self, opcode, parm, data):
        prev_pos = self.currpos()
        itype = 3     # glyph
        super().xglyphs(opcode, parm, data)
        if self.h != prev_pos[0]:
            self.add_item(prev_pos, itype)      

    # FIXME: define this method in the line array class, if i make one.
    def add_line(self, prev_pos):
        # add the width of the previous line in position 2
        self.lines[self.currline, 2, 0] = 2
        self.lines[self.currline, 2, 1] = prev_pos[0] - self.lines[self.currline, 0, 0]
        
        self.currline += 1
        try:
            self.lines[self.currline,0,0] = 0
            self.lines[self.currline,0,1] = self.h
        except IndexError:
            #TODO: resize array here, more rows needed
            print("more rows needed ")
        # add starting coordinates of new line
        self.lines[self.currline,1,0] = 1
        self.lines[self.currline, 1, 1] = self.v
        self.currindex = 3
    
    def add_item(self, prev_pos, itype):
        if self.currline >= self.lines.shape[0]:
            print("array too small, more columns needed.")
            # TODO: resize array
        # add item with its type to the line
        self.lines[self.currline, self.currindex, 0] = itype
        self.lines[self.currline, self.currindex, 1] = self.h - prev_pos[0]
        self.currindex += 1

    # TODO: check if xxx changes position in any way
    # TODO: check what changes when multiparm is used.
    # TODO: add set_char, since this changes h with the width of the glyph printed. (not called??)

    # FIXME: is the topt method of positioned reader actually used? Are we measuring in pt now?

class Spaces:
    def __init__(self, x, y, z):

       
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
   # for l in reader.lines:
    #    print(l)
    #print(reader.lines.shape)
    #print(reader.lines[25, 0, 1])
    #print(reader.lines[25, 1, 0])

if __name__ == "__main__":
    main()
    
   
