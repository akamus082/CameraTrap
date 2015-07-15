import cv2

class Camera:
	''' The camera. '''

	def __init__ (self, devNum, resolution_x, resolution_y)
		self.dev = devNum
		self.width = resolution_x
		self.height = resolution_y

		cam = cv2.VideoCapture(self.dev)
		cam.set



