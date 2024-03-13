import cv2
import os

def get_chessboard_images(output_folder_path):
	"""Set up a video stream where you can press "s" to take a picture and store
	it to a folder path. Press q to quit

    Args:
        output_folder_path (string): File path of folder to store images
    """
	picture_count = 0
	cam = cv2.VideoCapture(0)
	if not cam.isOpened():
		print("Error: Could not open camera.")
		quit()

	while True:
		res, img = cam.read()

		if not res:
			print("Error: Could not read frame.")
			break
		
		cv2.imshow("Out", img)
		
		if cv2.waitKey(1) & 0xFF == ord("s"):
			save_location = os.path.join(
				output_folder_path, f"chessboard_{picture_count}.png"
			)
			cv2.imwrite(save_location, img)
			picture_count += 1
		if cv2.waitKey(1) & 0xFF == ord("q"): break

	cam.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	get_chessboard_images("images/")