import math
import numpy as np
from PiStorms import PiStorms
from PID import PIDController
import time
psm = PiStorms()
#psm.BAM1.setSpeed(-100)
#psm.BAM2.setSpeed(-100)
#psm.BBM1.setSpeed(-100)
startpos = [psm.BAM1.pos(), psm.BAM2.pos(), psm.BBM1.pos()]
controllers = [PIDController(Scalar=1), PIDController(Scalar=1), PIDController(Scalar=1)]
try:
    while True:
        curpos = [psm.BAM1.pos() - startpos[0], psm.BAM2.pos() - startpos[1], psm.BBM1.pos() - startpos[2]]
        output = [controllers[0].step(0  - curpos[0]),controllers[1].step(0  - curpos[1]),controllers[2].step(0  - curpos[2])]
        for i in range(3):
            if abs(output[i]) > 100:
                output[i] = 100 * np.sign(output[i])
        print output
        #print "pos",psm.BAM1.pos(), psm.BAM2.pos(), psm.BBM1.pos()
        psm.BAM1.setSpeed(output[0])
        psm.BAM2.setSpeed(output[1])
        psm.BBM1.setSpeed(output[2])
        
        time.sleep(0.05)
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
print forwardKinematicsMatrix([[45, 2],[0, 1], [10, 7]], np.array([[0],[0]]))#degrees, length

print forwardKinematics([[45, 2],[0, 1], [10, 7]])