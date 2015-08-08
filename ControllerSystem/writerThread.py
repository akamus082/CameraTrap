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

running = True

# Function for parsing the tuple and writing the frame to a file using a 
# naming scheme that indicates the camera number and the timestamp. 
def writeFrame(frameData):
	# Parse the information from frameData.
	frame = frameData[0]
	timestampStr = str(frameData[1])
	cameraNumberStr = str(frameData[2])
	# Format the filename.
	filename = 'cam' + cameraNumberStr + '_' + timestampStr
	# Create the new file and write the frame out as binary.
	f = open(filename, 'w')
	f.write(frame.tostring())
	f.close

# The main function to run when the thread is created.
def write(frameQ):
	print 'Initializing the writer thread.'

	starttime = time.time()
	# Continuously check the queue for a new frame tuple from the controller.
	while (running) and (time.time() - starttime < 2):
		# Pick up the next frame if the queue is not empty.
		if not frameQ.empty():
			# Write the next frame to file.
			frame = frameQ.get()
			writeFrame(frame)
			starttime = time.time()


		



