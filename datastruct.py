class SelectionData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.zero_frame = 0
        self.start_frame = 0
        self.end_frame = 0

    def set_x(self, x):
        self.x = int(x)

    def set_y(self, y):
        self.y = int(y)

    def set_radius(self, r):
        self.radius = int(r)

    def set_radius_delta(self, rd):
        self.radius += int(rd)

    def set_start_frame(self, f):
        self.start_frame = int(f)

    def set_end_frame(self, f):
        self.end_frame = int(f)

    def set_zero_frame(self, f):
        self.zero_frame = int(f)
