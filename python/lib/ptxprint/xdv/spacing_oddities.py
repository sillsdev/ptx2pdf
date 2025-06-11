from xdv import XDViPositionedReader 
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

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
        #print(f"Start of parmop method: pos are {self.currpos()}")
        if opcode <= 142:
            itype = 3
        else:
            itype = 4
            #print("Parmop enters a space now.")
        prev_pos = self.currpos()
        super().parmop(opcode, parm, data)   
        # value change of v indicates a new line
        if self.v != prev_pos[1]: 
            print(f"PARMOP: We add line, v went from {prev_pos[1]} to {self.v}")        
            # add new line 
            self.add_line(prev_pos)
            # FIXME: this operates on self now, but it modifies the line array. 
            # should i make a class for the line array and call the methods on the object itself?
        # value change of h indicates new glyph / space
        if self.h != prev_pos[0]:
            print(f"PARMOP: We add item, h went from {prev_pos[0]} to {self.h}")
            if self.h < prev_pos[0]:
                print("Weird, now h is lower than before so moved back to beginning?")
                print(f"This happened at index {self.currline}")
                print(f"With opcode {opcode}, parm {parm} and data {data}")
            # add the width of item to current line
            self.add_item(prev_pos, itype)
        #print(f"End of parmop method: pos are {self.currpos()}")

    def simple(self, opcode, parm, data):
        #print(f"Start of simple method: pos are {self.currpos()}")
        prev_pos = self.currpos()
        itype = 4 # FIXME: is this really always a space?
        #print("Simple will add a space now.")
        super().simple(opcode, parm, data)
        if self.v  != prev_pos[1]:
            print(f"SIMPLE: We add line, v went from {prev_pos[1]} to {self.v}")
            self.add_line(prev_pos)
        if self.h != prev_pos[0]:
            print(f"SIMPLE: We add item, h went from {prev_pos[0]} to {self.h}")
            self.add_item(prev_pos, itype)
        #print(f"End of simple method: pos are {self.currpos()}")

    def xglyphs(self, opcode, parm, data):
        #print(f"Start of xglyphs method, pos are {self.currpos()}")
        prev_pos = self.currpos()
        itype = 3     # glyph
        super().xglyphs(opcode, parm, data)
        if self.h != prev_pos[0]:
            print(f"XGLYPHS: We add item, h went from {prev_pos[0]} to {self.h}")
            self.add_item(prev_pos, itype)  
        #print(f"End of xglyphs method, pos are {self.currpos()}")    

    def add_line(self, prev_pos):
        # fixme: this is not a foolproof method since np empty initializes with random values
        # Check if previous line is empty, otherwise re-use space.
        if self.currindex == 3:
            self.lines[self.currline, 2, 0] = 2
            self.lines[self.currline, 2, 1] = abs(prev_pos[0] - self.lines[self.currline, 0, 0])    
            self.currline += 1
        # resize array if out of bounds
        if self.currline >= self.lines.shape[0]:
            nlines, nitems, nwidths = self.lines.shape
            temp_array = np.empty([math.ceil(1.5*nlines), nitems, nwidths])
            self.lines = np.concatenate((self.lines, temp_array))            
        # add starting v of new line
        self.lines[self.currline,1,0] = 1
        self.lines[self.currline, 1, 1] = self.v
        self.currindex = 3
    
    def add_item(self, prev_pos, itype):
        # If first item in line, save starting h of line.
        if self.currindex == 3:
            self.lines[self.currline, 0, 0] = 0
            self.lines[self.currline, 0, 1] = prev_pos[0]
        # resize array if out of bounds
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
    
    def get_spaces(self, line):
        spaces = 0
        count = 0
        width = line[2,1]
        for itype, width in line:
            if itype == 4:
                spaces += width
                count +=1

        return spaces, count, width
    
    
    # todo: extract the glyphs and get stats on htem.s

    # todo: when it's the time, the output of xxx method in og class gives the book + verse.
    # todo: flag any lines that touch each other. for this, font is necessary cuz need glyph boxes.
    # todo: check if need class for a line instead of what im doing now. 

    # NEXT: Perform statistics on the lines: ratio, average etc.

    # next: relate the lines that we now have to the blocks in ptxprint. Plug the code inn ptxprint and start colouring
    # write own routine that colours overlays over the text. Also fix some report with things like 
    # look at x in these references. 
    
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
    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        if reader.pageno > 10:
            break
        pass
    space_lines = []
    for l in reader.lines:
        s,c,w = reader.get_spaces(l)
        space_lines.append([s,c,w])
    space_df = pd.DataFrame(space_lines, columns = ['Space width', 'Space count', 'Line width'])
    #space_filt = [space_df['Line width']==0]
    #space_filt2 = space_filt[space_filt['Space width']==0]
    print(space_df.describe())


def chill():
    #import sys
    #if len(sys.argv) < 3:
        #   print("Don't really know what this comment is for.")

    reader = SpacingOddities("C:/Users/jedid//Documents/VSC_projects/ptx2pdf/test/projects/OGNT/local/ptxprint/Default/OGNT_Default_JHN_ptxp.xdv")
    for (opcode, data) in reader.parse():
        # if reader.pageno > 10:
        #    break
        pass

    # Calculate the glyph/space ratio per line
    g_s_ratios = []
    for l in reader.lines:
        g_s_ratios.append(reader.glyph_space_ratio(l))
    # filter out the 1 and 0 ratios.
    filt_ratios = [i for i in g_s_ratios if i != 0 and i != 1]
    ratios_series = pd.Series(filt_ratios)
    ratio_str = ratios_series.describe()
    print(ratio_str) 

    # Calculate the amount of space per line
    space_lines = []
    # todo: kind of copy the np array with lines, but only keep the spaces. 
    # so that we can calculate statistics on amounts of spaces, and sizes of spaces. 
    #line_sr = pd.DataFrame(reader.lines)
    #sprint(line_sr.describe())
    for l in reader.lines:
        s,c,w = reader.get_spaces(l)
        space_lines.append([s,c,w])
    space_df = pd.DataFrame(space_lines, columns = ['Space width', 'Space count', 'Line width'])
    space_filt = [space_df['Line width']==0]
    #space_filt2 = space_filt[space_filt['Space width']==0]
    print(space_filt.describe())


            



if __name__ == "__main__":
    main()