import numpy as np
import cv2
import runavg as ra
import camera as Camera
import time

myCamera0 = Camera.Camera(0, "cam0.avi")
myCamera1 = Camera.Camera(1, "cam1.avi")
myCamera2 = Camera.Camera(2, "cam2.avi")

winName = "1", "2"
myCamera1.off()
myCamera2.off()

x = int(640/2)
#previous_y = 0

while(myCamera0.isOn() or myCamera1.isOn() or myCamera2.isOn() ):
	
	if(myCamera0.isOn()):
		got_frame0, frame0 = myCamera0.getFrame()
		running_average_in_display = frame0
		avg = np.float32(frame0)

		while got_frame0:
			frame_copy = frame0.copy()

			#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			
			previous_x = x
			masked_img, x, y = ra.track(frame_copy,running_average_in_display, avg)
			#print "x = %d  prevx = %d",  x, previous_x
			cv2.imshow( winName[0], frame0 )
			got_frame0, frame0 = myCamera0.getFrame()
			
			delta_x = x - previous_x
			
			if((x > 0) and (50 > x) ): #and (delta_x < 0)
				myCamera1.on()
				myCamera0.off()
				#print "turn camera 1"

			if((x > 590) and (640 > x) ): #and (delta_x > 0)
				myCamera2.on()
				myCamera0.off()
				#print "turn camera 2"

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera0.off()
				break
	if(myCamera1.isOn()):
		got_frame1, frame1 = myCamera1.getFrame()

		running_average_in_display = frame1
		avg = np.float32(frame1)

		while got_frame1:
			frame_copy = frame1.copy()
			previous_x = x
			#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			masked_img, x, y = ra.track(frame_copy,running_average_in_display, avg)
			#print "x = %d  prevx = %d",  x, previous_x

			cv2.imshow( winName[0], frame1 )
			got_frame1, frame1 = myCamera1.getFrame()

			if((x > 590) and (x < 640) ): #and (delta_x > 0)
				myCamera0.on()
				myCamera1.off()
				
			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera1.off()
				break
	if(myCamera2.isOn()):
		got_frame2, frame2 = myCamera2.getFrame()

		running_average_in_display = frame2
		avg = np.float32(frame2)

		while got_frame2:
			frame_copy = frame2.copy()
			previous_x = x
			#cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			
			masked_img, x, y = ra.track(frame_copy,running_average_in_display, avg)
			#print "x = %d  prevx = %d",  x, previous_x

			cv2.imshow( winName[0], frame2 )
			got_frame2, frame2 = myCamera2.getFrame()

			if((x > 0) and (50 > x) ): #and (delta_x < 0)
				myCamera0.on()
				myCamera2.off()

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera2.off()
				break


print 'hello'