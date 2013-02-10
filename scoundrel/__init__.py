import random

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

# Where to start drawing the map data
view = (0, 0)

# See below, but two columns and rows of tiles extra for scrolling
map_size = (100, 100)
view_size = (27,20)
tile_size = 32
game_map = []
move_increment = 2
world_ratio = 8

class Scoundrel(object):

    def __init__(self, conf):
        make_map(map_size[0], map_size[1])
        scoundrel.engine.init(conf, tile_size, view_size, world_ratio)
        self.init_keymap(conf)
        player = scoundrel.actor.player.PlayerActor([10, 10])
        self.world = scoundrel.world.World(player, conf)

        # Default values weren't working on a mac
        pygame.key.set_repeat(100, 50)

        # NOTE(mdietz): for now, going to say 1 in game unit is 4 player
        #               steps across a single standard tile.
        #               Let's say we want to show 25x18 tiles max, so we're
        #               designing the game for 800x600

    def init_keymap(self, conf):
        self.keymap = {
            pygame.locals.K_LEFT: self.key_arrow_left,
            pygame.locals.K_RIGHT: self.key_arrow_right,
            pygame.locals.K_UP: self.key_arrow_up,
            pygame.locals.K_DOWN: self.key_arrow_down,
            pygame.locals.K_ESCAPE: self.quit}

    #TODO(cerberus): un-harcode the movement
    def key_arrow_left(self):
        global view
        ctxt = scoundrel.engine.context
        offset = ctxt.screen_offset
        camera = ctxt.camera
        player = self.world.player
        player.position[0] -= move_increment

        # Scroll?
        sx = (player.position[0] - camera[0]) * world_ratio
        if sx <= 0.35 * scoundrel.engine.context.screen.get_size()[0]:
            scoundrel.engine.context.screen_offset = \
                        (offset[0] + move_increment * world_ratio, offset[1])
            ctxt.camera = (camera[0] - move_increment, camera[1])

        # should we move the view?
        if tile_size - offset[0] == 0:
            view = (view[0] - 1, view[1])
            scoundrel.engine.context.screen_offset = (0, offset[1])

        if player.position[0] < move_increment:
            player.position[0] = move_increment

    def key_arrow_right(self):
        global view
        player = self.world.player
        player.position[0] += move_increment
        ctxt = scoundrel.engine.context
        offset = ctxt.screen_offset
        camera = ctxt.camera

        # Scroll?
        sx = (player.position[0] - camera[0]) * world_ratio
        if sx >= 0.65 * scoundrel.engine.context.screen.get_size()[0]:
            scoundrel.engine.context.screen_offset = \
                        (offset[0] - move_increment * world_ratio, offset[1])
            ctxt.camera = (camera[0] + move_increment, camera[1])

        # should we move the view?
        if tile_size + offset[0] == 0:
            view = (view[0] + 1, view[1])
            scoundrel.engine.context.screen_offset = (0, offset[1])

        if player.position[0] > self.world.conf['width']-move_increment:
            player.position[0] = self.world.conf['width']-move_increment

    def key_arrow_up(self):
        player = self.world.player
        player.position[1] -= move_increment
        if player.position[1] < move_increment:
            player.position[1] = move_increment

    def key_arrow_down(self):
        player = self.world.player
        player.position[1] += move_increment
        if player.position[1] > self.world.conf['height']-move_increment:
            player.position[1] = self.world.conf['height']-move_increment

    def quit(self):
        raise StopExecution()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                raise StopExecution()
            if event.type == pygame.locals.KEYDOWN:
                handler = self.keymap.get(event.key, None)
                if handler:
                    self.keymap[event.key]()
                    self.world.step()

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
        with scoundrel.engine.drawing_context() as ctxt:
            ctxt.screen.fill(scoundrel.engine.colors['black'])
            e = scoundrel.engine.colors
            colors = [e["green"], e["gray"], e["blue"], e["white"],
                      e["yellow"], e["brown"]]
            for x in xrange(0, view_size[0]+1):
                for y in xrange(0, view_size[1]+1):
                    s_x = (x * ctxt.window_scaling[0] *
                                tile_size + ctxt.screen_offset[0] - tile_size)
                    s_y = (y * ctxt.window_scaling[1] *
                                tile_size + ctxt.screen_offset[1] - tile_size)
                    s_w = tile_size * ctxt.window_scaling[0]
                    s_h = tile_size * ctxt.window_scaling[1]
                    m_x = x + view[0]
                    m_y = y + view[1]
                    if m_x > len(game_map) or m_y > len(game_map[m_x]):
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
