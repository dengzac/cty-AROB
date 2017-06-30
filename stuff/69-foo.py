from PiStorms import PiStorms
import time
import thread
import sys
import os


psm = PiStorms()
def check():
	while not psm.BAS1.isTouchedEV3():
		pass
	psm.BAM1.brake()
	psm.BAM2.brake()
	os._exit(1)
#thread.start_new_thread(check, ())
t=2
psm.BAM1.runSecs(t, -100, True)
psm.BAM2.runSecs(t, -100, True)
time.sleep(t)
t=2
psm.BAM1.runSecs(t, -100, True)
psm.BAM2.runSecs(t, 100, True)
time.sleep(t)
t=8
psm.BAM1.runSecs(t, -33, True)
psm.BAM2.runSecs(t, -100, True)
time.sleep(t)
t=3
psm.BAM1.runSecs(t, -70, True)
psm.BAM2.runSecs(t, 100, True)
time.sleep(t)
t=6
psm.BAM1.runSecs(t, -100, True)
psm.BAM2.runSecs(t, -100, True)
time.sleep(t)