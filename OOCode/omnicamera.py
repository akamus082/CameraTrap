import cv2
import numpy as np
import CameraTrapCV as CTCV

MIN_BLOB_SIZE = 10

class OmniCamera:

	def __init__(self):
		self.video_in = cv2.VideoCapture(0)
		self.ctcv = CTCV.CameraTrapCV()

	def getFrame(self):
		self.got_frame, self.frame = self.video_in.read()
		return self.got_frame, self.frame

	def getContour(self, img_thresh):
		return self.ctcv.getLargestContourIndex(img_thresh)

	def trackFrame(self, frame):
		img_out = frame
		x_pos = 0
		y_pos = 0
		mask = np.zeros(frame.shape, dtype=np.uint8)
		height, width, channels = frame.shape
		cv2.circle(frame, (312,262), 62, (0,0,0), -1)
		cv2.circle(mask, (312,262), 160, (255,255,255), -1)
		frame = frame & mask
		img_thresh = self.ctcv.bg_subtractor.apply(frame, None, 0.01)
		
		if np.count_nonzero(img_thresh) > 5:
			max_index = self.getContour(img_thresh)
			if cv2.contourArea(self.ctcv.contours[max_index]) >= MIN_BLOB_SIZE:
				img_out = np.zeros(img_thresh.shape).astype(np.uint8)
				cv2.drawContours(img_out, self.ctcv.contours, max_index, (255, 255, 255), -1)
				x_pos, y_pos = self.ctcv.getCentroid(self.ctcv.contours[max_index])
                theta = self.ctcv.getPolar(312,262, x_pos, y_pos)
                print theta
                return img_out, theta
		
		return np.zeros(frame.shape).astype(np.uint8), x_pos