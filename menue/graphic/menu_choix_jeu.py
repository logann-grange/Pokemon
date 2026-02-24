import os
import sys
import pygame

# Ajouter la racine du projet au path pour les imports absolus
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
os.chdir(project_root)

from menue.graphic.Feuille import init_leafs
from menue.graphic import menu_option
from menue.events.menu_choix_jeu_events import handle_menu_choix_event
from menue.graphic.menu_choix_jeu_render import draw_menu_choix_frame
from display_manager import get_screen

screen = get_screen("Menu Choix Jeu")
clock = pygame.time.Clock()

menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
button_new_game = pygame.image.load("./Asset/menue/nouvelle_partie_.png")
button_new_game_hover = pygame.image.load("./Asset/menue/nouvelle_partie_hover.png")
button_load_game = pygame.image.load("./Asset/menue/charger_partie.png")
button_load_game_hover = pygame.image.load("./Asset/menue/charger_partie_hover.png")
button_pokedex = pygame.image.load("./Asset/menue/button_pokedex.png")
button_pokedex_hover = pygame.image.load("./Asset/menue/button_pokedex_hover.png")
leaf = pygame.image.load("./Asset/menue/leaf.png")
leafs = init_leafs(leaf, 20)
hover_sound = pygame.mixer.Sound("./Asset/menue/hover.mp3")
button_return = pygame.image.load("./Asset/menue/button_return.png")
button_return_hover = pygame.image.load("./Asset/menue/button_return_hover.png")

# Variables pour tracker l'etat de hover precedent
def menu_choix_jeu():
    audio_options = menu_option.load_audio_options()
    menu_option.apply_audio_options(audio_options)
    _, sfx_volume = menu_option.get_effective_volumes(audio_options)
    hover_sound.set_volume(sfx_volume)

    buttons = {
        "new_game": button_new_game,
        "new_game_hover": button_new_game_hover,
        "load_game": button_load_game,
        "load_game_hover": button_load_game_hover,
        "pokedex": button_pokedex,
        "pokedex_hover": button_pokedex_hover,
        "return": button_return,
        "return_hover": button_return_hover,
    }

    button_rects = {
        "new_game": button_new_game.get_rect(topleft=(390, 250)),
        "load_game": button_load_game.get_rect(topleft=(390, 380)),
        "pokedex": button_pokedex.get_rect(topleft=(390, 510)),
        "return": button_return.get_rect(topleft=(40, 30)),
    }

    hover_state = {
        "new_game": False,
        "load_game": False,
        "pokedex": False,
        "return": False,
    }

    running = True
    while running:
        for event in pygame.event.get():
            running, action = handle_menu_choix_event(event, button_rects, screen)
            if action == "start_game":
                return

        hover_state = draw_menu_choix_frame(
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