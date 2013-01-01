import pygame
import pygame.locals

import scoundrel.actor.player
import scoundrel.engine
import scoundrel.world


class StopExecution(Exception): pass


class Scoundrel(object):

    def __init__(self, conf):
        scoundrel.engine.init(conf)
        self.init_keymap(conf)
        player = scoundrel.actor.player.PlayerActor([15, 15])
        self.world = scoundrel.world.World(player, conf)

        # Default values weren't working on a mac
        pygame.key.set_repeat(100, 50)

    def init_keymap(self, conf):
        self.keymap = {
            pygame.locals.K_LEFT: self.key_arrow_left,
            pygame.locals.K_RIGHT: self.key_arrow_right,
            pygame.locals.K_UP: self.key_arrow_up,
            pygame.locals.K_DOWN: self.key_arrow_down,
            pygame.locals.K_ESCAPE: self.quit}

    #TODO(cerberus): un-harcode the movement
    def key_arrow_left(self):
        player = self.world.player
        player.position[0] -= 15
        if player.position[0] < 15:
            player.position[0] = 15

    def key_arrow_right(self):
        player = self.world.player
        player.position[0] += 15
        if player.position[0] > self.world.conf['width']-15:
            player.position[0] = self.world.conf['width']-15

    def key_arrow_up(self):
        player = self.world.player
        player.position[1] -= 15
        if player.position[1] < 15:
            player.position[1] = 15

    def key_arrow_down(self):
        player = self.world.player
        player.position[1] += 15
        if player.position[1] > self.world.conf['height']-15:
            player.position[1] = self.world.conf['height']-15

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
            self.world.draw(context)

    def play(self):
        while True:
            #self.play_audio()
            self.draw()
            self.handle_events()
            #self.ai()
