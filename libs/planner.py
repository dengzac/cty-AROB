import math
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

class PathPlanner(object):
    def __init__(self, path):
        self.origPath = list(path)
        self.pathA= 0.7
        self.pathB=0.3
        self.pathTolerance = 0.0000001

        self.velocityA = 0.1
        self.velocityB = 0.3
        self.velocityTolerance = 0.0000001
        self.heading = []

    def inject(self, orig, numToInject):
        morePoints = []
        for i in range(len(orig) + ((numToInject) * (len(orig)-1))):
            morePoints.append([0, 0])

        index = 0
        for i in range(len(orig)-1):
            morePoints[index][0] = orig[i][0]
            morePoints[index][1] = orig[i][1]
            index+=1

            for j in range(1, numToInject+1):
                morePoints[index][0] = j*((float(orig[i+1][0] - orig[i][0])/float(numToInject+1))) + orig[i][0]
                morePoints[index][1] = j*((float(orig[i+1][1] - orig[i][1])/float(numToInject+1))) + orig[i][1]
                index += 1
        morePoints[index][0] = orig[len(orig)-1][0]
        morePoints[index][1] = orig[len(orig)-1][1]
        
        print "injection done"
        #print morePoints

        return list(morePoints)

    def smoother(self, path, weight_data, weight_smooth, tolerance):


        newPath =list(path)
        #print newPath
        #print path
        change = tolerance
        iter = 0
        while change >= tolerance:
            iter += 1
            #print change
            change = 0.0
            for i in range(1, len(path)-1):
                for j in range(len(path[i])):
                    val = float(newPath[i][j])
                    newPath[i][j] += weight_data * (path[i][j] - newPath[i][j]) + weight_smooth * (newPath[i-1][j] + newPath[i+1][j] - (2.0 * newPath[i][j]))
                    #print i, j, newPath[i][j], val
                    #print "dx", abs(val - newPath[i][j]) 
                    change += abs(val - newPath[i][j])
            if (iter > 0):
                break
        #print "smooth done", iter
        #print newPath
        return list(newPath)

    def onlyNodeWayPoints(self, path):
        li = []
        li.append(path[0])
        for i in range(1, len(path)-1):
            v1 = math.atan2((path[i][1]-path[i-1][1]), path[i][0]-path[i-1][0])
            v2 = math.atan2((path[i+1][1]-path[i][1]), path[i+1][0] - path[i][0])
            if abs(v2 - v1) >= 0.01:
                li.append(path[i])
        li.append(path[len(path)-1])
        return list(li)

    def velocity(self, smoothPath, timeStep):
        dx = []
        dy = []
        velocities = []

        for i in range(len(smoothPath)):
            dx.append(0)
            dy.append(0)
            velocities.append([0, 0])
            self.heading.append([0, 0])

        for i in range(1, len(smoothPath)):
            dx[i] = (smoothPath[i][0] - smoothPath[i-1][0])/float(timeStep)
            dy[i] = (smoothPath[i][1] - smoothPath[i-1][1])/float(timeStep)
            velocities[i][0] = velocities[i-1][0] + timeStep
            self.heading[i][0] = self.heading[i-1][0] + timeStep
            velocities[i][1] = math.sqrt(dx[i]**2 + math.sqrt(dy[i]**2))
        return velocities

    def velocityFix(self, smoothVelocity, origVelocity, tolerance):
        difference = self.errorSum(origVelocity, smoothVelocity)
        fixVelocity = list(smoothVelocity)

        increase = 0
        while (abs(difference[len(difference)-1]) > tolerance):
            increase = float(difference[len(difference)-1])/1.0/50.0;
            for i in range(1, len(fixVelocity)-1):
                fixVelocity[i][1] = fixVelocity[i][1] - increase
            difference = self.errorSum(origVelocity, fixVelocity)

        return fixVelocity

    def errorSum(self, origVelocity, smoothVelocity):
        tempOrigDist = range(len(origVelocity))
        tempSmoothDist = range(len(smoothVelocity))
        difference = range(len(smoothVelocity))

        timeStep =origVelocity[1][0] - origVelocity[0][0]
        tempOrigDist[0] = origVelocity[0][1]
        tempSmoothDist[0] = smoothVelocity[0][1]

        for i in range(1, len(origVelocity)):
            tempOrigDist[i] = origVelocity[i][1]*timeStep + tempOrigDist[i-1]
            tempSmoothDist[i] = smoothVelocity[i][1]*timeStep + tempSmoothDist[i-1]
            difference[i] = tempSmoothDist[i] - tempOrigDist[i]

        return list(difference)

    def injectionCounter(self, numNodeOnlyPoints, maxTime, timeStep):
        first = 0
        second = 0
        third = 0
        oldPointsTotal = 0
        self.numFinalPoints = 0
        ret = []
        totalPoints = (float(maxTime) / float(timeStep))

        if (totalPoints < 100):
            pointsFirst = 0
            pointsTotal = 0
            for i in range(4, 7):
                for j in range(1, 9):
                    pointsFirst = i*(numNodeOnlyPoints-1) + numNodeOnlyPoints
                    pointsTotal = (j*(pointsFirst-1) + pointsFirst)
                    if (pointsTotal <= totalPoints and pointsTotal > oldPointsTotal):
                        first = i
                        second = j
                        numFinalPoints = pointsTotal
                        oldPointsTotal = pointsTotal
            return (first, second, third)
        else:
            pointsFirst = 0
            pointsSecond = 0
            pointsTotal = 0
            for i in range(1, 6):
                for j in range(1, 9):
                    for k in range(1, 9):
                        pointsFirst = i*(numNodeOnlyPoints-1) + numNodeOnlyPoints
                        pointsSecond = (j*(pointsFirst-1) + pointsFirst)
                        pointsTotal = (k*(pointsSecond-1) + pointsSecond)
                        if (pointsTotal<=totalPoints):
                            first = i
                            second = j
                            third = k
                            numFinalPoints = pointsTotal
            return (first, second, third)

    def wheelSpeeds(self, smoothPath, trackWidth):
        leftPath = []
        rightPath = []

        gradient = []

        for i in range(len(smoothPath)):
            leftPath.append([0, 0])
            rightPath.append([0,0])
            gradient.append([0, 0])

        for i in range(len(smoothPath)-1):
            gradient[i][1] = math.atan2(smoothPath[i+1][1] - smoothPath[i][1], smoothPath[i+1][0] - smoothPath[i][0])

        gradient[len(gradient)-1][1] = gradient[len(gradient) - 2][1]

        for i in range(len(gradient)):
            print gradient[i][1] * 180.0/math.pi
            leftPath[i][0] = (trackWidth/2.0 * math.cos(gradient[i][1] + math.pi/2.0)) + smoothPath[i][0]
            leftPath[i][1] = (trackWidth/2.0 * math.sin(gradient[i][1] + math.pi/2.0)) + smoothPath[i][1]

            rightPath[i][0] = (trackWidth/2.0 * math.cos(gradient[i][1]  - math.pi/2.0)) + smoothPath[i][0] 
            rightPath[i][1] = (trackWidth/2.0 * math.sin(gradient[i][1]  - math.pi/2.0)) + smoothPath[i][1]
            print leftPath[i], rightPath[i]
            deg = ((gradient[i][1] * 180.0/math.pi+180)% 360) - 180
            gradient[i][1] = deg

        self.heading = gradient
        self.leftPath = leftPath
        self.rightPath =rightPath

