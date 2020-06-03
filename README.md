## 1.INTRODUCTION
In this project, the speed of the cars moving on a double-lane one way road is calculated
by using the connect companents of per frame of a video.
In this project, the images taken from a high point in the direction of the vehicles moving
on a double-lane road were subjected to some filtering operations to obtain the desired image and
the areas and centeroids of vehicles were found by using the image's connect components. Speed
is determined according to the reception times

## 2.METHODS
This Code mask the cars foreground and destroy the backgroun and uses the connected
components of the filtered images to find image’s centroids. From centroid it calculates the in
time and out time and calculate the speed of cars.

# 3.6*K/(departure time – arrival time)
    (K: length of way (meter))
Imported libraries:

cv2

numpy

time
### Connected Componenets[3]
Computes the connected components labeled image of boolean image image with 4 or 8
way connectivity - returns N, the total number of labels [0, N-1] where 0 represents the
background label. ltype specifies the output label image type, an important consideration
based on the total number of labels or alternatively the total number of pixels in the source
image.
#### Parameters:
image – the image to be labeled

labels – destination labeled image

connectivity – 8 or 4 for 8-way or 4-way connectivity respectively

ltype – output image label type. Currently CV_32S and CV_16U aresupported.
statsv –
statistics output for each label, including the background label, see below for
available statistics. Statistics are accessed via statsv(label, COLUMN) where
available columns are defined below.

CC_STAT_LEFT The leftmost (x) coordinate which is the inclusive start of
the bounding box in the horizontal direction.

CC_STAT_TOP The topmost (y) coordinate which is the inclusive start of the
bounding box in the vertical direction.

CC_STAT_WIDTH The horizontal size of the bounding box

CC_STAT_HEIGHT The vertical size of the bounding box

CC_STAT_AREA The total area (in pixels) of the connected component
centroids – floating point centroid (x,y) output for each label, including the
background label


