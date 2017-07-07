from PID import PIDController
from MotorManager import MotorManager
from PiStorms import PiStorms
from time import time, sleep
from Reckoning import Reckoner
from math import atan

class Traverser(object):
    def __init__(self, motorManager, rotatePID, drivePID, reckoner, points, pointThreshold=40):
        self.manager = motorManager

        self.reckoner = reckoner

        self.rotate = rotatePID
        self.drive = drivePID
        self.threshold = pointThreshold
        self.points = points

        self.pointsIndex = 0
        
    def step(self):
        if self.pointsIndex >= len(self.points):
            return
        goalPoint = self.points[self.pointsIndex]
        realPoint = self.reckoner.getPosition()

        distanceError = ((goalPoint[0] - realPoint[0])**2 + (goalPoint[1] - realPoint[1])**2)**(0.5)
        if distanceError < self.threshold:
            self.pointsIndex += 1
            return

        rotationError = atan((goalPoint[1]-realPoint[1]) / (goalPoint[0] - realPoint[0])) - realPoint[2]


        # PID speed on distance, PID turn on rotation

        # move towards the point

        self.reckoner.step()
        self.manager.step()

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
