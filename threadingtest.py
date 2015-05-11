import time
from threading import Thread
import cv2


def writer(dev):
	cap = cv2.VideoCapture(dev)
	cap.set(3, 640)
	cap.set(4, 480)
	while True:
		ret, frame = cap.read()
		cv2.imshow(str(dev), frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	


t0 = Thread(target=writer, args=(0,))
t1 = Thread(target=writer, args=(2,))

cv2.namedWindow("0", flags=cv2.WINDOW_NORMAL)
cv2.namedWindow("1", flags=cv2.WINDOW_NORMAL)

t1.start()
t0.start()

# cap.release()
# cv2.destroyAllWindows()


