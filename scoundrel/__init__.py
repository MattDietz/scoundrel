import pygame
import pygame.locals

import scoundrel.actor.player
import scoundrel.engine
import scoundrel.engine.context
from scoundrel import state_machine
import scoundrel.world


class StopExecution(Exception): pass


class Scoundrel(object):

    @classmethod
    def init(cls, conf):
        cls.context = scoundrel.engine.init(conf)
        cls.init_keymap(conf)
        player = scoundrel.actor.player.PlayerActor()
        cls.world = scoundrel.world.World(player)
        state_machine.playing()

    @classmethod
    def init_keymap(cls, conf):
        cls.keymap = {
            pygame.locals.K_LEFT: cls.key_left,
            pygame.locals.K_RIGHT: cls.key_right,
            pygame.locals.K_UP: cls.key_up,
            pygame.locals.K_DOWN: cls.key_down}

    @classmethod
    def key_left(cls):
        print "Left"

    @classmethod
    def key_right(cls):
        print "Right"

    @classmethod
    def key_up(cls):
        print "Up"

    @classmethod
    def key_down(cls):
        print "Down"

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
        scoundrel.engine.begin_draw(cls.context)
        cls.context.screen.fill(scoundrel.engine.colors['black'])
        for i in xrange(20):
            for j in xrange(40):
                rect = pygame.Rect(j*30, i*30, 20, 20)
                pygame.draw.rect(cls.context.screen,
                                 scoundrel.engine.colors['green'],
                                 rect)
        scoundrel.engine.end_draw(cls.context)

    @classmethod
    def play(cls):
        while True:
            #cls.play_audio()
            cls.draw()
            cls.handle_events()
            #cls.ai()
            
