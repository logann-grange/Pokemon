import pygame
import sys
import choix_premier_pokemon
import Feuille
import json
import os
import interface_pokedex

pygame.init()

pygame.display.set_caption("Menu Choix Jeu")
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()

menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
button_new_game = pygame.image.load("./Asset/menue/nouvelle_partie_.png")
button_new_game_hover = pygame.image.load("./Asset/menue/nouvelle_partie_hover.png")
button_load_game = pygame.image.load("./Asset/menue/charger_partie.png")
button_load_game_hover = pygame.image.load("./Asset/menue/charger_partie_hover.png")
button_pokedex = pygame.image.load("./Asset/menue/button_pokedex.png")
button_pokedex_hover = pygame.image.load("./Asset/menue/button_pokedex_hover.png")
leaf = pygame.image.load("./Asset/menue/leaf.png")
leafs = Feuille.init_leafs(leaf, 20)
hover_sound = pygame.mixer.Sound("./Asset/menue/hover.mp3")

# Variables pour tracker l'etat de hover precedent
prev_hover_new_game = False
prev_hover_load_game = False
prev_hover_pokedex = False
def menu_choix_jeu():
    global prev_hover_new_game, prev_hover_load_game, prev_hover_pokedex
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.get_rect(topleft=(390, 250)).collidepoint(event.pos):
                    with open('equipe.json', 'w') as f:
                        json.dump([], f)
                    with open('pokedex.json', 'r') as f:
                        pokedex_data = json.load(f)
                        for pokemon in pokedex_data:
                            pokemon['hidden'] = True
                    with open('pokedex.json', 'w') as f:
                        json.dump(pokedex_data, f, indent=4, ensure_ascii=False)    
                    choix_premier_pokemon.lancer_choix_pokemon()
                elif button_load_game.get_rect(topleft=(390, 380)).collidepoint(event.pos):
                    print("Charger partie sélectionnée")
                elif button_pokedex.get_rect(topleft=(390, 510)).collidepoint(event.pos):
                    interface_pokedex.afficher_interface_pokedex(screen.copy())
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(menu_background, (0, 0))

        for leaf in leafs:
            leaf.update()
        for leaf in leafs:
            leaf.draw(screen)

        if button_new_game.get_rect(topleft=(390, 250)).collidepoint(mouse_pos):
            screen.blit(button_new_game_hover, (390, 250))
            if not prev_hover_new_game:
                hover_sound.play()
            prev_hover_new_game = True
        else:
            screen.blit(button_new_game, (390, 250))
            prev_hover_new_game = False

        if button_load_game.get_rect(topleft=(390, 380)).collidepoint(mouse_pos):
            screen.blit(button_load_game_hover, (390, 380))
            if not prev_hover_load_game:
                hover_sound.play()
            prev_hover_load_game = True
        else:
            screen.blit(button_load_game, (390, 380))
            prev_hover_load_game = False
            
        if button_pokedex.get_rect(topleft=(390, 510)).collidepoint(mouse_pos):
            screen.blit(button_pokedex_hover, (390, 510))
            if not prev_hover_pokedex:
                hover_sound.play()
            prev_hover_pokedex = True
        else:
            screen.blit(button_pokedex, (390, 510))
            prev_hover_pokedex = False
            
        pygame.display.flip()
        clock.tick(60)