import json
import os
import importlib.util
import pygame
from game.choix_premier_pokemon import lancer_choix_pokemon
from Pokedex.graphic.interface_pokedex import afficher_interface_pokedex

# Get project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

game_spec = importlib.util.spec_from_file_location("game_main_module", os.path.join(PROJECT_ROOT, "game.py"))
game_main_module = importlib.util.module_from_spec(game_spec)
game_spec.loader.exec_module(game_main_module)

def handle_menu_choix_event(event, button_rects, screen):
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return False, None

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_rects["new_game"].collidepoint(event.pos):
            equipe_file = os.path.join(PROJECT_ROOT, "equipe.json")
            with open(equipe_file, "w") as file:
                json.dump([], file)

            pokedex_file = os.path.join(PROJECT_ROOT, "pokedex.json")
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
            game_main_module.run_game(load_saved=True)
        if button_rects["pokedex"].collidepoint(event.pos):
            afficher_interface_pokedex(screen.copy())

        if button_rects["return"].collidepoint(event.pos):
            return False, None

    return True, None
