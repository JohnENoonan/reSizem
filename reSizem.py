#!/usr/bin/env python

import sys, getopt
import os.path
from PIL import Image

# data holder for image
class Data:
    def __init__(self, _file):
        try:
            self.im = Image.open(_file)
        except IOError:
            # failed to open Image
            sys.exit("Error: failed to open file %s, please make \
                      sure the name and path to the file is are correct" %(_file))
        self.path, self.name = os.path.split(_file)
        if self.path == "":
            self.path = os.getcwd()
        self.origWidth = self.im.width
        self.origHeight = self.im.height
    # resizers with fixed dimensions
    def resizeFixed(self, x, y):
        copy = im.copy()
        copy.resize(x,y)
    # resizes based on fixed width
    def resizeWidth(self, w):
        percent = float(w) / float(self.origWidth)
        newHeight = self.height * percent
    # resizes based on fixed width
    def resizeHeight(self, h):
        percent = float(h) / float(self.origHeight)
        newWidth = self.width * percent


# def getInput(argv):
#     inputfile = ''
#     outputfile = ''
#     try:
#         opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#     except getopt.GetoptError:
#         print 'test.py -i <inputfile> -o <outputfile>'
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h' or opt == "-help":
#             print 'test.py -i <inputfile> -o <outputfile>'
#             sys.exit()
#         elif opt in ("-i", "--ifile"):
#             inputfile = arg
#         elif opt in ("-o", "--ofile"):
#             outputfile = arg
#         else:
#             print "anal"
#     print 'Input file is "', inputfile
#     print 'Output file is "', outputfile

if __name__ == "__main__":
    # getInput(sys.argv[1:])
