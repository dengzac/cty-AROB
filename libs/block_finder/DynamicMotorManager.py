
class DynManager(object):
    def __init__(self, left, right, wheelcirc, wheelbase):
        self.left = left
        self.right = right

        self.wheelcirc = wheelcirc
        self.wheelbase = wheelbase

        self.forward = 0
        self.turn = 0

    def setSpeedForwardMMPerSecond(self, speed):
        self.forward = speed

    def setTurnRadiansPerSecond(self, speed):
        self.turn = speed

    def step(self):
        mmLeft = (self.turn * self.wheelbase + self.forward * 2) / 2.0
        mmRight = self.forward * 2 - mmLeft

        # speed 100 = 1000 degs per second
        left = (mmLeft / self.wheelcirc) * 360.0 / 6.0
        right = (mmRight / self.wheelcirc) * 360.0 / 6.0
        
        # scale up so one is exactly 100
        larger = max(left,right)
        if larger > 100:
            print("casting 100")
            left = left * (100.0/larger)
            right = right * (100.0/larger)

        # hope to god that neither are below -100

        print "left: {}\tright: {}".format(left,right)
        self.left.setSpeed(-int(left))
        self.right.setSpeed(-int(right))
