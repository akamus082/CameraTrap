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
import cv2
from datetime import datetime
import time

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

	q = Queue.Queue()

	t = threading.Thread(target=writerThread.write, args=(q,))
	t.start()

	print 'hi from main'
	cap = cv2.VideoCapture(0)
	cap.set(3,640)   #Match width
	cap.set(4,480)   #Match height

	starttime = time.time()
	while (time.time() - starttime) < 5:
		ret, frame = cap.read()
		if ret:
			timestamp = datetime.utcnow().strftime('%y%m%d%H%M%S%f')
			devNum = 0  # this needs to be changed by the controller later.
			tup = (frame, timestamp, devNum)
			q.put(tup)
	
	#t.join()

if __name__=='__main__':
	print "starting program"
	main()