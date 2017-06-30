import time
from PiStorms import PiStorms
psm = PiStorms()


class PIDController:
	Kp = 1
	Ki = 0
	Kd = 0.01
	prev_error = 0
	total_error = 0
	prev = []
	secs_per_step = 0.1

	def run(error):
		D = float(error-prev_error)/secs_per_step
		prev.append(secs_per_step * error)
		while len(prev) > 30:
			prev.pop(0)
		total_error = sum(prev)
		prev_error = error

		output = Kp * error + Ki * total_error - Kd * D
		if output < -100:
			output = -100
		elif output > 100:
			output = 100

		return output






try: 
	controller = PIDController()
except:
	psm.BAM1.setSpeed(0)
	psm.BAM2.setSpeed(0)

