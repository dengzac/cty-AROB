from pixy import *
from ctypes import *
from PID import *
from MarcMapper import *
from FloatRangeMotorManager import *
from PiStorms import PiStorms


class Pixy(object):
    def __init__(self):
        print pixy_init()
        self.blocks = BlockArray(100)
        self.frame  = 0
    def getBlocks(self):
        count = pixy_get_blocks(100, self.blocks)
        ret = []
        if count > 0:
            self.frame = self.frame + 1
            for index in range (0, count):
                ret.append(self.blocks[index])
                #print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (self.blocks[index].type, self.blocks[index].signature, self.blocks[index].x, self.blocks[index].y, self.blocks[index].width, self.blocks[index].height)
        return ret
# Pixy Python SWIG get blocks example #


# Initialize Pixy Interpreter thread #


class Blocks (Structure):
        _fields_ = [ ("type", c_uint),
        ("signature", c_uint),
        ("x", c_uint),
        ("y", c_uint),
        ("width", c_uint),
        ("height", c_uint),
        ("angle", c_uint) ]

pixycam = Pixy()
psm = PiStorms()
rPID = PIDController(Kp=1, Ki=0, Kd=0.1, Scalar=-0.02)
dPID = PIDController(Kp=1, Ki=0, Kd=0.15, Scalar=0.01)
r = Mapper(psm.BAM1, psm.BAM2, psm.BBS1, psm, True)
m = DynManager(psm.BAM1, psm.BAM2, 8.7)


# Wait for blocks #
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
            continue
    print largestblock.x,largestblock.y
    x_diff = 160 - largestblock.x
    distance = 20.0/largestblock.height
    print x_diff
    print "distance", distance
    output = rPID.step(x_diff)
    output2 = dPID.step(30 - distance)
    print output
    m.setSpeed((output2))
    m.setTurn(output)
    m.step()
    


