import pygame
from Pokedex import Pokedex
from Pokemon import Pokemon

pokedex = Pokedex()

#======== Affichage du numéro de la page ==========#
def display_page(pokedex):
    font = pygame.font.SysFont('Arial', 35, bold=True)
    txt_page = font.render(str(pokedex.page), 1, (0, 0, 0))
    screen.blit(txt_page, (528, 622))

#=========== Affichage de la grille ===========#
def display_grid():
    for i in range(4):
        if i == 0 or i == 3:
            border = 10
        else:
            border = 0
        pygame.draw.line(screen, (160, 160, 160), (337+border, 442+(56*i)), (735-border, 442+(56*i)), 2)
    for i in range(5):
        pygame.draw.line(screen, (160, 160, 160), (360+(59*(i+1)), 442), (360+(59*(i+1)), 610), 2)


#======== Affichage des pokemon ========#
def display_pokemon(pokedex):
    font = pygame.font.SysFont('Arial', 15, bold=True)
    list_rect = []
    row = 0
    column = 0
    if len(pokedex.displayed_pokemon) > 0:
        for pokemon in pokedex.displayed_pokemon[pokedex.page - 1]:
            if column >= 6:  # 3 ligne pour 6 colonne
                row += 1
                column = 0
            rect = pygame.Rect(360+(55+5)*column, 445+55*row, 55, 55)
            img_pokemon = pygame.transform.scale(pygame.image.load(pokemon.image), (55, 55))
            if not pokemon.hidden:
                screen.blit(img_pokemon, (360+(55+5)*column, 445+55*row))
                txt_id = font.render(str(pokemon.id), 1, (0, 0, 0))
            else:
                img_black = img_pokemon.copy()
                img_black.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(img_black, (360+(55+5)*column, 445+55*row))
                txt_id = font.render(str(pokemon.id), 1, (200, 0, 0))

            screen.blit(txt_id, (400+(55+5)*column, 440+55*row))
            column += 1
            list_rect.append(rect)
    return list_rect

#======== Affichage des infos du pokemon ========#
def display_info(pokedex, index_info, page):
    if not pokedex.displayed_pokemon[page-1][index_info].hidden:  # si pokemon trouver
        font = pygame.font.SysFont('Arial', 20, bold=False)
        txt_name = font.render(str(pokedex.displayed_pokemon[page-1][index_info].name), 1, (0, 0, 0))
        txt_type = font.render(f"type : {pokedex.displayed_pokemon[page-1][index_info].type}", 1, (0, 0, 0))
        txt_hp = font.render(f"HP : {pokedex.displayed_pokemon[page-1][index_info].hp}", 1, (0, 0, 0))
        txt_attack = font.render(f"attaque : {pokedex.displayed_pokemon[page-1][index_info].attack}", 1, (0, 0, 0))
        txt_defense = font.render(f"défense : {pokedex.displayed_pokemon[page-1][index_info].defense}", 1, (0, 0, 0))

        # affichage des infos
        screen.blit(pygame.transform.scale(pygame.image.load(pokedex.displayed_pokemon[page-1][index_info].image), (155, 155)), (375, 215))
        screen.blit(txt_name, (400, 200))
        screen.blit(txt_type, (610, 200))
        screen.blit(txt_hp, (610, 230))
        screen.blit(txt_attack, (610, 260))
        screen.blit(txt_defense, (610, 290))

#======= Affichage de l'encadrement de la sélection ========#
def display_select_square(pokedex, index_info, page, select_rect, hover_rect, is_hover):
    if not pokedex.displayed_pokemon[page-1][index_info].hidden:  # si pokemon trouver
        # changement de couleur si souris sur le rect
        if select_rect == hover_rect and is_hover:
            color = (220, 220, 100)
        else:
            color = (255, 255, 255)
        # afficher l'encadrement
        if page == pokedex.page:
            column = index_info % 6
            row = index_info // 6
            pygame.draw.rect(screen, (0, 100, 250), pygame.Rect(360-3+(55+5)*column, 445-3+55*row, 61, 61), 10, 10)
            pygame.draw.rect(screen, color, pygame.Rect(360+(55+5)*column, 445+55*row, 55, 55), 10, 10)

