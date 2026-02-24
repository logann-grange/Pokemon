import pygame


def draw_menu_option_frame(
    screen,
    menu_background,
    leafs,
    font_title,
    font_text,
    options,
    rects,
    button_return,
    button_return_hover,
    button_return_rect,
    prev_hover_return,
    hover_sound,
):
    mouse_pos = pygame.mouse.get_pos()

    screen.blit(menu_background, (0, 0))

    for flake in leafs:
        flake.update()
    for flake in leafs:
        flake.draw(screen)

    title_surface = font_title.render("Options Audio", True, (255, 255, 255))
    screen.blit(title_surface, (390, 150))

    pygame.draw.rect(screen, (35, 35, 35), rects["minus_music"], border_radius=8)
    pygame.draw.rect(screen, (35, 35, 35), rects["plus_music"], border_radius=8)
    pygame.draw.rect(screen, (35, 35, 35), rects["minus_sfx"], border_radius=8)
    pygame.draw.rect(screen, (35, 35, 35), rects["plus_sfx"], border_radius=8)
    pygame.draw.rect(screen, (35, 35, 35), rects["mute"], border_radius=8)

    music_text = font_text.render(f"Musique: {int(options['music_volume'] * 100)}%", True, (255, 255, 255))
    sfx_text = font_text.render(f"Effets: {int(options['sfx_volume'] * 100)}%", True, (255, 255, 255))
    mute_state = "ON" if options["mute"] else "OFF"
    mute_text = font_text.render(f"Mute: {mute_state}", True, (255, 255, 255))

    minus_text = font_text.render("-", True, (255, 255, 255))
    plus_text = font_text.render("+", True, (255, 255, 255))

    screen.blit(music_text, (430, 270))
    screen.blit(sfx_text, (430, 360))
    screen.blit(mute_text, (500, 465))
    screen.blit(minus_text, (385, 268))
    screen.blit(plus_text, (683, 268))
    screen.blit(minus_text, (385, 358))
    screen.blit(plus_text, (683, 358))

    if button_return_rect.collidepoint(mouse_pos):
        screen.blit(button_return_hover, button_return_rect.topleft)
        if not prev_hover_return:
            hover_sound.play()
        return True

    screen.blit(button_return, button_return_rect.topleft)
    return False
