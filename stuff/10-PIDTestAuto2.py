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
    def __init__(self, points , driver, gyro, controller1, controller2, ultrasonic):
        self.points = points
        self.driver = driver
        self.gyro = gyro
        self.controller1 = controller1
        self.controller2 = controller2
        self.current_index = 0
        self.follower = None
        self.done = False
        self.ultrasonic = ultrasonic

    def step (self):
        try:
            if self.follower == None or self.follower.driveDone:
                if (self.follower == None):
                    pass
                else:
                    #self.driver.mapper.x = self.points[self.current_index-1][0]
                    #self.driver.mapper.y = self.points[self.current_index-1][1] 
                    pass
                self.follower = Point(self.points[self.current_index][0], self.points[self.current_index][1], self.driver, self.gyro, self.controller1, self.controller2, self.driver.mapper, self.ultrasonic)
                self.current_index += 1
            else:
                self.follower.step()
        except:
            psm.BAM1.setSpeed(0)
            psm.BAM2.setSpeed(0)
            self.done = True

gyro = Gyro(psm.BAS2)
psm.BBM1.setSpeed(100)
gyro.calibrate(1)
print "Calibrate done error=", gyro.error_rate
controller = PIDController(1, 0, 0.1)
controller2 = PIDController(0.5, 0, 0.1)
driver = Driver(psm.BAM1, psm.BAM2, gyro, 3)
POINTS = [[1000, 1000], [3000,1000], [3000, -750],[1000, -750], [1000, 1100], [3000, 1120],[5000,0]]
POINTSX = []
POINTSY = []
for i in POINTS:
    POINTSX.append(i[0])
    POINTSY.append(i[1])
follower = PathFollower(POINTS,driver, gyro, controller, controller2 , psm.BAS1)
#try:
while not follower.done:
    follower.step()
#except:
#   psm.BAM1.setSpeed(0)
#   psm.BAM2.setSpeed(0)


psm.BAM1.setSpeed(0)
psm.BAM2.setSpeed(0)
driver.mapper.plot(POINTSX, POINTSY)