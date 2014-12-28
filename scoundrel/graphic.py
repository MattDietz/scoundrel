class Graphic(object):
    """An element to be displayed to the screen.

    Differs from pygame Surfaces in that it represents a reference and
    rectangular area to be drawn from said reference. Employed as a means
    of keeping all relevant data in the central resource registry rather
    than directly instantiated by the engine objects.

    At this time, I don't forsee Graphic objects being used directly in the
    game so much as owned by other game and engine parent objects.
    """
    def __init__(self, image, rect):
        self._image = image
        self._rect = rect
        self._kwargs = {"area": rect}

    def draw(self, context, position):
        context.screen.blit(self._image, position, **self._kwargs)
