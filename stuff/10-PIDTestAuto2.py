from PIDController import PIDController

from PiStorms import PiStorms
import time
from Gyro import Gyro
from Driver import *

psm = PiStorms()     

class Follower(object):
    def __init__(self, controller, driver, ultrasonic):
        self.controller = controller
        self.driver = driver
        self.ultrasonic = ultrasonic
        self.output = 0
    def get_error(self):
        return 250 - self.ultrasonic.distanceUSEV3()
    def follow(self):
        error = self.get_error()
        #print "error", error

        output = self.controller.run(self.get_error())
        self.output = output
        #print "PID " + str(output)
        self.driver.drive_straight(output)
        self.driver.step()

    def step(self):
        self.follow()
    def done(self):
        if self.output < 10 and abs(self.get_error()) < 20:
            return True
        else:
            return False

gyro = Gyro(psm.BAS2)
gyro.calibrate(1)
print "Calibrate done error=", gyro.error_rate
controller = PIDController(1.5, 0, 0.1)
controller2 = PIDController(1, 0, 0.1)
driver = Driver(psm.BAM1, psm.BAM2, gyro, 3)

point = Point(100, 100, driver, gyro, controller, controller2, driver.mapper)
try:
    while True:
        point.step()
except:
    psm.BAM1.setSpeed(0)
    psm.BAM2.setSpeed(0)

