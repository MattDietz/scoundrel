class World(object):
    def __init__(self, player):
        self.actors = []

        # the player is an actor, but still a special one
        self.player = player
        self.actors.append(player)

    def draw(self, context):
        for actor in self.actors:
            actor.draw(context)
