import cv2
import numpy as np
import CameraTrapCV as CTCV

MIN_BLOB_SIZE = 30

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

ctcv = CTCV.CameraTrapCV()

cam = cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

winName = "1", "2"
cv2.namedWindow(winName[0], cv2.CV_WINDOW_AUTOSIZE)
cv2.namedWindow(winName[1], cv2.CV_WINDOW_AUTOSIZE)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

#fgbg = cv2.BackgroundSubtractorMOG()


while True:

  #gray = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
  img = diffImg(t_minus, t, t_plus)
  imgcopy = img
  
  #des = cv2.bitwise_not(img)
  #mask = np.zeros(img.shape, dtype=np.uint8)
  #frame = img | mask

  ret,img = cv2.threshold( img, 10, 255, cv2.THRESH_BINARY )
  img_grey = cv2.GaussianBlur(img,(5,5),0)
  ret,img_grey = cv2.threshold( img_grey, 10, 255, cv2.THRESH_BINARY )
  
  contours,hier = cv2.findContours(img_grey,1,2)
  for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    cv2.drawContours(t,[cnt],0,255,-1)
  
  '''
  gray = cv2.bilateralFilter(img_grey, 11, 17, 17)
  edged = cv2.Canny(gray, 30, 200)

  (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
  screenCnt = None

  for c in cnts:
  # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    cv2.drawContours(t, [approx], -1, (0, 255, 0), 3)
  '''


  '''
  contour,hier = cv2.findContours(img_grey,1,2)
  if contour:
    cnt = contour[0]
    epsilon = 0.1*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
  
  '''
  #imgcopy = img
  #ret,img = cv2.threshold( img, 10, 255, cv2.THRESH_BINARY )

  '''
  contour,hier = cv2.findContours(img_grey,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
  if contour:
    areas = [cv2.contourArea(c) for c in contour]
    if (areas > 1):
      max_index = np.argmax(areas)
      cnt=contour[max_index]
      
      if cv2.contourArea(contour[max_index]) >= MIN_BLOB_SIZE:
        img_out = np.zeros(img_grey.shape).astype(np.uint8)
        cv2.drawContours(img_grey, contour, max_index, (255, 255, 255), -1)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(t,(x,y),(x+w,y+h),(0,255,0),2)
  '''

  
  #contour,hier = cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)



  #for cnt in contour:
 # cv2.drawContours(img,[cnt],0,255,-1)
  #gray = cv2.bitwise_not(img)

  #fgmask = fgbg.apply(img)

  cv2.imshow( winName[0], t )
  cv2.imshow( winName[1], img )
  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break

print "Goodbye"
