# TRACKER THREAD
#
# file: trackerThread.py
# date: 14 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#


import cv2, sys
import Queue
from threading import Thread, current_thread
import threading
import time
import numpy as np
import trackingalgos as ta
from kalman2d import Kalman2D


def drawCross(img, center, r, g, b):
    '''
    Draws a cross a the specified X,Y coordinates with color RGB
    '''

    d = 5
    t = 2

    color = (r, g, b)

    ctrx = center[0]
    ctry = center[1]

    cv2.line(img, (ctrx - d, ctry - d), (ctrx + d, ctry + d), color, t, cv2.CV_AA)
    cv2.line(img, (ctrx + d, ctry - d), (ctrx - d, ctry + d), color, t, cv2.CV_AA)

def track(frame, avg_daw0):
	
	#image = cv2.resize(frame,None,fx=1, fy=1, interpolation = cv2.INTER_NEAREST)

	t0 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	f0 = t0.copy()
	img_threshold, x, y = ta.diffaccWeight(f0,t0, avg_daw0)
	return img_threshold, x, y

class Tracker(Thread):

	def __init__(self, queue, lock, parent=None):
		threading.Thread.__init__(self)
		self.parent = parent
		self.setName("tracker")
		self.frameQ = queue
		self.lock = lock
		self.lastFrame = None

	def getFrame(self):
		#self.lock.acquire()
		if not self.frameQ.empty():
			frame = self.frameQ.get()
			self.lastFrame = frame
			return frame
		#self.lock.release()
		return None, None

	def run(self):
		print str(self.name) + ': Initializing the tracker thread.'

		#initialize parameters for the Kalman Filter
		kalman2d0 = Kalman2D()
		measured_points0 = []
		#kalman_points = []
		measured0 = (0,0)

		#Initialize parameters
		delta = 0
		prev_estx = 0
		prev_esty = 0
		prev_x = 0
		prev_y = 0
		frames_processed = 0
		outsideLoop = True
		insideLoop = False

		while outsideLoop:
			print "outsideLoop"

			while self.frameQ.empty():
					#print "waiting on contoller for initial Q value."
					time.sleep(0)
			
			frame = self.getFrame()
			t0 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			avg_daw0 = np.float32(t0)
			
			while (frames_processed < 15):
				if (not self.frameQ.empty()):
					frame = self.getFrame()
					track(frame, avg_daw0)
					frames_processed+=1

		#if (frames_processed == 15):
			insideLoop = True
			triggerWidthRight = frame.shape[1]*0.9
			triggerWidthLeft = frame.shape[1]*0.1
		
			while insideLoop:
				#print "inside loop"
				while self.frameQ.empty():
					#print "waiting on contoller for initial Q value."
					time.sleep(0)
				
				frame = self.getFrame()
				track_img, x, y = track(frame, avg_daw0)
					
				if((x != -1) | (y != -1)):
					
					prev_x = x
					prev_y = y
					measured0 = (x,y)
					drawCross(frame, (x, y), 0,   0,   255)
				else:
					measured0 = (prev_x, prev_y)

				measured_points0.append(measured0)
				kalman2d0.update(measured0[0], measured0[1])

				estimated0 = [int (c) for c in kalman2d0.getEstimate()]

				delta = estimated0[0] - prev_estx

				#print delta
				
				prev_estx = estimated0[0]
				prev_esty = estimated0[1]

				drawCross(frame, estimated0, 255, 255, 255)

				if((delta < 0) and (estimated0[0] < triggerWidthLeft) and (prev_x < triggerWidthLeft)):
					self.lock.acquire()
					self.frameQ.queue.clear()
					self.lock.release()
					delta = 0
					prev_estx = 0
					prev_esty = 0
					prev_x = 0
					prev_y = 0
					frames_processed = 0
					insideLoop = False
					print "moving left"
					kalman2d0 = Kalman2D()
					measured_points0 = []
					#kalman_points = []
					measured0 = (0,0)
					self.parent.moveLeft()

				if((delta > 0) and (estimated0[0] > triggerWidthRight) and (prev_x > triggerWidthRight)):
					self.lock.acquire()
					self.frameQ.queue.clear()
					self.lock.release()
					delta = 0
					prev_estx = 0
					prev_esty = 0
					prev_x = 0
					prev_y = 0
					frames_processed = 0
					insideLoop = False
					print "moving right"
					kalman2d0 = Kalman2D()
					measured_points0 = []
					#kalman_points = []
					measured0 = (0,0)
					self.parent.moveRight()
					
				cv2.imshow("frame", frame)
				key = cv2.waitKey(1)
				if key == 27:
					cv2.destroyWindow("0")
					insideLoop = False
					outsideLoop = False
					break

		self.parent.finish()  # Tell the Controller Thread that tracking is finished.

		print str(self.name) + ": DONE"
