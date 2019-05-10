import math


class Robot:
    class Servo:
        def __init__(self, angle, geometry, previous_servos=None):
            self.deg = angle
            self.rad = self._get_rad(self.deg)
            self.geometry = geometry
            self.max, self.min = self._get_max_min()
            self.previous_servos = None
            self.total_angle_deg = None
            self.total_angle_rad = None
            self.delta = None

        def add_previous_servos(self, previous_servos=None):
            self.previous_servos = previous_servos
            self.total_angle_deg = self.deg
            if previous_servos:
                for servo in self.previous_servos:
                    self.total_angle_deg += servo.deg
                self.delta = self.deg + previous_servos[-1].deg
                if self.delta < 0:
                    self.delta *= -1
            self.total_angle_rad = self._get_rad(self.total_angle_deg)

        def _get_rad(self, deg):
            rad = deg * math.pi / 180
            return rad

        def set_angle(self, angle):
            self.deg = angle
            self.rad = self._get_rad(self.deg)

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

    class Arm:
        def __init__(self, attatched_to, length, height=0.0):
            self.attachted_to = attatched_to
            self.length = length
            self.height = height

    class CoordinateSystem:
        def __init__(self, x, y):
            self.xmin = x[0]
            self.xmax = x[1]
            self.ymin = y[0]
            self.ymax = y[1]

        def is_inside(self, x, y):
            return self.xmin <= x <= self.xmax and self.ymin <= y <= self.ymax

    class Database:

        class Entry:
            def __init__(self, x, y, effi, s1, s2, s3):
                self.x = x
                self.y = y
                self.effi = effi
                self.s1 = s1
                self.s2 = s2
                self.s3 = s3

            def pos_is_equal_to(self, other_entry):
                return self.x == other_entry.x and self.y == other_entry.y

            def other_efficency_better(self, other_entry):
                return self.effi > other_entry.effi

        def __init__(self):
            self.database = []

        def _is_contained(self, entry):
            for existing_entry in self.database:
                if existing_entry.pos_is_equal_to(entry):
                    return existing_entry
            return None

        def get_entry(self, x, y):
            wanted = self.Entry(x, y, 0, 0, 0, 0)
            return self._is_contained(wanted)

        def add_entry(self, entry):
            contained = self._is_contained(entry)
            if contained:
                if contained.other_efficency_better(entry):
                    self.database.append(entry)
            else:
                self.database.append(entry)

    def __init__(self, s1, s2, s3, coordinatessystem):
        self.servo1 = s1
        self.servo2 = s2
        self.servo3 = s3
        self.coordinatesystem = coordinatessystem
        self.arm1 = None
        self.arm2 = None
        self.arm3 = None
        self.data = self.Database()
        self.x = None
        self.y = None
        self.efficency = None

    def init_depending(self, a1, a2, a3, s1_prev=None, s2_prev=None, s3_prev=None):
        self.arm1 = a1
        self.arm2 = a2
        self.arm3 = a3
        self.servo1.add_previous_servos(s1_prev)
        self.servo2.add_previous_servos(s2_prev)
        self.servo3.add_previous_servos(s3_prev)
        self.x, self.y = self._get_position()
        self.efficency = self._get_efficency()

    def _get_position(self):
        x = 0
        y = 0
        for arm in [self.arm1, self.arm2, self.arm3]:
            x += math.sin(arm.attachted_to.total_angle_rad) * arm.length + math.sin(
                arm.attachted_to.total_angle_rad + 1.5708) * arm.height
            y += math.cos(arm.attachted_to.total_angle_rad) * arm.length + math.cos(
                arm.attachted_to.total_angle_rad + 1.5708) * arm.height
        return x, y

    def _get_efficency(self):
        effi = 0
        multipliers = [8, 4, 2]
        for i, servo in enumerate([self.servo1, self.servo2, self.servo3]):
            effi += servo.delta * multipliers[i]
        return effi