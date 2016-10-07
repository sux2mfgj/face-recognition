# -*- coding:utf-8 -*-

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import threading
import os.path
import requests
import commands
from datetime import datetime


class FaceThread(threading.Thread):
    def __init__(self, frame):
        super(FaceThread, self).__init__()
#          self._cascade_path = "./haarcascade_frontalface_default.xml"
#          self._cascade_path = "./haarcascade_frontalface_alt_tree.xml"
#          self._cascade_path = "./haarcascade_frontalface_alt.xml"
        self._cascade_path = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt2.xml"

        if not os.path.exists(self._cascade_path):
            raise OSError("cascade file not found")

        self._frame = frame
        self._color = (255, 255, 255)

    def run(self):
#          self._frame_gray = cv2.cvtColor(self._frame, cv2.cv.CV_BGR2GRAY)
        self._frame_gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)

        self._cascade = cv2.CascadeClassifier(self._cascade_path)

        facerect = self._cascade.detectMultiScale(
                    self._frame_gray,
                    scaleFactor=1.2,
                    minNeighbors=3,
                    minSize=(10, 10))

        if len(facerect) > 0:
            print('detect face')
            for self._rect in facerect:

                cv2.rectangle(
                        self._frame,
                        tuple(self._rect[0:2]),
                        tuple(self._rect[0:2] + self._rect[2:4]),
                        self._color, thickness=2)

                # triming face
                x = self._rect[0]
                y = self._rect[1]
                width = self._rect[2]
                height = self._rect[3]
                dst = self._frame[y:y+height, x:x+width]

                self.now = datetime.now().strftime('%Y%m%d%H%M%S')
                image_path = 'images/' + self.now + '.jpg'
                cv2.imwrite(image_path, dst)
                image = open(image_path, 'rb')

                send_image(image)


	def send_image(image):
	    files = {'file': ('a.jpg', image, 'image/jpeg')}
	    # requests.post('http://localhost:5000/upload', files=files)
	    commands.getoutput("mosquitto_pub --cafile ../../certs/root-CA.crt --cert ../../certs/certificate.pem.crt --key ../../certs/private.pem.key   -h xxx.iot.us-west-2.amazonaws.com  -p 8883 -q 1 -d -t 'topic/pi_db' -m '{\"deviceid\":\"pi_03\", \"date\":%s, \"image_id\":\"%s\"}'" % (now, 'google'))
	    exit(1)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("can't open the camera")
    exit(1)


# set up fps??
cap.set(5, 20)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow('camera capture', frame)

    if(threading.activeCount() == 1):
        th = FaceThread(frame)
        th.start()

    k = cv2.waitKey(1000)

    c = chr(k & 255)
    if c in ['q', chr(27)]:
        break

cap.release()
cv2.destroyAllWindows()
