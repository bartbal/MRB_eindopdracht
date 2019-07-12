import cv2 as cv
import sys

class camera():
    
    """camera constructor, creates a camera object with the given paramters

    Parameters
    ----------
    camNumber : int
        number of the camera
    """
    def __init__(self, camNumber):
        # Read video
        self.video = cv.VideoCapture(1)
    
        # Exit if video not opened.
        if not self.video.isOpened():
            print("Could not open video")
            sys.exit()
    
        # Read first frame.
        self.ok, self.frame = self.video.read()
        if not self.ok:
            print('Cannot read video file')
            sys.exit()

    """getFrame, get the frame. this is not a new frame! use getNewFrame to get a new frame and update the variable that is returned by this function

    Return
    ----------
    frame : list
        the frame variable stored in this object
    """
    def getFrame(self):
        return self.frame

    # update the frame and return it
    """getNewFrame, get a new frame. Sets the self.frame variable and returns it

     Return
    ----------
    frame : list
        the frame variable stored in this object
    """
    def getNewFrame(self):
        self.ok, self.frame = self.video.read()
        return self.frame

