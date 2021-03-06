# adapted from http://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
import cv2
import sys

sys.path.append("../modules")
from camera import Camera


def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()
	
if __name__ == "__main__":
	cam = Camera(cameraNum=1)
	cv2.namedWindow("Image", flags=cv2.CV_WINDOW_AUTOSIZE)
	while True:
		image = cam.grabFrame()
		# detect focus
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		fm = variance_of_laplacian(gray)
		text = "Not Blurry"
		if fm < 100:
			text = "Blurry"
		
		# show the image
		cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
		cv2.imshow("Image", image)	
		
		# call waitKey otherwise image won't show. Max 60fps
		key = cv2.waitKey(16) & 0xFF
		if key != 255: break;
	
	cam.cleanup()	
	cv2.destroyAllWindows()
