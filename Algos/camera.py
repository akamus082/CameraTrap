import numpy as np
import cv2
import time

class Camera:
	
	def __init__(self, deviceNumber, filename):
		self.devNum = deviceNumber
		self.filename = filename
		self.filecount = 0
		self.cap = cv2.VideoCapture(self.devNum)

	def on(self):
		# turn the camera on
		self.cap.open(self.devNum)

	def off(self):
		# turn the camera off
		self.cap.release()

	def isOn(self):
		# return true if the camera is on
		return self.cap.isOpened()
		
	def isOff(self):
		# return true if the camera is off
		return not self.cap.isOpened()

	def getFrame(self):
		# get the next video frame
		got_frame, frame = cam.read()
		return got_frame, frame



myCamera = Camera(0, "mytestfile.avi")

myCamera.on()
time.sleep(5)
print str(myCamera.isOn())
print str(myCamera.isOff())
time.sleep(5)
myCamera.off()


print "goodbye"


