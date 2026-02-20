import pygame
from pc import Pc
#from Pokedex import Pokedex

#======== Affichage du numéro de la page ==========#
def display_page(pc, screen):
    font = pygame.font.SysFont('Arial', 35, bold=True)
    txt_page = font.render(str(pc.page), 1, (0, 0, 0))
    screen.blit(txt_page, (528, 622))
    return pygame.Rect(453, 620, 45, 45), pygame.Rect(580, 620, 45, 45)

#=========== Affichage de la grille ===========#
def display_grid(pc,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect, screen):
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(337, 442, 402, 170), 25, 25)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(362, 442, 352, 25))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(362, 585, 352, 25))
    display_hoover(pc,is_hover, index_hover, page_hover, new_hover_rect, screen, old_hover_rect)
    for i in range(4):
        pygame.draw.line(screen, (160, 160, 160), (337+24, 442+(56*i)), (735-20, 442+(56*i)), 2)
    for i in range(7):
        pygame.draw.line(screen, (160, 160, 160), (360+(59*(i)), 442), (360+(59*(i)), 610), 2)
    
    pygame.draw.line(screen, (160, 160, 160), (337, 370), (570, 370), 2)


#======== Affichage des pokemon dans la grille ========#
def display_pokemon(pc, screen):
    font = pygame.font.SysFont('Arial', 15, bold=True)
    list_rect = []
    row = 0
    column = 0
    if len(pc.displayed_pokemon) > 0:
        for pokemon in pc.displayed_pokemon[pc.page - 1]:
            if column >= 6:  # 3 ligne pour 6 colonne
                row += 1
                column = 0
            rect = pygame.Rect(360+(55+5)*column, 445+55*row, 55, 55)
            img_pokemon = pygame.transform.scale(pygame.image.load(pokemon.image), (55, 55))

            screen.blit(img_pokemon, (360+(55+5)*column, 445+55*row))
            if pokemon.index_team is not None :
                pygame.draw.rect(screen, (0,100,250), pygame.Rect(401+(55+5)*column, 444+55*row, 16, 16))
                txt_index_team = font.render(str(pokemon.index_team + 1), 1, (0, 0, 0))
                screen.blit(txt_index_team, (405+(55+5)*column, 440+55*row))
            column += 1
            list_rect.append(rect)
    return list_rect


#======== Affichage des infos du pokemon ========#
def display_info(pc, screen): 
    
    if pc.selected_pokemon != None :  # si pokemon trouver
        font = pygame.font.SysFont('Arial', 20, bold=False)
        font_name = pygame.font.SysFont('Arial', 20, bold=True)
        txt_name = font_name.render(str(pc.selected_pokemon.name), 1, (0, 0, 0))
        str_type = ""
        index = 0
        for i in range(len(pc.selected_pokemon.type)) :
            str_type = pc.selected_pokemon.type[i]
            txt_type = font.render(str_type, 1, (0, 0, 0))
            screen.blit(txt_type, (660, 200+i*25))
            index = i
        txt_hp = font.render(f"HP : {pc.selected_pokemon.hp}", 1, (0, 0, 0))
        txt_attack = font.render(f"attaque : {pc.selected_pokemon.attack}", 1, (0, 0, 0))
        txt_defense = font.render(f"défense : {pc.selected_pokemon.defense}", 1, (0, 0, 0))
        txt_type = font.render(f"type :", 1, (0, 0, 0))

        # affichage des infos
        screen.blit(pygame.transform.scale(pygame.image.load(pc.selected_pokemon.image), (155, 155)), (375, 215))
        screen.blit(txt_name, (78+260+(231-font_name.size(pc.selected_pokemon.name)[0])/2, 190))
        screen.blit(txt_type, (610, 200))
        screen.blit(txt_hp, (610, 230+index*25))
        screen.blit(txt_attack, (610, 260+index*25))
        screen.blit(txt_defense, (610, 290+index*25))


#======= Affichage de l'encadrement de la sélection ========#
def display_select_square(pc, screen):
    if pc.selected_pokemon != None :
        if len(pc.displayed_pokemon) > 0 :
            for i in range(len(pc.displayed_pokemon[pc.page-1])) :
                if pc.displayed_pokemon[pc.page-1][i] == pc.selected_pokemon :
                    column = i % 6
                    row = i // 6
                    pygame.draw.rect(screen, (0, 100, 250), pygame.Rect(360-3+(55+5)*column, 445-3+55*row, 61+2, 61), 4, 10)


#======= Affichage de l'effet de survol =========#  
def display_hoover(pc, is_hover, index, page, new_rect, screen, old_rect=None):
    if is_hover:
        column = index % 6
        row = index // 6
        # afficher l'encadrement
        if page == pc.page:
            pygame.draw.rect(screen, (255, 255, 150), pygame.Rect(360+(54+5)*column, 443+55*row, 59, 57))
            if new_rect != old_rect:
                pygame.mixer.Sound("assets/sons/hover.mp3").play()


