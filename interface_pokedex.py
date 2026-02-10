import pygame
from Pokedex import Pokedex
from Pokemon import Pokemon

p1 = Pokemon(1, 'Bulbizare', "image.png", 500, 150, 15, 10, 1, 0)
p2 = Pokemon(2, 'Salamèche', "image.png", 500, 150, 15, 10, 1, 0)
list_pokemon = [p1, p2]
pokedex = Pokedex()

def display_page(pokedex) :
    font = pygame.font.SysFont('Arial', 35, bold=True)
    txt_page = font.render(str(pokedex.page), 1, (0, 0, 0))
    screen.blit(txt_page, (528, 622))
    pygame.display.flip()



# Initialisation de pygame
pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()

screen = pygame.display.set_mode((1080, 720))
screen.fill((255,255,255), (0, 0, 1080, 720))
pokedex_background = pygame.image.load("assets/images/pokedex.jpg")

btn_add_page = pygame.Rect(580, 620, 45, 45)
btn_moins_page = pygame.Rect(453, 620, 45, 45)


running = True
while running :
    pygame.display.flip()
    screen.blit(pokedex_background, (260,0))
    #pygame.draw.rect(screen, (0, 0, 0), btn_add_page)
    #pygame.draw.rect(screen, (0, 0, 0), btn_moins_page)
    display_page(pokedex)

    for event in pygame.event.get() :

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            if btn_add_page.collidepoint(event.pos) :
                pokedex.switch_page(1)
            if btn_moins_page.collidepoint(event.pos) :
                pokedex.switch_page(-1)
            
            


