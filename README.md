![GitHub repo size](https://img.shields.io/github/repo-size/CALHCI/RealSense)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

# RealSense
A framework to gather data from Intel RealSense devices
>[!IMPORTANT] 
> Useful information that users should know, even when skimming content.


# Content
> [!IMPORTANT]
> Give a title to each of the followinng

- [Installation Guidelines](#Installation-Guidelines)
- [both](#both_py)
- [cam](#cam_py)
- [camVision](#camVision_py)
- [depth](#depth_py)
- [objects](#objects_py)
- [AprilTag Detection](#AprilTag-Detection)

## Installation Guidelines 

Type in terminal:
```
camVision.py, depth.py, :
-pip install numpy
-pip install pyrealsense2
-pip install opencv-python

objects.py:
-pip install opencv-python
-pip install numpy
```

## both_py
* Purpose: Trackes object in user inputed region of interest and distance to the center of the region is calcualted in 
real time.
* Result: Objects are tracked successful and distance is correctly track from center of object to camera

## cam_py

> [!IMPORTANT]
> complete this

## camVision_py

> [!IMPORTANT]
> complete this

## depth_py

* Purpose: Attempted to in realtime track the distance of the camera to 3 random points on the webfeed.
* Result: Successfully used camera depth sensing to accurately track the distance from the camera
to 3 points that are randomly generated. Precursor to both.py where the distance to the center
of the object is accurately tracked in realtime.

## objects_py

" Purpose: Tracks multiple items using a region of interest algorithm. Users are prompted to draw
shape around object they want to detect and algorithm draws a bounding box around said object.
* Result: Tracks multiple objects but must be manually selected by user. Number of items tracked can 
be change in for loop in line 18.

## AprilTag Detection
### Overview
Provides the functionality to take a picture of a Tower of Hanoi instance where each ring is surrounded by AprilTags and represent their order and rod location in the form of an array "state/frame."

### How to Use
1. Print multiple "tag36h11" AprilTags with IDs from 1 to n and surround the outside of each ring with its corresponding ID AprilTag (with an ID of 1 being the smallest and n being the biggest).
2. Print 2 AprilTags with IDs of 0 and place them in between each pole.
3. Plug in the Intel RealSense camera and place it so the AprilTags are in view.
4. Run `python apriltag_detect.py <n> --debug --delay 1000` to test it in debug mode with a delay of 1000 ms and `n` rings.
5. Run `python apriltag_detect.py <n>` to continually print a Tower of Hanoi frame for `n` rings.

(TODO) ADD A VISUAL OF THE TOWER

### Design Choices
#### *How do we detect the rings?*
#### Goals (in order of importance)
* High accuracy (minimize the number of mistakes the robot makes)
* Fast processing time (minimize "thinking time" done by the robot)
* Adaptable to different environments (minimize the number of conditions that need to be perfect for it to work)

#### Four Possible Solutions:
* Color
    * Pretty consistent if done in the right environment
    * Very quick to process
    * Strict environment that has to have the same lighting and be free of colors that could mistake the camera
* Width
    * Very inconsistent as each width is relative to the camera
    * Very quick to process
    * Very strict environment where if the camera is moved even a bit, it will cause inaccuracy
* Numbers
    * Inconsistent as OCR can easily mix one number/letter with another
    * Somewhat quick to process
    * Not a particularly strict environment, but the numbers have to be drawn/written precisely
* AprilTags
    * Very consistent as each tag is very unique (high hamming distance)
    * Somewhat quick to process
    * Not a strict environment at all

I chose to use AprilTags as, at the cost of minimal computing power and processing time, they can provide the most accurate estimation for where each ring is while maximizing the amount of external variables that can be ignored. Additionally, I chose to use the "36h11" family opposed to the "16h5" family since, as indicated through testing, the small hamming distance of "16h5" led to the program detecting the background as AprilTags. Although this is filtered out in the final product, considering that the camera's resolution is good enough, we might as well use the "36h11" family to minimize error.

### How Does It Work?
1. Use the fx, fy, cx, cy and distance coefficients of the Intel RealSense camera to unwarp the picture taken.
2. Track the AprilTags and find their location in 3d space.
3. Average the coordinates of all of the tags with the same ID into one from 1-n.
4. Separate them into three arrays representing the 3 rods and place the id based on it's x value in relation to the x values of the two dividers.
5. Sort those arrays based on the y value of their average position