def plot2d(arr):
    x = []
    y = []
    for i in arr:
        try:
            x.append(i[0])
            y.append(i[1])
        except:
            pass
    return (x, y)
total_time = 8
time_step = 0.1
p = PathPlanner([[1,1], [5,1], [9, 12], [12, 9], [15, 6], [19, 12], [0,0]])
nodeOnlyPath = p.onlyNodeWayPoints(p.origPath)
print nodeOnlyPath
inject = p.injectionCounter(len(nodeOnlyPath), total_time, time_step)
print
#print inject
for i in range(len(inject)):
    if i==0:
        smoothPath = p.inject(nodeOnlyPath, inject[0])
        print "inject" 
        print smoothPath
        smoothPath = p.smoother(smoothPath, 0.7, 0.3, p.pathTolerance)
        print "smooth"
        print smoothPath
    else:
        smoothPath = p.inject(smoothPath, inject[i])
        smoothPath = p.smoother(smoothPath, 0.1, 0.3, 0.0000001)


print smoothPath

p.wheelSpeeds(smoothPath, 6)

leftVelocity = p.velocity(p.leftPath, time_step)
leftVelocity[len(leftVelocity)-1][1] = 0
#leftVelocity = p.smoother(leftVelocity,0.1, 0.3, 0.0000001 )
print leftVelocity
x = []
y = []
for i in leftVelocity:
    x.append(i[0])
    y.append(i[1])
plt.plot(x, y)

x = []
y = []
for i in smoothPath:
    x.append(i[0])
    y.append(i[1])
plt.plot(x, y, color="green")

x = []
y = []
for i in p.leftPath:
    x.append(i[0])
    y.append(i[1])
plt.plot(x, y, color="blue")

x = []
y = []
for i in p.rightPath:
    x.append(i[0])
    y.append(i[1])
plt.plot(x, y, color="red")
x = []
y = []
for i in [[1,1], [5,1], [9, 12], [12, 9], [15, 6], [19, 12],[0,0]]:
    x.append(i[0])
    y.append(i[1])
#plt.plot(x, y, color="red")
plt.tight_layout()
print "save"
plt.savefig("/home/zachary/path.png")
