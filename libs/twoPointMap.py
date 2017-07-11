from PiStorms import PiStorms
from math import tan, radians
from pixy import *
from ctypes import *
from PID import *
from MarcMapper import *
from FloatRangeMotorManager import *
from PiStorms import PiStorms
import time
from math import *
from mindsensors_i2c import mindsensors_i2c
from mindsensors import ABSIMU

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


class TwoPointMapper(object):
	def __init__(self, gyro, pixy):

		self.x1 = 2000
		self.y1 = -1050
		self.sig1 = 10
		self.x2 = 1500
		self.y2 = 1050
		self.x3 = 1000
		self.y3 = -1050
		self.selfsig2 = 19
		self.gyro = gyro
		self.pixy = pixy

		self.startTheta = gyro.get_heading()
		self.searching = False
		self.theta1 = None
		self.theta2 = None
		self.theta3 = None
	def step(self):
		if self.theta1 != None and self.theta2 != None and self.theta3 != None:
			return True
		elif self.searching:
			blocks = pixy.getBlocks()
			for block in blocks:
				if block.signature == 10 and abs(block.x - 160) < 30:
					if abs(abs(block.angle)-180) < 5:
						self.theta1 = -(self.gyro.get_heading() - self.startTheta)
						print "found theta1",self.theta1
						continue
					if abs(block.angle + 90) < 5:
						self.theta2 = -(self.gyro.get_heading() - self.startTheta)
						print "found theta2",self.theta2
						continue
					if abs(block.angle) < 5:
						self.theta3 = -(self.gyro.get_heading() - self.startTheta)
						print "found theta3",self.theta3
						continue
					else:
						print "found block, sig, theta, phi, x", block.signature, self.gyro.get_heading(), block.angle, block.x


			# if self.theta1 == None:
			# 	for block in blocks:
			# 		print "searching theta1", block.signature, self.gyro.get_heading(), block.angle, block.x
			# 		if block.signature == 10 and abs(block.x - 160) < 30 and abs(abs(block.angle)-180) < 20:
			# 			self.theta1 = self.gyro.get_heading() - self.startTheta
			# 			print "found theta1",self.theta1
			# 			flag = True
			# 			break

			# if self.theta2 == None:
			# 	blocks = pixy.getBlocks()
			# 	for block in blocks:
			# 		print "searching theta2", block.signature, self.gyro.get_heading(), block.angle, block.x
			# 		if block.signature == 10 and abs(block.x - 160) < 30 and abs(block.angle + 90) < 20:
			# 			self.theta2 = self.gyro.get_heading() - self.startTheta
			# 			print "found theta2", self.theta2
			# 			flag = True
			# 			break

			# if self.theta3 == None:
				
			# 	for block in blocks:
			# 		print "searching theta2", block.signature, self.gyro.get_heading(), block.angle, block.x
			# 		if block.signature == 10 and abs(block.x - 160) < 30 and abs(block.angle) < 20:
			# 			self.theta3 = self.gyro.get_heading() - self.startTheta
			# 			print "found theta3", self.theta3
			# 			flag = True
			# 			break
psm = PiStorms()
pixy = Pixy()

imu = ABSIMU()
psm.BAS1.activateCustomSensorI2C()
time.sleep(.1)


mapper = TwoPointMapper(imu, pixy)
mapper.searching = True
psm.BAM1.setSpeed(20)
psm.BAM2.setSpeed(-20)
while mapper.theta2 == None or mapper.theta1 == None or mapper.theta3 == None:
	mapper.step()
theta1 = (mapper.theta1)
theta2 = (mapper.theta2)
theta3 = (mapper.theta3)



print theta1, theta2, theta3
m1 = tan(radians(theta1))
m2 = tan(radians(theta2))
m3 = tan(radians(theta3))


# three possible solutions
# x = ((-m1) * mapper.x1 + m2*mapper.x2 + mapper.y1 - mapper.y2)/(-(m1-m2))
# y = m1 * (x - mapper.x1) + mapper.y1

def solveSystem(x1, y1, m1, x2, y2, m2):
	x = ((-m1) * x1 + m2*x2 + y1 - y2)/(-(m1-m2))
	y = m1 * (x - x1) + y1
	return (x, y)


# exclude slopes that are close to eachother
if 0.9 < m1/m2 < 1.1:
	solutions = [solveSystem(mapper.x3, mapper.y3, m3, mapper.x2, mapper.y2, m2),
				 solveSystem(mapper.x1, mapper.y1, m1, mapper.x3, mapper.y3, m3)]
elif 0.9 < m2/m3 < 1.1:
	solutions = [solveSystem(mapper.x1, mapper.y1, m1, mapper.x2, mapper.y2, m2),
				 solveSystem(mapper.x1, mapper.y1, m1, mapper.x3, mapper.y3, m3)]
elif 0.9 < m3/m1 < 1.1:
	solutions = [solveSystem(mapper.x1, mapper.y1, m1, mapper.x2, mapper.y2, m2),
				 solveSystem(mapper.x2, mapper.y2, m2, mapper.x3, mapper.y3, m3)]
else:
	solutions = [solveSystem(mapper.x1, mapper.y1, m1, mapper.x2, mapper.y2, m2), 
	             solveSystem(mapper.x3, mapper.y3, m3, mapper.x2, mapper.y2, m2),
	             solveSystem(mapper.x1, mapper.y1, m1, mapper.x3, mapper.y3, m3)]

x = sum([i for i,j in solutions])/len(solutions)
y = sum([j for i,j in solutions])/len(solutions)
print solutions
print x,y