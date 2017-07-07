from PiStorms import PiStorms
from time import sleep

pms = PiStorms()
test = [0,10,20,30,40,50,60,70,80,90,100]
out = []
pms.BAM2.setSpeed(0)
    
for speed in test:
    print("testing", speed)
    pms.BAM2.setSpeed(0)
    pms.BAM2.resetPos()
    pms.BAM2.setSpeed(speed)
    sleep(5)
    deg = pms.BAM2.pos()
    out.append((speed,deg/5.0))

print("speed, degs/sec\n", out)
pms.BAM2.setSpeed(0)
