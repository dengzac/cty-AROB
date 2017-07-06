class PathNavigator(object):
    def __init__(self, PointFollower, points=[(0,0)]):
        self.pointFollower = PointFollower
        self.points = points

        self.pointsIndex = 0

    def appendPoint(self,point):
        self.points.append(point)
        
    def step(self):
        print(self.pointsIndex)
        if self.pointsIndex >= len(self.points):
            return
        self.pointFollower.setPoint(self.points[self.pointsIndex])
        if self.pointFollower.step():
            self.pointsIndex += 1

if __name__ == "__main__":
    from PID import PIDController
    from MarcMapper import Mapper 
    from PiStorms import PiStorms
    from FloatRangeMotorManager import DynManager
    from PointNavigator import PointNavigator
    from time import sleep

    sleep(1)

    psm = PiStorms()
    rPID = PIDController(Kp=1, Ki=0, Kd=0.1, stepSec=0.05, Scalar=1.4)
    dPID = PIDController(Kp=1, Ki=0, Kd=0.15, stepSec=0.05, Scalar=0.001)
    r = Mapper(psm.BAM1, psm.BAM2, psm.BBS1, psm, True)
    m = DynManager(psm.BAM1, psm.BAM2, 8.7)
    p = PointNavigator(m, r, rPID, dPID)
    PN = PathNavigator(p,[(700,750),(1900,700),(1900,-250),(700,-250),(-100,200)])
    while not psm.isKeyPressed():
        PN.step()
        sleep(0.02)
    p.manager.setSpeed(0)
    p.manager.setTurn(0)
    p.manager.step()
    p.mapper.plotWithPoints(PN.points)