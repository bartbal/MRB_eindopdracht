from simple_pid import PID
from vectorAlgebra import VectorAlgebra
from servoFirmata import servoFirmata


class Servo():
    
    
    # param servoCoordinate as list
    # param setPoint as list
    def __init__(self, direction, servoFir, p, i, d, setPoint):    
        # min and max are inverted
        self.minServoPos = 70
        self.maxServoPos = 10

        self.minPidOut = 0
        self.maxPidOut = 10
        self.direction = direction
        self.servoFir = servoFir

        self.pid = PID(p, i, d, VectorAlgebra.projectionLength(setPoint, direction))
        self.pid.output_limits = (self.minPidOut, self.maxPidOut) # set pid controller output limit



    def setSetPoint(self, setPoint):
        self.pid.setpoint(VectorAlgebra.projectionLength(setPoint, self.direction))

    def update(self, ballPosition):
        control = self.pid(VectorAlgebra.projectionLength(ballPosition, self.direction))
        
        self.servoFir.setPosition(0, (control - self.minPidOut) * (self.maxServoPos - self.minServoPos) / (self.maxPidOut - self.minPidOut) + self.minServoPos)
