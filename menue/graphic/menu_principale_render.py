import pygame


def draw_menu_frame(screen, menu_background, buttons, button_rects, hover_state, hover_sound, leafs):
    screen.blit(menu_background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    updated_hover_state = {}

    for key in ("play", "option", "quit"):
        is_hovering = button_rects[key].collidepoint(mouse_pos)

        if is_hovering:
            screen.blit(buttons[f"{key}_hover"], button_rects[key].topleft)
            if not hover_state[key]:
                hover_sound.play()
            updated_hover_state[key] = True
        else:
            screen.blit(buttons[key], button_rects[key].topleft)
            updated_hover_state[key] = False

    for leaf in leafs:
        leaf.update()
    for leaf in leafs:
        leaf.draw(screen)

    return updated_hover_state
