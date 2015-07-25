import time
from threading import Thread
import numpy as np
import cv2
import runavg
import camera
import Queue

# Main Thread Request Signals
# 0 	Please turn off
#
#
# Watcher Thread Request Signals
# 0 	About to turn off
#
#

def watcher(dev, qin, qout):
	running = True

	cap = cv2.VideoCapture(dev)
	cap.set(3, 640)
	cap.set(4, 480)
	cap.set(5, 5.0)
	while True:
		ret, frame = cap.read(dev)
		running_average_in_display = frame
		avg = np.float32(frame)

		
		while ret:
			frame_copy = frame.copy()
			trackedImg, x, y = runavg.track(frame_copy,running_average_in_display, avg)
			print "thread " + str(dev) + " " + str(x) + ", " + str(y)
			ret, frame = cap.read(dev)

			# if x < 50:
			# 	qout.put("left")
			# elif x > 590:
			# 	qout.put("right")

			# if not qin.empty():
			# 	signal = qin.get()
			# 	print str(signal)
			# 	if signal == 0: # 0 tells the camera to stop
			# 		cv2.destroyWindow(str(dev))
			# 	 	return


			cv2.imshow(str(dev), frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				running = False
				cv2.destroyWindow(str(dev))
				return
				#break

		# if not running:
		# 	print "not running"
		# 	return
		# 	#break

	return


def main(args):

	qout = Queue.Queue()

	t0_in = Queue.Queue()
	t0_out = Queue.Queue()
	t1_in = Queue.Queue()
	t1_out = Queue.Queue()

	t0 = Thread(target=watcher, args=(0, t0_in, t0_out))
	t1 = Thread(target=watcher, args=(1, t1_in, t1_out))

	t0.start()
	t1.start()

	t1_in.put(0)

	#t0.join()
	t1.join()


if __name__ == '__main__':
	import sys
	main(sys.argv[1:])