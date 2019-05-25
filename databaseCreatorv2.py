import numpy as npy
import sys

from RobotLib import *


class Looper:
    def __init__(self, Robot):
        self.stepsize = 1
        self.robot = Robot
        self.servo1_start = self.robot.servo1.min
        self.servo2_start = self.robot.servo2.min
        self.servo3_start = self.robot.servo3.min

    def run(self):
        try:
            for ang_servo1 in npy.arange(self.servo1_start, self.robot.servo1.max, self.stepsize):
                self.robot.servo1.set_angle(ang_servo1)
                for ang_servo2 in npy.arange(self.servo2_start, self.robot.servo2.max, self.stepsize):
                    self.robot.servo2.set_angle(ang_servo2)
                    for ang_servo3 in npy.arange(self.servo3_start, self.robot.servo3.max, self.stepsize):
                        self.robot.servo3.set_angle(ang_servo3)
                        self.robot.calculate()
                        self.robot.data.add_entry(self.robot.Database.Entry(self.robot.x, self.robot.y,
                                                                            self.robot.efficency,
                                                                            self.robot.servo1, self.robot.servo2,
                                                                            self.robot.servo3))
            print("A database with {} entries has been created.".format(len(self.robot.data.database)))
        except KeyboardInterrupt:
            self.serialize("database.temp")
            print("Serialized")
            sys.exit()

    def export(self):
        file = open("database.data", 'w')
        file.write(self.robot.data.serialize())
        file.flush()
        file.close()
        print("Exported")

    def serialize(self, filepath):
        with open(filepath, 'w') as file:
            line = "{},{},{}\n".format(self.robot.servo1.deg, self.robot.servo2.deg, self.robot.servo3.deg)
            file.write(line)
            file.write(self.robot.data.serialize())
            file.flush()

    def deserialize(self, filepath):
        with open(filepath, 'r') as file:
            line = file.readline()
            line = line.split(',')
            self.servo1_start = float(line[0])
            self.servo2_start = float(line[1])
            self.servo3_start = float(line[2])
            lines = file.read()
            self.robot.data.deserialize(lines)


test = Robot(Robot.Servo(1, Robot.Servo.Geometry(0.55, 2.3, 1.4)),
             Robot.Servo(2, Robot.Servo.Geometry(2.5, 0.55, 1.55)),
             Robot.Servo(3, Robot.Servo.Geometry(0.7, 2.25, 2.25)),
             Robot.CoordinateSystem([-100, 100], [-100, 100]))
test.init_depending(Robot.Arm(test.servo1, 10.26, 0.84), Robot.Arm(test.servo2, 9.85), Robot.Arm(test.servo3, 12, -3),
                    None, [test.servo1], [test.servo1, test.servo2])

looper = Looper(test)
# looper.deserialize('database.temp')
looper.run()
looper.export()
print("finished")
print("test")
