from time import time
from math import cos, sin, pi


import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import tempfile

image = tempfile.NamedTemporaryFile()

class Reckoner(object):
    def __init__(self, gyro, leftm, rightm):
        self.gyro = gyro
        self.left = leftm
        self.right = rightm
        self.left.resetPos()
        self.right.resetPos()
        

        self.firstGryo = self.gyro.gyroAngleEV3()
        self.lastLeft = self.left.pos()
        self.lastRight = self.right.pos()
        
        self.lastTheta = self.getGyro()

        self.historyX = []
        self.historyY = []
        self.historyT = []
        self.currentPosition = (0,0,self.lastTheta)
        self.lastTime = time()

        self.counter = 0

    def getPosition(self):
        return self.currentPosition

    def getGyro(self):
        # avoid zeroing the gyro with subtraction
        return (self.gyro.gyroAngleEV3() - self.firstGryo) * pi / 180.0

    def degsToMM(self, deg):
        return (deg * 56.0 * pi / 360.0) # 56 is mm diameter wheel tire
        
    def step(self):
        global data

        # approximate arc
        leftPos = self.left.pos()
        rightPos = self.right.pos()
       
        # if leftPos - self.lastLeft > 100000 or rightPos - self.lastRight > 100000:
        #     return

        deltaD = (self.degsToMM(leftPos - self.lastLeft) + self.degsToMM(rightPos - self.lastRight)) / 2.0
        
        self.lastLeft = leftPos
        self.lastRight = rightPos

        # current theta and theta delta
        theta = self.getGyro()
        deltaTheta = theta - self.lastTheta
        self.lastTheta = theta


        # diff in coords
        self.currentPosition = (
            self.currentPosition[0] - (deltaD * cos(self.currentPosition[2] + deltaTheta/2.0)),
            self.currentPosition[1] + (deltaD * sin(self.currentPosition[2] + deltaTheta/2.0)),
            theta
            )
        print(self.currentPosition)

        #print every 15 steps
        self.counter += 1
        if self.counter % 50 == 0:
            self.historyX.append(self.currentPosition[0] * 3.1)
            self.historyY.append(self.currentPosition[1] * 3.1)
            self.historyT.append(self.currentPosition[2])
              
    def plot(self):
        plt.plot(self.historyX, self.historyY, color="blue")
        plt.tight_layout()
        plt.savefig(image.name, format="png")
        plt.savefig("/home/pi/Pictures/robot_position.png")
            