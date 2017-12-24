#!/usr/bin/env python

import sys, getopt
import os.path
from PIL import Image

FILE_TYPES = ["ppm", "png", "jpeg", "jpg", "gif", "tiff", "bmp"]


# data holder for image
class Data:
    """
    local fields:
        im = PIL image representing input
        origWidth = width of original image
        origHeight = height of original image
        path = path to input image
        name = name of input image
        extension = file type of image

    """
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
        self.parseInput(_file)
        # store original image dimensions
        self.origWidth = self.im.width
        self.origHeight = self.im.height
        # parse name for copy of image and set flag
        self.copyName = _copyName
        self.parseCopyName()

    # helper in constructor to parse file input into substrings
    def parseInput(self, _file):
        self.path, self.name = os.path.split(_file)
        # if no path given assume current directory
        if self.path == "":
            self.path = os.getcwd()
        self.name, self.extension = os.path.splitext(self.name);
        self.extension = self.extension.split('.')[1]

    def parseCopyName(self):
        self.saveCopy = len(self.copyName) > 0
        if (self.saveCopy):
            self.copyName = os.path.basename(self.copyName)
            self.copyName = os.path.splitext(self.copyName)[0]

    # resizes with fixed dimensions
    # requires x,y be integers
    def resizeFixed(self, x, y):
        self.saveImage(x,y)

    # resizes based on fixed width wit height maintaing aspect ratio
    # requires w be an integer
    def resizeWidth(self, w):
        percent = float(w) / float(self.origWidth)
        newHeight = self.origHeight * percent
        self.saveImage(w,int(newHeight))

    # resizes based on fixed height with the width maintaing aspect ratio
    # requires h be an integer
    def resizeHeight(self, h):
        percent = float(h) / float(self.origHeight)
        newWidth = self.origWidth * percent
        self.saveImage(int(newWidth), h)

    # resizes both dimensions by percent.
    # require percent be a real number > 1
    def resizeByPercent(self, percent):
        percent /= 100.0
        self.saveImage(int(self.origWidth*percent), int(self.origHeight*percent))

    # takes file format and creates new image of format type
    def convertType(self, _type):
        _type = _type.strip('.')
        copy = self.im.copy()
        try:
            copy.save(self.path + '/' + self.name + "." + _type)
            print "Converted {} from {} to {}".format(self.name, self.extension, _type)
        except IOError as e:
            sys.stderr.write(str(e))
            sys.stderr.write("\n\nSomething went wrong when writing new image.",
                    "Either no new image was created or the new image may",
                    "be corrupted")
            sys.exit(1)


    # compresses image as much as can be with quality of 90
    #TODO pass quality and compression type
    def compressImage(self):
        # original file size
        origSize = os.path.getsize(self.path + '/' + self.name + "." + self.extension)
        # if making new file
        if self.saveCopy:
            copy = self.im.copy()
            try:
                copy = copy.resize((self.origWidth, self.origHeight))
                copy.save(self.path + '/' + self.copyName + "." + self.extension, \
                          quality=90, optimize=True)
                newSize = os.path.getsize(self.path + '/' + self.copyName + "." + self.extension)
            except IOError as e:
                saveError(e)
        # if overwriting
        else:
            try:
                self.im.save(self.path + '/' + self.name + "." + self.extension, \
                             quality=90, optimize=True)
                newSize = os.path.getsize(self.path + '/' + self.name + "." + self.extension)
            except IOError as e:
                saveError(e)
        percent = 1-newSize/float(origSize)
        print "Compressed file by {:.2%} from {:,} kb to {:,} kb".\
               format(percent, origSize/1024, newSize/1024)



    # function takes absolute sizes of the image to be saved
    # requires x,y be integers
    def saveImage(self, x, y):
        if self.saveCopy:
            copy = self.im.copy()
            copy = copy.resize((x,y))
            try:
                print self.path + '/' + self.copyName, self.extension
                copy.save(self.path + '/' + self.copyName + "." +  self.extension)
            except IOError as e:
                saveError(e)
        else:
            self.im = self.im.resize((x,y))
            try:
                self.im.save(self.path + '/' + self.name + "." + self.extension)
            except IOError as e:
                saveError(e)

def saveError(e):
    sys.stderr.write(str(e))
    sys.stderr.write("\n\nSomething went wrong when writing new image.",
            "Either no new image was created or the new image may",
            "be corrupted")
    sys.exit(1)


if __name__ == "__main__":
    # getInput(sys.argv[1:])
    d = Data("./images/square.png", "squareCopy")
    # d = Data("C:\\Users\\noonaj2\\Pictures\\artistScreenshot.png", "artistSmaller")
    d.resizeWidth(602)
    # d.convertType("jpg")
