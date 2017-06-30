from PiStorms import PiStorms
from PIDController import PIDController
from Gyro import Gyro
import datetime
psm = PiStorms()
controller = PIDController(2, 0, 0.1)
gyro = Gyro(psm.BAS2)
print "Calibrating"
gyro.calibrate(2)
print "Calibrate done error=", gyro.error_rate

try:
	while True:
		output = controller.run(gyro.get_angle() -100)
		psm.BAM1.setSpeed(-output)
		psm.BAM2.setSpeed(output)
		print output
		print "angle", psm.BAS2.gyroAngleEV3(), gyro.get_angle()
except:
	psm.BAM1.setSpeed(0)
	psm.BAM2.setSpeed(0)