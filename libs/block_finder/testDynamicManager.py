from PiStorms import PiStorms
from FloatRangeMotorManager import DynManager

psm = PiStorms()
m = DynManager(psm.BAM1, psm.BAM2, 8.7)


m.setSpeed(1)
m.setTurn(1)
while not psm.isKeyPressed():
    m.step()
m.setSpeed(0)
m.setTurn(0)
m.step()
