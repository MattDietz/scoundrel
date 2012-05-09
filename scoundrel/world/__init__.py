class World(object):
    def __init__(self, player):
        self.actors = []

        # the player is an actor, but still a special one
        self.player = player

    def step(self, count=1):
        print "World step"
