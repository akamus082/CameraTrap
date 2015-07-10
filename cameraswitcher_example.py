import cameraswitcher  # import the camera switcher module
import time

camera_0 = cameraswitcher.Camera(0) # Create camera to control /dev/video0
camera_1 = cameraswitcher.Camera(1) # Create camera to control /dev/video1

print 'start recording camera 0'
camera_0.start_recording()			# Start recording on camera_0
print 'start recording camera 1'
camera_1.start_recording()			# Start recording on camera_1
time.sleep(3)
print 'stop recording camera 0'
camera_0.stop_recording()
print 'stop recording camera 1'
camera_1.stop_recording()
