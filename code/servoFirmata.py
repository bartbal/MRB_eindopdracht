class servoFirmata:
    """Class to control servo's on a arduino that runs standard Firmata"""

    def __init__(self, arduinoBoard, pinNumbers, initalPositions):
        """servoFirmata constructor, creates a servoFirmata object with the given paramters

        Parameters
        ----------
        arduinoBoard : Board
            The arduino board this class will send the Firmata commands to.
        pinNumbers : list
            A list with integers that represent the pin numbers on which servo's are connected
        initalPositions : list
            A list with integers that represent the initial positions of the servo's
        """
        self.arduino = arduinoBoard

        self.pins = pinNumbers
        for index in range(len(pinNumbers)):
            self.arduino.servo_config(pinNumbers[index], initalPositions[index])
            self.arduino.digital[pinNumbers[index]].write(initalPositions[index])# set the pos to the initialPositions
                                                                                # because the servo_config function
                                                                                # does not seem to do so.


    def setPosition(self, servoID, position):
        """servoFirmata constructor, creates a servoFirmata object with the given paramters

        Parameters
        ----------
        servoID : integer
            The number of the servo. Note that this is NOT the pin number
        position : integer
            The position the servo has to go to in degrees
        """
        self.arduino.digital[self.pins[servoID]].write(position)
