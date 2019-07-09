from simple_pid import PID
from vectorAlgebra import VectorAlgebra


class Servo():
    # param servoCoordinate as list
    # param setPoint as list
    def __init__(self, servoCoordinate, direction, servo, p, i, d, setPoint):
        self.position = (x, y)
        self.direction = direction
        self.servo = servo

        self.pid = PID(p, i, d, VectorAlgebra.projectionLength(setPoint, direction)))


    def setSetPoint(self, x, y):
        self.pid.setpoint(VectorAlgebra.projectionLength([x, y], self.direction))

    def update(self, ballPosition):
        # pid controller
        # calculate ball position os it's own axes

