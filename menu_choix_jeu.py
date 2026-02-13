import pygame
import sys
import choix_premier_pokemon
import Feuille
import json
import os

pygame.display.set_caption("Menu Choix Jeu")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
button_new_game = pygame.image.load("./Asset/menue/nouvelle_partie_.png")
button_new_game_hover = pygame.image.load("./Asset/menue/nouvelle_partie_hover.png")
button_load_game = pygame.image.load("./Asset/menue/charger_partie.png")
button_load_game_hover = pygame.image.load("./Asset/menue/charger_partie_hover.png")
leaf = pygame.image.load("./Asset/menue/leaf.png")
leafs = Feuille.init_leafs(leaf, 20)


pygame.init()
def menu_choix_jeu():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.get_rect(topleft=(300, 200)).collidepoint(event.pos):
                    with open('equipe.json', 'w') as f:
                        json.dump([], f)
                    with open('pokedex.json', 'r') as f:
                        pokedex_data = json.load(f)
                        for pokemon in pokedex_data:
                            pokemon['hidden'] = True
                    with open('pokedex.json', 'w') as f:
                        json.dump(pokedex_data, f, indent=4, ensure_ascii=False)    
                    choix_premier_pokemon.lancer_choix_pokemon()
                elif button_load_game.get_rect(topleft=(300, 300)).collidepoint(event.pos):
                    print("Charger partie sélectionnée")

        mouse_pos = pygame.mouse.get_pos()

        screen.blit(menu_background, (0, 0))

        for leaf in leafs:
            leaf.update()
        for leaf in leafs:
            leaf.draw(screen)

        if button_new_game.get_rect(topleft=(300, 200)).collidepoint(mouse_pos):
            screen.blit(button_new_game_hover, (300, 200))
        else:
            screen.blit(button_new_game, (300, 200))

        if button_load_game.get_rect(topleft=(300, 300)).collidepoint(mouse_pos):
            screen.blit(button_load_game_hover, (300, 300))
        else:
            screen.blit(button_load_game, (300, 300))
            
        pygame.display.flip()
        clock.tick(60)