import datetime
class SafeDriver(object):
    def __init__(self, min_distance, driver, ultrasonic, reset_time):
        self.driver = driver
        self.min_distance = min_distance
        self.ultrasonic = ultrasonic
        self.reset_time = reset_time

        self.prev_time = None

    def checkSafe(self):
        return self.ultrasonic.distanceUSEV3() > self.min_distance

    def step(self):
        if self.prev_time != None:
            if float(-(self.prev_time - datetime.datetime.now()).total_seconds()) < self.reset_time:
                return
            else:
                self.prev_time = None
        if self.checkSafe():
            self.driver.tick()
        else:
            self.driver.brake()
            self.prev_time = datetime.datetime.now()