import cv2

cam = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)
cam2 = cv2.VideoCapture(2)

while True:

  got_frame, frame = cam.read()
  got_frame1, frame1 = cam1.read()
  got_frame2, frame2 = cam2.read()

  cv2.imshow( "0", frame )
  cv2.imshow( "1", frame1 )
  cv2.imshow( "2", frame2 )

  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow("0")
    cam.release()
    cv2.destroyWindow("1")
    cam1.release()
    cv2.destroyWindow("2")
    cam2.release()
    break

print "Goodbye"