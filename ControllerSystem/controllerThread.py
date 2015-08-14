# CONTROLLER THREAD
#
# file: controllerThread.py
# date: 7 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#

# To postprocess the video in the command line:
# cat cam* | avconv -f rawvideo -pix_fmt bgr24 -s 640x480 -r 30 -i - -an -f avi -q:v 2 -r 30 test.avi


import threading
import Queue
import writerThread
import trackerThread
import devmap
import cv2
from datetime import datetime
import time
from threading import Thread, current_thread


class Controller(object):
	def __init__(self, ports, isCircle, firstCamera):
		self.name = "controller"

		self.isRunning = True

		# Make queues for communicating with other threads.
		self.writerQ = Queue.Queue(maxsize=0)
		self.trackerQ = Queue.Queue(maxsize=1)

		# Create a lock for safely using the callback function.
		self.lock = threading.RLock()

		
		self.is360 = isCircle  # I need to consider the case when this is true too it will be pretty different.
		#self.portList = ["1-1.1", "1-1.2", "1-1.3", "1-1.4"] # THIS SHOULD BE SLIGHTLY MORE AUTOMATED MAYBE???
		self.portList = ports
		self.numCameras = len(self.portList)
		# I will arbitrarily declare here that the port numbers count min to max and left to right.
		
		self.currentDev = 0 # for initialization.
		self.currentPort = None  # takes care of edge case where no ports were selected.
		if len(self.portList) > 0:
			self.currentPort = self.portList[firstCamera]
			print "current port: " + str(self.currentPort)
			self.currentDev = devmap.getdevnum(self.currentPort)

		self.cap = cv2.VideoCapture(self.currentDev)
		self.cap.set(3,640)
		self.cap.set(4,480)

		print str(self.name) + ": initializing the controller"

	def createWriter(self):
		print str(self.name) + ": creating the writer"
		writer = writerThread.Writer(self.writerQ, parent=self)
		return writer

	def createTracker(self):
		print str(self.name) + ": creating the tracker"
		tracker = trackerThread.Tracker(self.trackerQ, self.lock, parent=self)
		print "Port List = " + str(self.portList)
		return tracker

	def finish(self):
		self.isRunning = False

	# callback function for the tracker to tell the view to move left
	def moveLeft(self):
		self.currentDev = self.getCameraLeft()
		self.lock.acquire()
		self.cap.release()
		self.cap.open(self.currentDev)
		self.lock.release()


	# callback function for the tracker to tell the view to move right
	def moveRight(self):
		self.currentDev = self.getCameraRight()
		self.lock.acquire()
		self.cap.release()
		self.cap.open(self.currentDev)
		self.lock.release()	


	# Should return the devnum of the camera to the left.
	def getCameraRight(self):
		nextPort = self.currentPort
		currentIndex = self.portList.index(self.currentPort)
		if currentIndex > 0:
			nextPort = self.portList[currentIndex - 1]
		elif self.is360 == True and currentIndex == 0:
			nextPort = self.portList[-1]
		print "nextport = " + str(nextPort)
		self.currentPort = nextPort
		return devmap.getdevnum(nextPort) 
		

	def getCameraLeft(self):
		nextPort = self.currentPort  # If this is the last camera in the array, it should just continue recording.
		currentIndex = self.portList.index(self.currentPort)
		print "currentIndex = " + str(currentIndex)
		if currentIndex < self.numCameras - 1:
			nextPort = self.portList[currentIndex + 1]
		elif self.is360 == True and currentIndex == self.numCameras - 1:
			nextPort = self.portList[0]
		print "nextport = " + str(nextPort)
		self.currentPort = nextPort
		return devmap.getdevnum(nextPort)


	def control(self):
		writer = self.createWriter()
		tracker = self.createTracker()

		writer.start()
		tracker.start()

		# starttime = time.time()
 	# 	while (time.time() - starttime) < 10:
 		#self.cap.open(self.currentDev)
 		print self.cap.get(3)
 		print self.cap.get(4)
 		while self.isRunning:
 			self.lock.acquire()
			ret, frame = self.cap.read()
			self.lock.release()
			if ret:
				#print str(self.name) + ": got a frame."
				timestamp = datetime.utcnow().strftime('%y%m%d%H%M%S%f')
				devNum = self.currentDev  # this needs to be changed by the controller later.
				
				filename = 'cam' + str(devNum) + '_' + timestamp

				tup = (frame, timestamp, devNum, self.isRunning)
				self.writerQ.put(tup)
				cv2.imshow('frame', frame)
		        if cv2.waitKey(1) & 0xFF == ord('q'):
		        	break
		writer.join()
		tracker.join()

if __name__=='__main__':
	orderedPorts = ["1-1.1", "1-1.2", "1-1.3", "1-1.4"]
	firstCamera = 1

	controller = Controller(ports=orderedPorts, isCircle=True, firstCamera=1)
	controller.control() # The writer and tracker are created by the controller
					 	 # so they will be started by it, not here.
	
