# TRACKER THREAD
#
# file: trackerThread.py
# date: 7 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#

import Queue

# Any functions that can be split into parts for simplicity can go here.

def main():
	print 'Initializing the tracker thread.'

	# Pick up the avaliable frame from the controller. Consider sending the
	# frames as a tuple (frame, camera number) so the tracker can be aware
	# that its view has changed.

	# Use the frame to run the tracking algorithm.

	# If the algorithm says that the cameras should switch to the left or right,
	# run the controller's callback function to change the camera state.

