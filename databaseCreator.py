import math
import csv

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


def get_pos(anglesdeg):
    factor = math.pi / 180
    angles = anglesdeg.copy()
    for i in angles:
        # print(angles[i])
        angles[i] = angles[i] * factor
        # print(angles[i])
    x = 0
    z = 0
    for angle in range(0, 3):
        x += (math.sin(summe([angles[i] for i in range(1, angle + 1)])) * arms[angle])
        z += (math.cos(summe([angles[i] for i in range(1, angle + 1)])) * arms[angle])
    x += arms[0]
    z += arms["height"]
    angle = 3
    x += (math.sin(summe([angles[i] for i in range(1, angle + 1)]) - 15 * factor) * arms["claw"])
    z += (math.cos(summe([angles[i] for i in range(1, angle + 1)]) - 15 * factor) * arms["claw"])
    coordinateback = [x, z]
    # print(str(x))
    # print(str(y))
    # print(str(z))
    return coordinateback


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
    change = 1 / 90
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


def get_max_min(servo):
    minimum = "servo" + str(servo) + "min"
    maximum = "servo" + str(servo) + "max"
    middle = "servo" + str(servo) + "mid"
    val_min = geometry[minimum]
    val_max = geometry[maximum]
    val_mid = geometry[middle]
    change = 1 / 90
    if val_min > val_max:
        change *= -1
    minimum = (val_min - val_mid) / change
    maximum = (val_max - val_mid) / change

    return [minimum, maximum]


def get_efficency(anglesdeg):
    eff = 0
    i = 1
    for servo in reversed(anglesdeg):
        eff += i * servo
        i += 1
    return eff


pos = []
for servoR in range(5):
    pos[servoR] = get_max_min(servoR)

"""
pos = [x, y, z, eff]
if eff < replace
"""
db = {}
for steps in range(1, 0, -0.2):
    for servo1 in range(pos[1][0], pos[1][1], steps):
        for servo2 in range(pos[2][0], pos[2][1], steps):
            for servo3 in range(pos[3][0], pos[3][1], steps):
                for servo4 in range(pos[4][0], pos[4][1], steps):
                    coordinate = []
                    coordinate.append(get_pos([servo1, servo2, servo3, servo4]))
                    # coordinate.append(get_efficency([servo0, servo1, servo2, servo3, servo4]))
                    if coordinate in db:
                        if db[coordinate][]
