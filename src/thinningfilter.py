import numpy
from imagefilter import ImageFilter

class ThinningFilter(ImageFilter):
    def __init__(self, iterations):
        self.iterations = iterations
        pass

    # Defining neighbours of a specific pixel
    def _neighbours_vec(self, image):
        return image[2:,1:-1], image[2:,2:], image[1:-1,2:], image[:-2,2:], image[:-2,1:-1], image[:-2,:-2], image[1:-1,:-2], image[2:,:-2]

    # Defining transition between neighbouring pixels around a specific pixel
    def _transitions_vec(self, P2, P3, P4, P5, P6, P7, P8, P9):
        return ((P3-P2) > 0).astype(int) + ((P4-P3) > 0).astype(int) + \
        ((P5-P4) > 0).astype(int) + ((P6-P5) > 0).astype(int) + \
        ((P7-P6) > 0).astype(int) + ((P8-P7) > 0).astype(int) + \
        ((P9-P8) > 0).astype(int) + ((P2-P9) > 0).astype(int)

    # main function to be called.
    def filter(self, image):
        for iter in range (1, self.iterations):
            # step 1    
            P2,P3,P4,P5,P6,P7,P8,P9 = self._neighbours_vec(image)
            condition0 = image[1:-1,1:-1]
            condition4 = P4*P6*P8
            condition3 = P2*P4*P6
            condition2 = self._transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9) == 1
            condition1 = (2 <= P2+P3+P4+P5+P6+P7+P8+P9) * (P2+P3+P4+P5+P6+P7+P8+P9 <= 6)
            cond = (condition0 == 1) * (condition4 == 0) * (condition3 == 0) * (condition2 == 1) * (condition1 == 1)
            changing1 = numpy.where(cond == 1)
            image[changing1[0]+1,changing1[1]+1] = 0
            # step 2
            P2,P3,P4,P5,P6,P7,P8,P9 = self._neighbours_vec(image)
            condition0 = image[1:-1,1:-1]
            condition4 = P2*P6*P8
            condition3 = P2*P4*P8
            condition2 = self._transitions_vec(P2, P3, P4, P5, P6, P7, P8, P9) == 1
            condition1 = (2 <= P2+P3+P4+P5+P6+P7+P8+P9) * (P2+P3+P4+P5+P6+P7+P8+P9 <= 6)
            cond = (condition0 == 1) * (condition4 == 0) * (condition3 == 0) * (condition2 == 1) * (condition1 == 1)
            changing2 = numpy.where(cond == 1)
            image[changing2[0]+1,changing2[1]+1] = 0
        return image