import cv2 as cv
from simple_pid import PID
import sys
from camera import camera
from tracking import tracking
from GUIController import GUIController
from servoFirmata import servoFirmata
from servo import Servo
from pyfirmata import Board, boards
 
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

    kp = 1
    ki = 0.1
    kd = 0.05

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
    servoFirmata1 = servoFirmata(arduino, [3], [servoInitPos])
    servoFirmata2 = servoFirmata(arduino, [5], [servoInitPos])
    servoFirmata3 = servoFirmata(arduino, [12], [servoInitPos])

    #---------------------------create servo objects----------------------------------------------------------------------

    # calculate the avarage of servoPos2 and servoPos3 and substract servoPos1. result is direction of servo1
    dirServo = [(servoPos2[0] + servoPos3[0]/2) - servoPos1[0], (servoPos2[1] + servoPos3[1]/2) - servoPos1[1]]
    servo1 = Servo(dirServo, servoFirmata1, kp, ki, kd, targetPosition)

    # calculate the avarage of servoPos1 and servoPos3 and substract servoPos2. result is direction of servo2
    dirServo = [(servoPos1[0] + servoPos3[0]/2) - servoPos2[0], (servoPos1[1] + servoPos3[1]/2) - servoPos2[1]]
    servo2 = Servo(dirServo, servoFirmata2, kp, ki, kd, targetPosition)

    # calculate the avarage of servoPos2 and servoPos1 and substract servoPos3. result is direction of servo3
    dirServo = [(servoPos2[0] + servoPos1[0]/2) - servoPos3[0], (servoPos2[1] + servoPos1[1]/2) - servoPos3[1]]
    servo3 = Servo(dirServo, servoFirmata3, kp, ki, kd, targetPosition)

    #-----------------------------------------------------------------------------------------------------------------------

    # calculate servo direction and create servo objects

#-------------------------main loop---------------------------------------

    while True:

        position = tracking.run()

        # draw the targetPosition circle
        if GUI.getLastClick() is not False:
            targetPosition = GUI.getLastClick()
            servo1.setSetPoint(targetPosition)
            servo2.setSetPoint(targetPosition)
            servo3.setSetPoint(targetPosition)
        GUI.update(position, camera.getFrame(), targetPosition)
        if position is not False:
            servo1.update(position[2])
            servo2.update(position[2])
            servo3.update(position[2])
 
        # Exit if ESC pressed
        k = cv.waitKey(1) & 0xff
        if k == 27 : break