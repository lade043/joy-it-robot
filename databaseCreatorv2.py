import math


class Robot:
    class Servo:
        def __init__(self, angle, geometry):
            self.deg = angle
            self.rad = self._get_rad()
            self.geometry = geometry
            self.max, self.min = self._get_max_min()

        def _get_rad(self):
            rad = self.deg * math.pi / 180
            return rad

        def set_angle(self, angle):
            self.deg = angle
            self.rad = self._get_rad()

        def _get_angle(self, ms):
            val_min = self.geometry.min
            val_max = self.geometry.max
            val_mid = self.geometry.mid
            change = 1 / 90
            if val_min > val_max:
                change *= -1
            angle = (ms - val_mid) / change
            return angle

        def _get_max_min(self):
            return self._get_angle(self.geometry.max), self._get_angle(self.geometry.min)

        class Geometry:
            def __init__(self, _max, _min, mid):
                self.max = _max
                self.min = _min
                self.mid = mid

    class CoordinateSystem:
        def __init__(self, x, y):
            self.xmin = x[0]
            self.xmax = x[1]
            self.ymin = y[0]
            self.ymax = y[1]

        def is_inside(self, x, y):
            return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    def __init__(self, s1, s2, s3, coordinatessystem):
        self.servo1 = s1
        self.servo2 = s2
        self.servo3 = s3
        self.coordinatesystem = coordinatessystem
        # get position based on servos
        # get efficency based on servos

    def _get_position(self):
        return x, y

    def _get_efficency(self):
        return effi


test = Robot(Robot.Servo(1, Robot.Servo.Geometry(0.55, 2.3, 1.4)), Robot.Servo(2, Robot.Servo.Geometry(2.5, 0.55, 1.55)),
             Robot.Servo(3, Robot.Servo.Geometry(0.7, 2.25, 2.25)), Robot.CoordinateSystem([-100, 100], [-100, 100]))
print("finished")
