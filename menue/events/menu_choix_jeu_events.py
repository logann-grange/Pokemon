import json
import os
import pygame
from game.choix_premier_pokemon import lancer_choix_pokemon
from game.graphic.game import run_game
from Pokedex.graphic.interface_pokedex import afficher_interface_pokedex

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

def handle_menu_choix_event(event, button_rects, screen):
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return False, None

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_rects["new_game"].collidepoint(event.pos):
            equipe_file = os.path.join(PROJECT_ROOT, "data", "equipe.json")
            with open(equipe_file, "w") as file:
                json.dump([], file)

            pokedex_file = os.path.join(PROJECT_ROOT, "data", "pokedex.json")
            with open(pokedex_file, "r") as file:
                pokedex_data = json.load(file)
                for pokemon in pokedex_data:
                    pokemon["hidden"] = True

            with open(pokedex_file, "w") as file:
                json.dump(pokedex_data, file, indent=4, ensure_ascii=False)

            lancer_choix_pokemon()
            return False, "start_game"

        if button_rects["load_game"].collidepoint(event.pos):
            print("Charger partie sélectionnée")
            run_game(load_saved=True)
        if button_rects["pokedex"].collidepoint(event.pos):
            afficher_interface_pokedex(screen.copy())

        if button_rects["return"].collidepoint(event.pos):
            return False, None

    return True, None
