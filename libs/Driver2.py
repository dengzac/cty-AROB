import math
import datetime
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import time
import threading
plt.figure(figsize=(4, 3), dpi = 80)
plt.xlabel('x')
plt.ylabel('y')
plt.title('location')
plt.grid(True)
class Mapper(object):
    def __init__(self, left_motor, right_motor, gyro):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.left_prev = left_motor.pos()
        self.right_prev = right_motor.pos()
        self.gyro = gyro
        self.x = 0
        self.y = 0
        self.historyx = []
        self.historyy = []

    def step(self):
        angle = -self.gyro.get_angle()
        left_dist = self.left_motor.pos() - self.left_prev
        right_dist = self.right_motor.pos() - self.right_prev

        self.left_prev = self.left_motor.pos()
        self.right_prev = self.right_motor.pos()

        if (abs(left_dist) > 100 or abs(right_dist) > 100):
            return
        #print left_dist, right_dist
        average = (left_dist + right_dist)/2
        if (len(self.historyx) == 0 ):
            average = 0
        self.x -=  average* math.cos(angle*(math.pi/180.0))
        self.y -=  average*math.sin(angle*(math.pi/180.0))
        self.historyx.append(self.x*0.87096774*.9)
        self.historyy.append( self.y*0.87096774*.9)
        print self.x*0.87096774*.9, self.y*0.87096774*.9, angle%360

        if (len(self.historyx)%15==0):
            pass #threading.Thread(target=self.plot).start()

    def plot(self):
        x = list(self.historyx)
        y = list(self.historyy)
        plt.plot(x, y, color="blue")
        plt.tight_layout()
        print "save"
        plt.savefig("/home/pi/Pictures/robot_position.png")


class Driver(object):
    def __init__(self, left_motor, right_motor, gyro, axle_length = 3):
        self.left_motor = left_motor
        self.right_motor = right_motor

        self.gyro = gyro
        self.direction = 0
        self.speed = 0
        self.radius = None
        self.axle_length = axle_length
        self.x = 0
        self.y = 0
        self.prev_time = datetime.datetime.now()
        self.mapper = Mapper(left_motor, right_motor, gyro)

    def drive_straight(self, speed):
        self.speed = speed
        self.direction = 0

    def turn_left(self, speed, radius=0):
        self.speed = speed
        self.direction = 1
        self.radius = radius

    def turn_right(self, speed, radius=0):
        self.speed = speed
        self.direction = 2
        self.radius = radius

    def drive(self):
        if self.direction == 0:
            self.left_motor.setSpeed(self.speed)
            self.right_motor.setSpeed(self.speed)
        elif self.direction == 1:
            print "turn left"
            # self.left_motor.setSpeed(self.speed)
            # self.right_motor.setSpeed(-self.speed)
            ratio = float(self.radius+self.axle_length)/float(self.radius-self.axle_length)
            outer_speed = self.speed
            inner_speed = int(float(outer_speed) / ratio)
            if abs(inner_speed) > 100:
                outer_speed *= 100/abs(inner_speed)
                inner_speed *= 100/abs(inner_speed)
            self.left_motor.setSpeed(-inner_speed)
            self.right_motor.setSpeed(-outer_speed)
        elif self.direction == 2:
            # print "turn right"
            # self.left_motor.setSpeed(-self.speed)
            # self.right_motor.setSpeed(self.speed)
            ratio = float(self.radius+self.axle_length)/float(self.radius-self.axle_length)
            outer_speed = self.speed
            inner_speed = int(float(outer_speed) / ratio)
            if abs(inner_speed) > 100:
                outer_speed *= 100/abs(inner_speed)
                inner_speed *= 100/abs(inner_speed)
            self.left_motor.setSpeed(-outer_speed)
            self.right_motor.setSpeed(-inner_speed)
    def brake(self):
        self.left_motor.brake()
        self.right_motor.brake()
        
    def drive_to_point(self , x_goal, y_goal, controller):
        x_distance = abs(x_goal - self.x)
        y_distance = abs(y_goal - self.y)
        distance = math.sqrt(math.pow(x_distance,2)+math.pow(y_distance,2))
        angle = (math.acos(x_distance/distance))
        if self.gyro.get_angle()%360 > angle:
            self.left_motor.setSpeed()
            self.right_motor.setSpeed(controller.run(self.gyro.get_angle() - angle))
        elif self.gyro.get_angle()%360 < angle:
            self.left_motor.setSpeed()
            self.right_motor.setSpeed()
        else :

    def step(self):
        self.drive()
        #self.drive_straight(0)
        self.mapper.step()


        