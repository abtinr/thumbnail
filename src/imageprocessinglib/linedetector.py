from patterndetector import PatternDetector
from utils import bresenham
import pymorph 
import numpy
import scipy.signal as signal
import math


class LineDetector(PatternDetector):
    def __init__(self, segmentSize, variation, lineThr, lineSurrThr, lineConnected, margin, minLength):
        self.segmentSize = segmentSize
        self.variation = variation
        self.lineThr = lineThr
        self.lineSurrThr = lineSurrThr
        self.lineConnected = lineConnected
        self.margin = margin
        self.minLength = minLength


    # Build line filters 
    def _getLineFilter(self, segmentSize, variation):
        smallDisk = pymorph.sedisk(1);
        bigDisk = pymorph.sedisk(2);
        
        horizontal_filter = numpy.zeros((variation*2+1,variation*2+1,segmentSize))
        horizontal_surrounding = numpy.zeros((variation*2+1,variation*2+1,segmentSize))

        index = -1
        for i in range(-variation,variation+1):
            index = index + 1;
            # find the line between selected points
            points = bresenham(variation+i,0,variation-i,segmentSize-1)
            tmp = numpy.zeros((variation*2+1)*segmentSize).reshape((variation*2+1, segmentSize))
            for l in range(0, len(points)):
                tup_point = points[l]
                tmp[tup_point[0], tup_point[1]] = 1
            tmp_filter = pymorph.dilate(pymorph.binary(tmp), smallDisk)
            tmp_surrounding = pymorph.subm(pymorph.dilate(pymorph.binary(tmp), bigDisk) , pymorph.dilate(pymorph.binary(tmp), smallDisk))
            horizontal_filter[index,:,:] = tmp_filter
            horizontal_surrounding[index,:,:] = tmp_surrounding
        
        return horizontal_filter, horizontal_surrounding
        
        
    # Find horizontal lines in an image 
    def _findHorizontalLinesInImage(self, image):
        horizontal_filter, horizontal_surrounding = self._getLineFilter(self.segmentSize, self.variation)
        line_thr = self.lineThr * self.segmentSize # 0.75
        surr_thr = self.lineSurrThr * self.segmentSize  #0.02
        I_line_filter = signal.convolve(image,horizontal_filter[0,:,:],mode='same') > line_thr
        I_line_surrounding = signal.convolve(image,horizontal_surrounding[0,:,:],mode='same') < surr_thr
        I_line = (I_line_surrounding*I_line_filter).astype(int)
        
        # Filter the image with the line segments and surrounding filters
        for i in range(1,len(horizontal_filter)):
            I_line_filter = signal.convolve(image,horizontal_filter[i,:,:],mode='same') > line_thr
            I_line_surrounding = signal.convolve(image,horizontal_surrounding[i,:,:],mode='same') < surr_thr
            I_line = I_line + (I_line_surrounding*I_line_filter).astype(int)

        I_line = I_line > 0;
        orig_line = I_line  
        lines = []
        # Detecting lines and connect them as we progress in the image
        for j in range(self.segmentSize/2+1,len(I_line[0])-self.segmentSize/2-1):
            for i in range(self.margin,len(I_line)-self.margin):
                if(I_line[i,j]):
                    if not lines:
                        lines.append((i, j-self.segmentSize/2, i, j+self.segmentSize/2))
                    else:
                        hasFound = 0
                        index = -1
                        for eachLine in lines:  
                            index = index + 1                   
                            if (abs(eachLine[0]-i) < self.variation and j-eachLine[-1] < self.lineConnected):
                                newLine = ((i+eachLine[0])/2, eachLine[1], (i+eachLine[0])/2, j+self.segmentSize/2)
                                del lines[index]
                                lines.append(newLine)
                                hasFound = 1
                                break
                        if hasFound == 0:
                            lines.append((i, j-self.segmentSize/2, i, j+self.segmentSize/2))
                    I_line[i-self.margin:i+self.margin,j-self.segmentSize/2:j+self.segmentSize/2] = 0
        
        return lines

    # Find vertical and horizontal lines in a binary image
    def detect(self, image):
        horizontalLine = self._findHorizontalLinesInImage(image.copy())
        image = image.transpose()
        # Vertical lines can be found by transposing the image and finding the horizontal lines
        verticalLine = self._findHorizontalLinesInImage(image.copy())
        for lines in verticalLine:
            newLine = (lines[1], lines[0], lines[3], lines[2])
            horizontalLine.append(newLine)
        
        # Only keep those lines with length greater than a minimum
        allLines = []
        for lines in horizontalLine:
            if(math.sqrt((lines[0]-lines[2])*(lines[0]-lines[2])+(lines[1]-lines[3])*(lines[1]-lines[3])) > self.minLength):
                allLines.append(lines)
        
        return allLines    