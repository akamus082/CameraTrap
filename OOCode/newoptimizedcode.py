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

print 'hello world :)'

myCamera0 = Camera.Camera(0, "cam0.avi")
myCamera1 = Camera.Camera(1, "cam1.avi")
myCamera2 = Camera.Camera(2, "cam2.avi")

winName = "0", "1", "2"

print "preparing cameras"
kalman2d0 = Kalman2D()
measured_points0 = []

kalman2d1 = Kalman2D()
measured_points1 = []

kalman2d2 = Kalman2D()
measured_points2 = []

measured0 = (0,0)
measured1 = (0,0)
measured2 = (0,0)

got_frame0, frame0 = myCamera0.getFrameLowRes()
t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
avg_daw0 = np.float32(t0)
myCamera0.off()

got_frame1, frame1 = myCamera1.getFrameLowRes()
t1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
avg_daw1 = np.float32(t1)
myCamera1.off()

got_frame2, frame2 = myCamera2.getFrameLowRes()
t2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
avg_daw2 = np.float32(t2)
myCamera2.off()

# This assumes the sizes of the frames are identical for all
# cameras. Otherwise, do this for each camera.
triggerWidthRight = frame0.shape[1]*0.9
triggerWidthLeft = frame0.shape[1]*0.1
centerx = int(frame0.shape[1]/2)
<<<<<<< HEAD
centery = int(frame0.shape[0]/2)
prev_x0 = centerx
prev_x1 = centerx
prev_x2 = centerx
prev_y0 = centery
prev_y1 = centery
prev_y2 = centery
=======

prev_x0 = centerx
prev_x1 = centerx
prev_x2 = centerx
prev_y0= int(480/2)
prev_y1= int(480/2)
prev_y2= int(480/2)
>>>>>>> 200723833ddb53414b7c64ca3637b65b376d9dbf


myCamera0.on()

while(myCamera0.isOn() or myCamera1.isOn() or myCamera2.isOn()):
<<<<<<< HEAD
	'''
=======
	
>>>>>>> 200723833ddb53414b7c64ca3637b65b376d9dbf
	while myCamera0.isOn() and myCamera1.isOn() and myCamera2.isOff():
		
		got_frame0, frame0 = myCamera0.getAndWriteFrame()
		got_frame1, frame1 = myCamera1.getAndWriteFrame()

		t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		t1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

		f0 = t0.copy()
		f1 = t1.copy()

		masked_img0, x0, y0 = ta.diffaccWeight(f0,t0, avg_daw0)
		masked_img1, x1, y1 = ta.diffaccWeight(f1,t1, avg_daw1)


		if((x0 != -1) | (y0 != -1)):
			measured0 = (x0,y0)
			prev_x0 = x0
			prev_y0 = y0
		else:
			measured0 = (prev_x0,prev_y0)

		if((x1 != -1) | (y1 != -1)):
			measured1 = (x1,y1)
			prev_x1 = x1
			prev_y1 = y1
		else:
			measured1 = (prev_x1,prev_y1)


		measured_points0.append(measured0)
		measured_points1.append(measured1)
		
		kalman2d0.update(measured0[0], measured0[1])
		kalman2d1.update(measured1[0], measured1[1])

		estimated0 = [int (c) for c in kalman2d0.getEstimate()]
		
		estimated1 = [int (a) for a in kalman2d1.getEstimate()]

		drawCross(frame0, estimated0, 255, 255, 255)
		drawCross(frame1, estimated1, 255, 255, 255)
		
		drawCross(frame0, measured0, 0,   0,   255)
		drawCross(frame1, measured1, 0,   0,   255)

		cv2.imshow( winName[0], frame0 )
		cv2.imshow( winName[1], frame1 )

		delta_x0 = prev_x0 - estimated0[0]
		delta_x1 = prev_x1 - estimated1[0]


		if((delta_x1 < 0) and (estimated1[0] <= triggerWidthLeft)):
			print "turn camera 0 off"
			myCamera1.off()
			cv2.destroyWindow("1")
			prev_x0 = centerx
		
		if((delta_x0 > 0) and (estimated0[0] >= triggerWidthRight)):
			print "turn camera 0 off"
			myCamera0.off()
			cv2.destroyWindow("0")
			prev_x1 = centerx

		if(estimated0[0] < centerx ):
			myCamera1.off()
			cv2.destroyWindow("1")
		if(estimated1[0] > centerx ):
			myCamera0.off()
			cv2.destroyWindow("0")


		key = cv2.waitKey(1)
		if key == 27:
			cv2.destroyWindow("0")
			cv2.destroyWindow("1")
			myCamera0.off()
			myCamera1.off()
			break
	

	while myCamera0.isOn() and myCamera2.isOn() and myCamera1.isOff():

		got_frame0, frame0 = myCamera0.getAndWriteFrame()
		got_frame2, frame2 = myCamera2.getAndWriteFrame()
		
		t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		t2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
		
		f0 = t0.copy()
		f2 = t2.copy()
		
		gray0 = t0.copy()
		gray2 = t2.copy()

		masked_img0, x0, y0 = ta.diffaccWeight(f0,t0, avg_daw0)
		masked_img2, x2, y2 = ta.diffaccWeight(f2,t2, avg_daw2)


		if((x0 != -1) | (y0 != -1)):
			measured0 = (x0,y0)
			prev_x0 = x0
			prev_y0 = y0
		else:
			measured0 = (prev_x0,prev_y0)

		if((x2 != -1) | (y2 != -1)):
			measured1 = (x2,y2)
			prev_x2 = x2
			prev_y2 = y2
		else:
			measured2 = (prev_x2,prev_y2)


		measured_points0.append(measured0)
		measured_points2.append(measured2)
		
		kalman2d0.update(measured0[0], measured0[1])
		kalman2d2.update(measured2[0], measured2[1])

		estimated0 = [int (c) for c in kalman2d0.getEstimate()]
		estimated2 = [int (a) for a in kalman2d2.getEstimate()]

		drawCross(frame0, estimated0, 255, 255, 255)
		drawCross(frame2, estimated2, 255, 255, 255)
		
		drawCross(frame0, measured0, 0,   0,   255)
		drawCross(frame2, measured2, 0,   0,   255)

		cv2.imshow( winName[0], frame0 )
		cv2.imshow( winName[2], frame2 )

		delta_x0 = prev_x0 - estimated0[0]
		delta_x2 = prev_x2 - estimated2[0]

		
		if((delta_x2 > 0) and (estimated2[0] >= triggerWidthRight)):
			print "turn camera 2 off"
			myCamera2.off()
			cv2.destroyWindow("2")
			prev_x0 = centerx
		
		if((delta_x0 < 0) and (estimated0[0] <= triggerWidthLeft)):
			print "turn camera 0 off"
			myCamera0.off()
			cv2.destroyWindow("0")
			prev_x2 = centerx

		
		if(estimated0[0] > centerx ):
			myCamera2.off()
			cv2.destroyWindow("2")
		
		if(estimated2[0] < centerx ):
			myCamera0.off()
			cv2.destroyWindow("0")
		
		key = cv2.waitKey(1)
		if key == 27:
			cv2.destroyWindow("0")
			cv2.destroyWindow("2")
			myCamera0.off()
			myCamera2.off()
			break
<<<<<<< HEAD
	'''
