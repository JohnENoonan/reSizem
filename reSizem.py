#!/usr/bin/env python

import sys, argparse
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
        saveCopy = boolean flag, true if a resizing will save a copy
        copyName = string name to be used for saving a new image
    """
    def __init__(self, _file, _copyName = ""):
        # try to load image
        self.loadImage(_file)
        # parse for file path, name, and extension
        self.parseInput(_file)
        # store original image dimensions
        self.origWidth = self.im.width
        self.origHeight = self.im.height
        # parse name for copy of image and set flag
        self.copyName = _copyName
        self.parseCopyName()

    # helper to load image as PIL.Image in constructor
    def loadImage(self, _file):
        try:
            self.im = Image.open(_file)
        except IOError as e:
            # failed to open Image
            errorMsg = "\n\nFailed to open file {}, please make".format(_file) + \
                       " sure the name and path to the file is correct"
            sys.stderr.write(str(e))
            sys.stderr.write(errorMsg)
            sys.exit(1)

    # helper in constructor to parse file input into substrings
    def parseInput(self, _file):
        self.path, self.name = os.path.split(_file)
        # if no path given assume current directory
        if self.path == "":
            self.path = os.getcwd()
        self.name, self.extension = os.path.splitext(self.name);
        self.extension = self.extension.split('.')[1]

    # helper to parse the copy name and set whether to save a copy
    def parseCopyName(self):
        self.saveCopy = len(self.copyName) > 0
        if (self.saveCopy):
            self.copyName = os.path.basename(self.copyName)
            self.copyName = os.path.splitext(self.copyName)[0]

    # resizes with fixed dimensions
    # requires x,y be integers
    def resizeFixed(self, x, y):
        self.saveImage(x,y)

    # resizes based on fixed width with height maintaing aspect ratio
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

    # resizes with maintained aspect ratio making it as large as possible but
    # <= (targetW, targetH)
    # requires targetW, targertH be integers
    def resizeToFit(self, targetW, targetH):
        scaleW = float(targetW) / float(self.origWidth)
        scaleH = float(targetH) / float(self.origHeight)
        scale = min(scaleW, scaleH)
        self.saveImage(int(self.origWidth*scale), int(self.origHeight*scale))

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
            saveError(e)


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
                print "Saved new image {} of size {}x{}".format( \
                                self.copyName + '.' + self.extension, x, y)
                copy.save(self.path + '/' + self.copyName + "." +  self.extension)
            except IOError as e:
                saveError(e)
        else:
            self.im = self.im.resize((x,y))
            try:
                print "Overwrote {} with size {}x{}".format( \
                                        self.name + '.' + self.extension, x, y)
                self.im.save(self.path + '/' + self.name + "." + self.extension)
            except IOError as e:
                saveError(e)

# error output for when an image is improperly saved
def saveError(e):
    sys.stderr.write(str(e))
    sys.stderr.write("\n\nSomething went wrong when writing new image.",
            "Either no new image was created or the new image may",
            "be corrupted")
    sys.exit(1)

class PercentAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print '%r %r %r' % (namespace, values, option_string)
        setattr(namespace, self.dest, values)


# add options to command line
def addopts(parser):
    parser.add_argument('inImg', metavar="'Input Image'",
        help="Input image to be resized")
    parser.add_argument('--outImg', '-o', metavar="'Output Image'",
        help="Output image if not overwriting", default="")

    # add commands
    commands = parser.add_mutually_exclusive_group(required=True)
    # resize by percent
    commands.add_argument('--percent', '-p',  metavar="percent",
        help="Resize image by percent", type=float)
    # resize with width
    commands.add_argument('--resizeWidth', '-rw', metavar="width",
        help="Resize image to maintain ratio with width set to argument", type=int)
    # resize with height
    commands.add_argument('--resizeHeight', '-rh', metavar="height",
        help="Resize image to maintain ratio with height set to argument", type=int)
    # resize with fixed dimensions
    commands.add_argument('--resizeAbsolute', '-ra', metavar=("width", "height"),
        help="Resize image with given width and height", nargs=2, type=int)
    # resize to fit dimensions
    commands.add_argument('--resizeToFit', '-rf', metavar=("'target width'",
        "'target height'"),
        help="Resize image to maintain aspect ratio while <= given target dimension",
        nargs=2, type=int)
    commands.add_argument('--convertFile', '-c', metavar="extension",
        help="Convert image to type given")

def runCommand(args):
    for key in sys.argv[1:]:
        if key == "-p":
            d.resizeByPercent(args.percent)
            break
        elif key == "-rw":
            d.resizeWidth(args.resizeWidth)
            break
        elif key == "-rh":
            d.resizeHeight(args.resizeHeight)
            break
        elif key == "-ra":
            d.resizeWidth(args.resizeAbsolute[0], args.resizeAbsolute[1])
            break
        elif key == "-rf":
            d.resizeToFit(args.resizeToFit[0], args.resizeToFit[1])
            break
        elif key =='-c':
            d.convertType(args.convertFile)
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Resize and convert images')
    addopts(parser)
    args = parser.parse_args()
    d = Data(args.inImg, args.outImg)
    runCommand(args)
