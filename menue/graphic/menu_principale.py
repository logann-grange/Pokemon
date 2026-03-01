import os
import sys
import pygame

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
os.chdir(project_root)

from menue.graphic.menu_choix_jeu import menu_choix_jeu
from menue.graphic import menu_option
from menue.graphic.Feuille import init_leafs
from menue.events.menu_principale_events import handle_menu_event
from menue.graphic.menu_principale_render import draw_menu_frame
from game.graphic.display_manager import get_screen

def main():
    screen = get_screen("Pokemon")

    menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
    button_play = pygame.image.load("./Asset/menue/Jouer.png")
    button_play_hover = pygame.image.load("./Asset/menue/Jouer_hover.png")
    button_option = pygame.image.load("./Asset/menue/Option.png")
    button_option_hover = pygame.image.load("./Asset/menue/Option_hover.png")
    button_quit = pygame.image.load("./Asset/menue/Quitter.png")
    button_quit_hover = pygame.image.load("./Asset/menue/Quitter_hover.png")
    leaf = pygame.image.load("./Asset/menue/leaf.png")
    clock = pygame.time.Clock()
    leafs = init_leafs(leaf, 20)

    pygame.mixer.music.load("./Asset/menue/menu_music.mp3")
    pygame.mixer.music.play(-1)
    hover_sound = pygame.mixer.Sound("./Asset/menue/hover.mp3")
    saved_audio = menu_option.load_audio_options()
    menu_option.apply_audio_options(saved_audio)
    _, sfx_volume = menu_option.get_effective_volumes(saved_audio)
    hover_sound.set_volume(sfx_volume)

    buttons = {
        "play": button_play,
        "play_hover": button_play_hover,
        "option": button_option,
        "option_hover": button_option_hover,
        "quit": button_quit,
        "quit_hover": button_quit_hover,
    }

    button_rects = {
        "play": button_play.get_rect(topleft=(390, 250)),
        "option": button_option.get_rect(topleft=(390, 375)),
        "quit": button_quit.get_rect(topleft=(390, 500)),
    }

    hover_state = {"play": False, "option": False, "quit": False}

    running = True
    while running:
        for event in pygame.event.get():
            running = handle_menu_event(event, button_rects, screen, hover_sound) and running

        hover_state = draw_menu_frame(
            screen,
            menu_background,
            buttons,
            button_rects,
            hover_state,
            hover_sound,
            leafs,
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()