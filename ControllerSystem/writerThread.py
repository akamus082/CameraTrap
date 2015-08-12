# WRITER THREAD
#
# file: writerThread.py
# date: 7 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#
import cv2, sys
import Queue
import time
import threading
from threading import Thread, current_thread


class Writer(Thread):

	def __init__(self, queue, parent=None):
		threading.Thread.__init__(self)
		self.parent = parent
		self.setName("writer") # Give the thread a human-readable name.
		self.running = True
		self.frameQ = queue
		

	# Function for parsing the tuple and writing the frame to a file using a 
	# naming scheme that indicates the camera number and the timestamp. 
	def writeFrame(self, frameData):
		# Parse the information from frameData.
		frame = frameData[0]
		timestampStr = str(frameData[1])
		cameraNumberStr = str(frameData[2])
		# Format the filename.
		filename = 'cam' + cameraNumberStr + '_' + timestampStr
		# Create the new file and write the frame out as binary.
		# f = open(filename, 'w')
		# f.write(frame.tostring())
		# f.close

	# The main function to run when the thread is created.
	def run(self):
		print str(self.name) + ': Initializing the writer thread.'
	
		starttime = time.time()
		# Continuously check the queue for a new frame tuple from the controller.
		#while (self.running) and (time.time() - starttime < 10):
		while True:
			# Pick up the next frame if the queue is not empty.
			if not self.frameQ.empty():
				# Write the next frame to file.
				frame = self.frameQ.get()
				self.writeFrame(frame)
				#print str(self.name) + ': writing a frame.'
				starttime = time.time()

		print str(self.name) + ": goodbye"
		



