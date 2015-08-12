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
import cv2
from datetime import datetime
import time
from threading import Thread, current_thread


class Controller(object):
	def __init__(self):
		self.name = "controller"
		self.writerQ = Queue.Queue(maxsize=0)
		self.trackerQ = Queue.Queue(maxsize=1)

		self.lock = threading.RLock()

		self.currentDev = 0

		self.cap = cv2.VideoCapture(self.currentDev)
		self.cap.set(3,800)
		self.cap.set(4,600)
		#self.cap.release()



		print str(self.name) + ": initializing the controller"

	def createWriter(self):
		print str(self.name) + ": creating the writer"
		writer = writerThread.Writer(self.writerQ, parent=self)
		return writer

	def createTracker(self):
		print str(self.name) + ": creating the tracker"
		tracker = trackerThread.Tracker(self.trackerQ, self.lock, parent=self)
		return tracker


	def callback(self, devnum):
		self.currentDev = devnum
		self.lock.acquire()
		self.cap.release()
		self.cap.open(self.currentDev)
		self.lock.release()


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
 		while True:
 			self.lock.acquire()
			ret, frame = self.cap.read()
			self.lock.release()
			if ret:
				#print str(self.name) + ": got a frame."
				timestamp = datetime.utcnow().strftime('%y%m%d%H%M%S%f')
				devNum = self.currentDev  # this needs to be changed by the controller later.
				
				filename = 'cam' + str(devNum) + '_' + timestamp


				tup = (frame, timestamp, devNum)
				self.writerQ.put(tup)
				cv2.imshow('frame', frame)
		        if cv2.waitKey(1) & 0xFF == ord('q'):
		        	break


if __name__=='__main__':
	controller = Controller()
	controller.control() # The writer and tracker are created by the controller
					 # so they will be started by it, not here.
	

############################################################################


# def printThread(myStr):
# 	print current_thread().name + ": " + myStr


# # Callback function for changing camera state. Might take in arguments that
# # mean move main viewing window left or right of the current viewing window.



# # Frame distribution function for continuously sending frames to the writer and
# # the tracker. The writer needs a tuple containing the frame, timestamp and
# # the camera number.

# #def frameCapture(devnum):


# def main():
# 	# Detect cameras and set them up with video captures. The controller should
# 	# be aware of the physical camera setup (in some way) so that it can react
# 	# appropriately when the callback function is called and knows which camera
# 	# the tracker needs next.
# 	cap0 = cv2.VideoCapture(0)    # This is gonna need to be much more automatic...probably something with serial numbers
# 	cap0.set(3,640)   #Match width
# 	cap0.set(4,480)   #Match height

# 	cap1 = cv2.VideoCapture(1)
# 	cap1.set(3,640)
# 	cap1.set(4,480)

# 	# Make queues etc. for the other threads.
# 	trackerQ = Queue.Queue(maxsize=1) # not sure if the maxsize arg is necessary
# 	writerQ = Queue.Queue(maxsize=0)

# 	# Create threads for the writer and the tracker.
# 	writer = threading.Thread(target=writerThread.write, args=(writerQ,))
# 	tracker = threading.Thread(target=trackerThread.track, args=(trackerQ,callbackQ,))

# 	# Name the threads. This is useful for debugging.
# 	writer.setName('Writer')
# 	tracker.setName('Tracker')

# 	# Start the writer and tracker threads.
# 	writer.start()
# 	tracker.start()

# 	x = 0

# 	while True:
# 		try:
# 			callback = callbackQ.get(False)
# 		except Queue.Empty:
# 			break

# 		printThread(str(callback))

# 		printThread(str(x))
# 		x += 1

# 	# Begin controlling frame distribution. (check parameters each time to see 
# 	# if callback happened)


# 	# #### below is mostly just test code for now. ####
# 	# q = Queue.Queue()

# 	# t = threading.Thread(target=writerThread.write, args=(q,))
# 	# t.start()

# 	# printThread('hi from main')
# 	# cap = cv2.VideoCapture(0)
# 	# cap.set(3,640)   #Match width
# 	# cap.set(4,480)   #Match height

# 	# starttime = time.time()
# 	# while (time.time() - starttime) < 5:
# 	# 	ret, frame = cap.read()
# 	# 	if ret:
# 	# 		timestamp = datetime.utcnow().strftime('%y%m%d%H%M%S%f')
# 	# 		devNum = 0  # this needs to be changed by the controller later.
# 	# 		tup = (frame, timestamp, devNum)
# 	# 		q.put(tup)
	
# 	# #t.join()

# if __name__=='__main__':
# 	print ": starting program"
# 	main()