import pygame
from Pokedex import Pokedex
from Pokemon import Pokemon

pokedex = Pokedex()

#======== Affichage du numéro de la page ==========#
def display_page(pokedex) :
    font = pygame.font.SysFont('Arial', 35, bold=True)
    txt_page = font.render(str(pokedex.page), 1, (0, 0, 0))
    screen.blit(txt_page, (528, 622))

#======== Affichage de la grille des pokemon ========#
def display_pokemon(pokedex) :
    font = pygame.font.SysFont('Arial', 15, bold=False)
    list_rect = []
    row = 0
    column = 0
    for pokemon in pokedex.displayed_pokemon[pokedex.page -1] :
        if column >= 6 : # 3 ligne pour 6 colonne
            row += 1
            column = 0
        rect = pygame.Rect(360+(55+5)*column, 445+55*row, 55, 55)
        # pygame.draw.rect(screen, (0, 0, 0), rect)
        img_pokemon = pygame.transform.scale(pygame.image.load(pokemon.image), (55, 55))
        if not pokemon.hidden :
            screen.blit(img_pokemon, (360+(55+5)*column, 445+55*row))
            txt_id = font.render(str(pokemon.id), 1, (0, 0, 0))
        else :
            img_black = img_pokemon.copy()
            img_black.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(img_black, (360+(55+5)*column, 445+55*row))
            txt_id = font.render(str(pokemon.id), 1, (200, 0, 0))

        screen.blit(txt_id, (400+(55+5)*column, 440+55*row))
        column +=1
        list_rect.append(rect)
    return list_rect

#======== Affichage des infos du pokemon ========#
def display_info(pokedex, index_info, page) :
    if not pokedex.displayed_pokemon[page-1][index_info].hidden : # si pokemon trouver
        font = pygame.font.SysFont('Arial', 20, bold=False)
        txt_name = font.render(str(pokedex.displayed_pokemon[page-1][index_info].name), 1, (0, 0, 0))
        txt_type = font.render(f"type : {pokedex.displayed_pokemon[page-1][index_info].type}", 1, (0, 0, 0))
        txt_hp = font.render(f"HP : {pokedex.displayed_pokemon[page-1][index_info].hp}", 1, (0, 0, 0))
        txt_attack = font.render(f"attaque : {pokedex.displayed_pokemon[page-1][index_info].attack}", 1, (0, 0, 0))
        txt_defense = font.render(f"défense : {pokedex.displayed_pokemon[page-1][index_info].defense}", 1, (0, 0, 0))

        screen.blit(pygame.transform.scale(pygame.image.load(pokedex.displayed_pokemon[page-1][index_info].image), (155, 155)), (375, 215))
        screen.blit(txt_name,(400, 200))
        screen.blit(txt_type,(610, 200))
        screen.blit(txt_hp,(610, 230))
        screen.blit(txt_attack,(610, 260))
        screen.blit(txt_defense,(610, 290))

# Initialisation de pygame
pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()

screen = pygame.display.set_mode((1080, 720))
screen.fill((255,255,255), (0, 0, 1080, 720))
pokedex_background = pygame.image.load("assets/images/pokedex.jpg")

btn_add_page = pygame.Rect(580, 620, 45, 45)
btn_moins_page = pygame.Rect(453, 620, 45, 45)

list_rect = []
index_info = None
is_info = False
page_info = 1
running = True
while running :
    pygame.display.flip()
    screen.blit(pokedex_background, (260,0))
    display_page(pokedex)
    list_rect = display_pokemon(pokedex)
    if is_info :
        display_info(pokedex, index_info, page_info)

    for event in pygame.event.get() :

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 :
            #bouton de changement de page
            if btn_add_page.collidepoint(event.pos) :
                pokedex.switch_page(1)
            elif btn_moins_page.collidepoint(event.pos) :
                pokedex.switch_page(-1)
            #bouton pokemon
            else :
                for i in range(len(list_rect)) :
                    if list_rect[i].collidepoint(event.pos) :
                        is_info = True
                        index_info = i
                        page_info = pokedex.page
                        


                        
            


