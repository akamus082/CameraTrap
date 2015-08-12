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

import cv2
import time
import camera as Camera
import trackingalgos as ta
import numpy as np

myCamera0 = Camera.Camera(0, "cam0.avi")

got_frame, frame = myCamera0.getFrame()
t0 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
avg_daw0 = np.float32(t0)


i = 0
start_time = time.time()
while True:
	
	got_frame, frame = myCamera0.getFrame()
	t0 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	f0 = t0.copy()
	masked_img0, x0, y0 = ta.diffaccWeight(f0,t0, avg_daw0)
	#if((x0 != -1) | (y0 != -1)):
	drawCross(masked_img0, (x0, y0), 0,   0,   255)
	cv2.imwrite('frame' + str(i) + ".jpg", masked_img0)

	cv2.imshow( "frame", masked_img0 )

	i+=1
	if (i == 30): 
		#finish_time = time.time()
		break
	key = cv2.waitKey(1)
	if key == 27:
		cv2.destroyWindow("0")
		myCamera0.off()
		break

print("--- %s seconds ---" % (time.time() - start_time))