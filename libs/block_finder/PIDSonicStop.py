import time
from PiStorms import PiStorms
psm = PiStorms()

import sys
from collections import deque

MESSAGE = "P: {}\nI: {}\nD: {}\nKP: {}\nKI: {}\nKD: {}\nSpeed: {}"

STEP_SEC = 0.1
FOLLOW_DIST = 250

OUTOFRANGE = 450

SPINTIME = 1
SPINTIME_ADD = 0.5
SPINSPEED = 25

print("DOING")
if len(sys.argv) >= 4:
	Kp = float(sys.argv[1])
	Kd = float(sys.argv[2])
	Ki = float(sys.argv[3])
	print("PARSED K")
else:
	Kp = 1
	Kd = 0.05
	Ki = 0

if len(sys.argv) >= 5:
	SCALAR = float(sys.argv[4])
	print("PARSED SCALAR")
else:
	SCALAR = 0.5

time.sleep(0.5)

intKeepTime = 1

intToKeep = int(intKeepTime / STEP_SEC)

integral = deque([0 for i in range(intToKeep)])

totalInt = 0

def setSpeed(speed):
	if speed > 100:
		speed = 100
	elif speed < -100:
		speed = -100
	psm.BAM1.setSpeedSync(-speed)
	if speed == 0:
		psm.BAM1.brakeSync()

def getDistanceToGoal():
	return psm.BAS2.distanceUSEV3() - FOLLOW_DIST

def waitForSensor(dist,timeout):
	t = time.time()

	while psm.BAS2.distanceUSEV3() > dist and (not psm.isKeyPressed()):
		if time.time() - t > timeout:
			return False
	return True



curError = getDistanceToGoal()

while not psm.isKeyPressed():
	tm = time.time()


	while psm.BAS2.distanceUSEV3() > OUTOFRANGE and (not psm.isKeyPressed()):
		spinTime = SPINTIME
		#move left
		psm.BAM1.setSpeed(SPINSPEED)
		psm.BAM2.setSpeed(-SPINSPEED)
		if waitForSensor(OUTOFRANGE, spinTime):
			break

		setSpeed(0)
		if waitForSensor(OUTOFRANGE, 0.5):
			break

		# move to the right
		psm.BAM1.setSpeed(-SPINSPEED)
		psm.BAM2.setSpeed(SPINSPEED)
		if waitForSensor(OUTOFRANGE, spinTime * 2):
			break

		setSpeed(0)
		if waitForSensor(OUTOFRANGE, 0.5):
			break

		#move center
		psm.BAM1.setSpeed(SPINSPEED)
		psm.BAM2.setSpeed(-SPINSPEED)
		if waitForSensor(OUTOFRANGE, spinTime):
			break

		spinTime += SPINTIME_ADD

	oldError = curError
	curError = getDistanceToGoal()

	curInt = curError * STEP_SEC
	totalInt += curInt
	totalInt -= integral.popleft()
	integral.append(curInt)
	
	deriv = (curError - oldError) / STEP_SEC

	P = curError * Kp
	I = totalInt * Ki
	D = deriv * Kd

	sp = SCALAR * (P + I + D)
	setSpeed( sp )

	# psm.screen.termPrintAt(1, str(curError))
	# psm.screen.termPrintAt(2, str(P))
	# psm.screen.termPrintAt(3, str(I))
	# psm.screen.termPrintAt(4, str(D))
		
	#print(MESSAGE.format(curError,totalInt,deriv,P,I,D,sp))

	sleept = STEP_SEC - (time.time() - tm)
	if sleept < 0:
		sleept = 0
	time.sleep(sleept)

setSpeed(0)
