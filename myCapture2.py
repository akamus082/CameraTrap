# based on code from http://stackoverflow.com/questions/5825173/pipe-raw-opencv-images-to-ffmpeg
# cat pic* | avconv -f rawvideo -pix_fmt bgr24 -s 640x480 -r 30 -i - -an -f avi -q:v 2 -r 30 test.avi
import cv2, sys

# Open the video capture object
cap = cv2.VideoCapture(0)
# Set the resolution. If this is changed, the avconv
# code should be altered to reflect the changes.
cap.set(3, 640)
cap.set(4, 480)

filecount = 0 	# This allows us to write out the files in order.   
ret = True
while True :
	if not ret : break
	# Read a frame.
	ret, frame = cap.read()
	# Create the fileame with the next number. Note that you may 
	# need many more than 4 zeros of padding.
	filename = "pic%04d" % filecount
	# Create a new file and write the raw frame data into it.
	# Note: we could also probably just dump all the raw data
	# into a single file but it might mean losing data in the
	# event of a system failure.
	f = open(filename, 'w')
	f.write(frame.tostring())
	f.close()
	# Update the file count.
	filecount += 1

	# Include these lines so you can see what you are filming for testing.
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == 27:
			break

# Release the VideoCapture object.
cap.release()