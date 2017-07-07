import time
from PiStorms import PiStorms
psm = PiStorms()

import PID

def setSpeed(speed):
	if speed > 100:
		speed = 100
	elif speed < -100:
		speed = -100
	psm.BAM1.setSpeedSync(-speed)
	if speed == 0:
		psm.BAM1.brakeSync()

def getDistanceToGoal():
	return psm.BAS2.distanceUSEV3() - 400

controller = PID.PIDController(1,0,0.05, getDistanceToGoal, 0.1, 0.5)

while not psm.isKeyPressed():
	tm = time.time()

	setSpeed(controller.tick())

	sleept = 0.1 - (time.time() - tm)
	if sleept < 0:
		sleept = 0
	time.sleep(sleept)

setSpeed(0)
