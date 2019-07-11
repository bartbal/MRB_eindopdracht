import cv2 as cv
import time

class Circle():
    def __init__(self, position, radius, color):
        self.position = position
        self.radius = radius
        self.color = color


class GUIController():
    
    def __init__(self, camera, tracking):
        # create named window
        cv.namedWindow('Tracking')
        
        # set mouse event
        cv.setMouseCallback('Tracking', self.select_point)

        self.lastClick = False

        self.camera = camera

        self.tracking = tracking

        self.cirlces = []

    # function to detect click and save mouse location to targetPosition
    def select_point(self, event,x,y,flags, params):
        if event == cv.EVENT_LBUTTONDOWN:
            self.lastClick = (x, y)

    # get the location of the last click, false if there hasn't been a click yet
    def getLastClick(self):
        return self.lastClick

    # update the window
    def update(self, position, frame, targetPosition):

        for circle in self.cirlces:
            cv.circle(frame, circle.position, circle.radius, circle.color)

        # Draw bounding box
        if position is not False:
            # Tracking success
            cv.rectangle(frame, position[0], position[1], (255,0,0), 2, 1)
            cv.circle(frame, position[2], 5, (0,0,255)) #mark center of rectangle
        else :
            # Tracking failure
            cv.putText(frame, "Tracking failure detected", (100,80), cv.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        cv.circle(frame, targetPosition, 5, (0,255,0)) 

        # Display result
        cv.imshow("Tracking", frame)


    # def showOnFrame(self, string, position, fontsize = 0.5):


    def setCircle(self, position, radius, color):
        self.cirlces.append(Circle(position, radius, color))

    def selectPoint(self, frame):
        self.lastClick = False 

        for circle in self.cirlces:
            cv.circle(frame, circle.position, circle.radius, circle.color)

        # Display result
        cv.imshow("Tracking", frame)
       
        while True:
            if self.lastClick is not False:
                lastClick = self.lastClick
                self.lastClick = False
                
                cv.circle(frame, lastClick, 5, (0,0,255))
                cv.imshow("Tracking", frame)
                return lastClick

            # Exit if ESC pressed
            k = cv.waitKey(1) & 0xff
            if k == 27 : break
            # time.sleep(0.5)
