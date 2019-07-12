import cv2 as cv
import time

class Circle():
    
    def __init__(self, position, radius, color):
        """GUIController constructor, creates a GUIController object with the given paramters

        Parameters
        ----------
        position : list(x, y)
            position of the circle
        radius : int
            radius of the circle
        color : tuple(B, G, R)
            The RGB color values of the circle
        """
        self.position = position
        self.radius = radius
        self.color = color


class GUIController():
    
    """GUIController constructor, creates a GUIController object with the given paramters

    Parameters
    ----------
    camera : camera
        camera object
    tracking : tracking
        tracking object
    """
    def __init__(self, camera, tracking):
        # create named window
        cv.namedWindow('Tracking')
        
        # set mouse event
        cv.setMouseCallback('Tracking', self.select_point)

        self.lastClick = False
        self.camera = camera
        self.tracking = tracking
        self.cirlces = []

    """select_point, detect click and save mouse location to targetPosition

    Parameters
    ----------
    event : cv event
        event that triggered this function
    x : int
        x position of the mouse
    y : int
        y position of the mouse
    flags : 
        flags
    params :
        params
    """
    def select_point(self, event,x,y,flags, params):
        if event == cv.EVENT_LBUTTONDOWN:
            self.lastClick = (x, y)


    """getLastClick, get the location of the last click, false if there hasn't been a click yet

    Return
    ----------
    lastClick : tuple(x, y) or bool
        tuple with the position where was clicked the last time
        or
        bool with False if there hasn't been clicked yet
    """
    def getLastClick(self):
        return self.lastClick

    """update, update the GUI

    Parameters
    ----------
    position : tuple((x, y), (x, y), (x, y))
        position[0] top left corner of the bounding box
        position[1] bottem right corner of the bounding box
        position[2] center of the bounding box
    frame : list
        the frame to display
    targetPosition : tuple(x, y)
        The position the ball should go to
    """
    def update(self, position, frame, targetPosition):
        # draw the circles
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

        # draw a circle at the targetPosition
        cv.circle(frame, targetPosition, 5, (0,255,0)) 

        # Display result
        cv.imshow("Tracking", frame)

    """setCircle, add a circle to the circles list. This list contains circles that have to b drawn every time a frame is shown

    Parameters
        ----------
        position : list(x, y)
            position of the circle
        radius : int
            radius of the circle
        color : tuple(B, G, R)
            The RGB color values of the circle
    """
    def setCircle(self, position, radius, color):
        self.cirlces.append(Circle(position, radius, color))

    """selectPoint, select a point on the frame

    Parameters
        ----------
        frame : list
            frame
    Return
        ----------
        lastClick : list(x, y)
            the position where was clicked on the frame
    """
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
