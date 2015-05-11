import cameraswitcher as cs
import time

camera_0 = cs.Camera(0)
camera_1 = cs.Camera(1)



camera_1.start_recording()
time.sleep(5)
camera_1.stop_recording()
time.sleep(5)

# camera_0.start_recording()
# time.sleep(5)
# camera_0.stop_recording()
# time.sleep(5)

# camera_0.start_recording()
# camera_1.start_recording()
# time.sleep(8)
# camera_0.stop_recording()
# camera_1.stop_recording()
