from __future__ import division
import Adafruit_PCA9685
import sys
import time
import csv
from RobotLib import *

pwm = Adafruit_PCA9685.PCA9685(address=0x41)
pwm.set_pwm_freq(50)

joy_it = Robot(Robot.Servo(1, Robot.Servo.Geometry(0.55, 2.3, 1.4)),
               Robot.Servo(2, Robot.Servo.Geometry(2.5, 0.55, 1.55)),
               Robot.Servo(3, Robot.Servo.Geometry(0.7, 2.25, 2.25)),
               Robot.CoordinateSystem([-100, 100], [-100, 100]))
joy_it.init_depending(Robot.Arm(joy_it.servo1, 10.26, 0.84), Robot.Arm(joy_it.servo2, 9.85),
                      Robot.Arm(joy_it.servo3, 12, 9), None, [joy_it.servo1], [joy_it.servo1, joy_it.servo2])

# the values for all the servos (are different for each robot)
servo0min = 0.5
servo0max = 2.5
servo0mid = 1.85
servo4min = 0.5
servo4max = 2.5
servo4mid = 1.5


class argvReader:
    def __init__(self, argv):
        self.argv = argv

    def home(self):
        for i, servo in enumerate([joy_it.servo1, joy_it.servo2, joy_it.servo3]):
            servo.set_angle(0)
            set_servo_pulse(i+1, servo.get_ms(True))

    def servo(self):
        servo_int = int(self.argv[2])
        pos = float(self.argv[4])
        if servo_int == 1:
            servo = joy_it.servo1
        elif servo_int == 2:
            servo = joy_it.servo2
        elif servo_int == 3:
            servo = joy_it.servo3
        if servo_int <= 3:
            if not servo.geometry.is_inside(pos):
                print("Position to big or to small")
                sys.exit()
            elif 0 < servo < 5:
                print("Servo is not on robotarm")
            else:
                servo.set_ms(pos)
                set_servo_pulse(servo_int, servo.ms)
        elif servo_int <= 5:
            set_servo_pulse(servo_int, pos)
        else:
            sys.exit()
        print(str(servo_int) + ": " + str(pos))

    def list(self):
        commands = self.argv[2:]
        for entry in commands:
            servo_int = int(entry.split(',')[0])
            pos = float(entry.split(',')[1])
            if servo_int == 1:
                servo = joy_it.servo1
            elif servo_int == 2:
                servo = joy_it.servo2
            elif servo_int == 3:
                servo = joy_it.servo3
            if 0 < servo_int <= 3:
                if not servo.geometry.is_inside(pos):
                    print("Position to big or to small")
                    sys.exit()
                elif 0 < servo < 5:
                    print("Servo is not on robotarm")
                else:
                    servo.set_ms(pos)
                    set_servo_pulse(servo_int, servo.ms)
            elif servo_int <= 5 or servo_int == 0:
                set_servo_pulse(servo_int, pos)
            else:
                sys.exit()
            print(str(servo_int) + ": " + str(pos))

    def angle(self):
        commands = self.argv[2:]
        for entry in commands:
            servo_int = int(entry.split(',')[0])
            pos = float(entry.split(',')[1])
            if servo_int == 1:
                servo = joy_it.servo1
            elif servo_int == 2:
                servo = joy_it.servo2
            elif servo_int == 3:
                servo = joy_it.servo3
            if 0 < servo_int <= 3:
                servo.set_angle(pos)
                ms = servo.get_ms(True)
                if not servo.geometry.is_inside(ms):
                    print("Position to big or to small")
                    sys.exit()
                elif 0 < servo < 5:
                    print("Servo is not on robotarm")
                else:
                    set_servo_pulse(servo_int, servo.ms)
            elif servo_int == 4:
                ms = get_ms_servo4(pos)
                set_servo_pulse(servo_int, ms)
            elif servo_int == 0:
                ms = get_ms_servo0(pos)
                set_servo_pulse(servo_int, ms)
            else:
                sys.exit()

    def csv(self):
        file = self.argv[2]

        with open(file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if "delay" in row[0]:
                    print("sleep " + row[0].split(" ")[1])
                    time.sleep(int(row[0].split(" ")[1]))
                else:
                    for servo_int, pos in enumerate(row):
                        if servo_int == 1:
                            servo = joy_it.servo1
                        elif servo_int == 2:
                            servo = joy_it.servo2
                        elif servo_int == 3:
                            servo = joy_it.servo3
                        if 0 < servo_int <= 3:
                            servo.set_angle(pos)
                            ms = servo.get_ms(True)
                            if not servo.geometry.is_inside(ms):
                                print("Position to big or to small")
                                sys.exit()
                            elif 0 < servo < 5:
                                print("Servo is not on robotarm")
                            else:
                                set_servo_pulse(servo_int, servo.ms)
                        elif servo_int == 4:
                            ms = get_ms_servo4(pos)
                            set_servo_pulse(servo_int, ms)
                        elif servo_int == 0:
                            ms = get_ms_servo0(pos)
                            set_servo_pulse(servo_int, ms)
                        else:
                            sys.exit()


def get_ms_servo4(deg):
    change = 1 / 90
    if servo4min > servo4max:
        change *= -1
    ms = (deg * change + servo4mid)
    return ms


def get_ms_servo0(deg):
    change = 1 / 90
    if servo0min > servo0max:
        change *= -1
    ms = (deg * change + servo0mid)
    return ms


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
        argv_reader.home()
    elif sys.argv[1] == "-servo":
        argv_reader.servo()
    elif sys.argv[1] == "-list":  # -list 0,1.5 2,2 3,1.75
        argv_reader.list()
    elif sys.argv[1] == "-angle":
        argv_reader.angle()
    elif sys.argv[1] == "-csv":
        argv_reader.csv()


argv_reader = argvReader(sys.argv)
read_argv()

