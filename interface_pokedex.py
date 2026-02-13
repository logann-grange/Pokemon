import pygame
from Pokedex import Pokedex
from Pokemon import Pokemon
from PIL import Image


pokedex = Pokedex()

#======== Affichage du numéro de la page ==========#
def display_page(pokedex):
    font = pygame.font.SysFont('Arial', 35, bold=True)
    txt_page = font.render(str(pokedex.page), 1, (0, 0, 0))
    screen.blit(txt_page, (528, 622))

#=========== Affichage de la grille ===========#
def display_grid(pokedex,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect):
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(337, 442, 402, 170), 25, 25)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(362, 442, 352, 25))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(362, 585, 352, 25))
    display_hoover(pokedex,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect)
    for i in range(4):
        if i == 0 or i == 3:
            border = 0
        else:
            border = 0
        pygame.draw.line(screen, (160, 160, 160), (337+24, 442+(56*i)), (735-20, 442+(56*i)), 2)
    for i in range(7):
        pygame.draw.line(screen, (160, 160, 160), (360+(59*(i)), 442), (360+(59*(i)), 610), 2)
    
    pygame.draw.line(screen, (160, 160, 160), (337, 370), (570, 370), 2)



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

def get_pokemon_by_index(pokedex, index_info, page) :
    if index_info < 1000 :
        return pokedex.displayed_pokemon[page-1][index_info]

#======== Affichage des infos du pokemon ========#
def display_info(pokedex, page, is_writting): 
    
    if pokedex.selected_pokemon != None and not pokedex.selected_pokemon.hidden:  # si pokemon trouver
        font = pygame.font.SysFont('Arial', 20, bold=False)
        font_name = pygame.font.SysFont('Arial', 20, bold=True)
        txt_name = font_name.render(str(pokedex.selected_pokemon.name), 1, (0, 0, 0))
        str_type = ""
        index = 0
        for i in range(len(pokedex.selected_pokemon.type)) :
            str_type = pokedex.selected_pokemon.type[i]
            txt_type = font.render(str_type, 1, (0, 0, 0))
            screen.blit(txt_type, (660, 200+i*25))
            index = i
        txt_hp = font.render(f"HP : {pokedex.selected_pokemon.hp}", 1, (0, 0, 0))
        txt_attack = font.render(f"attaque : {pokedex.selected_pokemon.attack}", 1, (0, 0, 0))
        txt_defense = font.render(f"défense : {pokedex.selected_pokemon.defense}", 1, (0, 0, 0))
        txt_type = font.render(f"type :", 1, (0, 0, 0))


        #affichage des evo et sub_evo :
        list_rect_evo = []
        if pokedex.selected_pokemon.sub_evo != "" :
            sub_evo = pokedex.get_pokemon_by_id(pokedex.selected_pokemon.sub_evo)
            img_sub_evo = pygame.image.load(sub_evo.image)
            if not sub_evo.hidden :
                screen.blit(img_sub_evo, (350, 370))
            else :
                img_sub_evo_black = img_sub_evo.copy()
                img_sub_evo_black.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(img_sub_evo_black, (350, 370))

        if pokedex.selected_pokemon.evo != "" :
            evo = pokedex.get_pokemon_by_id(pokedex.selected_pokemon.evo)
            img_evo = pygame.image.load(evo.image)
            if not evo.hidden :
                screen.blit(img_evo, (490, 370))
            else :
                img_evo_black = img_evo.copy()
                img_evo_black.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(img_evo_black, (490, 370))
            list_rect_evo.append(pygame.Rect(420, 370, 55, 55))

        # affichage des infos
        screen.blit(pygame.transform.scale(pygame.image.load(pokedex.selected_pokemon.image), (155, 155)), (375, 215))
        screen.blit(txt_name, (78+260+(231-font_name.size(pokedex.selected_pokemon.name)[0])/2, 190))
        screen.blit(txt_type, (610, 200))
        screen.blit(txt_hp, (610, 230+index*25))
        screen.blit(txt_attack, (610, 260+index*25))
        screen.blit(txt_defense, (610, 290+index*25))

        return list_rect_evo

#======= Affichage de l'encadrement de la sélection ========#
def display_select_square(pokedex):
    # if not is_writting and not pokedex.displayed_pokemon[page-1][index_info].hidden:  # si pokemon trouver
    #     pokedex.selected_pokemon = pokedex.displayed_pokemon[page-1][index_info]
    #     # changement de couleur si souris sur le rect
    #     if select_rect == hover_rect and is_hover:
    #         color = (255, 255, 150)
    #     else:
    #         color = (255, 255, 255)
    #     # afficher l'encadrement
    #     if page == pokedex.page:
    #         column = index_info % 6
    #         row = index_info // 6
    #         pygame.draw.rect(screen, (0, 100, 250), pygame.Rect(360-3+(55+5)*column, 445-3+55*row, 61+2, 61), 10, 10)
    #         pygame.draw.rect(screen, color, pygame.Rect(360+(55+5)*column, 445+55*row, 55+2, 55), 10, 10)
    
    if pokedex.selected_pokemon != None :
        for i in range(len(pokedex.displayed_pokemon[pokedex.page-1])) :
            if pokedex.displayed_pokemon[pokedex.page-1][i] == pokedex.selected_pokemon :
                column = i % 6
                row = i // 6
                pygame.draw.rect(screen, (0, 100, 250), pygame.Rect(360-3+(55+5)*column, 445-3+55*row, 61+2, 61), 4, 10)
                
