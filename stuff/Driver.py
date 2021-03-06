import cv2
import numpy as np

def callback():
	
image = cv2.imread("/home/rush/")
cv2.namedWindow("window", 1)

cv2.createTrackbar("Rmin", "window",0,255,callback)

                                                                                                                                                                                                                                                                                                                                                            self.direction = 2

    def arcturn(self, speed, radius, reverse_direction = False):
        if radius==0:
            return
        self.outside_speed = -speed
        self.inside_speed = -(int(self.outside_speed - (self.axle_width*self.outside_speed)/radius))
        self.reverse_direction = reverse_direction
        self.direction = 3
    def drive(self):
        if self.direction == 0:
            self.left_motor.setSpeed(self.speed)
            self.right_motor.setSpeed(self.speed)
        elif self.direction == 1:
            self.left_motor.setSpeed(-self.speed)
            self.right_motor.setSpeed(self.speed)
        elif self.direction == 2:
            print self.speed
            self.left_motor.setSpeed(self.speed)
            self.right_motor.setSpeed(-self.speed)
        elif self.direction == 3:
            if self.reverse_direction:
                self.left_motor.setSpeed(self.outside_speed)
                self.right_motor.setSpeed(self.inside_speed)
            else:
                self.left_motor.setSpeed(self.inside_speed)
                self.right_motor.setSpeed(self.outside_speed)

    def brake(self):
        self.left_motor.brake()
        self.right_motor.brake()
        
    def step(self):
        self.drive()
