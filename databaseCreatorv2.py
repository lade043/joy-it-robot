from RobotLib import *

test = Robot(Robot.Servo(1, Robot.Servo.Geometry(0.55, 2.3, 1.4)),
             Robot.Servo(2, Robot.Servo.Geometry(2.5, 0.55, 1.55)),
             Robot.Servo(3, Robot.Servo.Geometry(0.7, 2.25, 2.25)),
             Robot.CoordinateSystem([-100, 100], [-100, 100]))
test.init_depending(Robot.Arm(test.servo1, 10.26, 0.84), Robot.Arm(test.servo2, 9.85), Robot.Arm(test.servo3, 12, 9),
                    None, [test.servo1], [test.servo1, test.servo2])
print("finished")
print("test")
