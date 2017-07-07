from math import atan2, pi, radians

class PointNavigator(object):
    def __init__(self, manager, mapper, rotatePID, drivePID, pointThreshold=20):
        self.manager = manager
        self.mapper = mapper
        self.rotatePID = rotatePID
        self.drivePID = drivePID
        self.point = (0,0)
        self.pointThreshold = pointThreshold
    
    def setPoint(self, point):
        self.point = point

    def step(self):
        self.mapper.step()
        currentPos = self.mapper.getLocation()
        #print "PointNav: at {}, {} going to {}, {}".format(currentPos[0], currentPos[1], self.point[0], self.point[1])
        

        if (abs(currentPos[0] - self.point[0]) < self.pointThreshold) and (abs(currentPos[1] - self.point[1]) < self.pointThreshold):
            self.manager.setSpeed(0)
            self.manager.setTurn(0)
            self.manager.step()
            return True

        angleToPoint = atan2(self.point[1] - currentPos[1], self.point[0] - currentPos[0])
        angleError = (((angleToPoint - radians(self.mapper.getHeading())) + pi) % (2*pi)) - (pi)
        distanceError = ((currentPos[0] - self.point[0])**2 + (currentPos[1] - self.point[1])**2)**(0.5)
        #print "Desired Angle: {}".format(angleToPoint)
        s = self.drivePID.step(distanceError)
        t = self.rotatePID.step(angleError)
        #print "Stuff: AE {}, DE {}, S {}, T {}".format(angleError, distanceError, s,t)
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
    rPID = PIDController(Kp=1, Ki=0, Kd=0.1, stepSec=0.05, Scalar=1.2)
    dPID = PIDController(Kp=1, Ki=0, Kd=0.15, stepSec=0.05, Scalar=0.001)
    r = Mapper(psm.BAM1, psm.BAM2, psm.BBS1, psm, True)
    m = DynManager(psm.BAM1, psm.BAM2, 8.7)
    p = PointNavigator(m, r, rPID, dPID)

    p.setPoint((1000,1000))
    while not psm.isKeyPressed():
        p.step()
        sleep(0.02)
    p.manager.setSpeed(0)
    p.manager.setTurn(0)
    p.manager.step()