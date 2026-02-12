import pygame
import sys
import choix_premier_pokemon



menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
button_new_game = pygame.image.load("./Asset/menue/nouvelle_partie_.png")
button_new_game_hover = pygame.image.load("./Asset/menue/nouvelle_partie_hover.png")
button_load_game = pygame.image.load("./Asset/menue/charger_partie.png")
button_load_game_hover = pygame.image.load("./Asset/menue/charger_partie_hover.png")
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Menu Choix Jeu")
pygame.init()

def menu_choix_jeu():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_new_game.get_rect(topleft=(300, 200)).collidepoint(mouse_pos):
                    choix_premier_pokemon.lancer_choix_pokemon()
                elif button_load_game.get_rect(topleft=(300, 300)).collidepoint(mouse_pos):
                    print("Charger partie sélectionnée")

        screen.blit(menu_background, (0, 0))

        if button_new_game.get_rect(topleft=(300, 200)).collidepoint(mouse_pos):
            screen.blit(button_new_game_hover, (300, 200))
        else:
            screen.blit(button_new_game, (300, 200))

        if button_load_game.get_rect(topleft=(300, 300)).collidepoint(mouse_pos):
            screen.blit(button_load_game_hover, (300, 300))
        else:
            screen.blit(button_load_game, (300, 300))
            
        pygame.display.flip()