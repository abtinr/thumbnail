import numpy
from scipy.ndimage.measurements import label
from patterndetector import PatternDetector

class LogoDetector(PatternDetector):
    def __init__(self, logo_minDensity, logo_minX, logo_minY):
        self.logo_minDensity = logo_minDensity
        self.logo_minX = logo_minX
        self.logo_minY = logo_minY

    def detect(self, image):
        label_im, nb_labels = label(image > 0)
        
        # Logos are large component with density and size greater than a minimum
        logo = []
        for i in range(1, nb_labels):
            component_sizeX = max(numpy.where(label_im == i)[0])-min(numpy.where(label_im == i)[0])+1
            component_sizeY = max(numpy.where(label_im == i)[1])-min(numpy.where(label_im == i)[1])+1
            component_density = float(sum(sum(label_im == i)))/float(component_sizeX*component_sizeY)
            if(component_density > self.logo_minDensity and \
            component_sizeX > self.logo_minX and component_sizeY > self.logo_minY):
                logo.append((min(numpy.where(label_im == i)[0]), min(numpy.where(label_im == i)[1]), max(numpy.where(label_im == i)[0]), max(numpy.where(label_im == i)[1])))
        
        return logo