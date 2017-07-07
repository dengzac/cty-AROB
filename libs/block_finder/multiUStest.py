from PiStorms import PiStorms
psm=PiStorms()

from time import sleep
while not psm.isKeyPressed():
    leftus=psm.BBS2.distanceUSEV3()
    rightus=psm.BAS2.distanceUSEV3()

    print "Left: {0}\tRight: {1}\tDifference: {2}".format(leftus,rightus,leftus-rightus)
    sleep(0.1)