import pygame


colors = pygame.color.THECOLORS
context = None


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

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pygame.display.flip()
        context.clock.tick(60)
        pygame.display.set_caption("Scoundrel FPS: %d" %\
                                   context.clock.get_fps())


def init(conf):
    global context
    pygame.init()
    context = Context()
    context.screen = pygame.display.set_mode((conf['width'],
                                              conf['height']),
                                              conf['mode_flags'])
    context.clock = pygame.time.Clock()


def drawing_context():
    return context
