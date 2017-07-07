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
                ret.append(self.blocks[index])
                #print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (self.blocks[index].type, self.blocks[index].signature, self.blocks[index].x, self.blocks[index].y, self.blocks[index].width, self.blocks[index].height)
        return ret
# Pixy Python SWIG get blocks example #


# Initialize Pixy Interpreter thread #


class Blocks(Structure):
    _fields_ = [("type", c_uint),
                ("signature", c_uint),
                ("x", c_uint),
                ("y", c_uint),
                ("width", c_uint),
                ("height", c_uint),
                ("angle", c_uint) ]

pixycam = Pixy()
psm = PiStorms()
rPID = PIDController(Kp=0.2, Ki=0.05, Kd=0.5, Scalar=0.0002)
dPID = PIDController(Kp=1, Ki=0.01, Kd=0.15, Scalar=0.08)
r = Mapper(psm.BAM1, psm.BAM2, psm.BBS1, psm, True)
m = DynManager(psm.BAM1, psm.BAM2, 8.7)


# Wait for blocks #
try:
    while 1:
        ret = pixycam.getBlocks()
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
            m.setSpeed(0)
            m.step()
            continue
        #print largestblock.x,largestblock.y
        x_diff = 160 - largestblock.x
       # distance = (25.4*160)/largestblock.height
        distance = largestblock.height
        #print x_diff
        print "distance", distance
        output = rPID.step(x_diff)
        
        if abs(output)<100 and abs(x_diff) < 30:
            print "done turning"

            output2 = dPID.step(120 - distance)
            print "speed", output2
            m.setSpeed(output2)
            m.setTurn(0)
            m.step()
        else:
            m.setSpeed(output)
            m.setTurn(-1)
            m.step()


        # output2 = dPID.step(120 - distance)
        # print output, output2
        # time.sleep(0.05)
except:
    m.setSpeed(0)
    m.step()


