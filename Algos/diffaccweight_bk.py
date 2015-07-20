

import cv2
import numpy as np
import math
import CameraTrapCV as CTCV


#############################################################

import cameraswitcher as cs

cam0 = cs.Camera(1)
cam1 = cs.Camera(2)
firstPoint = True


def angleControl(angle, oldangle):
  #print "old angle = " + str(oldangle)
  if angle == 0:
    turnOffAllCameras()
  elif cameraAngleChanged(oldangle, angle):
    switchCameraAngle(angle, oldangle)


def cameraAngleChanged(old_angle, new_angle):
  if old_angle == 0 and new_angle > 0:
    return True
  elif old_angle < 180:
    if new_angle >= 180:
      return True
  elif old_angle >= 180:
    if new_angle < 180:
      return True
  else:
    return False


def switchCameraAngle(angle, oldangle):
  if oldangle == 0:
    if angle < 180:
      cam0.start_recording()
    else:
      cam1.start_recording()
  elif cam1.is_recording():
    cam1.stop_recording()
    cam0.start_recording()
  elif cam0.is_recording():
    cam0.stop_recording()
    cam1.start_recording()


def turnOffAllCameras():
  if cam1.is_recording():
    cam1.stop_recording()
  if cam0.is_recording():
    cam0.stop_recording()



##############################################################




def getPolar(x, y, frame_w):
        r = (x ** 2 + y ** 2) ** 1/2
        theta = math.atan2(y, (x-frame_w)/2) * 180. / np.pi
        return [r, theta]

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

MIN_BLOB_SIZE = 200
ctcv = CTCV.CameraTrapCV()

cam = cv2.VideoCapture(0)

t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

f = t.copy()
gray = t.copy()
avg = np.float32(f)

# Read three images first:
#fgbg = cv2.BackgroundSubtractorMOG()

while(1):
    #_,f = c.read()
  #img = f.copy()
  mask = np.zeros(t.shape, dtype=np.uint8)
  height, width = t.shape
  cv2.circle(t, (312,262), 62, (0,0,0), -1)
  cv2.circle(mask, (312,262), 160, (255,255,255), -1)

  t = t & mask







  f = cv2.GaussianBlur(f,(5,5),0)
  cv2.accumulateWeighted(f,avg,0.4)
  res = cv2.convertScaleAbs(avg)
  #res1 = cv2.absdiff(t_minus, res.copy())
  res2 = cv2.absdiff(t, res.copy())
  #res3 = cv2.absdiff(t_plus, res.copy())

  ret,img_grey2 = cv2.threshold( res2, 7, 255, cv2.THRESH_BINARY )
  img_grey2 = cv2.GaussianBlur(img_grey2,(5,5),0)
  ret2,img_grey2 = cv2.threshold( img_grey2, 240, 255, cv2.THRESH_BINARY )


  img_thresh = ctcv.bg_subtractor.apply(img_grey2, None, 0.05)

  if np.count_nonzero(img_thresh) > 5:
    # Get the largest contour
    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    '''for cnt in contours:
        cv2.drawContours(zeros, [cnt], 0,255,-1)
    '''
    
    #gray = cv2.bitwise_not(t)
    #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    #res = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
    




    
        # totally not from stack overflow
    areas = [cv2.contourArea(c) for c in contours]
    i_max  = np.argmax(areas)
    max_index = ctcv.getLargestContourIndex(img_thresh)

    # Make sure it's big enough
    if cv2.contourArea(contours[max_index]) >= MIN_BLOB_SIZE:
      img_out = np.zeros(img_thresh.shape).astype(np.uint8)
      cv2.drawContours(t, contours, max_index, (255, 255, 255), -1)
      #print "img_out.shape = " + str(img_out.shape)
      x_pos, y_pos = ctcv.getCentroid(contours[max_index])
      cv2.circle(t, (x_pos, y_pos), 5, (0,0,0), -1)
    
      x_pos, y_pos = ctcv.getCentroid(ctcv.contours[max_index])
      theta = ctcv.getPolar(312,262, x_pos, y_pos)
      
	#print theta

      if firstPoint:
	oldangle = 0
	firstPoint = False
      angleControl(theta, oldangle)
      oldangle = theta





  #cv2.imshow('mask',mask)
  cv2.imshow('original',t)
  #cv2.imshow('img_thresh',img_thresh)
  
  
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
  f = t.copy()
  k = cv2.waitKey(20)
 
  if k == 27:
    break
 
cv2.destroyAllWindows()
cam.release()