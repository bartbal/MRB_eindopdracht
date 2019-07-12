import cv2 as cv
from simple_pid import PID
import sys
from camera import camera
from tracking import tracking
from GUIController import GUIController
from servoFirmata import servoFirmata
from servo import Servo
from pyfirmata import Board, boards
from vectorAlgebra import VectorAlgebra as VecMath
 
if __name__ == '__main__' :
 
 
#-----------------------set debug-------------------

    debug = False

#----------------------------setup camera----------------

    # create camera object
    camera = camera(1)

     
#-----------------------------tracker setup----------------------------------

    # create camera object
    tracking = tracking(camera)
    
    # set targetPosition to the center of the bounding box
    targetPosition = (int((tracking.bbox[0] + tracking.bbox[2] - tracking.bbox[0]) / 2 + tracking.bbox[0]), int((tracking.bbox[1] + tracking.bbox[3] - tracking.bbox[1]) / 2 + tracking.bbox[1]))
 
#--------------------------window setup---------------------------------------

    # create GUIController object
    GUI = GUIController(camera, tracking)

#--------------------------setup PID controller ---------------------------------
    #set the pid values

    # tafel voedbal balltje
    # kp = 0.37
    # ki = 0.03
    # kd = 0.25

    # knikker
    kp = 0.85
    ki = 0.11
    kd = 0.54

#----------------------------setup servo--------------------------

    # set the post
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

    # create a Board object
    arduino = Board(Comport, boards.BOARDS["arduino_due"])

    # set initial servo position
    servoInitPos = 65
    
    # create a servoFirmate object per servo
    servoFirmata1 = servoFirmata(arduino, [2], [servoInitPos])
    servoFirmata2 = servoFirmata(arduino, [3], [servoInitPos])
    servoFirmata3 = servoFirmata(arduino, [4], [servoInitPos])

    #---------------------------create servo objects----------------------------------------------------------------------

    # calculate the avarage of servoPos2 and servoPos3 and substract servoPos1. result is direction of servo1
    dirServo1 = [(servoPos2[0] + servoPos3[0])/2 - servoPos1[0], (servoPos2[1] + servoPos3[1])/2 - servoPos1[1]]
    # create servo1 object
    servo1 = Servo(dirServo1, servoFirmata1, kp, ki, kd, targetPosition, 52, debug)

    # calculate the avarage of servoPos1 and servoPos3 and substract servoPos2. result is direction of servo2
    dirServo2 = [(servoPos1[0] + servoPos3[0])/2 - servoPos2[0], (servoPos1[1] + servoPos3[1])/2 - servoPos2[1]]
    # create servo2 object
    servo2 = Servo(dirServo2, servoFirmata2, kp, ki, kd, targetPosition, 45, debug)

    # calculate the avarage of servoPos2 and servoPos1 and substract servoPos3. result is direction of servo3
    dirServo3 = [(servoPos2[0] + servoPos1[0])/2 - servoPos3[0], (servoPos2[1] + servoPos1[1])/2 - servoPos3[1]]
    # create servo3 object
    servo3 = Servo(dirServo3, servoFirmata3, kp, ki, kd, targetPosition, 48, debug)

    #-----------------------------------------setup pid sliders----------------------------------------------------

    # create window fot the pid sliders
    cv.namedWindow('sliders')

    """setKp, set the kp for the pid system of every servo

    Parameters
    ----------
    value : int
        new kp value
    """
    def setKp(value):
        value /= 100
        servo1.pid.Kp = value
        servo2.pid.Kp = value
        servo3.pid.Kp = value

    """setKi, set the ki for the pid system of every servo

    Parameters
    ----------
    value : int
        new ki value
    """
    def setKi(value):
        value /= 100
        servo1.pid.Ki = value
        servo2.pid.Ki = value
        servo3.pid.Ki = value

    """setKd, set the kd for the pid system of every servo

    Parameters
    ----------
    value : int
        new kd value
    """
    def setKd(value):
        value /= 100
        servo1.pid.Kd = value
        servo2.pid.Kd = value
        servo3.pid.Kd = value

    # create trackbars for the pid sliders
    cv.createTrackbar('kp','sliders',int(kp*100),100,setKp)
    cv.createTrackbar('ki','sliders',int(ki*100),100,setKi)
    cv.createTrackbar('kd','sliders',int(kd*100),100,setKd)

#-------------------------main loop---------------------------------------

    while True:   

        # get the position of the ball
        position = tracking.run()

        # get a new frame
        frame = camera.getFrame()

        # show the pid values in the window
        cv.putText(frame, "KP: {}".format(servo1.pid.Kp), (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)
        cv.putText(frame, "KI: {}".format(servo1.pid.Ki), (10, 70), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)
        cv.putText(frame, "KD: {}".format(servo1.pid.Kd), (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),1)

        # update the setPoint and draw the targetPosition circle
        if GUI.getLastClick() is not False:
            targetPosition = GUI.getLastClick()
            servo1.setSetPoint(targetPosition)
            servo2.setSetPoint(targetPosition)
            servo3.setSetPoint(targetPosition)

        if debug:
            #-----------------------------run program and print debug info and lines----------------------------------------------------
            if position is not False:
                # update the servo positions and draw their debug values
                cv.putText(frame, "servo1: {}".format(servo1.update(position[2])), servoPos1, cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
                cv.putText(frame, "servo2: {}".format(servo2.update(position[2])), servoPos2, cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
                cv.putText(frame, "servo3: {}".format(servo3.update(position[2])), servoPos3, cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
            else:
                # tracking error, set servo's to initial positions, and print message
                servoFirmata1.setPosition(0, servoInitPos)
                servoFirmata2.setPosition(0, servoInitPos)
                servoFirmata3.setPosition(0, servoInitPos)
                print("tracking error")
            # calculate the a second point on the line of every servo exes
            p1 = VecMath.vectorAdd(servoPos1, VecMath.vectorNumMultiply(dirServo1, 1))
            p2 = VecMath.vectorAdd(servoPos2, VecMath.vectorNumMultiply(dirServo2, 1))
            p3 = VecMath.vectorAdd(servoPos3, VecMath.vectorNumMultiply(dirServo3, 1))
            # draw the servo exes line for every servo
            cv.line(frame, servoPos1, (int(p1[0]), int(p1[1])), (255, 0, 0), 1)
            cv.line(frame, servoPos2, (int(p2[0]), int(p2[1])), (255, 0, 0), 1)
            cv.line(frame, servoPos3, (int(p3[0]), int(p3[1])), (255, 0, 0), 1)
        else:
            #-----------------------------run program withoud debug info and lines----------------------------------------------------
            if position is not False:  
                # update the servo positions
                servo1.update(position[2])
                servo2.update(position[2])
                servo3.update(position[2])
            else:
                # tracking error, set servo's to initial positions, and print message
                servoFirmata1.setPosition(0, 90)
                servoFirmata2.setPosition(0, 90)
                servoFirmata3.setPosition(0, 90)
                print("tracking error")
 
        # update the GUI
        GUI.update(position, frame, targetPosition)
        
        # Exit if ESC pressed
        k = cv.waitKey(1) & 0xff
        if k == 27 : 
            # set the servo's to the down position
            servoFirmata1.setPosition(0, 90)
            servoFirmata2.setPosition(0, 90)
            servoFirmata3.setPosition(0, 90)
            arduino.exit()
            break
            
        