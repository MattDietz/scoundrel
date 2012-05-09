class Context(object):
    def __init__(self, screen=None, clock=None):
        self._clock = clock
        self._screen = screen

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, screen):
        self._screen = screen

    @property
    def clock(self):
        return self._clock

    @clock.setter
    def clock(self, clock):
        self._clock = clock
