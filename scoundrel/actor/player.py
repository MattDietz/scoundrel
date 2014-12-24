import pygame

import scoundrel.actor.base
import scoundrel.context


class PlayerActor(scoundrel.actor.base.Actor):
    def __init__(self, position, path):
        super(PlayerActor, self).__init__(position)
        self.img = pygame.image.load(path).convert_alpha()

    def draw(self, context):
        """
        Draws the player pip at the specified location, mapping from
        world coordinates to screen coordinates
        """
        screen_pos = context.screen_coords(self.position)
        rect = pygame.Rect(screen_pos[0], screen_pos[1], 32, 32)
        context.screen.blit(self.img, rect)
