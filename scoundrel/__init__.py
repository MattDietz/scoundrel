import pygame
import pygame.locals

import scoundrel.actor.player
import scoundrel.engine
from scoundrel import state_machine
import scoundrel.world


class StopExecution(Exception): pass


class Scoundrel(object):

    @classmethod
    def init(cls, conf):
        scoundrel.engine.init(conf)
        cls.init_keymap(conf)
        player = scoundrel.actor.player.PlayerActor([15, 15])
        cls.world = scoundrel.world.World(player, conf)

        # Default values weren't working on a mac
        pygame.key.set_repeat(100, 50)
        state_machine.playing()

    @classmethod
    def init_keymap(cls, conf):
        cls.keymap = {
            pygame.locals.K_LEFT: cls.key_arrow_left,
            pygame.locals.K_RIGHT: cls.key_arrow_right,
            pygame.locals.K_UP: cls.key_arrow_up,
            pygame.locals.K_DOWN: cls.key_arrow_down,
            pygame.locals.K_ESCAPE: cls.quit}

    #TODO(cerberus): un-harcode the movement
    @classmethod
    def key_arrow_left(cls):
        player = cls.world.player
        player.position[0] -= 15
        if player.position[0] < 15:
            player.position[0] = 15

    @classmethod
    def key_arrow_right(cls):
        player = cls.world.player
        player.position[0] += 15
        if player.position[0] > cls.world.conf['width']-15:
            player.position[0] = cls.world.conf['width']-15

    @classmethod
    def key_arrow_up(cls):
        player = cls.world.player
        player.position[1] -= 15
        if player.position[1] < 15:
            player.position[1] = 15

    @classmethod
    def key_arrow_down(cls):
        player = cls.world.player
        player.position[1] += 15
        if player.position[1] > cls.world.conf['height']-15:
            player.position[1] = cls.world.conf['height']-15

    @classmethod
    def quit(cls):
        raise StopExecution()

    @classmethod
    def handle_events(cls):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                raise StopExecution()
            if event.type == pygame.locals.KEYDOWN:
                handler = cls.keymap.get(event.key, None)
                if handler:
                    cls.keymap[event.key]()
                    if state_machine.state == state_machine.PLAYING:
                        cls.world.step()

    @classmethod
    def draw(cls):
        with scoundrel.engine.drawing_context() as context:
            context.screen.fill(scoundrel.engine.colors['black'])
            even = True
            for i in xrange(20):
                even = not even
                for j in xrange(40):
                    rect = pygame.Rect(j*30, i*30, 30, 30)
                    if even:
                        pygame.draw.rect(context.screen,
                                         scoundrel.engine.colors['green'],
                                         rect)
                    else:
                        pygame.draw.rect(context.screen,
                                         scoundrel.engine.colors['white'],
                                         rect)

                    even = not even
            cls.world.draw(context)

    @classmethod
    def play(cls):
        while True:
            #cls.play_audio()
            cls.draw()
            cls.handle_events()
            #cls.ai()
