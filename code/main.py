import cv2 as cv
from simple_pid import PID
import sys
from camera import camera
from tracking import tracking
from GUIController import GUIController
from servoFirmata import servoFirmata
from servo import Servo
from pyfirmata import Board, boards
from vectorAlgebra import VectorAlgebra
 
if __name__ == '__main__' :
 
 
 #----------------------------setup camera----------------

    camera = camera(1)

     
#-----------------------------tracker setup----------------------------------

    tracking = tracking(camera)
    
    #targetPosition = (int(tracking.bbox[0]), int(tracking.bbox[1]))
    targetPosition = (int((tracking.bbox[0] + tracking.bbox[2] - tracking.bbox[0]) / 2 + tracking.bbox[0]), int((tracking.bbox[1] + tracking.bbox[3] - tracking.bbox[1]) / 2 + tracking.bbox[1]))
 
#--------------------------window setup---------------------------------------

    GUI = GUIController(camera, tracking)

#--------------------------setup PID controller ---------------------------------

    # tafel voedbal balltje
    kp = 0.37
    ki = 0.03
    kd = 0.25

    # ping pong balletje
    # kp = 0.18
    # ki = 0.20
    # kd = 0.23

#----------------------------setup servo--------------------------

    Comport = "/dev/ttyACM0"

    #-------------select servo locations------------
    servoPos1 = GUI.selectPoint(camera.getNewFrame())
    GUI.setCircle(servoPos1, 5, (0,0,255))
    servoPos2 = GUI.selectPoint(camera.getNewFrame())
    GUI.setCircle(servoPos2, 5, (0,0,255))
    servoPos3 = GUI.selectPoint(camera.getNewFrame())
    GUI.setCircle(servoPos3, 5, (0,0,255))

    print('servo positions set')
    #-----------------------------------------------

    arduino = Board(Comport, boards.BOARDS["arduino_due"])

    servoInitPos = 65
    servoFirmata1 = servoFirmata(arduino, [2], [servoInitPos])
    servoFirmata2 = servoFirmata(arduino, [3], [servoInitPos])
    servoFirmata3 = servoFirmata(arduino, [4], [servoInitPos])

    #---------------------------create servo objects----------------------------------------------------------------------

    # calculate the avarage of servoPos2 and servoPos3 and substract servoPos1. result is direction of servo1
    dirServo1 = [(servoPos2[0] + servoPos3[0])/2 - servoPos1[0], (servoPos2[1] + servoPos3[1])/2 - servoPos1[1]]
    # dirServo1 = VectorAlgebra.unitVector(dirServo1)
    servo1 = Servo(dirServo1, servoFirmata1, kp, ki, kd, targetPosition)

    # calculate the avarage of servoPos1 and servoPos3 and substract servoPos2. result is direction of servo2
    dirServo2 = [(servoPos1[0] + servoPos3[0])/2 - servoPos2[0], (servoPos1[1] + servoPos3[1])/2 - servoPos2[1]]
    # dirServo2 = VectorAlgebra.unitVector(dirServo2)
    servo2 = Servo(dirServo2, servoFirmata2, kp, ki, kd, targetPosition)

    # calculate the avarage of servoPos2 and servoPos1 and substract servoPos3. result is direction of servo3
    dirServo3 = [(servoPos2[0] + servoPos1[0])/2 - servoPos3[0], (servoPos2[1] + servoPos1[1])/2 - servoPos3[1]]
    # dirServo3 = VectorAlgebra.unitVector(dirServo3)
    servo3 = Servo(dirServo3, servoFirmata3, kp, ki, kd, targetPosition)

    #-----------------------------------------------------------------------------------------------------------------------

    # calculate servo direction and create servo objects

    cv.namedWindow('sliders')

    def setKp(value):
        value /= 100
        servo1.pid.Kp = value
        servo2.pid.Kp = value
        servo3.pid.Kp = value

    def setKi(value):
        value /= 100
        servo1.pid.Ki = value
        servo2.pid.Ki = value
        servo3.pid.Ki = value

    def setKd(value):
        value /= 100
        servo1.pid.Kd = value
        servo2.pid.Kd = value
        servo3.pid.Kd = value

    # create trackbars for color change
    cv.createTrackbar('kp','sliders',int(kp*100),1000,setKp)
    cv.createTrackbar('ki','sliders',int(ki*100),1000,setKi)
    cv.createTrackbar('kd','sliders',int(kd*100),1000,setKd)

#-------------------------main loop---------------------------------------

    while True:

        

        position = tracking.run()

        frame = camera.getFrame()

        cv.putText(frame, "KP: {}".format(servo1.pid.Kp), (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)
        cv.putText(frame, "KI: {}".format(servo1.pid.Ki), (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)
        cv.putText(frame, "KD: {}".format(servo1.pid.Kd), (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)

        # draw the targetPosition circle
        if GUI.getLastClick() is not False:
            targetPosition = GUI.getLastClick()
            servo1.setSetPoint(targetPosition)
            servo2.setSetPoint(targetPosition)
            servo3.setSetPoint(targetPosition)
        if position is not False:
            cv.putText(frame, "servo1: {}".format(servo1.update(position[2])), servoPos1, cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
            cv.putText(frame, "servo2: {}".format(servo2.update(position[2])), servoPos2, cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
            cv.putText(frame, "servo3: {}".format(servo3.update(position[2])), servoPos3, cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
        p1 = VectorAlgebra.vectorAdd(servoPos1, VectorAlgebra.vectorNumMultiply(dirServo1, 1))
        p2 = VectorAlgebra.vectorAdd(servoPos2, VectorAlgebra.vectorNumMultiply(dirServo2, 1))
        p3 = VectorAlgebra.vectorAdd(servoPos3, VectorAlgebra.vectorNumMultiply(dirServo3, 1))
        cv.line(frame, servoPos1, (int(p1[0]), int(p1[1])), (255, 0, 0), 1)
        cv.line(frame, servoPos2, (int(p2[0]), int(p2[1])), (255, 0, 0), 1)
        cv.line(frame, servoPos3, (int(p3[0]), int(p3[1])), (255, 0, 0), 1)
        

        GUI.update(position, frame, targetPosition)
        # if position is not False:  
        #     servo1.update(position[2])
        #     servo2.update(position[2])
        #     servo3.update(position[2])
        # else:
        #     print("tracking error")
 
        # Exit if ESC pressed
        k = cv.waitKey(1) & 0xff
        if k == 27 : 
            servoFirmata1.setPosition(0, 90)
            servoFirmata2.setPosition(0, 90)
            servoFirmata3.setPosition(0, 90)
            arduino.exit()
            print("exit")
            break
        