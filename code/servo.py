from simple_pid import PID
from vectorAlgebra import VectorAlgebra
from servoFirmata import servoFirmata
import time


class Servo():
    
    
    # param servoCoordinate as list
    # param setPoint as list
    def __init__(self, direction, servoFir, p, i, d, setPoint):    
        # min and max are inverted
        self.minServoPos = 80
        self.maxServoPos = 20

        self.minPidOut = -100
        self.maxPidOut = 100
        self.direction = direction
        self.servoFir = servoFir

        self.pid = PID(p, i, d, VectorAlgebra.projectionLength(setPoint, direction))
        self.pid.sample_time = 0.01  # update every 0.01 seconds

        # self.pid.Kd
        self.pid.output_limits = (self.minPidOut, self.maxPidOut) # set pid controller output limit



    def setSetPoint(self, setPoint):
        self.pid.setpoint = VectorAlgebra.projectionLength(setPoint, self.direction)

    def update(self, ballPosition):
        ballPosition = VectorAlgebra.projectionLength(ballPosition, self.direction)
        control = control_old = self.pid(ballPosition)

        control = (control - self.minPidOut) * (self.maxServoPos - self.minServoPos) / (self.maxPidOut - self.minPidOut) + self.minServoPos
        
        # if(self.pid.setpoint - ballPosition < 0):
        #     # minus = True
        #     control = (control - self.minPidOut) * (self.maxServoPos - self.minServoPos) / (self.maxPidOut - self.minPidOut) + self.minServoPos
        #     # control = (control - self.minPidOut) * (self.minServoPos - self.maxServoPos) / (self.maxPidOut - self.minPidOut) + self.maxServoPos
        # else:
        #     # minus = False
        #     control = (control - self.minPidOut) * (self.minServoPos - self.maxServoPos) / (self.maxPidOut - self.minPidOut) + self.maxServoPos  
        #     # control = (control / (self.maxPidOut - self.minPidOut)*(self.minServoPos - self.maxServoPos)+((self.minServoPos-self.maxServoPos)/2)+self.maxServoPos)                   


        self.servoFir.setPosition(0, control)
        # self.servoFir.setPosition(0, (control - self.minPidOut) * (self.minServoPos - self.maxServoPos) / (self.maxPidOut - self.minPidOut) + self.maxServoPos)
        # temp = VectorAlgebra.projectionLength(ballPosition, self.direction)
        return (int(self.pid.setpoint - ballPosition), round(control, 3), control_old)
