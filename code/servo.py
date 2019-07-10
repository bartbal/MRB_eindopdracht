from simple_pid import PID
from vectorAlgebra import VectorAlgebra
from servoFirmata import servoFirmata


class Servo():
    
    
    # param servoCoordinate as list
    # param setPoint as list
    def __init__(self, servoCoordinate, direction, servoFir, p, i, d, setPoint):    
        self.position = (x, y)
        self.direction = direction
        self.servoFir = servoFir

        self.pid = PID(p, i, d, VectorAlgebra.projectionLength(setPoint, direction))
        self.pid.output_limits = (self.minPidOut, self.maxPidOut) # set pid controller output limit

        # min and max are inverted
        self.minServoPos = 70
        self.maxServoPos = 10

        self.minPidOut = 0
        self.maxPidOut = 10


    def setSetPoint(self, x, y):
        self.pid.setpoint(VectorAlgebra.projectionLength([x, y], self.direction))

    def update(self, ballPosition):
        control = self.pid(VectorAlgebra.projectionLength(ballPosition, self.direction))
        
        servoFir.setPosition(0, (control - self.minPidOut) * (self.maxServoPos - self.minServoPos) / (self.maxPidOut - self.minPidOut) + self.minServoPos)


        

