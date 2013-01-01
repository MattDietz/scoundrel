import scoundrel.engine

class World(object):
    def __init__(self, player, conf):
        self.actors = []

        # the player is an actor, but still a special one
        self.player = player
        self.actors.append(player)
        self.conf = conf

    def step(self, count=1):
        pass

    def draw(self, context):
        for actor in self.actors:
            actor.draw(context)
