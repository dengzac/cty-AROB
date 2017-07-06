from collections import deque
from time import time

class PIDController:
    def __init__(self, Kp=1, Ki=0, Kd=0.05,
                 Scalar=0.5, integralMemSeconds=0):
        #params
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.scale = Scalar

        #instances
        self.lastTime = time()
        self.totalInt = 0
        self.curError = 0
        
    def step(self, error):
        elapsedTime = time() - self.lastTime
        # print("PID: Stepping at {0} seconds".format(self.stepSec))
            
        self.lastTime = time()

        oldError = self.curError
        self.curError = error

        curInt = self.curError * elapsedTime
        self.totalInt += curInt
        
        deriv = (self.curError - oldError) / elapsedTime


        output = (self.scale * (self.curError * self.Kp + 
            self.totalInt * self.Ki + deriv * self.Kd))

        # print("PID: L: {0}, P: {1}, I: {2}, D: {3}".format(output, self.curError, self.totalInt, deriv))

        return output
