# TRACKER THREAD
#
# file: trackerThread.py
# date: 7 AUG 2015
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


	def run(self):
		print str(self.name) + ': Initializing the tracker thread.'

		# pretend to track.....
		while True:

			time.sleep(3)
			print str(self.name) + ': ' + str(1)

	 		self.lock.acquire()
			self.parent.callback(1)
			self.lock.release()

			time.sleep(3)
			print str(self.name) + ': ' + str(0)

			self.lock.acquire()
			self.parent.callback(0)
			self.lock.release()


	# Pick up the avaliable frame from the controller. Consider sending the
	# frames as a tuple (frame, camera number) so the tracker can be aware
	# that its view has changed.

	# Use the frame to run the tracking algorithm.

	# If the algorithm says that the cameras should switch to the left or right,
	# run the controller's callback function to change the camera state.
