import pygame

import scoundrel.engine

class World(object):
    def __init__(self, player, conf):
        self.actors = []

        # the player is an actor, but still a special one
        self.player = player
        self.conf = conf

    def step(self, count=1):
        pass

    def draw(self, context):
        #TODO(cerberus): un-hardcode the radius, store the tile width elsewhere
        pygame.draw.circle(context.screen, scoundrel.engine.colors['red'],
                           self.player.position, 15)
