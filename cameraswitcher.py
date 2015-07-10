import os
import signal
import subprocess


class Camera:
	''' The shifter allows you to input a signal 
	    and switch between cameras.'''

	def __init__(self, device_number):
		self.filecount = 0;
		self.dev = device_number
		self.proc_id = -1


	def start_recording(self):
		''' Begin recording on the camera at /dev/video<camera_number>.'''

		device = "/dev/video" + str(self.dev)
		filename = "dev" + str(self.dev) + "_output_" + str(self.filecount) + ".avi"
		subproc = "avconv -loglevel quiet -f video4linux2 -r 10 -i " + device + " " + filename

		print "Filming with " + str(device)
		print "writing file " + str(filename)
		p = subprocess.Popen(subproc, 
					 stdout=subprocess.PIPE,
					 shell=True,
					 preexec_fn=os.setsid)

		self.proc_id = p.pid

	def stop_recording(self):
		''' Send a signal to the queue to stop the camera.'''
		if self.proc_id > 0:
			os.killpg(self.proc_id, signal.SIGTERM)
			self.filecount += 1
		else:
			print "Camera " + str(self.dev) + "not running."
		






