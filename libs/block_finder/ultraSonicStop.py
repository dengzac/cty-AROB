from PiStorms import PiStorms
psm = PiStorms()


MIN_DIST_MM = 300
MAX_DIST_MM = 450


def setSpeed(speed):
	psm.BAM1.setSpeedSync(speed)
	if speed == 0:
		psm.BAM1.brakeSync()


while not psm.isKeyPressed():
	dist = psm.BAS2.distanceUSEV3()
	if MIN_DIST_MM < dist < MAX_DIST_MM:
		setSpeed(0)
	elif dist < MIN_DIST_MM:
		setSpeed(100)
	elif dist > MAX_DIST_MM:
		setSpeed(-100)

	psm.screen.termPrintAt(5, str(psm.BAS2.distanceUSEV3()))

setSpeed(0)