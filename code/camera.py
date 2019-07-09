import cv2 as cv
import sys

class camera():
    
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

    # get the frame
    def getFrame(self):
        return self.frame

    # update the frame and return it
    def getNewFrame(self):
        self.ok, self.frame = self.video.read()
        return self.frame

