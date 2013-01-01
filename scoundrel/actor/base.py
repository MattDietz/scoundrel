class Actor(object):
    def __init__(self, position=None):
        self.position = position

    @property
    def x(self):
        def fget(self):
            return self.position[0]

        def fset(self, x):
            self.position[0] = xv

    @property
    def y(self, yv):
        def fget(self):
            return self.position[1]

        def fset(self, y):
            self.position[1] = yv


    def draw(self, context):
        pass
