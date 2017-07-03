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
class PathFollower(object):
    def __init__(self, points , driver, gyro, controller1, controller2):
        self.points = points
        self.driver = driver
        self.gyro = gyro
        self.controller1 = controller1
        self.controller2 = controller2
        self.current_index = 0
        self.follower = None
        self.done = False

    def step (self):
        try:
            if self.follower == None or self.follower.driveDone:
                self.follower = Point(self.points[self.current_index][0], self.points[self.current_index][1], self.driver, self.gyro, self.controller1, self.controller2, self.driver.mapper)
                self.current_index += 1
            else:
                self.follower.step()
        except:
            psm.BAM1.setSpeed(0)
            psm.BAM2.setSpeed(0)
            self.done = True

gyro = Gyro(psm.BAS2)
gyro.calibrate(1)
print "Calibrate done error=", gyro.error_rate
controller = PIDController(1.5, 0, 0.1)
controller2 = PIDController(1, 0, 0.1)
driver = Driver(psm.BAM1, psm.BAM2, gyro, 3)

follower = PathFollower([[1000, 1000], [3700,1000],[6000,-100]],driver, gyro, controller, controller2)
try:
    while not follower.done:
        follower.step()
except:
    psm.BAM1.setSpeed(0)
    psm.BAM2.setSpeed(0)


psm.BAM1.setSpeed(0)
psm.BAM2.setSpeed(0)
driver.mapper.plot([1000,3700,6000], [1000,1000,-100])