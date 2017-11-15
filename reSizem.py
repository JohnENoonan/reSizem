#!/usr/bin/env python

import sys, getopt
import os.path
from PIL import Image

# data holder for image
class Data:
    def __init__(self, _file, _copyName = ""):
        # try to load image
        try:
            self.im = Image.open(_file)
        except IOError as e:
            # failed to open Image
            errorMsg = "\n\nFailed to open file {}, please make".format(_file) + \
                       " sure the name and path to the file is correct"
            sys.stderr.write(str(e))
            sys.stderr.write(errorMsg)
            sys.exit(1)
        # parse for file path, name, and extension
        self.path, self.name = os.path.split(_file)
        if self.path == "":
            self.path = os.getcwd()
        self.name, self.extension = os.path.splitext(self.name);
        self.extension = self.extension.split('.')[1]
        # store original image dimensions
        self.origWidth = self.im.width
        self.origHeight = self.im.height
        # flag to overwrite image or save to new image
        self.copyName = _copyName
        self.saveCopy = len(self.copyName) > 0
        
    # resizes with fixed dimensions
    def resizeFixed(self, x, y):
        self.saveImage(x,y)

    # resizes based on fixed width wit height maintaing aspect ratio
    def resizeWidth(self, w):
        percent = float(w) / float(self.origWidth)
        newHeight = self.height * percent
        self.saveImage(w,newHeight)

    # resizes based on fixed height with the width maintaing aspect ratio
    def resizeHeight(self, h):
        percent = float(h) / float(self.origHeight)
        newWidth = self.width * percent
        self.saveImage(newWidth, h)
    # function takes absolute sizes of the image to be saved
    def saveImage(self, x, y):
        if self.saveCopy:
            copy = self.im.copy()
            copy = copy.resize((x,y))
            try:
                print self.path + '/' + self.copyName, self.extension
                copy.save(self.path + '/' + self.copyName, self.extension)
            except IOError as e:
                sys.stderr.write(str(e))
                sys.stderr.write("\n\nSomething went wrong when writing new image.",
                        "Either no new image was created or the new image may",
                        "be corrupted")
        else:
            self.im = self.im.resize((x,y))


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
    d = Data("./images/square.png", "squareCopy.png")
    print d.path
    print d.name
    print d.saveCopy
    d.resizeFixed(300,300)
