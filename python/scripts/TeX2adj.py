# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:41:20 2020

@author: jakem
"""
import re, argparse

class Document:
    def __init__(self, logfile):
        self.paragraphs = []
        self.pages = []
        self.logfile = logfile # give it a file object
        self.resetstates()
        self.mode = "paragraph"
        self.pageinfo = ""
        regexps = [r"BALANCE pagebuild: cols=(\d+): textheight=#pt",
        r"BALANCE pageout: cols=(\d+): texta=#pt, #pt: textb=#pt, #pt: partial=#pt, #pt: topins=#pt\+#pt, #pt\+#pt, #pt\+#pt: bottomins=#pt\+#pt, #pt\+#pt, #pt\+#pt",
        r"BALANCE pageouttxt: notes=#pt, #pt",
        r"\[(\d*)\]"]
        self.pageparsers = [re.compile(regexp.replace("#", "([\d\.]+)")) for regexp in regexps] # used # for digits and dots 
        
    def resetstates(self):
        self.state = 0
        self.chunkstarted = False
        self.parfound = False
        self.skip = False
    
    def processpar(self, par):
        self.paragraphs.append(par)
        self.resetstates()
    
    def processpage(self, pag):
        if self.pageinfo != "":
            for pageparser in self.pageparsers:
                pag.vals.append(pageparser.search(self.pageinfo))
            #pag.pageinfo = self.pageinfo
            self.pages.append(pag)
            self.pageinfo = ""
            self.mode = "paragraph"
        
    def logparser(self, stretchcoeff):
        """"filepath: location of log file
        outpath: destination file name (will be appended to)
        stretchcoeff: maximum ratio between stretching option and optimum number of lines  """
        reffinder = re.compile("^BALANCE paradj: ref=(\w{3})(\d*).([\d-]*): para=(\d*)")
        optionparser = re.compile(r"@@\d*: line (\d*)\.(\d-?) t=(\d*)")
        self.resetstates()
        def parseref(line):
            possibleref = reffinder.match(line).groups()
            if possibleref[3] == "1":
                possiblerefgood = True
            else:
                possiblerefgood = False
            return possibleref, possiblerefgood
        self.pageinfo = ""   
        pag = Page()
        for line in self.logfile:
            if self.state == -1: # chunk finishing time
                self.processpar(par)
            if not self.chunkstarted:
                if line.startswith("BALANCE par"):
                    self.processpage(pag)
                    pag = Page()
                    reff = parseref(line)
                    par = Paragraph()
                    self.chunkstarted = True
                    par.ref, par.goodref = reff
                elif line.startswith("BALANCE page") or self.mode == "page":
                    self.pageinfo += line
                    if line.endswith("]\n"):
                        self.processpage(pag)
                        pag=Page()
                    else:
                        self.mode = "page"
                continue
            if self.state == 0: # looking for firstpass
                if line == "@firstpass\n":
                    self.state = 1
                elif not par.goodref:
                    if line.startswith("BALANCE par"):
                        par.ref, par.goodref = parseref(line)
            elif line == "\n" or line == ")\n": # Chunk can be sent off for processing
                self.state = -1
            elif self.state == 1: # we're looking for paragraphing info
                if line == "@secondpass\n" or line == "@emergencypass\n": # if we find a later pass, we can ditch what we've got so far
                    par.lines = []
                    self.parfound = False
                    self.skip = False
                    #par.minlines = None
                else:
                    if self.parfound: # Reached paragraph breaking bit
                        if not self.skip and line.startswith("@@") : # We're interested
                            ops = optionparser.match(line)
                            currentlines, currentdemerits = int(ops.group(1)), int(ops.group(3))
                            if par.lines == []: # We haven't found anything yet
                                par.deflines, par.mindemerits = currentlines, currentdemerits  
                            else:
                                if currentdemerits < par.mindemerits * stretchcoeff:
                                    if currentdemerits < par.mindemerits:
                                        par.deflines, par.mindemerits = currentlines, currentdemerits  
                                    if par.lines[-1][0] == currentlines:
                                        if par.lines[-1][1] > currentdemerits:
                                            par.lines.pop(-1)
                                        else: # The option we get isn't better
                                            continue
                                else:
                                    self.skip = True
                                    continue
                            par.lines.append((currentlines, currentdemerits))
                    elif line.startswith(r"@\par"):
                        self.parfound = True
        self.processpage(pag)
        
class Paragraph:
    def __init__(self):
        self.lines = []
        self.goodref = False
        # self.minlines = None can be inferred from the information stored in lines
    def getref(self):
        refline = "\n{} {}.{} 0".format(self.ref[0], self.ref[1], self.ref[2])
        if not self.goodref:
            refline += "[{}]".format(self.ref[3])
        return refline
    def getadjline(self):
        if self.ref[2] == "" or self.lines == []:
            return None
        outputline = self.getref()
        sizerange = (self.lines[0][0] - self.deflines, self.lines[-1][0] - self.deflines )
        if sizerange == (0, 0):
            return None
        elif sizerange == (0, 1):
            return outputline
        else:
            lowerbound, upperbound = sizerange
            outputline += " %"
            if lowerbound != 0:
                outputline += str(lowerbound)
            if upperbound != 0:
                outputline += "+{}".format(upperbound)
            return outputline
    def formatoptions(self, normalised=False): # returns minimum number of lines and the demerits associated with the other options
        if normalised:
            return self.lines[0][0], [ self.lines[i][1]/self.mindemerits for i in range(1, len(self.lines)) ]
        else:
            return self.lines[0][0], [ self.lines[i][1] for i in range(1, len(self.lines)) ]
    
class Page:
    def __init__(self):
        self.vals = []
        self.pageinfo = None

#"""
parser = argparse.ArgumentParser(description="Takes a TeX .log file and outputs the possible paragraph breaks (up to a badness defined by --stretchcoeff) to an .adj file")
parser.add_argument("logfile", help="TeX .log file path")
parser.add_argument("-o", "--outpath", help="Destination filename ([logfile].adj if omitted)")
parser.add_argument("-s", "--stretchcoeff", type=float, default=3.0, help="The maximum allowed demerits of a paragraph breaking option will be (stretchcoeff) * (demerits of best breaking option)")
x = parser.parse_args()
if x.outpath is None:
    x.outpath = x.logfile + ".adj"  # """
    
#"""
logfile = open(x.logfile, "r", encoding="utf8")
doc = Document(logfile)
doc.logparser(x.stretchcoeff) 
logfile.close() # """

#"""
adjfile = None
for par in doc.paragraphs:
    outputline = par.getadjline()
    if outputline is not None:
        if adjfile is None:
            adjfile = open(x.outpath, "a", encoding="utf8")
            outputline = outputline.strip("\n")
        adjfile.write(outputline)
adjfile.write("\n")
adjfile.close()  #"""
#"""#
#logfile = open(r"C:\Users\jakem\WST\ptxprint-GENWSG_tight.log", "r", encoding="utf8")
#doc = Document(logfile)
#doc.logparser(3.0) 
#logfile.close() # """