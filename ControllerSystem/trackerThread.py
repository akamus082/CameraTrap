# TRACKER THREAD
#
# file: trackerThread.py
# date: 14 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#
import cv2, sys
import Queue
from threading import Thread, current_thread
import threading
import time


class Tracker(Thread):

	def __init__(self, queue, lock, parent=None):
		threading.Thread.__init__(self)
		self.parent = parent
		self.setName("tracker")
		self.frameQ = queue
		self.lock = lock
		self.lastFrame = None

	def getFrame(self):
		#self.lock.acquire()
		if not self.frameQ.empty():
			frame = self.frameQ.get()
			self.lastFrame = frame
			return frame
		#self.lock.release()
		return self.lastFrame

	def run(self):
		print str(self.name) + ': Initializing the tracker thread.'

		# Function to switch cameras to the left: self.parent.moveLeft()
		# Function to switch cameras to the right: self.parent.moveRight()

		# Write code here...
		while self.frameQ.empty():
			print "waiting on contoller for initial Q value."
			time.sleep(0)

		#firstFrame = self.getFrame()

		while True:
			# time.sleep(2)
			# self.parent.moveRight()
			# time.sleep(2)
			# self.parent.moveLeft()
			print "size " + str(self.frameQ.qsize())

			# frame = self.getFrame()


			# cv2.imshow('frame', frame)
			# if cv2.waitKey(1) & 0xFF == ord('q'):
		 # 		break
			

			for x in range(100):
				print x
				frame = self.getFrame()

				cv2.imshow('frame', frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
			 		break
			
			self.parent.moveLeft()

			for x in range(100):
				print x
				frame = self.getFrame()

				cv2.imshow('frame', frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
			 		break
			

		# pull the current frame from the queue with self.getFrame()


		self.parent.finish()  # Tell the Controller Thread that tracking is finished.

		print str(self.name) + ": DONE"
