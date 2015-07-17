import omnicamera as oc
import numpy as np
import cv2

OCamera = oc.OmniCamera()
got_frame, frame = OCamera.getFrame()

while (got_frame == True):
	#cv2.imshow("out", frame )
	
	new_frame, theta  = OCamera.trackFrame(frame)
	if(theta):
		cv2.imshow("track", new_frame)

	got_frame, frame = OCamera.getFrame()
	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyWindow("track")
		#cv2.destroyWindow("mask")
		break

print "Goodbye"