from time import time

class MotorManager(object): #assumes motors are part of the same bank
    def __init__(self, leftm, rightm, mapper, forwardIsNegative=False):
        if forwardIsNegative:
            self.reverse = -1
        else:
            self.reverse = 1

        self.mapper = mapper
        
        self.right = rightm
        self.left = leftm

        self.leftSpeed = 0
        self.rightSpeed = 0
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

        self.leftSpeed = speed
        self.rightSpeed = speed

    def turnLeft(self, speed, seconds):
        speed = self.parseSpeed(speed)
        self.duration = seconds
        self.lastTime = time()
        
        self.left.setSpeed(-speed)
        self.right.setSpeed(speed)

        self.leftSpeed = -speed
        self.rightSpeed = speed        

    def turnRight(self, speed, seconds):
        speed = self.parseSpeed(speed)
        self.duration = seconds
        self.lastTime = time()
        
        self.left.setSpeed(speed)
        self.right.setSpeed(-speed)

        self.leftSpeed = speed
        self.rightSpeed = -speed
        

    def stopAll(self):
        self.left.setSpeed(0)
        self.right.setSpeed(0)
        self.left.brake()
        self.right.brake()
        self.lastTime = None
        self.duration = 0

        self.leftSpeed = 0
        self.rightSpeed = 0
    def step(self):
        if self.lastTime != None:
            if self.lastTime + self.duration < time():
                self.stopAll()
        self.left.setSpeed(self.leftSpeed)
        self.right.setSpeed(self.rightSpeed)

        self.mapper.step((self.leftSpeed + self.rightSpeed) / 2.0 * self.reverse)
        