def display_hoover(pokedex, is_hover, index, page, new_rect, old_rect=None):
    if is_hover:
        column = index % 6
        row = index // 6
        # afficher l'encadrement
        if page == pokedex.page:
            if not pokedex.displayed_pokemon[page-1][index].hidden : # si pokemon trouver
                pygame.draw.rect(screen, (255, 255, 150), pygame.Rect(360+(54+5)*column, 443+55*row, 59, 57))
                if new_rect != old_rect:
                    pygame.mixer.Sound("assets/sons/hover.mp3").play()

def display_hidden_window(pokedex, is_hover, index, page) :
    if is_hover and page == pokedex.page :
        if pokedex.displayed_pokemon[page-1][index].hidden:
            font = pygame.font.SysFont('Arial', 15, bold=True)
            txt_hidden = font.render("Non découvert", 1, (0, 0, 0))
            if index % 6 <= 2 :
                x = 100
            else :
                x = 0
            #rajouter une fenetre
            pygame.draw.rect(screen, (200, 50, 50), pygame.Rect(pygame.mouse.get_pos()[0]-x, pygame.mouse.get_pos()[1]-20, 100, 20))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pygame.mouse.get_pos()[0]-x, pygame.mouse.get_pos()[1]-20, 100, 20), 1)  # Bordure
            screen.blit(txt_hidden, (pygame.mouse.get_pos()[0]+5-x, pygame.mouse.get_pos()[1]-19))


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
def handle_search_input(pokedex, event, is_writting, is_info, index_info):
    if is_writting and event.type == pygame.KEYDOWN:
        pokedex.page = 1
        #is_info = False  # Réinitialiser l'affichage lors de la recherche
        index_info = None  # Réinitialiser l'index lors de la recherche
        
        if event.key == pygame.K_BACKSPACE:  # Effacer le dernier caractère
            pokedex.search = pokedex.search[:-1]
            pokedex.displayed_pokemon = pokedex.searching()
        elif event.key == pygame.K_RETURN:  # Entrée pour valider
            return False, is_info, index_info
        elif event.key == pygame.K_ESCAPE:  # Échap pour annuler
            pokedex.search = ""
            pokedex.displayed_pokemon = pokedex.searching()
            return False, is_info, index_info
        else:  # Ajouter le caractère saisi
            pokedex.search += event.unicode
            pokedex.displayed_pokemon = pokedex.searching()
    
    return is_writting, is_info, index_info

def display_num_unlock(pokedex) :
    font = pygame.font.SysFont('Arial', 15, bold=True)
    txt_num_unlock = font.render(f"Trouvé : {pokedex.num_unlock} / {len(pokedex.pokemon)}", 1, (0, 0, 0))
    screen.blit(txt_num_unlock, (648, 610))

def display_animated_img(last_update, current_frame) :
    # Charger le PNG animé
    apng = Image.open("assets/images/pokemon/dardargnan.png")
    # Extraire toutes les frames
    frames = []
    durations = []

    try:
        while True:
            # Convertir en RGBA pour la compatibilité
            frame = apng.convert("RGBA")
        
            # Convertir PIL Image en Pygame Surface
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            frame_surface = pygame.image.fromstring(data, size, mode)
        
            frames.append(frame_surface)
            durations.append(apng.info.get('duration', 100))
        
            apng.seek(apng.tell() + 1)
    except EOFError:
        pass

    # Animation
    
    now = pygame.time.get_ticks()
    if now - last_update > durations[current_frame]:
        current_frame = (current_frame + 1) % len(frames)
        last_update = now
    # Affichage
    screen.blit(frames[current_frame], (250, 250))
    return last_update, current_frame


# Initialisation de pygame
pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()
pygame.mixer.music.load("assets/sons/music_fond.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

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
list_rect_evo = []
last_update = pygame.time.get_ticks()
current_frame = 0

while running:
    pygame.display.flip()
    screen.blit(pokedex_background, (260, 0))
    display_page(pokedex)
    
    display_grid(pokedex,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect)
    display_num_unlock(pokedex)
    #last_update, current_frame = display_animated_img(last_update, current_frame)
    
    if is_info:
        #list_rect_evo = display_info(get_pokemon_by_index(pokedex, index_info, page_info), is_writting)
        list_rect_evo = display_info(pokedex,page_info, is_writting)
        #display_select_square(pokedex, index_info, page_info, select_rect, new_hover_rect, is_hover, is_writting)
        display_select_square(pokedex)

    list_rect = display_pokemon(pokedex)
    search_rect = display_search(pokedex, is_writting)
    display_hidden_window(pokedex, is_hover, index_hover, page_hover)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        is_writting, is_info, index_info = handle_search_input(pokedex, event, is_writting, is_info, index_info)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # boutons de changement de page
            if btn_add_page.collidepoint(event.pos):
                pokedex.switch_page(1)
                #is_info = False  # Réinitialiser l'affichage
                #index_info = None  # Réinitialiser l'index
                pygame.mixer.Sound("assets/sons/bouton.mp3").play()
            elif btn_moins_page.collidepoint(event.pos):
                pokedex.switch_page(-1)
                #is_info = False  # Réinitialiser l'affichage
                #index_info = None  # Réinitialiser l'index
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
                    #pokedex.selected_pokemon = pokedex.displayed_pokemon[page_info][index_info]
                    pokedex.select_pokemon(pokedex.displayed_pokemon[pokedex.page-1][i])
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