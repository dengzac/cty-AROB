from PIDController import PIDController
from Driver import Driver

from PiStorms import PiStorms
from Gyro import Gyro

psm = PiStorms()

class Follower(object):
    def __init__(self, controller, driver, ultrasonic, color):
        self.controller = controller
        self.driver = driver
        self.ultrasonic = ultrasonic
        self.color = color
    def get_error(self):
        return 200 - self.ultrasonic.distanceUSEV3()

    def follow(self):
        error = self.get_error()
        green_color = self.color.colorSensorEV3()
        #print error
        #print "color ", green_color
        if error < (-155):
            self.driver.turn_right(20)
        elif False: #error > 50:
            self.driver.turn_left(20)
        else:
            output = self.controller.run(self.get_error())
            #print "PID " + str(output)
            self.driver.drive_straight(output)
        self.driver.step()

    def step(self):
        self.follow()

gyro = Gyro(psm.BAS2)
gyro.calibrate(1)
print "Calibrate done error=", gyro.error_rate

controller = PIDController(1, 0, 0.1)
driver = Driver(psm.BAM1, psm.BAM2, gyro, 10)

follower = Follower(controller, driver, psm.BAS1, psm.BBS2)

# try:
while True:

    follower.step()
# except:
#     psm.BAM1.setSpeed(0)
#     psm.BAM2.setSpeed(0)