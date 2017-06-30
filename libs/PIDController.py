import datetime
import time
class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.total_error = 0
        self.prev = []
        self.prev_time = datetime.datetime.now()

    def run(self, error):
        self.secs_per_step = float(-(self.prev_time - datetime.datetime.now()).total_seconds())
        D = float(error-self.prev_error)/self.secs_per_step
        self.prev.append(self.secs_per_step * error)
        while len(self.prev) > 30:
            self.prev.pop(0)
        total_error = sum(self.prev)
        self.prev_error = error

        output = self.Kp * error + self.Ki * total_error - self.Kd * D
        if output < -100:
            output = -100
        elif output > 100:
            output = 100

        return 

    @staticmethod
    def calc_angle_error(target, cur):
        error = target - cur
        if (abs(error) > (180 + 180)/2):
            if (error > 0):
                error -=(180+180)
            else:
                error += (180+180)
        return error