=======
	
>>>>>>> 200723833ddb53414b7c64ca3637b65b376d9dbf
	
	while (myCamera0.isOn() and myCamera1.isOff() and myCamera2.isOff()):
		
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
		
<<<<<<< HEAD
		if((delta_x0 > 0) and (estimated0[0] >= triggerWidthRight)):
			print "turn camera 1 on"
			myCamera1.on()
			myCamera0.off()
			prev_x1 = centerx
		
		if((delta_x0 < 0) and (estimated0[0] <= triggerWidthLeft)):
			print "turn camera 2 on"
			myCamera2.on()
			myCamera0.off()
			prev_x2 = centerx
			
=======
		
		if(prev_x0 > 0):
			
			
			if((delta_x0 > 0) and (estimated0[0] >= triggerWidthRight)):
				print "turn camera 1 on"
				myCamera1.on()
				prev_x1 = centerx
			
			
			if((delta_x0 < 0) and (estimated0[0] <= triggerWidthLeft)):
				print "turn camera 2 on"
				myCamera2.on()
				prev_x2 = centerx
			

>>>>>>> 200723833ddb53414b7c64ca3637b65b376d9dbf
		key = cv2.waitKey(1)
		if key == 27:
			cv2.destroyWindow("0")
			myCamera0.off()
			break

	
	
	while (myCamera1.isOn() and myCamera0.isOff() and myCamera2.isOff()):
		
		got_frame1, frame1 = myCamera1.getAndWriteFrame()
		t1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
		f1 = t1.copy()
		masked_img1, x1, y1 = ta.diffaccWeight(f1,t1, avg_daw1)

		if((x1 != -1) | (y1 != -1)):
			measured1 = (x1,y1)
			prev_x1 = x1
			prev_y1 = y1
		else:
			measured1 = (prev_x1,prev_y1)

		measured_points1.append(measured1)
		kalman2d1.update(measured1[0], measured1[1])

		estimated1 = [int (c) for c in kalman2d1.getEstimate()]

		drawCross(frame1, estimated1, 255, 255, 255)
		drawCross(frame1, measured1, 0,   0,   255)

		cv2.imshow( winName[1], frame1 )
		delta_x1 = prev_x1 - estimated1[0]

		if(prev_x1 > 0):
			
			if((delta_x1 < 0) and (estimated1[0] <= triggerWidthLeft)):
				print "turn camera 0 on"
				myCamera0.on()
<<<<<<< HEAD
				prev_x0 = centerx
				myCamera1.off()
=======
>>>>>>> 200723833ddb53414b7c64ca3637b65b376d9dbf
				
		key = cv2.waitKey(1)
		if key == 27:
			cv2.destroyWindow("1")
			myCamera1.off()
			break
	
	
	
	while (myCamera2.isOn() and myCamera0.isOff() and myCamera1.isOff()):
		got_frame2, frame2 = myCamera2.getAndWriteFrame()
		t2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
		f2 = t2.copy()
		masked_img2, x2, y2 = ta.diffaccWeight(f2,t2, avg_daw2)

		if((x2 != -1) | (y2 != -1)):
			measured2 = (x2,y2)
			prev_x2 = x2
			prev_y2 = y2
		else:
			measured2 = (prev_x2,prev_y2)

		measured_points2.append(measured2)
		kalman2d2.update(measured2[0], measured2[1])

		estimated2 = [int (c) for c in kalman2d2.getEstimate()]

		drawCross(frame2, estimated2, 255, 255, 255)
		drawCross(frame2, measured2, 0,   0,   255)

		cv2.imshow( winName[2], frame2 )

		delta_x2 = prev_x2 - estimated2[0]

		
		if(estimated2[0] > 0):
			
			if((delta_x2 > 0) and (estimated2[0] >= triggerWidthRight)):
				print "turn camera 0 on"
				myCamera0.on()
<<<<<<< HEAD
				prev_x0 = centerx
				myCamera2.off()
=======
>>>>>>> 200723833ddb53414b7c64ca3637b65b376d9dbf
		

		key = cv2.waitKey(1)
		if key == 27:
			cv2.destroyWindow("2")
			myCamera2.off()
			break
	

print 'goodbye world :\'('
