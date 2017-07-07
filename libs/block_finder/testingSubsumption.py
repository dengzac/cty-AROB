from PiStorms import PiStorms
from MotorManager import MotorManager

psm = PiStorms()


manager = MotorManager(psm.BAM1, psm.BAM2, True)


manager.turnRight(100,5)


while (manager.isBusy()):
    pass
    manager.step()


manager.turnLeft(100,1)

while (manager.isBusy()):
    pass
    manager.step()
