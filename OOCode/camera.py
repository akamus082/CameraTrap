import numpy as np
import cv2
import time

class Camera:
	
	def __init__(self, deviceNumber, filename):
		self.devNum = deviceNumber
		self.filename = filename
		self.filecount = 0
		#self.inUse = False
		self.cap = cv2.VideoCapture(self.devNum)

	def on(self):
		# turn the camera on
		#self.inUse = True
		self.cap.open(self.devNum)

	def off(self):
		# turn the camera off
		#self.inUse = False
		self.cap.release()

	def isOn(self):
		# return true if the camera is on
		return self.cap.isOpened()
		
	def isOff(self):
		# return true if the camera is off
		return not self.cap.isOpened()

	def getFrame(self):
		# get the next video frame
		self.got_frame, self.frame = self.cap.read()
		return self.got_frame, self.frame
	
	def getName(self):
		return str(self.filename)

	def getDev(self):
		return deviceNumber



# myCamera = Camera(0, "mytestfile.avi")

# myCamera.on()
# time.sleep(2)
# print (myCamera.isOn() == True)
# print (myCamera.isOff() == False)
# time.sleep(2)
# myCamera.off()
# print myCamera.isOn()
# print myCamera.isOff()

# print "goodbye"

