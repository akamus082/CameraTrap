import cv2
import numpy as np

class ImgDiff(self):

	def __init__(self):
	self.video_in = cv2.VideoCapture(0)

	def getFrame(self):
	self.got_frame, self.frame = self.video_in.read()
	return self.got_frame, self.frame

	def imgDiff(self, frame):

		running_average_in_display = frame
		avg = np.float32(frame)
		display_image = frame.copy()

		#smooth image
		blur = cv2.GaussianBlur(display_image,(5,5),0)

		#calculate running avg
		cv2.accumulateWeighted(blur,avg,0.5)
		res = cv2.convertScaleAbs(avg)
		cv2.convertScaleAbs(avg,running_average_in_display, 1.0, 0.0)

		#get the difference between avg and image
		difference = cv2.absdiff(display_image, running_average_in_display)

		#convert image to grayscale
		img_grey = cv2.cvtColor(difference, cv2.COLOR_RGB2GRAY)

		#compute threshold
		ret,img_grey = cv2.threshold( img_grey, 2, 255, cv2.THRESH_BINARY )

		#smooth and threshold again to eliminate sparkles
		img_grey = cv2.GaussianBlur(img_grey,(5,5),0)
		ret,img_grey = cv2.threshold( img_grey, 240, 255, cv2.THRESH_BINARY )