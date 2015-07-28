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

myCamera0 = Camera.Camera('../videos/bearvid1.mp4', "cam0.avi")

winName = "1", "2"



previous_x = int(640/2)
center = int(640/2)


# These will get the trajectories for mouse location and Kalman estiamte
measured_points = []
kalman_points = []
prev_x = int(640/2)
prev_y = int(480/2)
#measured
# Create a new Kalman2D filter and initialize it with starting mouse location
kalman2d = Kalman2D()

while(myCamera0.isOn()):

	print "camera 0 is on"
	got_frame0, frame0 = myCamera0.getFrame()

	t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
	f = t.copy()
	avg_daw = np.float32(f)
	gray = t.copy()
	running_average_in_display = frame0
	
	avg_ra = np.float32(frame0)
	
	previous_x = center
	
	while got_frame0:
		frame_copy = frame0.copy()

		#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
		
		#masked_img0, x0, y0 = ta.runningAvg(frame_copy,running_average_in_display, avg_ra)
		
		masked_img1, x1, y1 = ta.diffaccWeight(f,t,gray, avg_daw)
		
		if((x1 != -1) | (y1 != -1)):
			measured = (x1,y1)
			prev_x = x1
			prev_y = y1
			measured_points.append(measured)
		else:
			measured = (prev_x,prev_y)
			measured_points.append(measured)

		#print measured[0], measured[1]

		measured_points.append(measured)
		kalman2d.update(measured[0], measured[1])

		estimated = [int (c) for c in kalman2d.getEstimate()]
		kalman_points.append(estimated)


		#drawLines(frame0, kalman_points,   0,   255, 0)
		drawCross(frame0, estimated,       255, 255, 255)
		#drawLines(frame0, measured_points, 255, 255, 0)
		drawCross(frame0, measured, 0,   0,   255)

		cv2.imshow( winName[1], masked_img1 )
		cv2.imshow( winName[0], frame0 )
		got_frame0, frame0 = myCamera0.getFrame()

		'''delta_x = x - previous_x

		if(x):
			if((delta_x < 0) and (x <= 60)):
				myCamera2.on()
				myCamera0.off()
			
			if((delta_x > 0) and (x >= 580)):
				myCamera1.on()
				myCamera0.off()
		
		previous_x = x
		'''
		#prev_x = x1
		#prev_y = y1
		t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		key = cv2.waitKey(10)
		if key == 27:
			cv2.destroyWindow("1")
			myCamera0.off()
			break