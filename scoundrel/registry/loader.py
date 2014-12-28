import pygame.image

from scoundrel.registry import resource


def load_image(name, resource_meta):
    path = resource_meta["path"]
    alpha = resource_meta.get("alpha")
    if alpha:
        img = pygame.image.load(path).convert_alpha()
    else:
        img = pygame.image.load(path).convert()

    # TODO(mdietz): update to include resource type if decided later
    res = resource.Resource(name, img, resource_meta["tags"])
    return res
