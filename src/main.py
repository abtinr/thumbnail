
import sys
from matplotlib.image import imread, imsave
from imageprocessinglib.thumbnailfilter import ThumbnailFilter

if __name__ == '__main__':
    imagefilename = sys.argv[1]
    thumbnailfilename = sys.argv[2]

    thumbnailfilter = ThumbnailFilter(100)
    image = imread(imagefilename)
    thumbnail = thumbnailfilter.filter(image)

    imsave(thumbnailfilename, thumbnail)
