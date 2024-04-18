## AprilTag Detection Algorithm Documentation
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

### How to Improve
* 
