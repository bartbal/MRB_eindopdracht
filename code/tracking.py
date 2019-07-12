import cv2 as cv
# from camera.py import camera

class tracking():
    
    """tracking constructor, creates a tracking object with the given paramters

    Parameters
    ----------
    camera : camera
        camera object
    """
    def __init__(self, camera):
        # set the tracker type
        self.tracker = cv.TrackerCSRT_create()

        # Define an initial bounding box
        self.bbox = (308, 308, 80, 62)
    
        # select a bounding box
        self.bbox = cv.selectROI(camera.frame, False)

        print("bounding box values: " + str(self.bbox))
    
        # Initialize tracker with first frame and bounding box
        self.ok = self.tracker.init(camera.frame, self.bbox)

        self.camera = camera

    """run, get the position of the tracked object, if the object can not be found the function returns False

    Return
    ----------
    position : tuple(p1, p2, p3)
        p1 : tuple(x, y) - top left corner of the bounding box
        p2 : tuple(x, y) - bottem right corner of the bounding box
        p3 : tuple(x, y) - center of the bounding box
    False : bool
        when a tracking error accours
    
    """
    def run(self):
        # Read a new frame
        self.frame = self.camera.getNewFrame()
        if not self.camera.ok:
            return False
 
        # Update tracker
        self.ok, self.bbox = self.tracker.update(self.frame)
 
        # Draw bounding box
        if self.ok:
            # Tracking success
            p1 = (int(self.bbox[0]), int(self.bbox[1]))
            p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]))
            # center coordinates of the detected object.
            p3 = (int((p2[0] - p1[0]) / 2 + p1[0]), int((p2[1] - p1[1]) / 2 + p1[1])) 
            return (p1, p2, p3)
        else :
            return False