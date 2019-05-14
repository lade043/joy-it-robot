from __future__ import division
import Adafruit_PCA9685
import sys
import math
import time
import csv
from RobotLib import *

pwm = Adafruit_PCA9685.PCA9685(address=0x41)

joy_it = Robot(Robot.Servo(1, Robot.Servo.Geometry(0.55, 2.3, 1.4)),
               Robot.Servo(2, Robot.Servo.Geometry(2.5, 0.55, 1.55)),
               Robot.Servo(3, Robot.Servo.Geometry(0.7, 2.25, 2.25)),
               Robot.CoordinateSystem([-100, 100], [-100, 100]))
joy_it.init_depending(Robot.Arm(joy_it.servo1, 10.26, 0.84), Robot.Arm(joy_it.servo2, 9.85),
                      Robot.Arm(joy_it.servo3, 12, 9), None, [joy_it.servo1], [joy_it.servo1, joy_it.servo2])

# the values for all the servos (are different for each robot)
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
# the length of the arms (same for each joy it robot)
arms = {
    0: 0.84,
    1: 10.26,
    2: 9.85,
    "claw": 12,
    "height": 9
}


def summe(i):
    """
    Returns the sum of a list
    :param i: list with float, int
    :return: int sum
    """
    r = 0
    for element in i:
        r += element
    return r


def set_servo_pulse(channel, pulse):
    """
    Sending the position to the servos
    :param channel: servo number
    :param pulse: position in ms
    :return:
    """
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
    """
    Calculates the position of the claw relative to the center of the baseplate
    Further details in documentation
    :param anglesdeg: dict with the servo number and position in degree (deg)
    :return: list: [x, y, z] in cm from the center of the baseplate of the robot
    """
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
    """
    Calculates the theoretical angles relative to a vertical position based on the ms values for each of the servos
    :param ms: dict with the servo number and ms
    :return: dict with the servo number and position in degree (deg)
    """
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
    """
    Calculates the ms value based on the given angle (deg)
    :param servo: servo number
    :param angle: angle in degree based of the vertical position
    :return: ms value for the servo
    """
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
    Reades and processes the start arguments. The main core of the program
    :param sys.argv: styles:    python3 terminalControl.py -servo x -pos y(ms)
                                python3 terminalControl.py -list servo,pos(ms) servo,pos(ms)
                                python3 terminalControl.py -angle servo,angle servo,angle
                                python3 terminalControl.py -csv file
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
