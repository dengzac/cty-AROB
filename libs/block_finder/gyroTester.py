from PiStorms import PiStorms

psm = PiStorms()

while not psm.isKeyPressed():
    print psm.BBS1.gyroAngleEV3()