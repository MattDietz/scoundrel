import pygame

import scoundrel.actor.base
import scoundrel.context

class PlayerActor(scoundrel.actor.base.Actor):
    def draw(self, context):
        """
        Draws the player pip at the specified location, mapping from
        world coordinates to screen coordinates
        """

        pygame.draw.circle(context.screen, scoundrel.context.colors['red'],
                           context.screen_coords(self.position), 15)
