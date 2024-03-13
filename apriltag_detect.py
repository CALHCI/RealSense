import apriltag
import numpy as np
import cv2
import time

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


def get_average_xyz(arr):
	"""Based on a given list of coordinates, find the average x, y, and z of a
	every tag in the array.

    Args:
        arr (List): 2D List containing coordinates grouped by id

    Returns:
        Tuple: A tuple which returns (x, y, z)
    """
	arr = np.array(arr)
	return (np.mean(arr[:, 0]), np.mean(arr[:, 1]), np.mean(arr[:, 2]))


def get_average_location_of_id(n, calibration_file, headless=True):
	"""Take a picture and locate average location of each tag. So get the
	average location of all tags with ID 0 and all tags with ID 1 and so on.

    Args:
        n (int): Quantity of all tower of hanoi blocks.
		calibration_file (string): File path to numpy calibration file
		headless (boolean): True to hide debug image

    Returns:
        List: List of tuples which store average (x, y, z) in the order of ID
    """
	# Set up April Tag detector to work with "tag36h11" tags.
	options = apriltag.DetectorOptions(families="tag36h11")
	detector = apriltag.Detector(options)

	# Set up the camera to take pictures.
	cam = cv2.VideoCapture(0) # Change the camera number if errors occur.
	if not cam.isOpened():
		raise ValueError("Camera not found. Maybe change cam number?")

	# Load numpy calibration results (loads fx, fy, cx, and cy).
	calib_data = np.load(calibration_file)
	mtx = [calib_data["mtx"][0][0],  # fx
			calib_data["mtx"][1][1], # fy
			calib_data["mtx"][0][2], # cx
			calib_data["mtx"][1][2]  # cy
			]

	# Take a picture.
	res, img = cam.read()
	if not res: raise ValueError("Couldn't take picture.")

	# Modify the image to undo warping and make grayscale version for detection.
	img = cv2.undistort(img,calib_data["mtx"], calib_data["dist"], None,
						calib_data["mtx"])
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Stores all coordinates of each id.
	coords = [[] for _ in range(n)]
	
	for april_tag in detector.detect(gray):
		# Draw bounding box, center, and id on top of each tag.
		if not headless: draw_details(april_tag, img)

		# Get 3D pose of the AprilTag. Change tag_size to the tag size.
		# e1 and e2 represent error (no idea how to use)
		pose, e1, e2 = detector.detection_pose(april_tag, mtx, tag_size=1)

		# Extract translation and rotation vectors from pose.
		rvec, tvec = pose[:-1, :3], pose[:-1, 3]

		# Store translation vector in coordinates array at its id's list.
		coords[april_tag.tag_id].append(tvec)
	
	# Show image with bounding boxes.
	if not headless: 
		cv2.imshow("Out", img)
		cv2.waitKey(1)

	cam.release()

	return [get_average_xyz(coord) for coord in coords if coord]

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

	for i, coord in enumerate(arr):
		if coord[0] < left_boundary:
			rod_1.append((i, coord[1]))
		elif coord[0] > right_boundary:
			rod_3.append((i, coord[1]))
		else:
			rod_2.append((i, coord[1]))

	rod_1 = sorted(rod_1, key=lambda item: item[1], reverse=True)
	rod_2 = sorted(rod_2, key=lambda item: item[1], reverse=True)
	rod_3 = sorted(rod_3, key=lambda item: item[1], reverse=True)

	return [
		[item[0] for item in rod_1],
		[item[0] for item in rod_2],
		[item[0] for item in rod_3]
	]


if __name__ == "__main__":
	# Repeatedly prints the average locations of the april tags by ID.
	print(get_hanoi_tower(
		get_average_location_of_id(4, "calibration_results.npz", False),
		4.0, # PLAY WITH THIS NUMBER A TON (and maybe swap these two around?)
		10.0 # PLAY WITH THIS NUMBER A TON
	))
	# while True:
	# 	print(get_average_location_of_id(4, "calibration_results.npz", False))