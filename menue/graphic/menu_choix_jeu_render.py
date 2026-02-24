import pygame


def draw_menu_choix_frame(screen, menu_background, buttons, button_rects, hover_state, hover_sound, leafs):
    mouse_pos = pygame.mouse.get_pos()

    screen.blit(menu_background, (0, 0))

    for leaf in leafs:
        leaf.update()
    for leaf in leafs:
        leaf.draw(screen)

    updated_hover_state = {}
    for key in ("new_game", "load_game", "pokedex", "return"):
        is_hovering = button_rects[key].collidepoint(mouse_pos)

        if is_hovering:
            screen.blit(buttons[f"{key}_hover"], button_rects[key].topleft)
            if not hover_state[key]:
                hover_sound.play()
            updated_hover_state[key] = True
        else:
            screen.blit(buttons[key], button_rects[key].topleft)
            updated_hover_state[key] = False

    return updated_hover_state
