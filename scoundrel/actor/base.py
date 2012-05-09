class Actor(object):
    def __init__(self, position):
        self.position = position

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x_setter(self, xv):
        self.position[0] = xv

    @y.setter
    def y_setter(self, yv):
        self.position[1] = yv

    @property
    def y(self):
        return self.position[1]
