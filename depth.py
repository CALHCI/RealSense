import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

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

        # Get the depth frame's width and height
        width = depth_frame.get_width()
        height = depth_frame.get_height()

        # Calculate the coordinates of the center pixel
        center_x = width // 2
        center_y = height // 2

        # Get the depth value at the center of the image
        distance_meters = depth_frame.get_distance(center_x, center_y)
        distance_inches = distance_meters * 39.37  # Convert meters to inches

        # Print out the distance in inches
        distance_text = f"Distance: {distance_inches:.2f} inches"
        print(distance_text)

        # Display the distance on the color image
        cv2.putText(color_image, distance_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Draw a circle at the center pixel
        cv2.circle(color_image, (center_x, center_y), 5, (0, 0, 255), -1)
        cv2.circle(depth_image, (center_x, center_y), 5, (255, 255, 255), -1)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.circle(depth_colormap, (center_x, center_y), 5, (255, 255, 255), -1)

        # Show images
        cv2.imshow('RealSense - Color', color_image)
        cv2.imshow('RealSense - Depth', depth_colormap)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop streaming
    pipeline.stop()
    cv2.destroyAllWindows()
