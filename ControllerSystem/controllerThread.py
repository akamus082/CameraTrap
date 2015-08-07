# CONTROLLER THREAD
#
# file: controllerThread.py
# date: 7 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#

import threading
import Queue
import writerThread
import trackerThread

# Callback function for changing camera state. Might take in arguments that
# mean move main viewing window left or right of the current viewing window.

# Frame distribution function for continuously sending frames to the writer and
# the tracker. The writer needs a tuple containing the frame, timestamp and
# the camera number.

def main():
	# Detect cameras and set them up with video captures. The controller should
	# be aware of the physical camera setup (in some way) so that it can react
	# appropriately when the callback function is called and knows which camera
	# the tracker needs next.

	# Make queues etc. for the other threads.

	# Create threads for the writer and the tracker.

	# Start the writer and tracker threads.

	# Begin controlling frame distribution. (check parameters each time to see 
	# if callback happened)

t = threading.Thread(target=writerThread.testThread())

t.start()





if __name__=='__main__':
	print "starting program"