import random
import time

import pygame
import pygame.locals

import scoundrel.actor.player
import scoundrel.engine
import scoundrel.world


class StopExecution(Exception): pass


def make_map(width, height):
    global game_map
    for i in xrange(height):
        game_map.append([])
        for j in xrange(width):
            game_map[i].append(random.randint(0, 5))

map_size = (100, 100)
game_map = []

timer = None
ticks = 0
move_increment = 1

class Scoundrel(object):

    def __init__(self, conf):
        make_map(map_size[0], map_size[1])

        pygame.init()
        screen = pygame.display.set_mode((conf['width'], conf['height']),
                                      conf['mode_flags'])
        self.init_keymap(conf)
        player = scoundrel.actor.player.PlayerActor([10, 10])
        self.world = scoundrel.world.World(player)
        for k in ["width", "height", "mode_flags", "scroll_percentage"]:
            conf.pop(k)
        conf["view"] = (0, 0)

        self.context = scoundrel.engine.Context(screen,
                                                pygame.time.Clock(),
                                                **conf)

        # Default values weren't working on a mac
        pygame.key.set_repeat(10, 10)

    def init_keymap(self, conf):
        self.keymap = {
            pygame.locals.K_LEFT: self.key_arrow_left,
            pygame.locals.K_RIGHT: self.key_arrow_right,
            pygame.locals.K_UP: self.key_arrow_up,
            pygame.locals.K_DOWN: self.key_arrow_down,
            pygame.locals.K_ESCAPE: self.quit}

    #TODO(cerberus): un-harcode the movement
    def key_arrow_left(self, ctxt):
        view = ctxt.view
        offset = ctxt.screen_offset
        camera = ctxt.camera
        player = self.world.player
        player.position[0] -= move_increment

        # Scroll?
        sx = (player.position[0] - camera[0]) * ctxt.world_ratio
        if sx <= 0.35 * ctxt.screen.get_size()[0]:
            ctxt.screen_offset = (offset[0] + move_increment
                                  * ctxt.world_ratio, offset[1])
            ctxt.camera = (camera[0] - move_increment, camera[1])

        # should we move the view?
        if ctxt.tile_size - offset[0] == 0:
            ctxt.view = (view[0] - 1, view[1])
            ctxt.screen_offset = (0, offset[1])

    def key_arrow_right(self, ctxt):
        view = ctxt.view
        player = self.world.player
        player.position[0] += move_increment
        offset = ctxt.screen_offset
        camera = ctxt.camera

        # Scroll?
        sx = (player.position[0] - camera[0]) * ctxt.world_ratio
        if sx >= 0.65 * ctxt.screen.get_size()[0]:
            ctxt.screen_offset = \
                        (offset[0] - move_increment * ctxt.world_ratio,
                         offset[1])
            ctxt.camera = (camera[0] + move_increment, camera[1])

        # should we move the view?
        if ctxt.tile_size + offset[0] == 0:
            ctxt.view = (view[0] + 1, view[1])
            ctxt.screen_offset = (0, offset[1])

    def key_arrow_up(self, ctxt):
        view = ctxt.view
        player = self.world.player
        offset = ctxt.screen_offset
        camera = ctxt.camera
        player = self.world.player
        player.position[1] -= move_increment

        # Scroll?
        sy = (player.position[1] - camera[1]) * ctxt.world_ratio
        if sy <= 0.20 * ctxt.screen.get_size()[1]:
            ctxt.screen_offset = \
                        (offset[0], offset[1] + move_increment *
                         ctxt.world_ratio)
            ctxt.camera = (camera[0], camera[1] - move_increment)

        # should we move the view?
        if ctxt.tile_size + offset[1] == 0:
            ctxt.view = (view[0], view[1] + 1)
            ctxt.screen_offset = (offset[0], 0)

    def key_arrow_down(self, ctxt):
        view = ctxt.view
        player = self.world.player
        offset = ctxt.screen_offset
        camera = ctxt.camera
        player = self.world.player
        player.position[1] += move_increment

        # Scroll?
        sy = (player.position[1] - camera[1]) * ctxt.world_ratio
        if sy >= 0.80 * ctxt.screen.get_size()[1]:
            ctxt.screen_offset = \
                        (offset[0], offset[1] - move_increment *
                         ctxt.world_ratio)
            ctxt.camera = (camera[0], camera[1] + move_increment)

        # should we move the view?
        if ctxt.tile_size + offset[1] == 0:
            ctxt.view = (view[0], view[1] + 1)
            ctxt.screen_offset = (offset[0], 0)

    def quit(self):
        raise StopExecution()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                raise StopExecution()
            if event.type == pygame.locals.KEYDOWN:
                handler = self.keymap.get(event.key)
                if handler:
                    handler(self.context)

    def draw(self):
        """
        Concepts:

        world - actual data from the world. Represented in game units
        map_view - how much of the world we're showing, in tiles
        camera - Offset to start drawing from in world coordinates Facilitates
                 scrolling
        display - the GUI viewport. The view is scaled to this. Always a bit
                  smaller than the actual map view we're drawing
                  Represented in pixels

        The display should always show the same amount of information,
        regardless of window size, so we need to scale to that size
        """

        #NOTE(mdietz): There's probably a window resized event we can catch
        #              so we should adjust the scaling numbers there
        with self.context as ctxt:
            ctxt.screen.fill(scoundrel.engine.colors['black'])
            e = scoundrel.engine.colors
            colors = [e["green"], e["gray"], e["blue"], e["white"],
                      e["yellow"], e["brown"]]
            for x in xrange(0, ctxt.view_size[0]+1):
                for y in xrange(0, ctxt.view_size[1]+1):
                    s_x = (x * ctxt.window_scaling[0] *
                                ctxt.tile_size + ctxt.screen_offset[0]
                                - ctxt.tile_size)
                    s_y = (y * ctxt.window_scaling[1] *
                                ctxt.tile_size + ctxt.screen_offset[1]
                                - ctxt.tile_size)
                    s_w = ctxt.tile_size * ctxt.window_scaling[0]
                    s_h = ctxt.tile_size * ctxt.window_scaling[1]
                    m_x = x + ctxt.view[0]
                    m_y = y + ctxt.view[1]
                    if m_x >= map_size[0] or m_y >= map_size[1]:
                        break
                    if m_x < 0 or m_y < 0:
                        break
                    rect = pygame.Rect(s_x, s_y, s_w, s_h)
                    pygame.draw.rect(ctxt.screen, colors[game_map[m_x][m_y]],
                                     rect)
            self.world.draw(ctxt)

    def play(self):
        while True:
            #self.play_audio()
            self.draw()
            self.handle_events()
            #self.ai()
