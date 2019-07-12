from simple_pid import PID
from vectorAlgebra import VectorAlgebra as VecMath
from servoFirmata import servoFirmata
import time


class Servo():
    
    """Servo constructor, creates a Servo object with the given paramters

    Parameters
    ----------
    direction : list(x, y)
        The direction of the axes of this servo
    servoFir : servoFirmata
        The servoFirmata object of this servo
    p : float
        kp for the pid system of this servo
    i : float
        ki for the pid system of this servo
    d : float
        kd for the pid system of this servo
    setPoint : list(x, y)
        The set point 
    level : int
        The value at which the servo is flat
    """
    def __init__(self, direction, servoFir, p, i, d, setPoint, level, debug = False):            
        # min and max are inverted for the servo
        self.minServoPos = 80
        self.maxServoPos = 20

        # min and max values for the pid system
        self.minPidOut = -100
        self.maxPidOut = 100

        self.level = level
        self.direction = direction
        self.servoFir = servoFir
        self.debug = debug

        # setup the pid system
        self.pid = PID(p, i, d, VecMath.projectionLength(setPoint, direction))

        # set pid controller output limit
        self.pid.output_limits = (self.minPidOut, self.maxPidOut) 

    """setDebug, sets the debug variable. if True the update function will return values for debugging

    Parameters
    ----------
    debug : bool
        new debug value
    """
    def setDebug(self, debug):
        self.debug = debug

    """setSetPoint, sets setPoint variable. This is the point where the system wants the ball to go. It will project the setpoint on the axes of the servo

    Parameters
    ----------
    setPoint : list(x, y)
        new setPoint
    """
    def setSetPoint(self, setPoint):
        self.pid.setpoint = VecMath.projectionLength(setPoint, self.direction)

    """update, updates the servo position based on the position of the ball

    Parameters
    ----------
    ballPosition : list(x, y)
        position of the ball
    Return, only returns if debug is True
    ----------
    : tuple
        (error, control, control_old)
    """
    def update(self, ballPosition):

        # project the ball on the servo axes
        ballPosition = VecMath.projectionLength(ballPosition, self.direction)

        # get control from the pid system
        control = self.pid(ballPosition)
        # remember old control for debugging
        if self.debug:
            control_old = control

        # convert control to value that the servo supports
        control = self.level + control * (self.maxServoPos - self.minServoPos) / (self.maxPidOut - self.minPidOut) /2

        # set the new servo position
        self.servoFir.setPosition(0, control)

        #return for debugging
        if self.debug:
            # return is the following tuple: (error, control, control_old)
            return (int(self.pid.setpoint - ballPosition), round(control, 3), control_old)
