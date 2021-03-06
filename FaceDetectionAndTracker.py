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

    #Initialize Webcam
    capture = cv2.VideoCapture(2)
    
    #Error Check for Opened Webcam
    if capture.isOpened() == False:
        print "Error: Webcam was not detected or accessed properly.\n\n"
        os.system("pause")
        return

    #Create Window to Display Video Feed
    cv2.namedWindow("Face Detection", cv2.WINDOW_AUTOSIZE)

    #Face Recognition Application Runs Until for ESC Key is Pressed or Error in Video Feed
    while cv2.waitKey(1) != 27 and capture.isOpened():
        
        #Capture Still Image Feed
        blnSuccess, imgCapture = capture.read()

        #Error Check for Capture Still
        if not blnSuccess or imgCapture is None:
            print "Error: Frame not read from Webcam. \n"
            os.system("pause")
            break
        
        #Convert Camera Still to Grayscale
        imgGrayScale = cv2.cvtColor(imgCapture, cv2.COLOR_BGR2GRAY)

        #Apply Face Cascade Classifier
        faces = faceCascade.detectMultiScale(imgGrayScale, 1.2, 5, minSize=(30,30), flags = cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT)

        print "Found {0} face(s)!".format(len(faces))

        #Draws Rectangles Around Recognized Faces and Sends Coordinates to Serial
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
