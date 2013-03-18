import pygame


colors = pygame.color.THECOLORS
context = None


class Context(object):
    def __init__(self, screen, clock, **kwargs):
        self.conf = kwargs
        self.screen = screen
        self.clock = clock
        self.slack = self._setup_scrolls(self.conf)

        # Where to start drawing from, for scrolling tiles correctly
        self.view = kwargs["view"]
        self.view_size = kwargs["view_size"]
        self.tile_size = kwargs["tile_size"]
        self.world_ratio = kwargs["world_ratio"]
        self.camera = (-40, -20)
        self.screen_offset = (0, 0)
        window_size = screen.get_size()
        self.window_scaling = (window_size[0] / 800, window_size[1] / 600)

    def _setup_scrolls(self, conf):
        slack_x, slack_y = 0, 0
        if conf["slack"] > conf["width"]:
            slack_y = conf["slack"]
            slack_x = (conf["height"] * slack_y) / conf["width"]
        else:
            slack_x = conf["slack"]
            slack_y = (conf["width"] * slack_x) / conf["height"]
        return slack_x, slack_y

    def screen_coords(self, position):
        return ((position[0] - self.camera[0]) * self.world_ratio,
                (position[1] - self.camera[1]) * self.world_ratio)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pygame.display.flip()
        self.clock.tick(60)
        self.view_ext = (self.view[0] + self.view_size[0],
                         self.view[1] + self.view_size[1])
        pygame.display.set_caption(
            "Scoundrel FPS: %d View: %s - %s Camera: %s Offset %s" %
                (self.clock.get_fps(), self.view, self.view_ext, self.camera,
                 self.screen_offset))
