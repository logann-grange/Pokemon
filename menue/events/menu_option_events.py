import pygame


def handle_menu_option_event(event, rects, options, button_return_rect):
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return False, False

    has_changed = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if rects["minus_music"].collidepoint(event.pos):
            options["music_volume"] = round(max(0.0, options["music_volume"] - 0.1), 1)
            has_changed = True
        elif rects["plus_music"].collidepoint(event.pos):
            options["music_volume"] = round(min(1.0, options["music_volume"] + 0.1), 1)
            has_changed = True
        elif rects["minus_sfx"].collidepoint(event.pos):
            options["sfx_volume"] = round(max(0.0, options["sfx_volume"] - 0.1), 1)
            has_changed = True
        elif rects["plus_sfx"].collidepoint(event.pos):
            options["sfx_volume"] = round(min(1.0, options["sfx_volume"] + 0.1), 1)
            has_changed = True
        elif rects["mute"].collidepoint(event.pos):
            options["mute"] = not options["mute"]
            has_changed = True
        elif button_return_rect.collidepoint(event.pos):
            return False, False

    return True, has_changed
