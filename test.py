#!/bin/python
# Prints "hello" to the screen at x frames per second.

import cv2
import sys
import time

cam = cv2.VideoCapture(0)
path = ('output.avi')

cam.set(1, 30.0) #Match fps
cam.set(3,640)   #Match width
cam.set(4,480)   #Match height

fourcc = cv2.cv.CV_FOURCC(*'DIV3')
video_writer = cv2.VideoWriter(path,fourcc, 30.0, (640,480))

fps = int(sys.argv[1])
delay = (1.0/fps)
read_count = 0
write_count = 0


winName = "1"
#got_frame, frame = cam.read()
Framelist = []
while True:
  
  got_frame, frame = cam.read()
  read_count += 1
  Framelist.append(frame)
  cv2.imshow( winName[0], frame )
  
  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break

print "done reading"

for f in Framelist:
  video_writer.write(f)
  write_count += 1
  time.sleep(delay)


print "len(FrameList): " + str(len(Framelist))
print "frames read: " + str(read_count)
print "frames written: " + str(write_count)

