import pygame
from menue.graphic.menu_choix_jeu import menu_choix_jeu
from menue.graphic import menu_option


def handle_menu_event(event, button_rects, screen, hover_sound):
    running = True

    if event.type == pygame.QUIT:
        return False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_rects["play"].collidepoint(event.pos):
            menu_choix_jeu()

        if button_rects["option"].collidepoint(event.pos):
            options = menu_option.menu_option(screen)
            menu_option.apply_audio_options(options)
            _, sfx_volume = menu_option.get_effective_volumes(options)
            hover_sound.set_volume(sfx_volume)

        if button_rects["quit"].collidepoint(event.pos):
            running = False

    return running
