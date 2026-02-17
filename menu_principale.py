import os
import pygame
import menu_choix_jeu
import Feuille

pygame.init()

pygame.display.set_caption("Pokemon")
screen = pygame.display.set_mode((1080, 720))

menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
button_play = pygame.image.load("./Asset/menue/Jouer.png")
button_play_hover = pygame.image.load("./Asset/menue/Jouer_hover.png")
button_option = pygame.image.load("./Asset/menue/Option.png")
button_option_hover = pygame.image.load("./Asset/menue/Option_hover.png")
button_quit = pygame.image.load("./Asset/menue/Quitter.png")
button_quit_hover = pygame.image.load("./Asset/menue/Quitter_hover.png")
leaf = pygame.image.load("./Asset/menue/leaf.png")
clock = pygame.time.Clock()
leafs = Feuille.init_leafs(leaf, 20)

pygame.mixer.music.load("./Asset/menue/menu_music.mp3")
pygame.mixer.music.play(-1)
hover_sound = pygame.mixer.Sound("./Asset/menue/hover.mp3")

# Variables pour tracker l'etat de hover precedent
prev_hover_play = False
prev_hover_option = False
prev_hover_quit = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_play.get_rect(topleft=(390, 250)).collidepoint(event.pos):
                menu_choix_jeu.menu_choix_jeu()
            if button_quit.get_rect(topleft=(390, 500)).collidepoint(event.pos):
                running = False

    screen.blit(menu_background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # Bouton Play
    is_hovering_play = button_play.get_rect(topleft=(390, 250)).collidepoint(mouse_pos)
    if is_hovering_play:
        screen.blit(button_play_hover, (390, 250))
        if not prev_hover_play:
            hover_sound.play()
        prev_hover_play = True
    else:
        screen.blit(button_play, (390, 250))
        prev_hover_play = False

    # Bouton Option
    is_hovering_option = button_option.get_rect(topleft=(390, 375)).collidepoint(mouse_pos)
    if is_hovering_option:
        screen.blit(button_option_hover, (390, 375))
        if not prev_hover_option:
            hover_sound.play()
        prev_hover_option = True
    else:
        screen.blit(button_option, (390, 375))
        prev_hover_option = False
    
    # Bouton Quit
    is_hovering_quit = button_quit.get_rect(topleft=(390, 500)).collidepoint(mouse_pos)
    if is_hovering_quit:
        screen.blit(button_quit_hover, (390, 500))
        if not prev_hover_quit:
            hover_sound.play()
        prev_hover_quit = True
    else:
        screen.blit(button_quit, (390, 500))
        prev_hover_quit = False    

    for leaf in leafs:
        leaf.update()
    for leaf in leafs:
        leaf.draw(screen)
    
    
    
    pygame.display.flip()
    clock.tick(60)
            
pygame.quit()