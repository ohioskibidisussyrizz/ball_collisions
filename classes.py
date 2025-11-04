import math

class Ball:
    def __init__(self,
                 pos_x,
                 vel_x,
                 pos_y,
                 vel_y,
                 mass,
                 radius,
                 color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.vel = math.sqrt(vel_x**2 + vel_y**2)
        self.radius = radius
        self.color = color
        self.mass = radius*2
    def get_pos_x(self):
        return self.pos_x
    def set_pos_x(self, pos_x):
        self.pos_x = pos_x
    def get_pos_y(self):
        return self.pos_y
    def set_pos_y(self, pos_y):
        self.pos_y = pos_y
    def get_vel_x(self):
        return self.vel_x
    def set_vel_x(self, vel_x):
        self.vel_x = vel_x
    def get_vel_y(self):
        return self.vel_y
    def set_vel_y(self, vel_y):
        self.vel_y = vel_y
    def get_radius(self):
        return self.radius
    def get_color(self):
        return self.color
    def set_color(self, color):
        self.color = color
    def get_mass(self):
        return self.mass
    def set_mass(self, mass):
        self.mass = mass
    def set_vel(self, vel):
        self.vel = vel
    def get_vel(self):
        return self.vel

