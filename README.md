# thumbnail 
Creates thumbnail from a given form. It basically detects logos, texts, border, and lines and will convert them into small-sized thumbnail.

## Setup


## Usage
`main.py` is the entry point of the code and can be used as following:
```
$ python main.py inputfile outputfile
```
for example:
```
$ python src/main.py testdata/form.jpg testdata/thumbnail.png
```

## The algorithm
The algorithm follows these steps:

1. **Thresholding.** Otsu method is used to find the threshold automatically
2. **Thinning.** With the assumption of a form being formed by logo, text and line only, the elements are thinned using Zhang-Suen algorithm.
3. **Line detection.** Lines are detected using an implementation of hough transform, with the assumption the lines are either horizontal or vertical with possible slight rotation. Lines are then removed from the image.
4. **Logo detection.** Connected components are first found on the image and those with sizes larger than a threshold are detected as logos.
5. **Text detection.** Remined image is convolved with a horizontal filter and connected components are detected as text
6. **Thumbnail creation.**