from RobotLib import *
import numpy as npy


class Looper:
    def __init__(self, Robot):
        self.stepsize = 0.3
        self.robot = Robot

    def run(self):
        for ang_servo1 in npy.arange(self.robot.servo1.min, self.robot.servo1.max, self.stepsize):
            self.robot.servo1.set_angle(ang_servo1)
            for ang_servo2 in npy.arange(self.robot.servo2.min, self.robot.servo2.max, self.stepsize):
                self.robot.servo2.set_angle(ang_servo2)
                for ang_servo3 in npy.arange(self.robot.servo3.min, self.robot.servo3.max, self.stepsize):
                    self.robot.servo3.set_angle(ang_servo3)
                    self.robot.calculate()
                    self.robot.data.add_entry(self.robot.Database.Entry(self.robot.x, self.robot.y,
                                                                        self.robot.efficency,
                                                                        self.robot.servo1, self.robot.servo2,
                                                                        self.robot.servo3))
        print("A database with {} entries has been created.".format(len(self.robot.data.database)))


test = Robot(Robot.Servo(1, Robot.Servo.Geometry(0.55, 2.3, 1.4)),
             Robot.Servo(2, Robot.Servo.Geometry(2.5, 0.55, 1.55)),
             Robot.Servo(3, Robot.Servo.Geometry(0.7, 2.25, 2.25)),
             Robot.CoordinateSystem([-100, 100], [-100, 100]))
test.init_depending(Robot.Arm(test.servo1, 10.26, 0.84), Robot.Arm(test.servo2, 9.85), Robot.Arm(test.servo3, 12, 9),
                    None, [test.servo1], [test.servo1, test.servo2])

looper = Looper(test)
looper.run()
print("finished")
print("test")
