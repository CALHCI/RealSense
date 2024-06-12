# RealSense
A framework to gather data from Intel RealSense devices


## Installation Guidelines (type in terminal):

camVision.py, depth.py, :
-pip install numpy
-pip install pyrealsense2
-pip install opencv-python

objects.py:
-pip install opencv-python
-pip install numpy

## Content

### both.py
* Purpose: Trackes object in user inputed region of interest and distance to the center of the region is calcualted in 
real time.
* Result: Objects are tracked successful and distance is correctly track from center of object to camera

### cam.py

* ?
* ?

### camVision.py

* ?
* ?

### depth.py

* Purpose: Attempted to in realtime track the distance of the camera to 3 random points on the webfeed.
* Result: Successfully used camera depth sensing to accurately track the distance from the camera
to 3 points that are randomly generated. Precursor to both.py where the distance to the center
of the object is accurately tracked in realtime.

### depth.py

" Purpose: Tracks multiple items using a region of interest algorithm. Users are prompted to draw
shape around object they want to detect and algorithm draws a bounding box around said object.
* Result: Tracks multiple objects but must be manually selected by user. Number of items tracked can 
be change in for loop in line 18.



