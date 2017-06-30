from PiStorms import PiStorms
from PIDController import PIDController
from Gyro import Gyro
import datetime
psm = PiStorms()
controller = PIDController(1, 0, 0)
gyro = Gyro(psm.BAS2)
print "Calibrating"
gyro.calibrate()
print "Calibrate done error=", gyro.error_rate

while True:
	output = controller.run(gyro.get_angle())
	psm.BAM1.setSpeed(-output)
	psm.BAM2.setSpeed(output)
	print output