import random
import time

import pygame
import pygame.image
import pygame.locals

import scoundrel.actor.player
import scoundrel.context
import scoundrel.world


class StopExecution(Exception): pass


def make_map(width, height):
    global game_map
    for i in xrange(height):
        game_map.append([])
        for j in xrange(width):
            game_map[i].append(1)

map_size = (100, 100)
game_map = []

move_increment = 2

class Scoundrel(object):

    def __init__(self, conf):
        make_map(map_size[0], map_size[1])
        pygame.init()
        screen = pygame.display.set_mode((conf['width'], conf['height']),
                                      conf['mode_flags'])
        self.init_keymap(conf)
        player = scoundrel.actor.player.PlayerActor([10, 10],
                                                    "content/zombie.png")
        self.world = scoundrel.world.World(player)
        conf["view"] = (0, 0)

        self.context = scoundrel.context.Context(screen,
                                                 pygame.time.Clock(),
                                                 **conf)
        self.images = [self.load_image("content/grass_32.png"),
                       self.load_image("content/heart32.png")]

        # Default values weren't working on a mac
        pygame.key.set_repeat(30, 30)

    def load_image(self, path):
        img = pygame.image.load(path).convert()
        return img

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
        if sx <= ctxt.slack[0] * ctxt.screen.get_size()[0]:
            ctxt.screen_offset = (offset[0] + move_increment
                                  * ctxt.world_ratio, offset[1])
            ctxt.camera = (camera[0] - move_increment, camera[1])

        # should we move the view?
        if ctxt.tile_size - offset[0] == 0:
            ctxt.view = (view[0] - 1, view[1])
            ctxt.screen_offset = (0, offset[1])

    def key_arrow_right(self, ctxt):
        view = ctxt.view
        offset = ctxt.screen_offset
        camera = ctxt.camera

        player = self.world.player
        player.position[0] += move_increment

        # Scroll?
        # if player is at or greater than x% from the edge, scroll
        sx = (player.position[0] - camera[0]) * ctxt.world_ratio
        if sx >= (1 - ctxt.slack[0]) * ctxt.screen.get_size()[0]:
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
        if sy <= ctxt.slack[1] * ctxt.screen.get_size()[1]:
            ctxt.screen_offset = \
                        (offset[0], offset[1] + move_increment *
                         ctxt.world_ratio)
            ctxt.camera = (camera[0], camera[1] - move_increment)

        # should we move the view?
        if ctxt.tile_size - offset[1] == 0:
            ctxt.view = (view[0], view[1] - 1)
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
        if sy >= (1 - ctxt.slack[1]) * ctxt.screen.get_size()[1]:
            ctxt.screen_offset = \
                        (offset[0], offset[1] - move_increment *
                         ctxt.world_ratio)
            ctxt.camera = (camera[0], camera[1] + move_increment)

        # should we move the view?
        if ctxt.tile_size + offset[1] == 0:
            ctxt.view = (view[0], view[1] + 1)
            ctxt.screen_offset = (offset[0], 0)

    def quit(self, key):
        raise StopExecution()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                raise StopExecution()
            if event.type == pygame.locals.KEYDOWN:
                keys = pygame.key.get_pressed()
                for key in self.keymap.keys():
                    if keys[key]:
                        self.keymap[key](self.context)
        pygame.event.pump()

    def draw(self):
        #NOTE(mdietz): There's probably a window resized event we can catch
        #              so we should adjust the scaling numbers there
        with self.context as ctxt:
            ctxt.screen.fill(scoundrel.context.colors['black'])
            for x in xrange(-1, ctxt.view_size[0]+1):
                for y in xrange(-1, ctxt.view_size[1]+1):
                    # Screen projection
                    s_x = (x * ctxt.window_scaling[0] *
                           ctxt.tile_size + ctxt.screen_offset[0])
                    s_y = (y * ctxt.window_scaling[1] *
                           ctxt.tile_size + ctxt.screen_offset[1])

                    # Scaled tile dimensions
                    s_w = ctxt.tile_size * ctxt.window_scaling[0]
                    s_h = ctxt.tile_size * ctxt.window_scaling[1]

                    # Map Indices
                    m_x = x + ctxt.view[0]
                    m_y = y + ctxt.view[1]

                    # Don't go array oob
                    if m_x >= map_size[0] - 1 or m_y >= map_size[1] - 1:
                        continue
                    if m_x < 0 or m_y < 0:
                        continue

                    rect = pygame.Rect(s_x, s_y, s_w, s_h)
                    if game_map[m_x][m_y]:
                        ctxt.screen.blit(self.images[0], rect)
                    else:
                        pygame.draw.rect(ctxt.screen,
                            scoundrel.context.colors["green"], rect, 2)
            self.world.draw(ctxt)

            # Trying out heart display
            for j in xrange(0, 2):
                for k in xrange(0, 8):
                    rect = pygame.Rect(k * 32 + 500, j * 32 + 10, 32, 32)
                    ctxt.screen.blit(self.images[1], rect)

    def play(self):
        try:
            while True:
                #self.play_audio()
                self.draw()
                self.handle_events()
                #self.ai()
        except scoundrel.StopExecution:
            pass
