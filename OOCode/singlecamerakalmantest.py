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

import numpy as np
import cv2
import trackingalgos as ta
import camera as Camera
from kalman2d import Kalman2D
import time

myCamera0 = Camera.Camera(0, "cam0.avi")

winName = "0"

print "preparing camera"
kalman2d0 = Kalman2D()
measured_points0 = []

measured0 = (0,0)

got_frame0, frame0 = myCamera0.getAndWriteFrame()
t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
avg_daw0 = np.float32(t0)

prev_x0 = int(640/2)
prev_y0= int(480/2)


while(myCamera0.isOn()):
		
	got_frame0, frame0 = myCamera0.getAndWriteFrame()
	t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
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

	drawCross(frame0, estimated0, 255, 255, 255)
	drawCross(frame0, measured0, 0,   0,   255)

	cv2.imshow( winName[0], frame0 )
	
	delta_x0 = prev_x0 - estimated0[0]
	
	
	if(prev_x0 > 0):
		

		if((delta_x0 > 0) and (prev_x0 >= 600)):
			print "turn camera 1 on"
			#myCamera1.on()
			prev_x1 = int(640/2)

		
		if((delta_x0 < 0) and (prev_x0 <= 40)):
			print "turn camera 2 on"
			#myCamera2.on()
			prev_x2 = int(640/2)
		

	key = cv2.waitKey(1)
	if key == 27:
		cv2.destroyWindow("0")
		myCamera0.off()
		break

	
print 'Done.'
