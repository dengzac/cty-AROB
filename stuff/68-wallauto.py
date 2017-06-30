import time
from PiStorms import PiStorms
psm = PiStorms()

def get_error():
    return 200 - psm.BAS1.distanceUSEV3()

secs_per_step = 0.1

Kp = 1
Ki = 0
Kd = 0.01
prev_error = 0
total_error = 0
prev = []
try: 
    while True:

        error = get_error()
        D = float(error-prev_error)/secs_per_step
        prev.append(secs_per_step * error)
        while len(prev) > 30:
            prev.pop(0)
        total_error = sum(prev)
        prev_error = error

        output = Kp * error + Ki * total_error - Kd * D
        if output < -100:
            output = -100
        elif output > 100:
            output = 100

        psm.BAM1.setSpeed(output)
        psm.BAM2.setSpeed(output)

        psm.screen.termPrintAt(0, str(error) + ' ' + str(Kp * error) + ' ' + str(Ki * total_error) + ' ' + str(- Kd * D)  + ' ' + str(error) + ' ' + str(total_error) + ' ' + str(-D))
        time.sleep(secs_per_step)
        if output < 10 and abs(error) < 20:
            print "done"
            raise KeyboardInterrupt
except:
    psm.BAM1.setSpeed(0)
    psm.BAM2.setSpeed(0)

t=1
psm.BAM1.runSecs(t, -30, True)
psm.BAM2.runSecs(t, 30, True)
time.sleep(t)

secs_per_step = 0.1

Kp = 1
Ki = 0
Kd = 0.01
prev_error = 0
total_error = 0
prev = []
try: 
    while True:

        error = get_error()
        D = float(error-prev_error)/secs_per_step
        prev.append(secs_per_step * error)
        while len(prev) > 30:
            prev.pop(0)
        total_error = sum(prev)
        prev_error = error

        output = Kp * error + Ki * total_error - Kd * D
        if output < -100:
            output = -100
        elif output > 100:
            output = 100

        psm.BAM1.setSpeed(output)
        psm.BAM2.setSpeed(output)

        psm.screen.termPrintAt(0, str(error) + ' ' + str(Kp * error) + ' ' + str(Ki * total_error) + ' ' + str(- Kd * D)  + ' ' + str(error) + ' ' + str(total_error) + ' ' + str(-D))
        time.sleep(secs_per_step)
        if output < 10 and abs(error) < 20:
            print "done"
            raise KeyboardInterrupt
except:
    psm.BAM1.setSpeed(0)
    psm.BAM2.setSpeed(0)


t=1
psm.BAM1.runSecs(t, 45, True)
psm.BAM2.runSecs(t, -45, True)
time.sleep(t)

secs_per_step = 0.1

Kp = 1
Ki = 0
Kd = 0.01
prev_error = 0
total_error = 0
prev = []
try: 
    while True:

        error = get_error()
        D = float(error-prev_error)/secs_per_step
        prev.append(secs_per_step * error)
        while len(prev) > 30:
            prev.pop(0)
        total_error = sum(prev)
        prev_error = error

        output = Kp * error + Ki * total_error - Kd * D
        if output < -100:
            output = -100
        elif output > 100:
            output = 100

        psm.BAM1.setSpeed(output)
        psm.BAM2.setSpeed(output)

        psm.screen.termPrintAt(0, str(error) + ' ' + str(Kp * error) + ' ' + str(Ki * total_error) + ' ' + str(- Kd * D)  + ' ' + str(error) + ' ' + str(total_error) + ' ' + str(-D))
        time.sleep(secs_per_step)
        if output < 10 and abs(error) < 20:
            print "done"
            raise KeyboardInterrupt
except:
    psm.BAM1.setSpeed(0)
    psm.BAM2.setSpeed(0)

t=1
psm.BAM1.runSecs(t, 35, True)
psm.BAM2.runSecs(t, -35, True)
time.sleep(t)

t=1
psm.BAM1.runSecs(t, -100, True)
psm.BAM2.runSecs(t, -100, True)
time.sleep(t)
t=5
psm.BAM1.runSecs(t, -100, True)
psm.BAM2.runSecs(t, -20, True)