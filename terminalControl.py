from __future__ import division
import Adafruit_PCA9685
import sys
import math
import time
import csv

pwm = Adafruit_PCA9685.PCA9685(address=0x41)

geometry = {
        "servo0min": 0.5,
        "servo0max": 2.5,
        "servo0mid": 1.85,
        "servo1min": 2.3,
        "servo1max": 0.55,
        "servo1mid": 1.4,
        "servo2min": 0.55,
        "servo2max": 2.5,
        "servo2mid": 1.55,
        "servo3min": 2.25,
        "servo3max": 0.7,
        "servo3mid": 2.25,
        "servo4min": 0.5,
        "servo4max": 2.5,
        "servo4mid": 1.5
    }
arms = {
    0: 0.84,
    1: 10.26,
    2: 9.85,
    "claw": 12,
    "height": 9
}


def summe(i):
    r = 0
    for element in i:
        r += element
    return r


def set_servo_pulse(channel, pulse):
    pulse_length = 1000000
    pulse_length /= 50
    pulse_length /= 4096
    pulse *= 1000
    pulse /= pulse_length
    pulse = round(pulse)
    pulse = int(pulse)
    pwm.set_pwm(channel, 0, pulse)


pwm.set_pwm_freq(50)


def get_pos(anglesdeg):
    factor = math.pi / 180
    angles = anglesdeg.copy()
    for i in angles:
        # print(angles[i])
        angles[i] = angles[i] * factor
        # print(angles[i])
    x = 0
    y = 0
    z = 0
    for angle in range(1, 3):
        x += (math.sin(summe([angles[i] for i in range(1, angle + 1)])) * arms[angle])
        z += (math.cos(summe([angles[i] for i in range(1, angle + 1)])) * arms[angle])
    x += arms[0]
    z += arms["height"]
    angle = 3
    x += (math.sin(summe([angles[i] for i in range(1, angle + 1)]) - 15 * factor) * arms["claw"])
    z += (math.cos(summe([angles[i] for i in range(1, angle + 1)]) - 15 * factor) * arms["claw"])
    y += (math.sin(angles[0]) * x)
    x = (math.cos(angles[0]) * x)
    coordinate = [x, y, z]
    # print(str(x))
    # print(str(y))
    # print(str(z))
    return coordinate


def get_angles(ms):
    angles = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for servo in angles:
        if ms[servo]:
            minimum = "servo" + str(servo) + "min"
            maximum = "servo" + str(servo) + "max"
            middle = "servo" + str(servo) + "mid"
            val_min = geometry[minimum]
            val_max = geometry[maximum]
            val_mid = geometry[middle]
            change = 1 / 90
            if val_min > val_max:
                change *= -1
            angles[servo] = (ms[servo] - val_mid) / change
    return angles


def get_ms(servo, angle):
    minimum = "servo" + str(servo) + "min"
    maximum = "servo" + str(servo) + "max"
    middle = "servo" + str(servo) + "mid"
    val_min = geometry[minimum]
    val_max = geometry[maximum]
    val_mid = geometry[middle]
    change = 1/90
    if val_min > val_max:
        change *= -1
    ms = (angle * change + val_mid)
    if change > 0:
        if ms < val_min or ms > val_max:
            return 0
    else:
        if ms > val_min or ms < val_max:
            return 0
    # ms = round(ms, 2)
    return ms


def read_argv():
    """
    :param TerminalParameter: style: python3 terminalControl.py -servo x -pos y
    :return:
    """
    if sys.argv[1] == "-home":
        for sv in range(0, 5):
            set_servo_pulse(sv, 1.5)
    elif sys.argv[1] == "-servo":
        servo = int(sys.argv[2])
        pos = float(sys.argv[4])
        if pos < 1 or pos > 2.5:
            print("Position to big or to small")
            sys.exit()
        elif servo < 0 or servo > 5:
            print("Servo is not on robotarm")
        print(str(servo) + ": " + str(pos))

        set_servo_pulse(servo, pos)
    elif sys.argv[1] == "-list":  # -list 0,1.5 2,2 3,1.75
        commands = sys.argv[2:]
        varTime = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for entry in commands:
            servo = int(entry.split(',')[0])
            pos = float(entry.split(',')[1])
            if servo != 4 or servo != 5:
                varTime[servo] = pos
            print(str(servo) + ": " + str(pos))
            set_servo_pulse(servo, pos)
        calcangles = get_angles(varTime)
        calcpos = get_pos(calcangles)
        for sentry in calcangles:
            print(str(sentry) + ": " + str(round(calcangles[sentry])))
        for sentry in calcpos:
            print(str(calcpos.index(sentry)) + ": " + str(sentry))
    elif sys.argv[1] == "-angle":
        commands = sys.argv[2:]
        # calcangles = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        varTime = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for entry in commands:
            servo = int(entry.split(',')[0])
            pos = float(entry.split(',')[1])
            # calcangles[servo] = pos
            pos = get_ms(servo, pos)
            if servo != 4:
                varTime[servo] = pos
            print(str(servo) + ": " + str(pos))
            set_servo_pulse(servo, pos)
        calcangles = get_angles(varTime)
        calcpos = get_pos(calcangles)
        for entry in calcangles:
            print(str(entry) + ": " + str(round(calcangles[entry])))
        for entry in calcpos:
            print(str(calcpos.index(entry)) + ": " + str(entry))
    elif sys.argv[1] == "-csv":
        file = sys.argv[2]

        with open(file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if "delay" in row[0]:
                    print("sleep " + row[0].split(" ")[1])
                    time.sleep(int(row[0].split(" ")[1]))
                else:
                    print(row)
                    varTime = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
                    f = 0
                    for i in row:
                        servo = f
                        print(str(servo))
                        pos = int(i)
                        pos = get_ms(servo, pos)
                        if servo != 4:
                            varTime[servo] = pos
                        print(str(servo) + ": " + str(pos))
                        set_servo_pulse(servo, pos)
                        f += 1
                    calcangles = get_angles(varTime)
                    calcpos = get_pos(calcangles)
                    for entry in calcangles:
                        print(str(entry) + ": " + str(round(calcangles[entry])))
                    for entry in calcpos:
                        print(str(calcpos.index(entry)) + ": " + str(entry))


read_argv()
