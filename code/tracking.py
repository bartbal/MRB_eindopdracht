import cv2 as cv
# from camera.py import camera

class tracking():
    
    def __init__(self, camera):
        self.tracker = cv.TrackerCSRT_create()

        # Define an initial bounding box
        self.bbox = (308, 308, 80, 62)
    
        # select a bounding box
        self.bbox = cv.selectROI(camera.frame, False)

        print("bounding box values: " + str(self.bbox))
    
        # Initialize tracker with first frame and bounding box
        self.ok = self.tracker.init(camera.frame, self.bbox)

        self.camera = camera

    # get the new position
    # @return position - list: 
    # position[0] : left top corner of the bounding box - tuple(int, int),
    # position[1] : right bottom corner of the bounding box - tuple(int, int),
    # position[2] : center of the bounding box - tuple(int, int)
    # when tracking error occurs the return value is False
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
            p3 = (int((p2[0] - p1[0]) / 2 + p1[0]), int((p2[1] - p1[1]) / 2 + p1[1])) # center coordinates of the detected object.
            return (p1, p2, p3)
        else :

            return False