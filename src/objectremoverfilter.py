from imagefilter import ImageFilter

class ObjectRemoverFilter(ImageFilter):
    def __init__(self, defaultvalue, margin):
        self.defaultvalue = defaultvalue
        self.margin = margin
        pass

    def setobjects(self, objects):
        self.objects = objects

    # Remove a line and its self.margin from an image and set it to a given value
    def filter(self, image):
        for l in self.objects:
            image[l[0]-self.margin:l[2]+self.margin,l[1]-self.margin:l[3]+self.margin] = self.defaultvalue
        return image