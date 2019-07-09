import cv2 as cv
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