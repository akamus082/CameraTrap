import cv2
import cv2.cv as cv
import numpy as np


cam = cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
winName = "1", "2", "3"
got_frame, frame = cam.read()

avg1 = np.float32(frame)
avg2 = np.float32(frame)

while True:
  #img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
  
  #smooth image
  blur = cv2.GaussianBlur(frame,(5,5),0)
  #calculate running avg
  cv2.accumulateWeighted(blur,avg1,0.01)
  cv2.accumulateWeighted(blur,avg2,0.32)

  res1 = cv2.convertScaleAbs(avg1)
  res2 = cv2.convertScaleAbs(avg2)
  #grey_imag  = CreateImage( GetSize(frame), IPL_DEPTH_8U, 1 )
  cv2.imshow( winName[0], frame )
  cv2.imshow( winName[1], res1)
  cv2.imshow( winName[2], res2)

  got_frame, frame = cam.read()
  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break

print "Goodbye"
