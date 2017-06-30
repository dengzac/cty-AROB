from PiStorms import PiStorms
import time
psm = PiStorms()

turnTime = .25
def leftTurn(time1):
	psm.BAM2.runSecs(time1, -100, True)
	psm.BAM1.runSecs(time1, 100, True)

def rightTurn(time1):
	psm.BAM2.runSecs(time1, 100, True)
	psm.BAM1.runSecs(time1, -100, True)

def driveStraight(time1):
	psm.BAM1.runSecs(time1, 100, True)
	psm.BAM2.runSecs(time1, 100, True)

driveStraight(3)
time.sleep(1)
rightTurn(turnTime)
time.sleep(1)
driveStraight(3)
time.sleep(1)
leftTurn(turnTime)