import os
import pygame
import menu_choix_jeu


menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
button_play = pygame.image.load("./Asset/menue/Jouer.png")
button_play_hover = pygame.image.load("./Asset/menue/Jouer_hover.png")
button_option = pygame.image.load("./Asset/menue/Option.png")
button_option_hover = pygame.image.load("./Asset/menue/Option_hover.png")
button_quit = pygame.image.load("./Asset/menue/Quitter.png")
buitton_quit_hover = pygame.image.load("./Asset/menue/Quitter_hover.png")
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pokemon")


pygame.init()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(menu_background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    if button_play.get_rect(topleft=(300, 200)).collidepoint(mouse_pos):
        screen.blit(button_play_hover, (300, 200))
    else:
        screen.blit(button_play, (300, 200))

    if button_option.get_rect(topleft=(300, 300)).collidepoint(mouse_pos):
        screen.blit(button_option_hover, (300, 300))
    else:
        screen.blit(button_option, (300, 300))
    if button_quit.get_rect(topleft=(300, 400)).collidepoint(mouse_pos): 
        screen.blit(buitton_quit_hover, (300, 400))
    else:
        screen.blit(button_quit, (300, 400))    

    pygame.display.flip()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_play.get_rect(topleft=(300, 200)).collidepoint(mouse_pos):
            menu_choix_jeu.menu_choix_jeu()
        if button_quit.get_rect(topleft=(300, 400)).collidepoint(mouse_pos): 
            running = False    
            
pygame.quit()