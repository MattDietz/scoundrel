import pygame

import scoundrel.actor.base
import scoundrel.engine

class PlayerActor(scoundrel.actor.base.Actor):
    def draw(self, context):
        pygame.draw.circle(context.screen, scoundrel.engine.colors['red'],
                           self.position, 15)
