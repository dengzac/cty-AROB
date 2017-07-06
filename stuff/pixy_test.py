import time
import datetime

from PixyCamget import *
from PIDController import PIDController
from Gyro import Gyro
from Driver import *

from PiStorms import PiStorms

psm = PiStorms()

gyro = Gyro(psm.BAS2)
TurnPID = PIDController(1, 0, 0,1)
DrivePID = PIDController(1,0,0)
pixy = Pixy()
gyro.calibrate(1)

driver = Driver(psm.BAM1, psm.BAM2, gyro, 3)

while True:
    blocks = pixy.get_blocks()
    found_block = None
    largest_block_size = 0
    for block in blocks:
        if block[1] != 1: # Check signature type
            continue
        current_size = block[4] * block[5] # Find block with largest area
        if current_size > largest_block_size:
            largest_block_size = current_size
            found_block = block

    if found_block == None:
        continue
    print "Found block", block
    block_pos = 2*(block[2]/100) - 1  #  Replace with actual image width
    distance = 1234/block[5]
    angle = HORIZONTAL_FOV * block_pos / 2
    print "angle", angle, "distance", distance
    output = TurnPID.calc(angle)
    speed = DrivePID.calc(100-distance)
    print "turn", output, "speed", speed
    driver.drive_straight(speed, output)
    driver.step()