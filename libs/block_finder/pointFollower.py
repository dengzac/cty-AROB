from PID import PIDController
from MotorManager import MotorManager
from PiStorms import PiStorms
from time import time, sleep
from Reckoning import Reckoner

class Follower(object):
    def __init__(self, motorManager, sensor, pidController, reckoner, followDistance=200, searchDistance=500, turnSpeed=25):
        self.manager = motorManager

        self.followDistance = followDistance
        self.searchDistance = searchDistance
        self.sensor = sensor
        self.reckoner = reckoner

        self.controller = pidController
        

        self.moveState = 0
        # 0 is following, one is scanning

        self.turnState = 0
        self.turnDuration = 1
        self.turnAdd = 0.5
        self.turnSpeed = turnSpeed
        # 0 is moveleft, 1 is moveright, 2 is reset center moving left

    def step(self):

        # print("Follower: MoveState: {0}\tturnState: {1}\tturnDuration:{2}".format(self.moveState,
        #     self.turnState,self.turnDuration))

        self.reckoner.step()

        lastSensorReading = self.sensor.distanceUSEV3()

        # if lastSensorReading < 50:
        #     self.manager.stopAll()
        #     return

        self.manager.step()
        if self.moveState == 1:
            if self.sensor.distanceUSEV3() < self.followDistance:
                self.moveState = 0
                self.manager.stopAll()
                return
            if not self.manager.isBusy():
                if self.turnState == 0:
                    self.manager.turnLeft(self.turnSpeed, self.turnDuration)
                elif self.turnState == 1:
                    self.manager.turnRight(self.turnSpeed, self.turnDuration * 2)
                else:
                    self.manager.turnLeft(self.turnSpeed, self.turnDuration)
                    self.turnDuration += self.turnAdd
                self.turnState = (self.turnState + 1) % 3
        else:
            if lastSensorReading > self.searchDistance:
                self.moveState = 1
                self.turnDuration = 1
                self.turnState = 0
                self.manager.stopAll()
                return
            self.manager.driveStraight(self.controller.step(lastSensorReading - self.followDistance), 1)


PSM = PiStorms()
RECKONER = Reckoner(PSM.BBS1, PSM.BAM1, PSM.BAM2)
MANAGER = MotorManager(PSM.BAM1, PSM.BAM2, True)
PID = PIDController()
F = Follower(MANAGER, PSM.BAS2, PID, RECKONER)

while not PSM.isKeyPressed():
    F.step()
    sleep(0.02)
F.manager.stopAll()
F.reckoner.plot()
