import cv2 as cv
from simple_pid import PID
import sys
from camera import camera
from tracking import tracking
from GUIController import GUIController
 
if __name__ == '__main__' :
 
 
 #----------------------------setup camera----------------

    camera = camera(1)

     
#-----------------------------tracker setup----------------------------------

    tracking = tracking(camera)
    
    targetPosition = (int(tracking.bbox[0]), int(tracking.bbox[1]))
 
#--------------------------window setup---------------------------------------

    GUI = GUIController(camera, tracking)

#----------------------------setup servo--------------------------

    Servo1 = GUI.selectPoint(camera.getNewFrame())
    GUI.setCircle(Servo1, 5, (0,0,255))
    Servo2 = GUI.selectPoint(camera.getNewFrame())
    GUI.setCircle(Servo2, 5, (0,0,255))
    Servo3 = GUI.selectPoint(camera.getNewFrame())
    GUI.setCircle(Servo3, 5, (0,0,255))

    # calculate servo direction and create servo objects

#--------------------------setup PID controller ---------------------------------

    kp = 1
    ki = 0.1
    kd = 0.05

#-------------------------main loop---------------------------------------

    while True:

        position = tracking.run()
 
        # draw the targetPosition circle
        if GUI.getLastClick() is not False:
            targetPosition = GUI.getLastClick()
        GUI.update(position, camera.getFrame(), targetPosition)
 
        # Exit if ESC pressed
        k = cv.waitKey(1) & 0xff
        if k == 27 : break