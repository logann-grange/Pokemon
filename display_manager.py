import pygame


_screen = None
_size = (1080, 720)


def get_screen(caption="Pokemon", size=(1080, 720)):
    global _screen, _size

    if not pygame.get_init():
        pygame.init()
    if not pygame.display.get_init():
        pygame.display.init()

    if _screen is None or _size != size:
        _screen = pygame.display.set_mode(size)
        _size = size

    pygame.display.set_caption(caption)
    return _screen
