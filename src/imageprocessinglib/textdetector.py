import numpy
import scipy.signal as signal
from scipy.ndimage.measurements import label
from patterndetector import PatternDetector

class TextDetector(PatternDetector):
    def __init__(self, text_wordDistance, text_minSizeX, text_minSizeY):
        self.text_wordDistance = text_wordDistance
        self.text_minSizeX = text_minSizeX
        self.text_minSizeY = text_minSizeY

    def detect(self, Image):      
        # Design a filter 
        filter  = numpy.ones((1, self.text_wordDistance))
        I_text = signal.convolve(Image, filter, mode='same') > 0
        
        text = []
        # Find connected components and detect text
        label_im, nb_labels = label(I_text)
        for i in range(1, nb_labels):
            component_sizeX = max(numpy.where(label_im == i)[0])-min(numpy.where(label_im == i)[0])
            component_sizeY = max(numpy.where(label_im == i)[1])-min(numpy.where(label_im == i)[1])
            if(component_sizeX > self.text_minSizeX and component_sizeY > self.text_minSizeY):
                posX = (max(numpy.where(label_im == i)[0])+min(numpy.where(label_im == i)[0]))/2
                posY1 = min(numpy.where(label_im == i)[1])+self.text_wordDistance
                posY2 = max(numpy.where(label_im == i)[1])-self.text_wordDistance
                text.append((posX, posY1, posX, posY2))
                
        return text        