def display_hoover(pokedex, index, page, new_rect, old_rect=None):
    if not pokedex.displayed_pokemon[page-1][index].hidden:  # si pokemon trouver
        # afficher l'encadrement
        if page == pokedex.page:
            column = index % 6
            row = index // 6
            pygame.draw.rect(screen, (220, 220, 100), pygame.Rect(360+(54+5)*column, 443+55*row, 59, 57))
        if new_rect != old_rect:
            pygame.mixer.Sound("assets/sons/hover.mp3").play()

#======= Affichage de la barre de recherche =======#
def display_search(pokedex, is_writting):
    font = pygame.font.SysFont('Arial', 20, bold=False)
    search_bar = pygame.Rect(585, 418, 150, 21)
    
    # Couleur différente si on écrit
    color = (255, 255, 200) if is_writting else (255, 255, 255)
    pygame.draw.rect(screen, color, search_bar)
    pygame.draw.rect(screen, (0, 0, 0), search_bar, 1)  # Bordure
    
    # Texte avec curseur clignotant
    text = pokedex.search
    if is_writting and pygame.time.get_ticks() % 1000 < 500:
        text += "|"
    
    txt_search = font.render(text, 1, (0, 0, 0))
    screen.blit(txt_search, (587, 415))
    
    return search_bar

#======== Saisie de la barre de recherche =========#
def handle_search_input(pokedex, event, is_writting):
    if is_writting and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:  # Effacer le dernier caractère
            pokedex.search = pokedex.search[:-1]
            pokedex.displayed_pokemon = pokedex.searching()
        elif event.key == pygame.K_RETURN:  # Entrée pour valider
            return False
        elif event.key == pygame.K_ESCAPE:  # Échap pour annuler
            pokedex.search = ""
            pokedex.displayed_pokemon = pokedex.searching()
            return False
        else:  # Ajouter le caractère saisi
            pokedex.search += event.unicode
            pokedex.displayed_pokemon = pokedex.searching()
    
    return is_writting


# Initialisation de pygame
pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()

screen = pygame.display.set_mode((1080, 720))
screen.fill((255, 255, 255), (0, 0, 1080, 720))
pokedex_background = pygame.image.load("assets/images/pokedex2.jpg")

btn_add_page = pygame.Rect(580, 620, 45, 45)
btn_moins_page = pygame.Rect(453, 620, 45, 45)

list_rect = []
index_info = None
is_info = False
page_info = 1
running = True
is_hover = False
index_hover = None
page_hover = 1
select_rect = None
new_hover_rect = None
old_hover_rect = None
search_rect = None
is_writting = False

while running:
    pygame.display.flip()
    screen.blit(pokedex_background, (260, 0))
    display_page(pokedex)
    
    if is_hover:
        display_hoover(pokedex, index_hover, page_hover, new_hover_rect, old_hover_rect)
    
    display_grid()
    
    if is_info:
        display_info(pokedex, index_info, page_info)
        display_select_square(pokedex, index_info, page_info, select_rect, new_hover_rect, is_hover)

    list_rect = display_pokemon(pokedex)
    search_rect = display_search(pokedex, is_writting)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        is_writting = handle_search_input(pokedex, event, is_writting)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # boutons de changement de page
            if btn_add_page.collidepoint(event.pos):
                pokedex.switch_page(1)
                pygame.mixer.Sound("assets/sons/bouton.mp3").play()
            elif btn_moins_page.collidepoint(event.pos):
                pokedex.switch_page(-1)
                pygame.mixer.Sound("assets/sons/bouton.mp3").play()
            # bar de recherche
            elif search_rect.collidepoint(event.pos):
                is_writting = True  # Activer l'écriture
            else:
                is_writting = False  # Désactiver si clic ailleurs

            # Clic sur un Pokémon
            for i in range(len(list_rect)):
                if list_rect[i].collidepoint(event.pos):
                    is_info = True
                    index_info = i
                    page_info = pokedex.page
                    select_rect = list_rect[i]
                    pygame.mixer.Sound("assets/sons/bouton.mp3").play()
        
        if event.type == pygame.MOUSEMOTION:  # si la souris bouge
            is_hover = False  # Réinitialiser le hover
            for i in range(len(list_rect)):  # Vérifier si la souris survole un Pokémon
                if list_rect[i].collidepoint(event.pos):
                    is_hover = True
                    index_hover = i
                    page_hover = pokedex.page
                    old_hover_rect = new_hover_rect
                    new_hover_rect = list_rect[i]
                    break