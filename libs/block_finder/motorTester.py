from PiStorms import PiStorms
psm = PiStorms()

print(psm.BAM1.resetPos())

while not psm.isKeyPressed():
    print(psm.BAM1.pos())