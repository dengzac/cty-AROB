from PiStorms import PiStorms
from math import cos
psm = PiStorms()

from time import sleep

WHEEL_CIRC = 7.25
WHEEL_BASE = 7.5
PI = 3.14159265358979323856264
ENTRY_THETA = 24
EXTRA_DIST = 24


# def runDegs2(motor1, motor2, degrees, speed):
# 	pos1 = motor1.pos()
# 	pos2 = motor2.pos()

# 	motor1.setSpeed(speed)
# 	motor2.setSpeed(speed)

# 	while True:
# 		doBreak = False
# 		if motor1.pos() - pos1 < degrees:
# 			motor1.setSpeed(0)
# 			doBreak = True
# 		if motor1.pos() - pos1 < degrees:
# 			motor1.setSpeed(0)

# 			if doBreak:
# 				break
# 	print("ended")	



def rotate(degrees): #clockwise, blocking
	amt = ((degrees * PI / 180) * WHEEL_BASE / 2) * (180/PI)
	print(amt)
	amt = int(amt)

	psm.BAM2.runDegs(-amt, 100, True, False)
	psm.BAM1.runDegs(amt, 100, True, False)

	psm.BAM1.waitUntilNotBusy()
	psm.BAM2.waitUntilNotBusy()

	return

def moveForward(inches): #blocking
	amt = inches/WHEEL_CIRC * 360
	print(amt)
	amt = -int(amt)
	# runDegs2(psm.BAM1, psm.BAM2, amt, 50)
	psm.BAM1.runDegs(amt, 50, True, False)
	psm.BAM2.runDegs(amt, 50, True, False)

	psm.BAM1.waitUntilNotBusy()
	psm.BAM2.waitUntilNotBusy()
	return

# # Actual Program:
# psm.BAM1.setSpeed(100)
# sleep(1)
# psm.BAM1.setSpeed(0)

# sleep(10)

rotate(ENTRY_THETA)
moveForward(60/cos(ENTRY_THETA * (PI/180)) + 5)
rotate((-2 * ENTRY_THETA) + 5)
moveForward(((60)/cos(ENTRY_THETA  * (PI/180))) + EXTRA_DIST)
