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
from pixy import *
from ctypes import *
from PID import *
from MarcMapper import *
from FloatRangeMotorManager import *
from PiStorms import PiStorms
import time


class Pixy(object):
    def __init__(self):
        print pixy_init()
        self.blocks = BlockArray(100)
        self.frame = 0
    def getBlocks(self):
        count = pixy_get_blocks(100, self.blocks)
        ret = []
        if count > 0:
            self.frame = self.frame + 1
            for index in range(0, count):
                if self.blocks[index].signature != 1:
                    pass#asscontinue
                ret.append(self.blocks[index])
                #print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (self.blocks[index].type, self.blocks[index].signature, self.blocks[index].x, self.blocks[index].y, self.blocks[index].width, self.blocks[index].height)
        return ret



class Blocks(Structure):
    _fields_ = [("type", c_uint),
                ("signature", c_uint),
                ("x", c_uint),
                ("y", c_uint),
                ("width", c_uint),
                ("height", c_uint),
                ("angle", c_uint) ]

class BlockFinder(object):
    def __init__(self,r, m):
        self.pixycam = Pixy()
        self.rPID = PIDController(Kp=0.2, Ki=0.05, Kd=0.5, Scalar=0.0002)
        self.dPID = PIDController(Kp=1, Ki=0.01, Kd=0.15, Scalar=0.08)
        self.r = r#Mapper(psm.BAM1, psm.BAM2, psm.BBS1, psm, True)
        self.m = m#DynManager(psm.BAM1, psm.BAM2, 8.7)

    def getBlocks(self):
        return self.pixycam.getBlocks()

    def step(self):
        self.drive()
    def drive(self):
        ret = self.getBlocks()
        largestsize = 0
        largestblock = None

        for i in ret:
            if i.signature!=1:
                continue
            size = i.width * i.height
            if size > largestsize:
                largestsize = size
                largestblock = i
        if largestblock == None:
            self.m.setSpeed(0)
            self.m.step()
            return
        #print largestblock.x,largestblock.y
        x_diff = 160 - largestblock.x
       # blockheight = (25.4*160)/largestblock.height
        blockheight = largestblock.height
        #print x_diff
        print "blockheight", blockheight
        output = self.rPID.step(x_diff)
        
        if abs(x_diff) < 30:
            print "done turning"

            output2 = self.dPID.step(120 - blockheight)
            if (abs(120-blockheight) < 30):
                print "at target"
                return True
            print "speed", output2
            self.m.setSpeed(output2)
            self.m.setTurn(0)
            self.m.step()
        else:
            self.m.setSpeed(output)
            self.m.setTurn(-1)
            m.step()
        return False
if __name__ == "__main__":
    from PID import PIDController
    from MarcMapper import Mapper 
    from PiStorms import PiStorms
    from FloatRangeMotorManager import DynManager
    from PointNavigator import PointNavigator
    from time import sleep

    sleep(1)

    psm = PiStorms()
    rPID = PIDController(Kp=1, Ki=0, Kd=0.1, Scalar=1.4)
    dPID = PIDController(Kp=1, Ki=0, Kd=0.15, Scalar=0.001)
    r = Mapper(psm.BAM1, psm.BAM2, psm.BBS1, psm, True)
    m = DynManager(psm.BAM1, psm.BAM2, 8.7)
    p = PointNavigator(m, r, rPID, dPID)
    PN = PathNavigator(p,[(700,550),(1500,550),(1500,-170),(700,-170),(-100,300)])
    blockpoints = []
    finder = BlockFinder(r, m)
    timer = time.time()
    while not psm.isKeyPressed():
        blocks = finder.getBlocks()
        print blocks
        if len(blocks)==0 and ((time.time() - timer) > 5):
            print "Follow path"
            PN.step()
            #sleep(0.02)
        else:
            if (len(blocks)>0):
                timer = time.time()
                print "Follow block"
                if finder.step():
                    blockpoints.append(r.getLocation())
                    print blockpoints
            else:
                m.setSpeed(0)
                m.step()
        r.step()
    p.manager.setSpeed(0)
    p.manager.setTurn(0)
    p.manager.step()
    p.mapper.plotWithPoints(PN.points)