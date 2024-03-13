import cv2
import numpy as np
import glob
import os

def create_calibration_file(input_folder_path, output_file, vert_x, vert_y):
    """Take in a folder of chessboard images and store fx, fy, cx, and cy of
    the camera (focal length, focal width, "center" x, and "center" y) into a
    numpy calibration file.

    Args:
        input_folder_path (string): Path to files named "chessboard_*.png"
		output_file (string): File path to output numpy calibration file
        vert_x (int): Count of verticals on x-axis of the chessboard (number of
        squares on the x-axis minus 1)
        vert_y (int): Count of verticals on y-axis of the chessboard (number of
        squares on the y-axis minus 1)
    """

    # Termination criteria for the corner sub-pixel algorithm.
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    objp = np.zeros((vert_y * vert_x, 3), np.float32)
    objp[:, :2] = np.mgrid[0:vert_x, 0:vert_y].T.reshape(-1, 2)

    objpoints = []  # 3D points in real world space.
    imgpoints = []  # 2D points in image plane.

    images = []  # List of chessboard images.

    for fname in glob.glob(os.path.join(input_folder_path, "chessboard_*.png")):
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners.
        ret, corners = cv2.findChessboardCorners(gray, (vert_x, vert_y), None)

        # If found, add object points, image points (after refining them).
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria
            )
            imgpoints.append(corners2)

            # Draw and save the corners on the chessboard.
            img = cv2.drawChessboardCorners(
                img, (vert_x, vert_y), corners2, ret
            )
            images.append(img)

    # Perform camera calibration.
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    print("Camera matrix : \n")
    print(mtx)
    print("dist : \n")
    print(dist)
    print("rvecs : \n")
    print(rvecs)
    print("tvecs : \n")
    print(tvecs)

    # Save the calibration results for later use.
    np.savez(output_file, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)


if __name__ == "__main__":
    # Uses the chessboard images in "images/" to make "calibration_results.npz".
    create_calibration_file("images/", "calibration_results.npz", 8, 6)