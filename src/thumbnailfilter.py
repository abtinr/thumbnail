
import numpy
from imagefilter import ImageFilter
from utils import removeObjectFromImage
from collections import namedtuple
from linedetector import LineDetector
from logodetector import LogoDetector
from textdetector import TextDetector
from thinningfilter import ThinningFilter
from thresholdfilter import ThresholdFilter
from objectremoverfilter import ObjectRemoverFilter

class ThumbnailFilter(ImageFilter):
    def __init__(self, thumbnailwidth):
        self.thumbnailwidth = thumbnailwidth
        pass

    def _createThumbnail(self, imageSize, lines, logo, text, newSize):
        thumbnail = numpy.empty((newSize[0],newSize[1],3))
        thumbnail.fill(255)
        
        ratioX = float(newSize[0])/float(imageSize[0])
        ratioY = float(newSize[1])/float(imageSize[1])
        
        def fillvalue(objects, value):
            for l in objects:
                pos = ((int(round(float(l[0])*ratioX)), int(round(float(l[1])*ratioY)), int(round(float(l[2])*ratioX)), int(round(float(l[3])*ratioY))))
                thumbnail[pos[0]:pos[2]+1, pos[1]:pos[3]+1,] = value

        fillvalue(text, [80, 0, 0])
        fillvalue(logo, [0, 80, 0])
        fillvalue(lines, [0, 0, 80])

        return thumbnail        

    def filter(self, image):
        # parameters
        ThumbnailOptions = namedtuple("MyStruct", "resizeX thinningIteration segmentSize \
        variation margin minLength lineConnected lineThr lineSurrThr removingMargin \
        logo_minDensity logo_minX logo_minY text_wordDistance text_minSizeX text_minSizeY \
        thumbnail_X")
        options = ThumbnailOptions(resizeX = 1000, thinningIteration = 3, segmentSize = 15, \
        variation = 2, margin = 5, minLength = 60, lineConnected = 4, lineThr = 0.75, \
        lineSurrThr = 0.02, removingMargin = 5, logo_minDensity = 0.1, logo_minX = 60, logo_minY = 60, \
        text_wordDistance = 60, text_minSizeX = 10, text_minSizeY = 15, \
        thumbnail_X = self.thumbnailwidth)
            
        thresholdfilter = ThresholdFilter(options.resizeX)
        thresholdedImage = thresholdfilter.filter(image) 

        thinningfilter = ThinningFilter(options.thinningIteration)
        thinnedImage = thinningfilter.filter(thresholdedImage.astype(int)) > 0
        thinnedImage = thinnedImage.astype(int)

        objectremoverfilter = ObjectRemoverFilter(0, options.removingMargin)
        linedetector = LineDetector(options.segmentSize, options.variation, options.lineThr, options.lineSurrThr, options.lineConnected, options.margin, options.minLength)
        lines = linedetector.detect(thinnedImage)
        objectremoverfilter.setobjects(lines)
        linesRemoved = objectremoverfilter.filter(thresholdedImage.copy())

        logodetector = LogoDetector(options.logo_minDensity, options.logo_minX, options.logo_minY)
        logos = logodetector.detect(linesRemoved)
        objectremoverfilter.setobjects(logos)
        logoRemoved = objectremoverfilter.filter(linesRemoved.copy())

        textdetector = TextDetector(options.text_wordDistance, options.text_minSizeX, options.text_minSizeY)
        text = textdetector.detect(logoRemoved) 

        thumbnail_Y = int(options.thumbnail_X/float(len(thresholdedImage))*len(thresholdedImage[0]))
        thumbnail = self._createThumbnail([len(thresholdedImage), len(thresholdedImage[0])], lines, logos, text, [options.thumbnail_X, thumbnail_Y])

        return thumbnail