import cameraswitcher as cs
import time

cam0 = cs.Camera(0)
cam1 = cs.Camera(1)

L = [0, 0, 0, 4, 15, 20, 3, 12, 45, 160, 166, 100, 90, 45, 20, 70, 180, 0, 120, 120, 120, 0]

#newangle = 0
#oldangle = 0


def angleControl(angle, oldangle):
	print "old angle = " + str(oldangle)
	if angle == 0:
		turnOffAllCameras()
	elif cameraAngleChanged(oldangle, angle):
		switchCameraAngle(angle, oldangle)
	#oldangle = angle


def cameraAngleChanged(old_angle, new_angle):
	if old_angle == 0 and new_angle > 0:
		return True
	elif old_angle < 90:
		if new_angle >= 90:
			return True
	elif old_angle >= 90:
		if new_angle < 90:
			return True
	else:
		return False


def switchCameraAngle(angle, oldangle):
	if oldangle == 0:
		if angle < 90:
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



oldangle = 0

for ang in L:
	angleControl(ang, oldangle)
	oldangle = ang
	time.sleep(1)
