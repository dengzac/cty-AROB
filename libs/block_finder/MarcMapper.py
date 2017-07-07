"""Mapper class keeps track of a robot's current location and previous path."""
import matplotlib
matplotlib.use('agg')
import math
import numpy
from matplotlib import pyplot

WHEEL_CIRCUMFERENCE = 56 * math.pi
FILE_NAME = "/home/pi/Pictures/robot_position.png"

class Mapper(object):
    def __init__(self, left_motor, right_motor, gyro_sensor, psm, motors_mounted_backwards=False):
        self.psm = psm
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.gyro_sensor = gyro_sensor

        self.initial_gyro_degrees = gyro_sensor.gyroAngleEV3()
        self.total_x = 0
        self.total_y = 0
        self.heading = 0
        self.motors_mounted_backwards = motors_mounted_backwards
        
        self.path = numpy.array([[0,0]])

        pyplot.figure(figsize=(4, 3), dpi=80)
        pyplot.title('Robot position')
        pyplot.xlabel('x')
        pyplot.ylabel('y')
        pyplot.grid(True)

    def step(self):
        # Get the angle from the sensor, calibrated against start point
        self.heading = ((self.gyro_sensor.gyroAngleEV3() - self.initial_gyro_degrees) * -1) % 360
        
        # Gather the position from both motor encoders
        left_motor_degrees = self.left_motor.pos()
        right_motor_degrees = self.right_motor.pos()

        # Check for sensor overflow and skip this step if present
        if abs(left_motor_degrees) > 10000 or abs(right_motor_degrees) > 10000:
            return 

        # Immediately reset after gathering data
        self.left_motor.resetPos()
        self.right_motor.resetPos()
        
        # Calculate the distance travelled by averaging both motors and converting degs to mms.
        average_degrees_moved = (left_motor_degrees + right_motor_degrees) / 2
        distance_traveled = average_degrees_moved * WHEEL_CIRCUMFERENCE / 360

        if self.motors_mounted_backwards:
            distance_traveled = distance_traveled * -1
        
        # Use trig to calculate X and Y travelled using heading and distance travelled.
        x_traveled = math.cos(math.radians(self.heading)) * distance_traveled
        y_traveled = math.sin(math.radians(self.heading)) * distance_traveled
        
        # Update current position using the most recent x and y changes.
        self.total_x += x_traveled
        self.total_y += y_traveled

        # print "Moved {0} at heading {1}. Traveled {2}, {3}. Now at {4}, {5}.".format(
        #     distance_traveled, self.heading, x_traveled, y_traveled, self.total_x, self.total_y)
 
        # Update the path by appending current coordinates to the end
        self.path = numpy.concatenate((self.path, [[self.total_x, self.total_y]]), 0)

    def plot(self):
        pyplot.plot(self.path[:,0], self.path[:,1])         
        pyplot.tight_layout() # make sure the entire plot fits on screen
        pyplot.savefig(FILE_NAME, format="png") # save it
        self.psm.screen.fillBmp(0, 0, 320, 240, FILE_NAME) # show it on PiStorms screen
    
    def plotWithPoints(self, points):
        [pyplot.scatter(x[0], x[1], color="red") for x in points]          
        pyplot.plot(self.path[:,0], self.path[:,1])
        pyplot.tight_layout() # make sure the entire plot fits on screen
        pyplot.savefig(FILE_NAME, format="png") # save it
        self.psm.screen.fillBmp(0, 0, 320, 240, FILE_NAME) # show it on PiStorms screen    

    def getLocation(self):
        return [self.total_x, self.total_y]

    def getHeading(self):
        return self.heading