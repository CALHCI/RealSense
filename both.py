import pyrealsense2 as rs
from itertools import zip_longest
import numpy as np
import cv2


"""
Purpose: Trackes object in user inputed region of interest and distance to the center of the region is calcualted in 
real time.
Result: Objects are tracked successful and distance is correctly track from center of object to camera
"""



# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)


# Start streaming
pipeline.start(config)

# Create a tracker object
tracker = cv2.legacy.TrackerCSRT_create()

# Get initial frame for ROI selection
frames = pipeline.wait_for_frames()
color_frame = frames.get_color_frame()
initial_frame = np.asanyarray(color_frame.get_data())

# Select ROI for tracker from the first frame
bbox = cv2.selectROI("Frame", initial_frame, fromCenter=False, showCrosshair=True)
tracker.init(initial_frame, bbox)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Update the tracker with the current frame
        ret, bbox = tracker.update(color_image)
        if ret:
            # Draw bounding box
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(color_image, p1, p2, (0, 255, 0), 2, 1)

            # Calculate the center of the bounding box
            center_x = int(bbox[0] + bbox[2] / 2)
            center_y = int(bbox[1] + bbox[3] / 2)
            cv2.circle(color_image, (center_x, center_y), 5, (0, 0, 255), -1)

            # Get the depth at the center point of the bounding box
            distance_meters = depth_frame.get_distance(center_x, center_y)
            distance_inches = distance_meters * 39.37  # Convert meters to inches
            distance_text = f"Distance: {distance_inches:.2f} inches"
            cv2.putText(color_image, distance_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show images
        cv2.imshow("Tracking", color_image)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
