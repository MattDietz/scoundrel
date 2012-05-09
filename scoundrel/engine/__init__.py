import pygame

import scoundrel.engine.context


colors = pygame.color.THECOLORS


def init(conf):
    pygame.init()
    context = scoundrel.engine.context.Context()
    context.screen = pygame.display.set_mode((conf['width'],
                                                  conf['height']),
                                                 conf['mode_flags'])
    context.clock = pygame.time.Clock()
    return context

def begin_draw(context):
    pass

def end_draw(context):
    pygame.display.flip()
    context.clock.tick(60)
    pygame.display.set_caption("Scoundrel FPS: %d" %\
                                    context.clock.get_fps())
