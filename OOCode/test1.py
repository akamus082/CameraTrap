import numpy as np
import cv2
import runavg as ra
import camera as Camera
import time

c0 = False
c1 = False
c2 = False

myCamera0 = Camera.Camera(0, "cam0.avi")
myCamera1 = Camera.Camera(1, "cam1.avi")
myCamera2 = Camera.Camera(2, "cam2.avi")

winName = "1", "2"
#time.sleep(2)
myCamera0.on()
c0 = True
myCamera1.off()
c1 = False
myCamera2.off()
c2 = False

while(c0 or c1 or c2 ):
	
	if(c0):
		got_frame0, frame0 = myCamera0.getFrame()

		running_average_in_display = frame0
		avg = np.float32(frame0)

		while got_frame0:
			frame_copy = frame0.copy()
			cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			masked_img, x, y = ra.track(frame_copy,running_average_in_display, avg)
			cv2.imshow( winName[0], frame0 )
			got_frame0, frame0 = myCamera0.getFrame()

			if((x > 0) and (128 > x)):
				myCamera1.on()
				myCamera0.off()
				c0 = False
				c1 = True
				#print "turn camera 1"

			if((x > 512) and (640 > x)):
				myCamera2.on()
				myCamera0.off()
				c0 = False
				c2 = True
				#print "turn camera 2"

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera0.off()
				c0 = False
				break
	if(c1):
		got_frame1, frame1 = myCamera1.getFrame()

		running_average_in_display = frame1
		avg = np.float32(frame1)

		while got_frame1:
			frame_copy = frame1.copy()
			cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			masked_img, x, y = ra.track(frame_copy,running_average_in_display, avg)
			cv2.imshow( winName[0], frame1 )
			got_frame1, frame1 = myCamera1.getFrame()

			if((x > 512) and (x < 640)):
				myCamera0.on()
				myCamera1.off()
				c1 = False
				c0 = True
				
			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera1.off()
				c1 = False
				break
	if(c2):
		got_frame2, frame2 = myCamera2.getFrame()

		running_average_in_display = frame2
		avg = np.float32(frame2)

		while got_frame2:
			frame_copy = frame2.copy()
			cv2.rectangle(frame_copy, (128, 0), (512, 480), (0,0,0), -1)
			masked_img, x, y = ra.track(frame_copy,running_average_in_display, avg)
			cv2.imshow( winName[0], frame2 )
			got_frame2, frame2 = myCamera2.getFrame()

			if((x > 0) and (128 > x)):
				myCamera0.on()
				myCamera2.off()
				c2 = False
				c0 = True
				#print "turn camera 1"

			key = cv2.waitKey(10)
			if key == 27:
				cv2.destroyWindow("1")
				myCamera2.off()
				c2 = False
				break

#cv2.destroyWindow("1")

print 'hello'