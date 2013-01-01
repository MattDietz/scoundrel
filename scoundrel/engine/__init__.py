import pygame


colors = pygame.color.THECOLORS
context = None


class Context(object):
    def __init__(self, screen=None, clock=None):
        self.clock = clock
        self.screen = screen

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
    context = Context(clock=pygame.time.Clock())
    context.screen = pygame.display.set_mode((conf['width'],
                                              conf['height']),
                                              conf['mode_flags'])


def drawing_context():
    return context
