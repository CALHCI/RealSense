import apriltag
import numpy as np
import pyrealsense2 as rs
import cv2
import argparse
import time

class DetectionError(Exception):
	"""Exception raised when the camera fails to detect an AprilTag"""
	pass

def draw_details(tag, img):
	"""Modify image to draw a bounding box, center, and id number on top of
	the april tags to show additional information.

	Args:
		tag (AprilTag): April tag object
		img (Image): Opencv image object
	"""
	(ptA, ptB, ptC, ptD) = tag.corners
	ptB = (int(ptB[0]), int(ptB[1]))
	ptC = (int(ptC[0]), int(ptC[1]))
	ptD = (int(ptD[0]), int(ptD[1]))
	ptA = (int(ptA[0]), int(ptA[1]))

	# Draw bounding box.
	cv2.line(img, ptA, ptB, (0, 255, 0), 2)
	cv2.line(img, ptB, ptC, (0, 255, 0), 2)
	cv2.line(img, ptC, ptD, (0, 255, 0), 2)
	cv2.line(img, ptD, ptA, (0, 255, 0), 2)

	# Draw the center.
	(cX, cY) = (int(tag.center[0]), int(tag.center[1]))
	cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)

	cv2.putText(img, "ID: " + str(tag.tag_id), (ptA[0], ptA[1] - 15),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def get_average_pos(arr):
	"""Based on a given list of coordinates, find the average x, y, and z of a
	every tag in the array.

	Args:
		arr (List): 2D List containing coordinates grouped by id

	Returns:
		Tuple: A tuple which returns (x, y, z)
	"""
	arr = np.array(arr)
	return (np.mean(arr[:, 0]), np.mean(arr[:, 1]), np.mean(arr[:, 2]))


def get_pos_of_dividers(pipe, reverse=False):
	"""Return the x of both AprilTags with IDs of 0 in sorted order (or in reverse
	sorted order depending on the camera's orientation).

	Args:
		pipe (PipeLine): Intel Realsense pipeline
		reverse (boolean): Whether to output the boundaries in reverse

	Returns:
		Tuple: A tuple which stores the x of both dividers in sorted order
	"""
	# Set up April Tag detector to work with "tag36h11" tags.
	options = apriltag.DetectorOptions(families="tag36h11")
	detector = apriltag.Detector(options)

	# Take a picture.
	frame = pipe.wait_for_frames()
	color_frame = frame.get_color_frame()
	img = np.asanyarray(color_frame.get_data())

	# Get calibration results.
	intr = color_frame.profile.as_video_stream_profile().intrinsics
	camera_matrix = np.array([[intr.fx, 0, intr.ppx],
							[0, intr.fy, intr.ppy],
							[0, 0, 1]])
	dist_coeffs = np.array(intr.coeffs)

	# Modify the image to undo warping and make grayscale version for detection.
	img = cv2.undistort(img, camera_matrix, dist_coeffs)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	found_tags = []

	for april_tag in detector.detect(gray):
		if april_tag.tag_id == 0:
			# Get 3D pose of the AprilTag. Change tag_size to the tag size.
			# e1 and e2 represent error (no idea how to use)
			mtx = [intr.fx, intr.fy, intr.ppx, intr.ppy]
			pose, e1, e2 = detector.detection_pose(april_tag, mtx, tag_size=1)

			# Extract translation vectors from pose.
			found_tags.append(pose[:-1, 3])
	
	if len(found_tags) < 2:
		raise ValueError("Two AprilTag dividers not found.")
	elif len(found_tags) > 2:
		raise ValueError("Too many AprilTag dividers found.")
	else:
		if reverse:
			return (max(found_tags[0][0], found_tags[1][0]),
					min(found_tags[0][0], found_tags[1][0])
				)
		else:
			return (min(found_tags[0][0], found_tags[1][0]),
					max(found_tags[0][0], found_tags[1][0])
				)
	
	


def get_average_location_of_id(pipe, n, headless=True):
	"""Take a picture and locate average location of each tag. So get the
	average location of all tags with ID 1 and all tags with ID 2 and so on.

	Args:
		pipe (PipeLine): Intel Realsense pipeline
		n (int): Quantity of all tower of hanoi blocks
		headless (boolean): Hide debug image if true

	Returns:
		List: List of tuples which store average (x, y, z) in the order of ID
	"""

	# Set up April Tag detector to work with "tag36h11" tags.
	options = apriltag.DetectorOptions(families="tag36h11")
	detector = apriltag.Detector(options)

	# Take a picture.
	frame = pipe.wait_for_frames()
	color_frame = frame.get_color_frame()
	img = np.asanyarray(color_frame.get_data())

	# Get calibration results (loads fx, fy, cx, and cy).
	intr = color_frame.profile.as_video_stream_profile().intrinsics
	camera_matrix = np.array([[intr.fx, 0, intr.ppx],
							[0, intr.fy, intr.ppy],
							[0, 0, 1]])
	dist_coeffs = np.array(intr.coeffs)

	# Modify the image to undo warping and make grayscale version for detection.
	img = cv2.undistort(img, camera_matrix, dist_coeffs)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Stores all coordinates of each id.
	coords = [[] for _ in range(n)]
	
	for april_tag in detector.detect(gray):
		if april_tag.tag_id <= n and april_tag.tag_id > 0:
			# Draw bounding box, center, and id on top of each tag.
			if not headless: draw_details(april_tag, img)

			# Get 3D pose of the AprilTag. Change tag_size to the tag size.
			# e1 and e2 represent error (no idea how to use)
			mtx = [intr.fx, intr.fy, intr.ppx, intr.ppy]
			pose, e1, e2 = detector.detection_pose(april_tag, mtx, tag_size=1)

			# Extract translation and rotation vectors from pose.
			rvec, tvec = pose[:-1, :3], pose[:-1, 3]

			# Store translation vector in coordinates array at its id's list.
			coords[april_tag.tag_id - 1].append(tvec)
	
	# Show image with bounding boxes.
	if not headless: 
		cv2.imshow("Out", img)
		cv2.waitKey(1)

	return [get_average_pos(coord) for coord in coords if coord]

def get_hanoi_tower(arr, left_boundary, right_boundary):
	"""From the tag locations, determine which rod the rings a part of and in
	what order they're in to generate a tower of hanoi frame.

	Args:
		arr (List): List of each hanoi block location in 3d space in order of ID
		left_boundary (double): x value which separates rod 1 and rod 2
		right_boundary (double): x value which separates rod 3 and rod 2

	Returns:
		List: Rods and the rings on them in their corresponding order
	"""
	rod_1 = []
	rod_2 = []
	rod_3 = []

	# Split locations into their rods based on their x value relative to the boundaries.
	for i, coord in enumerate(arr):
		if coord[0] < left_boundary:
			rod_1.append((i + 1, coord[1]))
		elif coord[0] > right_boundary:
			rod_3.append((i + 1, coord[1]))
		else:
			rod_2.append((i + 1, coord[1]))

	# Sort based on y value.
	rod_1 = sorted(rod_1, key=lambda item: item[1], reverse=True)
	rod_2 = sorted(rod_2, key=lambda item: item[1], reverse=True)
	rod_3 = sorted(rod_3, key=lambda item: item[1], reverse=True)

	return [
		[item[0] for item in rod_1],
		[item[0] for item in rod_2],
		[item[0] for item in rod_3]
	]


if __name__ == "__main__":
	# Set up args.
	parser = argparse.ArgumentParser(description="Track AprilTags on a hanoi tower to \
												return its digital state.")
	parser.add_argument("--debug", action="store_true", help="enable debug mode")
	parser.add_argument("n", type=int, help="amount of rings")
	parser.add_argument("-d", "--delay", default=0, type=int, help="delay in \
														milliseconds between message")
	args = parser.parse_args()

	# Set up Intel Realsense camera.
	pipe = rs.pipeline()
	cfg = rs.config()
	cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
	pipe.start(cfg)

	# Get both x values of tags seperating the rods
	try:
		left_boundary, right_boundary = get_pos_of_dividers(pipe, reverse=False)
	except Exception as e:
		if args.debug:
			left_boundary, right_boundary = 0, 0
			print("Error: ", e)
			print("Continuing with boundaries set to 0...")
			time.sleep(3)
		else:
			raise DetectionError(e)

	# Prints the state of the hanoi tower
	while True:
		try:
			print(get_hanoi_tower(
				get_average_location_of_id(pipe, args.n, not args.debug),
				left_boundary,
				right_boundary
			))
			time.sleep(args.delay / 1000.0)
		except KeyboardInterrupt:
			print("\nCtrl+C detected. Exiting...")
			break
	
	pipe.stop()
	cv2.destroyAllWindows()
