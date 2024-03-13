# RealSense Camera Detection
## AprilTag Detection Algorithm Documentation
### Overview
Provides the functionality to take a picture of a Tower of Hanoi instance where each ring is surrounded by AprilTags and represent their order and rod location in the form of an array "state/frame."

### How to Use
1. Print a chessboard/checkerboard pattern like [this one](https://raw.githubusercontent.com/MarkHedleyJones/markhedleyjones.github.io/master/media/calibration-checkerboard-collection/Checkerboard-A4-25mm-8x6.pdf) and attach it to a hard, movable surface.
2. Print multiple "tag36h11" AprilTags with IDs from 1 to n and surround the outside of each ring with its corresponding ID AprilTag (with an ID of 1 being the smallest and n being the biggest).
3. Run `apriltag_get_images.py` to take pictures of the chessboard at different locations, rotations, and angles by pressing `s` and hitting `q` to exit. The more images you take, the more accurate the calibration will be, but anywhere from 40-60 should be fine.
4. Run `apriltag_calibration.py` to take in all of the taken images and generate a calibration file. This should only be done once for each camera (as with the previous steps).
5. Run `apriltag_detect.py` to use the AprilTag locations and return a Tower of Hanoi frame.

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

I chose to use AprilTags as, at the cost of minimal computing power and processing time, they can provide the most accurate estimation for where each ring is while maximizing the amount of external variables that can be ignored.

### How Does It Work?
1. Calibrate the camera by getting its focal width, focal height, camera center x, and camera center y, which is done by determining its warping with a known image (like a commonly used chessboard pattern).
2. Identify the location of each AprilTag and average together the position of each tag.
3. Use the average of each tag to determine which rod they're most likely attached to and stack them in the order of y coordinates.

(TODO) ADD A VISUAL OF THE TOWER

### Performance
(TODO)

### How to Improve
* Instead of hardcoding a specific distance that separates one rod from another, place another tag with a unique ID in between the rods to prevent having to change the value (should be easy to implement)
* Experiment with a lower resolution AprilTag to allow for additional distance from the camera or to make the tags smaller (change only if necessary)
* Integrate code so that a new camera and detector object doesn't have to be initialized on each call (very easy fix that will significantly reduce the time)