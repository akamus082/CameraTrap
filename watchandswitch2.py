import time
from threading import Thread
import numpy as np
import cv2
import runavg
import Queue


class Watcher(Thread):

	def __init__(self, dev, qin, qout):
		''' Constructor for the watcher threads '''
		Thread.__init__(self)
		self.dev = dev
		self.qin = qin
		self.qout = qout
		self.running = True
		self.cap = cv2.VideoCapture(dev)
		self.cap.set(3, 640)
		self.cap.set(4, 480)
		cv2.namedWindow(str(self.dev), cv2.WINDOW_NORMAL)


	def run(self):
		''' Run the Watcher thread instance '''
		while True:
			ret, frame = self.cap.read(self.dev)
			print "entered OUTER while loop"
			#running_average_in_display = frame
			#avg = np.float32(frame)
			while ret:
				print "entered INNER while loop"
				#frame_copy = frame.copy()
				#trackedImg, x, y = runavg.track(frame_copy,running_average_in_display, avg)
				#print "thread " + str(self.dev) + " " + str(x) + ", " + str(y)
				ret, frame = self.cap.read(self.dev)

				# if not self.qin.empty():
				# 	signal = self.qin.get()
				# 	print str(signal)

					# if signal == 0: # 0 tells the camera to stop
					# 	self.turnOff()
					# 	time.sleep(5)
					# 	self.turnOn()
					# 	print "done turning on and off again"
					# 	#cv2.destroyWindow(str(self.dev))
					#  	#return
					 	
				if self.cap.isOpened():
					print "cap is opened, showing frame"
					cv2.imshow(str(self.dev), frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					print "this is the waitkey, it should only happen on q"
					running = False
					return
		print "this is before the final return"
		return


	def turnOff(self):
	 	self.cap.release()

	def turnOn(self):
		self.cap.open(self.dev)
	


def main(args):
	t0_in = Queue.Queue()
	t0_out = Queue.Queue()
	t1_in = Queue.Queue()
	t1_out = Queue.Queue()

	t0 = Watcher(0, t0_in, t0_out)
	t1 = Watcher(1, t1_in, t1_out)

	t0.start()
	t1.start()

	t0_in.put("hello thread 0!")

	# while True:
	# 	if not t0_in.empty():
	# 		print t0_in.get()



	
	t1_in.put("hello thread 1!")


	#t1_in.put(0)

	#t0.join()
	#t1.join()
	time.sleep(4)
	t1.turnOff()
	time.sleep(4)
	t1.turnOn()
	



if __name__ == '__main__':
	import sys
	main(sys.argv[1:])


