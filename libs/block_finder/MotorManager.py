from time import time

class MotorManager(object): #assumes motors are part of the same bank
    def __init__(self, leftm, rightm, forwardIsNegative=False):
        if forwardIsNegative:
            self.reverse = -1
        else:
            self.reverse = 1
        
        self.right = rightm
        self.left = leftm

        self.lastTime = None
        self.duration = 0

    def isBusy(self):
        return self.lastTime != None

    def parseSpeed(self, speed):
        speed = speed * self.reverse
        if speed < -100:
            return -100
        if speed > 100:
            return 100
        return speed

    def driveStraight(self, speed, seconds):
        speed = self.parseSpeed(speed)
        self.duration = seconds
        self.lastTime = time()
        
        self.left.setSpeed(speed)
        self.right.setSpeed(speed)

    def turnLeft(self, speed, seconds):
        speed = self.parseSpeed(speed)
        self.duration = seconds
        self.lastTime = time()
        
        self.left.setSpeed(-speed)
        self.right.setSpeed(speed)        

    def turnRight(self, speed, seconds):
        speed = self.parseSpeed(speed)
        self.duration = seconds
        self.lastTime = time()
        
        self.left.setSpeed(speed)
        self.right.setSpeed(-speed)        

    def stopAll(self):
        self.left.setSpeed(0)
        self.right.setSpeed(0)
        self.left.brake()
        self.right.brake()
        self.lastTime = None
        self.duration = 0

    def step(self):
        if self.lastTime != None:
            if self.lastTime + self.duration < time():
                self.stopAll()