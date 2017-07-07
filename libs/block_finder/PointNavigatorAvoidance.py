from math import atan2, pi, radians, sin, cos
from collections import deque
class PointNavigator(object):
    def __init__(self, manager, mapper, rotatePID, drivePID, ultra, pointThreshold=20, objectThreshold=200):
        self.manager = manager
        self.mapper = mapper
        self.rotatePID = rotatePID
        self.drivePID = drivePID
        self.ultra = ultra
        self.point = (0,0)
        self.avoidPoint = (0,0)
        self.targetPoint = (0,0)
        self.pointThreshold = pointThreshold
        self.objectThreshold = objectThreshold


        # 0 is driving normally, 1 is seeking temp point
        self.movementState = 0
    
    def setPoint(self, point):
        self.targetPoint = point

    def step(self):
        self.mapper.step()
        currentPos = self.mapper.getLocation()
        print "PointNav: at {}, {} going to {}, {}".format(currentPos[0], currentPos[1], self.point[0], self.point[1])
        
        # decide which point to follow
        if self.movementState == 0:
            self.point = self.targetPoint
        else:
            self.point = self.avoidPoint
    
        # pick a new avoidance point and go to it if we are close to obstacle
        if self.movementState == 0 and self.ultra.distanceUSEV3() < self.objectThreshold:
            print("\n\n\nFOUND FOUND FOUND\nFOUND FOUND FOUND\nFOUND FOUND FOUND\n\n\n\n")
            orientation = radians(self.mapper.getHeading()) + (pi/2)
            self.avoidPoint = ((currentPos[0] + 300*cos(orientation),currentPos[1] + 300*sin(orientation)))
            self.movementState = 1

        #check if at point
        if (abs(currentPos[0] - self.point[0]) < self.pointThreshold) and (abs(currentPos[1] - self.point[1]) < self.pointThreshold):
            self.manager.setSpeed(0)
            self.manager.setTurn(0)
            self.manager.step()
            if self.movementState == 0:
                return True
            else:
                self.movementState = 0

        angleToPoint = atan2(self.point[1] - currentPos[1], self.point[0] - currentPos[0])
        angleError = (((angleToPoint - radians(self.mapper.getHeading())) + pi) % (2*pi)) - (pi)
        distanceError = ((currentPos[0] - self.point[0])**2 + (currentPos[1] - self.point[1])**2)**(0.5)
        print "Desired Angle: {}".format(angleToPoint)
        s = self.drivePID.step(distanceError)
        t = self.rotatePID.step(angleError)
        print "Stuff: AE {}, DE {}, S {}, T {}".format(angleError, distanceError, s,t)
        self.manager.setSpeed(s)
        self.manager.setTurn(t)
        self.manager.step()
        return False

if __name__ == "__main__":
    from PID import PIDController
    from MarcMapper import Mapper 
    from PiStorms import PiStorms
    from FloatRangeMotorManager import DynManager
    from time import sleep

    sleep(1)

    psm = PiStorms()
    rPID = PIDController(Kp=1, Ki=0, Kd=0.1, stepSec=0.05, Scalar=1.4)
    dPID = PIDController(Kp=1, Ki=0, Kd=0.15, stepSec=0.05, Scalar=0.001)
    r = Mapper(psm.BAM1, psm.BAM2, psm.BBS1, psm, True)
    m = DynManager(psm.BAM1, psm.BAM2, 8.7)
    p = PointNavigator(m, r, rPID, dPID, psm.BAS2)

    p.setPoint((2000,0))
    while not psm.isKeyPressed():
        print(psm.BAS2.distanceUSEV3())
        p.step()
        sleep(0.02)
    p.manager.setSpeed(0)
    p.manager.setTurn(0)
    p.manager.step()