import pygame
import sys


def handle_post_evolution_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


def draw_post_evolution_frame(
    screen,
    background_apng_path,
    evolved_path,
    draw_animated_background,
    draw_animated_pokemon,
):
    draw_animated_background(screen, background_apng_path)

    if evolved_path:
        draw_animated_pokemon(screen, evolved_path, (540, 360), scale=3.0)
