import json
import random
import time

import pygame
import pygame.image
import pygame.locals

import scoundrel.actor.player
import scoundrel.context
import scoundrel.log
import scoundrel.registry
import scoundrel.registry.loader
import scoundrel.world

LOG = scoundrel.log.LOG


class StopExecution(Exception): pass


def load_map(path):
    global map_width, map_height
    with open(path) as map_file:
        metadata, map_data = map_file.read().split("\n")

        metadata = metadata.split(',')
        map_width = int(metadata[0])
        map_height = int(metadata[1])

        map_data = map_data.split(',')
        for i in xrange(map_height):
            game_map.append([])
            for j in xrange(map_width):
                offset = i * map_width + j

                # XOR with 1. Map gen produces 0s for open and 1 for blocked
                cell = int(map_data[offset]) ^ 1
                game_map[i].append(cell)


def make_map(width, height):
    global game_map
    for i in xrange(height):
        game_map.append([])
        for j in xrange(width):
            game_map[i].append(1)


def load_resources(registry, path):
    with open(path) as resource_file:
        resource_blob = json.load(resource_file)

    for key, resource_meta in resource_blob.items():
        loader_key = "load_%s" % resource_meta["type"]
        resource_loader = getattr(scoundrel.registry.loader, loader_key, None)
        if resource_loader:
            new_resource = resource_loader(key, resource_meta)
            registry.add(new_resource)
            LOG.debug("Loaded '%s' of type '%s'" % (key,
                                                    resource_meta["type"]))
        else:
            LOG.error("No loader found for type %s" % resource_meta["type"])


map_width, map_height = 100, 100
game_map = []
move_increment = 2


class Scoundrel(object):
    def __init__(self, conf):
        scoundrel.log.setup_logging()
        LOG.debug("Initializing Scoundrel...")

        self._registry = scoundrel.registry.Registry()
        load_map("output.txt")
        LOG.debug("Map loaded")
        pygame.init()
        screen = pygame.display.set_mode((conf['width'], conf['height']),
                                      conf['mode_flags'])
        self.init_keymap(conf)
        # TODO(mdietz): should be callable by the implementing game, later,
        #               with maps and resource paths

        load_resources(self._registry, "resources.json")
        player = scoundrel.actor.player.PlayerActor([10, 10],
                                                    "content/player.png")
        self.world = scoundrel.world.World(player)
        conf["view"] = (0, 0)

        self.context = scoundrel.context.Context(screen,
                                                 pygame.time.Clock(),
                                                 **conf)
        self.images = [self._registry.get_named("grass")._data]

        self.images.extend(self._split_tilesheet(32, "content/tile_sheet.png"))

        # Default values weren't working on a mac
        pygame.key.set_repeat(30, 30)

    def _split_tilesheet(self, tile_size, path):
        # TODO(mdietz): implement metadata for tile properties and bounds
        # TODO(mdietz): redo this so we can pass references and blit from one
        #               loaded surface

        img = pygame.image.load(path)
        surface = img.convert()
        width = surface.get_width()
        height = surface.get_height()
        offset_x, offset_y = 0, 0
        loaded_surfaces = []
        while offset_y < height:
            img_rect = pygame.Rect(offset_x, offset_y, tile_size, tile_size)
            s = pygame.Surface((tile_size, tile_size))
            s.blit(surface, (0, 0), area=img_rect)
            loaded_surfaces.append(s)
            offset_x += tile_size
            if offset_x > width:
                offset_x = 0
                offset_y += tile_size

        return loaded_surfaces



    def load_image(self, path, alpha=False):
        if alpha:
            img = pygame.image.load(path).convert_alpha()
        else:
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
        with self.context as (ctxt, last_frame):
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
                    if m_x >= map_width - 1 or m_y >= map_height - 1:
                        continue
                    if m_x < 0 or m_y < 0:
                        continue

                    rect = pygame.Rect(s_x, s_y, s_w, s_h)
                    if game_map[m_x][m_y]:
                        ctxt.screen.blit(self.images[0], rect)
                    else:
                        pygame.draw.rect(ctxt.screen,
                            scoundrel.context.colors["green"], rect, 2)
            # offset_x = 0
            # for img in self.images:
            #     rect = pygame.Rect(offset_x, 0, 32, 32)
            #     ctxt.screen.blit(img, rect)
            #     offset_x += 32

            self.world.draw(ctxt)

            # Trying out heart display
            # for j in xrange(0, 2):
            #     for k in xrange(0, 8):
            #         rect = pygame.Rect(k * 32 + 500, j * 32 + 10, 32, 32)
            #         ctxt.screen.blit(self.images[1], rect)

    def play(self):
        # Tick a frame once so the frame time looks appropriate
        with self.context:
            pass

        try:
            while True:
                #self.play_audio()
                self.draw()
                self.handle_events()
                #self.ai()
        except scoundrel.StopExecution:
            pass
