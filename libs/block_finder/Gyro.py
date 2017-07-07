from time import time
from math import cos, sin, pi

class Mapper(object):
    def __init__(self, gyro, motor):
        self.gyro = gyr
o
        self.history = []
        self.currentPosition = (0,0,0)

        self.lastTime = time()

        self.firstGryo = self.gyro.gyroAngleEV3()
        self.counter = 0

    def getGyro(self):
        return self.gyro.gyroAngleEV3() - self.firstGryo
        

    def step(self, velocity):
        timeDiff = self.lastTime - time()
        self.lastTime = time()

        headingRadians = self.getGyro() * pi / 180.0

        self.currentPosition = (self.currentPosition[0] + cos(headingRadians),
                                self.currentPosition[1] + sin(headingRadians),
                                headingRadians)

        print(self.currentPosition)
        
        self.counter += 1
        if self.counter % 15 == 0:
            self.history.append(self.currentPosition)
