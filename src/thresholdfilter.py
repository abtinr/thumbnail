import scipy.ndimage as ndimage
import scipy.misc as misc
import mahotas
import numpy as np
from imagefilter import ImageFilter

class ThresholdFilter(ImageFilter):
    def __init__(self, resizeX):
        self.resizeX = resizeX
        pass

    def rgb2gray(self, rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

    # Threshold and resize the image
    def filter(self, image):
        if(image.ndim == 3):
            image=self.rgb2gray(image)

        # Smooth the image
        smoothingSigma = len(image)*0.0005;
        smoothedImage = ndimage.gaussian_filter(image, smoothingSigma)

        # Resize the image
        resizeY = int(self.resizeX/float(len(smoothedImage))*len(smoothedImage[0]))
        resizedImage = misc.imresize(smoothedImage, (self.resizeX, resizeY), 'bilinear')

        # Threshold the image using otsu method
        thr = mahotas.otsu(resizedImage)
        thresholdedImage = resizedImage < thr
        
        # Correct the corners of the image
        thresholdedImage[0:5,] = 0
        thresholdedImage[-5:0,] = 0
        thresholdedImage[:,0:5] = 0
        thresholdedImage[:,-5:0] = 0

        return thresholdedImage