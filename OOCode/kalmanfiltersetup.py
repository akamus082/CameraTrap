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

myCamera0 = Camera.Camera(0, "cam0.avi")
myCamera1 = Camera.Camera(1, "cam1.avi")
myCamera2 = Camera.Camera(2, "cam2.avi")

winName = "0", "1", "2"
myCamera1.off()
myCamera2.off()

prev_x0 = int(640/2)
prev_x1 = 0
prev_x2 = 640
prev_y0= int(480/2)
prev_y1= int(480/2)
prev_y2= int(480/2)

while(myCamera0.isOn() or myCamera1.isOn() or myCamera2.isOn()):
	
	
	if(myCamera0.isOn() and myCamera1.isOn()):
		print "camera 0 and 1 are on"
		
		kalman2d0 = Kalman2D()
		kalman2d1 = Kalman2D()

		measured_points0 = []
		measured_points1 = []
		kalman_points0 = []
		kalman_points1 = []
		
		got_frame0, frame0 = myCamera0.getFrame()
		got_frame1, frame1 = myCamera1.getFrame()
		
		running_average_in_display0 = frame0
		running_average_in_display1 = frame1

		t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		t1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

		f0 = t0.copy()
		f1 = t1.copy()

		gray0 = t0.copy()
		gray1 = t1.copy()

		avg_daw0 = np.float32(f0)
		avg_daw1 = np.float32(f1)

		while myCamera0.isOn() and myCamera1.isOn():
			frame_copy0 = frame0.copy()
			frame_copy1 = frame1.copy()
			t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
			t1 = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)

			f0 = t0.copy()
			f1 = t1.copy()
			gray0 = t0.copy()
			gray1 = t1.copy()

			masked_img0, x0, y0 = ta.diffaccWeight(f0,t0,gray0, avg_daw0)
			masked_img1, x1, y1 = ta.diffaccWeight(f1,t1,gray1, avg_daw1)


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

			kalman_points0.append(estimated0)
			kalman_points1.append(estimated1)

			drawCross(frame0, estimated0, 255, 255, 255)
			drawCross(frame1, estimated1, 255, 255, 255)
			
			drawCross(frame0, measured0, 0,   0,   255)
			drawCross(frame1, measured1, 0,   0,   255)

			cv2.imshow( winName[0], frame0 )
			cv2.imshow( winName[1], frame1 )


			got_frame0, frame0 = myCamera0.getFrame()
			got_frame1, frame1 = myCamera1.getFrame()

			delta_x0 = prev_x0 - estimated0[0]
			delta_x1 = prev_x1 - estimated1[0]


			if( (prev_x1 > 60) and (delta_x1 > 0) ):
				myCamera0.off()
				cv2.destroyWindow("0")
			
			
			if( (prev_x0 < 580) and (delta_x0 < 0) ):
				myCamera1.off()
				cv2.destroyWindow("1")
			

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("0")
				cv2.destroyWindow("1")
				myCamera0.off()
				myCamera1.off()
				break


	if(myCamera0.isOn() and myCamera2.isOn()):
		print "camera 0 and 2 are on"
		
		kalman2d0 = Kalman2D()
		kalman2d2 = Kalman2D()

		measured_points0 = []
		measured_points2 = []
		kalman_points0 = []
		kalman_points2 = []
		
		got_frame0, frame0 = myCamera0.getFrame()
		got_frame2, frame2 = myCamera2.getFrame()
		
		running_average_in_display0 = frame0
		running_average_in_display2 = frame2

		t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		t2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)

		f0 = t0.copy()
		f2 = t2.copy()

		gray0 = t0.copy()
		gray2 = t2.copy()

		avg_daw0 = np.float32(f0)
		avg_daw2 = np.float32(f2)

		while myCamera0.isOn() and myCamera2.isOn():
			frame_copy0 = frame0.copy()
			frame_copy2 = frame2.copy()
			t0 = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
			t2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)

			f0 = t0.copy()
			f2 = t2.copy()
			gray0 = t0.copy()
			gray2 = t2.copy()

			masked_img0, x0, y0 = ta.diffaccWeight(f0,t0,gray0, avg_daw0)
			masked_img2, x2, y2 = ta.diffaccWeight(f2,t2,gray2, avg_daw2)


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

			kalman_points0.append(estimated0)
			kalman_points2.append(estimated2)

			drawCross(frame0, estimated0, 255, 255, 255)
			drawCross(frame2, estimated2, 255, 255, 255)
			
			drawCross(frame0, measured0, 0,   0,   255)
			drawCross(frame2, measured2, 0,   0,   255)

			print "prev_x2", prev_x2


			cv2.imshow( winName[0], frame0 )
			cv2.imshow( winName[2], frame2 )


			got_frame0, frame0 = myCamera0.getFrame()
			got_frame2, frame2 = myCamera2.getFrame()

			delta_x0 = prev_x0 - estimated0[0]
			delta_x2 = prev_x2 - estimated2[0]

			
			if( (prev_x2 <= 580) and (delta_x2 < 0) ):
				myCamera0.off()
				cv2.destroyWindow("0")
			
			
			if( (prev_x0 > 60) and (delta_x0 > 0) ):
				myCamera2.off()
				cv2.destroyWindow("2")
			

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("0")
				cv2.destroyWindow("2")
				myCamera0.off()
				myCamera2.off()
				break
	

	if(myCamera0.isOn() and myCamera1.isOff() and myCamera2.isOff()):
		print "camera 0 is on"
		kalman2d0 = Kalman2D()
		measured_points = []
		kalman_points = []
		
		got_frame0, frame0 = myCamera0.getFrame()
		
		running_average_in_display = frame0
		t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		gray = t.copy()
		avg_daw = np.float32(f)

		while (myCamera0.isOn() and myCamera1.isOff() and myCamera2.isOff()):
			
			frame_copy = frame0.copy()
			t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
			f = t.copy()
			gray = t.copy()

			masked_img0, x0, y0 = ta.diffaccWeight(f,t,gray, avg_daw)
			

			if((x0 != -1) | (y0 != -1)):
				measured = (x0,y0)
				prev_x0 = x0
				prev_y0 = y0
			else:
				measured = (prev_x0,prev_y0)

			measured_points.append(measured)
			kalman2d0.update(measured[0], measured[1])

			estimated = [int (c) for c in kalman2d0.getEstimate()]

			kalman_points.append(estimated)

			drawCross(frame0, estimated, 255, 255, 255)
			drawCross(frame0, measured, 0,   0,   255)

			cv2.imshow( winName[0], frame0 )
			
			got_frame0, frame0 = myCamera0.getFrame()
			
			delta_x = prev_x0 - estimated[0]
			
			if(estimated[0] > 0):
				
				if((delta_x > 0) and (estimated[0] >= 580)):
					print "turn camera 1 on"
					myCamera1.on()
					myCamera1.getFrame()
					prev_x0 = 640
					prev_x1 = 0

				if((delta_x < 0) and (estimated[0] <= 60)):
					print "turn camera 2 on"
					myCamera2.on()
					myCamera2.getFrame()
					prev_x0 = 0
					prev_x2 = 640


			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("0")
				myCamera0.off()
				break

	
	if(myCamera1.isOn() and myCamera0.isOff() and myCamera2.isOff()):
		print "camera 1 is on"
		kalman2d1 = Kalman2D()
		measured_points = []
		kalman_points = []
		
		got_frame1, frame1 = myCamera1.getFrame()
		
		running_average_in_display = frame1
		t = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		gray = t.copy()
		avg_daw = np.float32(f)

		while (myCamera1.isOn() and myCamera0.isOff() and myCamera2.isOff()):
			frame_copy = frame1.copy()
			t = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
			f = t.copy()
			gray = t.copy()
			
			masked_img1, x1, y1 = ta.diffaccWeight(f,t,gray, avg_daw)

			if((x1 != -1) | (y1 != -1)):
				measured = (x1,y1)
				prev_x1 = x1
				prev_y1 = y1
			else:
				measured = (prev_x1,prev_y1)

			measured_points.append(measured)
			kalman2d1.update(measured[0], measured[1])

			estimated = [int (c) for c in kalman2d1.getEstimate()]

			kalman_points.append(estimated)

			drawCross(frame1, estimated, 255, 255, 255)
			drawCross(frame1, measured, 0,   0,   255)

			cv2.imshow( winName[1], frame1 )

			got_frame1, frame1 = myCamera1.getFrame()

			delta_x = prev_x1 - estimated[0]

			
			if(estimated[0] > 0):
				
				if((delta_x < 0) and (estimated[0] <= 60)):
					print "turn camera 0 on"
					myCamera0.on()
			
			

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera1.off()
				break
	
	
	
	if(myCamera2.isOn() and myCamera0.isOff() and myCamera1.isOff()):
		print "camera 2 is on"
		kalman2d2 = Kalman2D()
		measured_points = []
		kalman_points = []
		
		got_frame2, frame2 = myCamera2.getFrame()
		
		running_average_in_display = frame2
		t = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		gray = t.copy()
		avg_daw = np.float32(f)

		while (myCamera2.isOn() and myCamera0.isOff() and myCamera1.isOff()):
			frame_copy = frame2.copy()
			t = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
			f = t.copy()
			gray = t.copy()
			
			masked_img2, x2, y2 = ta.diffaccWeight(f,t,gray, avg_daw)

			if((x2 != -1) | (y2 != -1)):
				measured = (x2,y2)
				prev_x2 = x2
				prev_y2 = y2
			else:
				measured = (prev_x2,prev_y2)

			measured_points.append(measured)
			kalman2d2.update(measured[0], measured[1])

			estimated = [int (c) for c in kalman2d2.getEstimate()]

			kalman_points.append(estimated)

			drawCross(frame2, estimated, 255, 255, 255)
			drawCross(frame2, measured, 0,   0,   255)

			cv2.imshow( winName[2], frame2 )

			got_frame2, frame2 = myCamera2.getFrame()

			delta_x = prev_x2 - estimated[0]

			
			if(estimated[0] > 0):
				
				if((delta_x > 0) and (estimated[0] >= 580)):
					print "turn camera 0 on"
					myCamera0.on()

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("2")
				myCamera2.off()
				break

print 'hello'