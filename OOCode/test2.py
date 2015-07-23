import numpy as np
import cv2
import runavg as ra
import camera as Camera
import time

myCamera0 = Camera.Camera(0, "cam0.avi")

winName = "1"



previous_x = int(640/2)
center = int(640/2)

while(myCamera0.isOn()):

	print "camera 0 is on"
	got_frame0, frame0 = myCamera0.getFrame()

	t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
	f = t.copy()
	avg = np.float32(f)
	gray = t.copy()
	running_average_in_display = frame0
	
	#avg = np.float32(frame0)
	
	previous_x = center
	
	while got_frame0:
		frame_copy = frame0.copy()

		#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
		
		#masked_img, x, y = ra.track(frame_copy,running_average_in_display, avg)
		masked_img, x, y = ra.diffaccWeight(f,t,gray, avg)
		cv2.imshow( winName[0], masked_img )
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
		t = cv2.cvtColor(frame0, cv2.COLOR_RGB2GRAY)
		f = t.copy()
		key = cv2.waitKey(10)
		if key == 27:
			cv2.destroyWindow("1")
			myCamera0.off()
			break