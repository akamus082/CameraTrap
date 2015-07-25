import time
from threading import Thread
import numpy as np
import cv2
import runavg
import camera
import Queue


def watcher(dev, qin, qout):
	running = True
	recording = False
	waitTime = 100
	margin = 50
	startTime = 0 # initialize the startTime

	path = ('output_thread' + str(dev) + '.avi')

	#cv2.namedWindow(str(dev), cv2.WINDOW_NORMAL)  # this breaks the threading for some reason

	cap = cv2.VideoCapture(dev)
	cap.set(3, 640)
	cap.set(4, 480)
	cap.set(5, 5.0)

	


	# initialize these variables so they exist
	ret, frame = cap.read(dev)
	running_average_in_display = frame
	avg = np.float32(frame)

	cap.release()


	fourcc = cv2.cv.CV_FOURCC(*'DIV3')
	video_writer = cv2.VideoWriter(path,fourcc, 5.0, (640,480))

	while True:
		# ret, frame = cap.read(dev)
		# running_average_in_display = frame
		# avg = np.float32(frame)

		

		if not qin.empty():
			signal = qin.get()
			print "thread " + str(dev) + ": recieved signal from Main     " + str(signal)
			if signal == 1: 
				recording = True
				startTime = time.time() # startTime
				#print "cap " + str(cap)
				cap.open(dev)
				#print cap.isOpened()
				ret, frame = cap.read(dev)
				#print frame
				running_average_in_display = frame
				avg = np.float32(frame)
				#print "recording " + str(recording)
				#print "ret " + str(ret)


		while ret and recording: #this used to be (while ret)
			ret, frame = cap.read(dev)
			#print "Frame: " + str(frame)
			frame_copy = frame.copy()

			# running_average_in_display = frame
			# avg = np.float32(frame)

			trackedImg, x, y = runavg.track(frame_copy,running_average_in_display, avg)

			#print "x " + str(x)
			
			if x != 0:
				#print "updating"
				startTime = time.time() # update the timestamp if the tracker sees movement


			if x < margin:
				qout.put([dev, 3]) 	# signal main that you saw something on the left
			# should probably consider the case when something is moving a lot in
			# this part of screen and it keeps sending signals to main.

			elapsedTime = time.time() - startTime
			#print "thread " + str(dev) + ": " + str(elapsedTime)

			# Write a frame of video because not enough time has 
			# elapsed since motion was last tracked
			if elapsedTime < waitTime: 
				# flip frame before displaying so it looks more intuitive
				flippedimg = cv2.flip(frame, 1)
				cv2.imshow(str(dev), flippedimg)
				video_writer.write(frame)  # This works, just slows everything down
			# No motion detected in waitTime time. Stop the Camera.
			else:
				print "thread " + str(dev) + ": stop recording"
				cap.release()
				recording = False


			# Detect any signals from the main thread
			if not qin.empty():
				signal = qin.get()
				print "thread " + str(dev) + ": recieved signal from Main     " + str(signal)
				if signal == 0: 	# The main thread wants this camera to stop recording
					cap.release()
					recording = False  # what happens if you pull a different signal from main? gets dropped now.
				# else:
				# 	qin.put(signal) # put the signal back if it wasn't a 
									# stop signal so we can deal with it later.

			
			
			# Detect the keypress to turn off the camera. The waitKey() command is required by 
			# opencv to show images to the screen. It might not be needed if I dont want 
			# to view the video real time, and may not be needed in a final implementation.
			if cv2.waitKey(1) & 0xFF == ord('q'):
				running = False
				cap.release()
				recording = False



	if cv2.waitKey(1) & 0xFF == ord('q'): # keyboard escape from outer while loop
		cv2.destroyWindow(str(dev))
		cap.release()
		video_writer.release()
		return

	if not running:
		cv2.destroyWindow(str(dev))
		cap.release()
		video_writer.release()
		return


def main(args):

	# Create Queues for interthread communication.
	qout = Queue.Queue()
	t0_in = Queue.Queue()
	t1_in = Queue.Queue()

	# Create a thread for each camera.
	t0 = Thread(target=watcher, args=(0, t0_in, qout))
	t1 = Thread(target=watcher, args=(1, t1_in, qout))

	# Start the camera threads
	t0.start()
	t1.start()

	# Put 1 into a thread's in queue to start recording on that camera.
	# Put 0 into a thread's in queue to stop recording on that camera.




	t0_in.put(1)

	while True:
		if not qout.empty():
			signal = qout.get()
			print signal
			camnum = signal[0]
			sig = signal[1]
			print signal
			if sig == 3 and camnum == 0: # camera saw something on the left
				t1_in.put(1)
				t0_in.put(0)
			elif sig == 3 and camnum == 1:
				t0_in.put(1)
				t1_in.put(0)
	

	# print "joining threads"
	# t0.join()
	# t1.join()

	print "end of main "

	


if __name__ == '__main__':
	import sys
	main(sys.argv[1:])