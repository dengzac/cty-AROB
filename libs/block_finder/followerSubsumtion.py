from PID import PIDController
from MotorManager import MotorManager
from PiStorms import PiStorms
from time import time, sleep

class Follower(object):
    def __init__(self, motorManager, sensor, pidController, followDistance=300, searchDistance=600, turnSpeed=25):
        self.manager = motorManager

        self.followDistance = followDistance
        self.searchDistance = searchDistance
        self.sensor = sensor

        self.controller = pidController
        

        self.moveState = 0
        # 0 is following, one is scanning

        self.turnState = 0
        self.turnDuration = 1
        self.turnAdd = 0.5
        self.turnSpeed = turnSpeed
        # 0 is moveleft, 1 is moveright, 2 is reset center moving left

    def step(self):
        print("Follower: MoveState: {0}\tturnState: {1}\tturnDuration:{2}".format(self.moveState,
            self.turnState,self.turnDuration))

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
            print("Follow Mode")
            if lastSensorReading > self.searchDistance:
                self.moveState = 1
                self.turnDuration = 1
                self.turnState = 0
                self.manager.stopAll()
                return
            self.manager.driveStraight(self.controller.step(lastSensorReading - self.followDistance), 1)


psm = PiStorms()

MANAGER = MotorManager(psm.BAM1,psm.BAM2, True)
PID = PIDController()
F = Follower(MANAGER, psm.BAS2, PID)

while not psm.isKeyPressed():
    F.step()
    sleep(0.02)
F.manager.stopAll()