import math
import datetime
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import time
import threading
from PIDController import *
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
        #print self.x*0.87096774*.9, self.y*0.87096774*.9, angle%360

        if (len(self.historyx)%15==0):
            pass #threading.Thread(target=self.plot).start()

    def plot(self):
        x = list(self.historyx)
        y = list(self.historyy)
        plt.plot(x, y, color="blue")
        plt.tight_layout()
        print "save"
        plt.savefig("/home/pi/Pictures/robot_position.png")

class Navigator(object):
    def __init__(self, points, driver, gyro, turnPID, drivePID, mapper):
        self.points = points
        self.gyro = gyro
        self.driver = driver
        self.turnPID = turnPID
        self.drivePID = drivePID
        self.mapper = mapper

        self.index = 0
        self.curPoint = None

    def step(self):
        if (self.curPoint != None):
            self.curPoint.step()
            if not self.curPoint.driveDone:
                return

        self.curPoint = Point(self.points[self.index][0], self.points[self.index][1], self.driver, self.gyro, self.turnPID, self.drivePID, self.mapper)
        self.index += 1

class Point(object):
    def __init__(self, dest_x, dest_y, driver, gyro, turnPID, drivePID, mapper):
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.gyro = gyro
        self.driver = driver
        self.turnPID = turnPID
        self.drivePID = drivePID
        self.mapper = mapper
        self.turnDone = False
        self.driveDone = False

    def drive_to_point(self):
        x_distance = (self.mapper.x - self.dest_x)
        y_distance = (self.mapper.y - self.dest_y)
        print "dist", x_distance, y_distance
        target_angle = (((((math.atan2(y_distance, x_distance)) * 180/math.pi))+180)% 360) - 180
        cur_angle = ((self.gyro.get_angle()+180)%360)-180
        print 'target', target_angle, 'cur', cur_angle
        error = PIDController.calc_angle_error(target_angle, cur_angle)
        print error

        output = self.turnPID.run(error)
        print output
        
        if (abs(output) < 10 and abs(error) < 10) or self.turnDone:
            self.turnDone = True
            print "-----------------------------------------------------------------"
            
        else:
            self.driver.turn_right(output, 0)
            return
        
        total_dist = math.sqrt((x_distance * x_distance) + (y_distance * y_distance))

        output = self.drivePID.run(total_dist)
        print "remain distance", total_dist, output
        self.driver.drive_straight(-output)
        if abs(total_dist) < 30 and abs(output) < 10:
            print "+++++++++++++++++++++++++++++++++++++++++++++"
            self.driveDone = True 

    def step(self):
        self.drive_to_point()
        self.driver.step()

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
        
    def step(self):
        self.drive()
        #self.drive_straight(0)
        self.mapper.step()


        