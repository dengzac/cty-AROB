import math
import numpy as np
#from PiStorms import PiStorms
from PID import PIDController
import time
#psm = PiStorms()
#psm.BAM1.setSpeed(-100)
#psm.BAM2.setSpeed(-100)
#psm.BBM1.setSpeed(-100)
class Arm(object):
    def __init__(self):
        self.startpos = [psm.BAM1.pos(), psm.BAM2.pos(), psm.BBM1.pos()]
        self.controllers = [PIDController(Scalar=1), PIDController(Scalar=1), PIDController(Scalar=1)]

        self.setpoints = [0,0,0]

    def setSetPoints(self, angles):
        self.setpoints = list(angles)
    def step(self):
        curpos = [psm.BAM1.pos() - self.startpos[0], psm.BAM2.pos() - self.startpos[1], psm.BBM1.pos() - self.startpos[2]]
        output = [self.controllers[0].step(self.setpoints[0]  - curpos[0]),self.controllers[1].step(self.setpoints[1]  - curpos[1]),self.controllers[2].step(self.setpoints[2]  - curpos[2])]
        for i in range(3):
            if abs(output[i]) > 100:
                output[i] = 100 * np.sign(output[i])
        print output
        #print "pos",psm.BAM1.pos(), psm.BAM2.pos(), psm.BBM1.pos()
        if abs(output[0]) > 10:
            psm.BAM1.setSpeed(output[0])
        else:
            psm.BAM1.brake()

        if abs(output[1]) > 10:
            psm.BAM2.setSpeed(output[1])
        else:
            psm.BAM2.brake()

        if abs(output[2]) > 10:
            psm.BBM1.setSpeed(output[2])
        else:
            psm.BBM1.brake()
try:
    arm = Arm()    
except:
    pass
try:
    pass
    # while True:
    #     arm.step()
    #     time.sleep(0.5)
except:
    psm.BAM1.setSpeed(0)
    psm.BAM2.setSpeed(0)
    psm.BBM1.setSpeed(0)
    psm.BAM1.brake(0)
    psm.BAM2.brake(0)
    psm.BBM1.brake(0)
def forwardKinematics(segments):
    x = 0
    y = 0
    theta = 0
    for segment in segments:
        theta += math.radians(segment[0])
        x += math.cos(theta) * segment[1]
        y += math.sin(theta) * segment[1]

    return (x, y)

def forwardKinematicsMatrix(segments,point):
    if len(segments) == 0:
        print "Point: ", point
        return
    print "shape", point.shape
    point = [point[0][0], point[1][0]]
    print "segments", segments, "point", point
    newpoint = np.array([[segments[-1][1] + point[0]], [point[1]]])
    print "t", newpoint
    rad = float(math.radians(segments[-1][0]))
    rotation = np.array([[math.cos(rad), -math.sin(rad)], [math.sin(rad), math.cos(rad)]])
    print "rotation matrix", rotation
    rotated = np.dot(rotation, newpoint)
    print "new point", rotated
    forwardKinematicsMatrix(segments[:-1], rotated)

def lawCosines(dist, l1, l2): # Gets angle opposite to segment of length dist
    return math.degrees(math.acos(float(l1**2 + l2**2 - dist**2) / float(2*l1*l2)))
def inverseKinematics(l1, l2, x, y):
    thetaEnd = math.degrees(math.atan2(y, x))
    distEnd = math.sqrt(x**2 + y **2)
    theta1 = lawCosines(l2, distEnd, l1)
    theta2 = lawCosines(distEnd, l2, l1)
    return (theta1 + thetaEnd,-theta2)

print inverseKinematics(10, 10, 10, 10)
print forwardKinematicsMatrix([[45, 2],[0, 1], [10, 7]], np.array([[0],[0]]))#degrees, length

print forwardKinematics([[45, 2],[0, 1], [10, 7]])