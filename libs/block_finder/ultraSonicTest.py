from PiStorms import PiStorms
psm = PiStorms()
import time

while not psm.isKeyPressed():
	psm.screen.termPrintAt(5, str(psm.BAS2.distanceUSEV3() / 10.0))
