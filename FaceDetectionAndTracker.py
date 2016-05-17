import cv2
import numpy as np
import os
import serial
from math import floor

#Defined Constants
CONST_screenMaxX = 640
CONST_screenMaxY = 480
CONST_servoMaxX = 180
CONST_servoMaxY = 180
CONST_baudRate = 57600
CONST_COMNUM = 'COM9'

#Train Classifier Through OpenCV Databases
faceCascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(faceCascPath)

#Estabilish Serial Communication With Arduino
arduinoCom = serial.Serial(CONST_COMNUM, CONST_baudRate)

def main():

    capture = cv2.VideoCapture(2)
    cenX = 0
    cenY = 0

    if capture.isOpened() == False:
        print "Error: Webcam was not detected or accessed properly.\n\n"
        os.system("pause")
        return


    cv2.namedWindow("Face Detection", cv2.WINDOW_AUTOSIZE)

    while cv2.waitKey(1) != 27 and capture.isOpened():
        blnSuccess, imgCapture = capture.read()

        if not blnSuccess or imgCapture is None:
            print "Error: Frame not read from Webcam. \n"
            os.system("pause")
            break

        imgGrayScale = cv2.cvtColor(imgCapture, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(imgGrayScale, 1.2, 5, minSize=(30,30), flags = cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT)

        print "Found {0} face(s)!".format(len(faces))

        for (x,y,w,h) in faces:
            cv2.rectangle(imgCapture, (x,y), (x+w,y+h), (0,255,0), 2)
            faceGray = imgGrayScale[y:y+h, x:x+w]
            faceColor = imgCapture[y:y+h, x:x+w]

            cenX = x+0.5*w
            cenY = y+0.5*h
            cenX = int(floor(cenX))
            cenY = int(floor(cenY))

            arduinoCom.write(chr((cenX >> 8) & 0xff))
            arduinoCom.write(chr(cenX & 0xff))
            arduinoCom.write(chr((cenY >> 8) & 0xff))
            arduinoCom.write(chr(cenY & 0xff))

        cv2.imshow("Face Detection", imgCapture)

    cv2.destroyAllWindows()

###################################################################################################
if __name__ == "__main__":
    main()