
class DynManager(object):
    def __init__(self, left, right, wb):
        self.left = left
        self.right = right

        self.speed = 0
        self.turn = 0
        self.wheelOffset = wb/2.0

    def setSpeed(self, speed):
        if speed > 1:
            self.speed = 1
            return
        elif speed < -1:
            self.speed = -1
            return
        self.speed = speed

    def setTurn(self, speed):
        if speed > 1:
            self.turn = 1
            return
        elif speed < -1:
            self.turn = -1
            return
        self.turn = speed

    def step(self):
        if self.turn == 0:
            left = self.speed
            right = self.speed
        else:
            rc = (1.0/(abs(self.turn)**2) - 1)
            if self.turn < 0:
                rc *= -1

            # theta = rc / self.speed

            if rc == 0:
                rc = self.turn / 999999999999999999999999.0
            left = (rc - self.wheelOffset) * self.speed / rc
            right = (rc + self.wheelOffset) * self.speed / rc


            # if rc == 0:
            #     rc = self.turn / 999999999999999999999999.0

            # theta = self.speed/rc
            # left = (rc - self.wheelOffset) * theta
            # right = (rc + self.wheelOffset) * theta


        #bound to positive        
        maxOne = max(abs(left),abs(right))

        if maxOne > 1:
            print("doin")
            left /= maxOne
            right/= maxOne

        print "FloatMotorManager: {}, {}".format(left, right)
        
        self.left.setSpeed(int(round(-100 * left)))
        self.right.setSpeed(int(round(-100 * right)))