# WRITER THREAD
#
# file: writerThread.py
# date: 7 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#
import cv2, sys
import Queue

running = True

# Function for parsing the tuple and writing the frame to a file using a 
# naming scheme that indicates the camera number and the timestamp. 
def writeFrame(frameData):
	# Parse the information from frameData.
	frame = frameData[0]
	timestampStr = str(frameData[1])
	cameraNumberStr = str(frameData[2])
	# Format the filename.
	filename = 'view' + cameraNumberStr + '_' + timestampStr
	# Create the new file and write the frame out as binary.
	f = open(filename, 'w')
	f.write(frame.tostring())
	f.close

# The main function to run when the thread is created.
def main(frameQ):
	print 'Initializing the writer thread.'

	# Continuously check the queue for a new frame tuple from the controller.
	while running:
		# Pick up the next frame if the queue is not empty.
		if not frameQ.empty():
			# Write the next frame to file.
			writeFrame(frameQ.get())

	