#======= Affichage de la barre de recherche =======#
def display_search(pc, is_writting, screen):
    font = pygame.font.SysFont('Arial', 20, bold=False)
    search_bar = pygame.Rect(585, 418, 150, 21)
    
    # Couleur différente si on écrit
    color = (255, 255, 200) if is_writting else (255, 255, 255)
    pygame.draw.rect(screen, color, search_bar)
    pygame.draw.rect(screen, (0, 0, 0), search_bar, 1)  # Bordure
    
    # Texte avec curseur clignotant
    text = pc.search
    if is_writting and pygame.time.get_ticks() % 1000 < 500:
        text += "|"
    
    txt_search = font.render(text, 1, (0, 0, 0))
    screen.blit(txt_search, (587, 415))
    
    return search_bar


#======== Saisie de la barre de recherche =========#
def handle_search_input(pc, event, is_writting, is_info, index_info):
    if is_writting and event.type == pygame.KEYDOWN:
        pc.page = 1
        index_info = None  # Réinitialiser l'index lors de la recherche
        
        if event.key == pygame.K_BACKSPACE:  # Effacer le dernier caractère
            pc.search = pc.search[:-1]
            pc.displayed_pokemon = pc.searching()
        elif event.key == pygame.K_RETURN:  # Entrée pour valider
            return False, is_info, index_info
        elif event.key == pygame.K_ESCAPE:  # Échap pour annuler
            pc.search = ""
            pc.displayed_pokemon = pc.searching()
            return False, is_info, index_info
        else:  # Ajouter le caractère saisi
            pc.search += event.unicode
            pc.displayed_pokemon = pc.searching()
    
    return is_writting, is_info, index_info


def display_num_unlock(pc, screen) :
    font = pygame.font.SysFont('Arial', 15, bold=True)
    txt_num_unlock = font.render(f"Trouvé : {pc.num_unlock} / {len(pc.pokemon)}", 1, (0, 0, 0))
    screen.blit(txt_num_unlock, (648, 610))


# Initialisation de pygame
pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()
pygame.mixer.music.load("assets/sons/music_fond.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)


def open_pc(pc, screen) : 

    pc_background = pygame.image.load("assets/images/pc.jpg")
    list_rect = []
    index_info = None
    is_info = False
    page_info = 1
    running = True
    is_hover = False
    index_hover = None
    page_hover = 1
    new_hover_rect = None
    old_hover_rect = None
    search_rect = None
    is_writting = False

    while running:
        pygame.display.flip()
        screen.blit(pc_background, (260, 0))
        btn_page = display_page(pc, screen)

        display_grid(pc,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect, screen)
        display_num_unlock(pc, screen)

        if is_info:
            display_info(pc, screen)
            display_select_square(pc, screen)

        list_rect = display_pokemon(pc, screen)
        search_rect = display_search(pc, is_writting, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            is_writting, is_info, index_info = handle_search_input(pc, event, is_writting, is_info, index_info)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # boutons de changement de page
                if btn_page[1].collidepoint(event.pos):
                    pc.switch_page(1)
                    pygame.mixer.Sound("assets/sons/bouton.mp3").play()
                elif btn_page[0].collidepoint(event.pos):
                    pc.switch_page(-1)
                    pygame.mixer.Sound("assets/sons/bouton.mp3").play()
                # bar de recherche
                elif search_rect.collidepoint(event.pos):
                    is_writting = True  # Activer l'écriture
                else:
                    is_writting = False  # Désactiver si clic ailleurs
                # Clic sur Pokemon
                for i in range(len(list_rect)):
                    if list_rect[i].collidepoint(event.pos):
                        is_info = True
                        index_info = i
                        page_info = pc.page
                        pc.selected_pokemon = pc.displayed_pokemon[pc.page-1][i]
                        pygame.mixer.Sound("assets/sons/bouton.mp3").play()

            if event.type == pygame.MOUSEMOTION:  # si la souris bouge
                is_hover = False  # Réinitialiser le hover
                for i in range(len(list_rect)):  # Vérifier si la souris survole un Pokemon
                    if list_rect[i].collidepoint(event.pos):
                        is_hover = True
                        index_hover = i
                        page_hover = pc.page
                        old_hover_rect = new_hover_rect
                        new_hover_rect = list_rect[i]
                        break
                        
            # parcours avec les flèches
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pc.add_to_team()
                    for pokemon in pc.team :
                        print(pokemon, ", ")

                if event.key == pygame.K_KP_1:
                    pc.switch_to_first_index()

                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN] :
                    add_index = 0
                    match event.key :
                        case pygame.K_LEFT:
                            add_index = -1
                        case pygame.K_RIGHT:
                            add_index = 1
                        case pygame.K_UP:
                            add_index = -6
                        case pygame.K_DOWN:
                            add_index = 6
                    index_info = pc.change_displayed_index(add_index, page_info)
                    is_info = True
                    pc.selected_pokemon = pc.displayed_pokemon[pc.page-1][index_info]
                    page_info = pc.page
                    pygame.mixer.Sound("assets/sons/bouton.mp3").play()
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_p and not is_writting):
                    return 0


#===== Programme principal =====#
screen = pygame.display.set_mode((1080, 720))
screen.fill((255, 255, 255), (0, 0, 1080, 720))
pc = Pc()
open_pc(pc, screen)