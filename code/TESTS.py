from pyfirmata import Board
from pyfirmata import boards
import time
import servoFirmata
import sys

# ========Test classes===========================================================================================

class servoFirmataTest:

    def __init__(self, comPort, pinNumbers):
        assert len(pinNumbers) > 0, "Parameter pinNumbers has to contain at least one number"
        assert type(pinNumbers[0]) is int and type(pinNumbers[1]) is int, "pinNumbers must contain integers"

        self.arduino = Board(comPort, boards.BOARDS["arduino_due"])

        if(len(pinNumbers)>1):
            self.pins = pinNumbers[:2]
        else:
            self.pins = pinNumbers

        self.servos = servoFirmata.servoFirmata(self.arduino, self.pins, [90,90])
        time.sleep(2)


    def execute(self):
        print("Servo zero to pos 0")
        self.servos.setPosition(0, 0)
        time.sleep(3)

        print("Servo one to pos 0")
        self.servos.setPosition(1, 0)
        time.sleep(3)

        print("Servo zero and one to pos 90")
        self.servos.setPosition(0, 90)
        self.servos.setPosition(1, 90)
        time.sleep(3)

        print("Test complete")

        self.arduino.exit()

        return True

# =========Test execution====================================================================================

print("Enter com port:")
comPort = input()

print("Enter first servo pin:")
pinOne = int(input())
print("Enter second servo pin:")
pinTwo = int(input())

servoTests = servoFirmataTest(comPort, [pinOne, pinTwo])

if(servoTests.execute()):
    print("ServoTests completed successfully!")
else:
    print("ServoTests failed!")

sys.exit()
