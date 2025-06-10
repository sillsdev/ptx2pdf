from xdv import XDViPositionedReader 
import numpy as np
import math
import pandas as pd

itypes = {0: 'h', 1: 'v', 2: 'width', 3: 'glyph', 4: 'space'}
class SpacingOddities(XDViPositionedReader):
    def __init__(self, fname, diffable = False):
        super().__init__(fname, diffable)
        self.lines = np.empty([200, 10, 2]) # numpy array of lines, items, width/type
        self.currline = 0 # index of current line, np array row
        self.currindex = 0 # index of current item in line, np array column
        
    def currpos(self):
        # Returns a tuple of the coordinates of the current position: h,v,w,x,y,z
        curr_pos = (self.h,self.v, self.w,self.x,self.y,self.z)
        return curr_pos

    def parmop(self, opcode, parm, data):
        if opcode <= 142:
            itype = 3
        else:
            itype = 4
        prev_pos = self.currpos()
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
        itype = 4 # FIXME: is this really always a space?
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
        self.lines[self.currline, 2, 1] = abs(prev_pos[0] - self.lines[self.currline, 0, 0])    
        self.currline += 1
        if self.currline >= self.lines.shape[0]:
            nlines, nitems, nwidths = self.lines.shape
            temp_array = np.empty([math.ceil(1.5*nlines), nitems, nwidths])
            self.lines = np.concatenate((self.lines, temp_array))
        self.lines[self.currline,0,0] = 0
        self.lines[self.currline,0,1] = self.h            
        # add starting coordinates of new line
        self.lines[self.currline,1,0] = 1
        self.lines[self.currline, 1, 1] = self.v
        self.currindex = 3
    
    def add_item(self, prev_pos, itype):
        if self.currindex >= self.lines.shape[1]:
            nlines, nitems, nwidths = self.lines.shape
            temp_array = np.empty([nlines, math.ceil(1.5*nitems), nwidths])
            self.lines = np.concatenate((self.lines, temp_array), axis = 1)
        # add item with its type to the line
        self.lines[self.currline, self.currindex, 0] = itype
        self.lines[self.currline, self.currindex, 1] = abs(self.h - prev_pos[0])
        self.currindex += 1
    
    def multiparm(self, opcode, parm, data):
        prev_pos = self.currpos()
        super().multiparm(opcode, parm, data)
        if self.currpos() != prev_pos:
            print("Multiparm changes values")

    def glyph_space_ratio(self, line):
        # line is a row of an array, in itself a 2d array with items along y and type + width along z
        # all widths are positive since we took abs of differences.
        # fixme: there's a bunch of lines with either glyphspace = 0 or space = 0, why?
        glyph = 0
        space = 0
        for itype, width in line:
            match itype:
                case 2:
                    line_width = width
                case 3:
                    glyph += width
                case 4:
                    space += width
        if space == 0:
            return 1
        elif glyph == 0:
            return 0
        ratio = glyph / space
        return ratio 
    
    

    # todo: when it's the time, the output of xxx method in og class gives the book + verse.

    # NEXT: Perform statistics on the lines: ratio, average etc.
    
    # FIXME: is the topt method of positioned reader actually used? Are we measuring in pt now?

    # NOTE: op argument is never lower than 128, so set_char is not called and is not overwritten.
    # NOTE: multiparm does not change positions, so not overwritten.
    # note: xxx method also doesn't change spacing.

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
    #import sys
    #if len(sys.argv) < 3:
     #   print("Don't really know what is happening but it looks cool.")
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    
    pgn = 1
    ratio_stats = []
    while pgn <10:
        for (opcode, data) in reader.parse():
            if reader.pageno > pgn:
                break
            pass
        # calculate glyph/space ratio per line
        ratios = []
        for l in reader.lines:
            ratios.append(reader.glyph_space_ratio(l))
        filt_ratios = [i for i in ratios if i != 0 and i != 1]
        ratios_series = pd.Series(filt_ratios)
        ratio_stats.append(ratios_series.describe())
        pgn +=1
        print(f"Starting to calculate up to page number {pgn} now...")

    ratios_frame = pd.concat(ratio_stats, axis=1)
    ratios_frame.columns = ['1','2','3','4','5','6','7','8','9']
    print(ratios_frame) 
    #with open('stats.txt', 'w') as f:
     #   f.write(ratios_frame.to_string())

if __name__ == "__main__":
    main()