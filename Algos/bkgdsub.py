import cv2
import numpy as np

MIN_BLOB_SIZE = 30

cam = cv2.VideoCapture(0)

winName = "1", "2"
cv2.namedWindow(winName[0], cv2.CV_WINDOW_AUTOSIZE)
bg = cv2.BackgroundSubtractorMOG(history=200, nmixtures=3, backgroundRatio=0.7, noiseSigma=0)
got_frame, frame = cam.read()
while True:

	#got_frame, frame = cam.read()
	fg = bg.apply(frame)
	kernel = np.zeros((11,11),np.uint8)
	erosion = cv2.erode(fg,kernel,iterations = 1)
	dilation = cv2.dilate(erosion,kernel,iterations = 1)
	contour,hier = cv2.findContours(dilation,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(frame, contour, -1, (0, 0, 255), 2)


	cv2.imshow( winName[0], frame )
	cv2.imshow( winName[1], fg )
	# Read next image
	got_frame, frame = cam.read()
	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyWindow(winName[1])
		break

print "Goodbye"
