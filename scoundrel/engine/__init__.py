import pygame


colors = pygame.color.THECOLORS
context = None


class Context(object):
    def __init__(self, screen, clock, tile_size, view_size, world_ratio):
        self.screen = screen
        self.clock = clock
        self.view_size = view_size
        self.tile_size = tile_size
        self.world_ratio = world_ratio

        # Where to start drawing from, for scrolling tiles correctly
        self.camera = (0, 0)
        self.screen_offset = (0, 0)
        window_size = screen.get_size()
        self.window_scaling = (window_size[0]/800, window_size[1]/600)

    def screen_coords(self, position):
        return ((position[0] - self.camera[0]) * self.world_ratio,
                (position[1] - self.camera[1]) * self.world_ratio)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pygame.display.flip()
        context.clock.tick(60)
        pygame.display.set_caption("Scoundrel FPS: %d" %\
                                   context.clock.get_fps())


def init(conf, *args):
    global context
    pygame.init()
    screen = pygame.display.set_mode((conf['width'], conf['height']),
                                      conf['mode_flags'])
    context = Context(screen, pygame.time.Clock(), *args)


def drawing_context():
    return context
