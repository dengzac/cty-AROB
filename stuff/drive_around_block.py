from PIDController import PIDController

from PiStorms import PiStorms
import time
from Gyro import Gyro
from Driver import Driver

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
        error = s