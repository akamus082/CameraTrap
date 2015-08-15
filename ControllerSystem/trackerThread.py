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

	def getFrame():
		self.lock.acquire()
		frame = self.frameQ.get()
		self.lock.release()
		return frame

	def run(self):
		print str(self.name) + ': Initializing the tracker thread.'

		# Function to switch cameras to the left: self.parent.moveLeft()
		# Function to switch cameras to the right: self.parent.moveRight()

		# Write code here...
		while True:
			time.sleep(2)
			self.parent.moveRight()
			time.sleep(2)
			self.parent.moveLeft()
			

		# pull the current frame from the queue with self.getFrame()


		self.parent.finish()  # Tell the Controller Thread that tracking is finished.

		print str(self.name) + ": DONE"
