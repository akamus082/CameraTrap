import numpy as np
import cv2
import trackingalgos as ta
import camera as Camera
import time

myCamera0 = Camera.Camera(0, "cam0.avi")
myCamera1 = Camera.Camera(1, "cam1.avi")
myCamera2 = Camera.Camera(2, "cam2.avi")

winName = "1", "2"
myCamera1.off()
myCamera2.off()

previous_x = int(640/2)
center = int(640/2)

while(myCamera0.isOn() or myCamera1.isOn() or myCamera2.isOn()):
	
	if(myCamera0.isOn()):
		print "camera 0 is on"
		
		got_frame0, frame0 = myCamera0.getFrame()
		running_average_in_display = frame0
		t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		gray = t.copy()
		avg_ra = np.float32(frame0)
		avg_daw = np.float32(f)

		previous_x = center

		while got_frame0:
			frame_copy = frame0.copy()
			t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
			f = t.copy()
			gray = t.copy()

			#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			
			#masked_img, x, y = ta.runningAvg(frame_copy,running_average_in_display, avg_ra)
			masked_img, x, y = ta.diffaccWeight(f,t,gray, avg_daw)
			cv2.imshow( winName[0], masked_img )
			
			got_frame0, frame0 = myCamera0.getFrame()
			
			delta_x = x - previous_x
			
			if(x):
				if((delta_x < 0) and (x <= 60)):
					myCamera2.on()
					myCamera0.off()
				
				if((delta_x > 0) and (x >= 580)):
					myCamera1.on()
					myCamera0.off()
			
			previous_x = x
			
			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera0.off()
				break


	if(myCamera1.isOn()):
		print "camera 1 is on"

		got_frame1, frame1 = myCamera1.getFrame()
		running_average_in_display = frame1
		t = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		gray = t.copy()
		avg_ra = np.float32(frame1)
		avg_daw = np.float32(f)

		previous_x = center


		while got_frame1:
			frame_copy = frame1.copy()
			t = cv2.cvtColor(frame1, cv2.COLOR_RGB2GRAY)
			f = t.copy()
			gray = t.copy()
			#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			#masked_img, x, y = ta.runningAvg(frame_copy,running_average_in_display, avg_ra)
			masked_img, x, y = ta.diffaccWeight(f,t,gray, avg_daw)
			#print "x = %d  prevx = %d",  x, previous_x

			cv2.imshow( winName[0], masked_img )
			got_frame1, frame1 = myCamera1.getFrame()

			delta_x = x - previous_x

			if(x):
				if((delta_x < 0) and (x < 60)):
					myCamera0.on()
					myCamera1.off()
			
			previous_x = x

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera1.off()
				break

	if(myCamera2.isOn()):
		print "camera 2 is on"

		got_frame2, frame2 = myCamera2.getFrame()
		running_average_in_display = frame2
		t = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		gray = t.copy()
		avg_ra = np.float32(frame2)
		avg_daw = np.float32(f)

		previous_x = center

		while got_frame2:
			frame_copy = frame2.copy()
			t = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
			f = t.copy()
			gray = t.copy()
			#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			#masked_img, x, y = ta.runningAvg(frame_copy,running_average_in_display, avg_ra)
			masked_img, x, y = ta.diffaccWeight(f,t,gray, avg_daw)
			#print "x = %d  prevx = %d",  x, previous_x

			cv2.imshow( winName[0], masked_img )
			got_frame2, frame2 = myCamera2.getFrame()
			print "x " + str(x)
			print "previous " + str(previous_x)
			delta_x = x - previous_x
			print "delta " + str(delta_x)
			
			if(x):
				if((delta_x > 0) and (x > 580)):
					myCamera0.on()
					myCamera2.off()

			previous_x = x
			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera2.off()
				break




print 'hello'