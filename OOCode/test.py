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


def drawLines(img, points, r, g, b):
    '''
    Draws lines 
    '''

    cv2.polylines(img, [np.int32(points)], isClosed=False, color=(r, g, b))


import numpy as np
import cv2
import trackingalgos as ta
import camera as Camera
import time
from kalman2d import Kalman2D

#myCamera0 = Camera.Camera('../videos/forest.mp4', "cam0.avi")
myCamera0 = Camera.Camera(0, "cam0.avi")
winName = "0", "1"

print "preparing cameras"
kalman2d0 = Kalman2D()
measured_points0 = []

measured0 = (0,0)

got_frame0, frame0 = myCamera0.getFrame()
image = cv2.resize(frame0,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
t0 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
avg_daw0 = np.float32(t0)

prev_x0 = image.shape[1]
prev_y0= image.shape[0]
image = None
while myCamera0.isOn():
	
	got_frame0, frame0 = myCamera0.getFrame()
	
	if got_frame0:
		image = cv2.resize(frame0,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)

		t0 = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		f0 = t0.copy()
		masked_img0, x0, y0 = ta.diffaccWeight(f0,t0, avg_daw0)
		

		if((x0 != -1) | (y0 != -1)):
			measured0 = (x0,y0)
			prev_x0 = x0
			prev_y0 = y0
		else:
			measured0 = (prev_x0,prev_y0)

		measured_points0.append(measured0)
		kalman2d0.update(measured0[0], measured0[1])

		estimated0 = [int (c) for c in kalman2d0.getEstimate()]

		drawCross(image, estimated0, 255, 255, 255)
		drawCross(image, measured0, 0,   0,   255)

		cv2.imshow( winName[0], image )
		
		delta_x0 = prev_x0 - estimated0[0]
		
		key = cv2.waitKey(10)
		if key == 27:
			cv2.destroyWindow("0")
			myCamera0.off()
			break

myCamera0.off()