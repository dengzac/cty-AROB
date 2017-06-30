import datetime
import time
class Gyro(object):
	def __init__(self, gyro):
		self.gyro = gyro
		self.error_rate = 0
		self.starttime = None
		self.startangle = 0

	def calibrate(self, calib_time):
		starttime = datetime.datetime.now()
		startval = self.gyro.gyroAngleEV3()

		time.sleep(calib_time)

		self.error_rate = float(self.gyro.gyroAngleEV3() - startval)/float((datetime.datetime.now() - starttime).total_seconds())
		print "error ", self.error_rate
		self.startangle = self.gyro.gyroAngleEV3()
		self.starttime = datetime.datetime.now()

	def get_angle(self):
		return self.gyro.gyroAngleEV3() - self.startangle - (self.error_rate* (datetime.datetime.now() - self.starttime).total_seconds())

