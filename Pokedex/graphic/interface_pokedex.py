import pygame
import json
import os
from Pokedex.logic.Pokedex import Pokedex
from menue.graphic import menu_option
from game.graphic.display_manager import get_screen


_sfx_cache = {}


def _current_audio_options():
    return menu_option.load_audio_options()


def _current_sfx_volume():
    options = _current_audio_options()
    _, sfx_volume = menu_option.get_effective_volumes(options)
    return sfx_volume


def _apply_music_volume_for_pokedex():
    options = _current_audio_options()
    music_volume, _ = menu_option.get_effective_volumes(options)
    pygame.mixer.music.set_volume(music_volume)


def play_sfx(sound_path):
    if sound_path not in _sfx_cache:
        _sfx_cache[sound_path] = pygame.mixer.Sound(sound_path)
    sound = _sfx_cache[sound_path]
    sound.set_volume(_current_sfx_volume())
    sound.play()

#======== Affichage du numéro de la page ==========#
def display_page(pokedex):
    font = pygame.font.SysFont('Arial', 35, bold=True)
    txt_page = font.render(str(pokedex.page), 1, (0, 0, 0))
    screen.blit(txt_page, (528, 622))
    return pygame.Rect(453, 620, 45, 45), pygame.Rect(580, 620, 45, 45)

#=========== Affichage de la grille ===========#
def display_grid(pokedex,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect):
    pygame.draw.rect(screen, (20, 20, 20), pygame.Rect(337, 442, 402, 170), 25, 25)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(362, 442, 352, 25))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(362, 585, 352, 25))
    display_hoover(pokedex,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect)
    for i in range(4):
        pygame.draw.line(screen, (160, 160, 160), (337+24, 442+(56*i)), (735-20, 442+(56*i)), 2)
    for i in range(7):
        pygame.draw.line(screen, (160, 160, 160), (360+(59*(i)), 442), (360+(59*(i)), 610), 2)
    
    pygame.draw.line(screen, (160, 160, 160), (337, 370), (570, 370), 2)


#======== Affichage des pokemon dans la grille ========#
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
                # si pokemon caché créer un masque noir à partir de l'image
                mask = pygame.mask.from_surface(img_pokemon)
                img_black = mask.to_surface(setcolor=(0, 0, 0, 240), unsetcolor=(0, 0, 0, 0))
    
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
            img_sub_evo = pygame.transform.scale(pygame.image.load(sub_evo.image), (55, 55))
            
            if not sub_evo.hidden :
                screen.blit(img_sub_evo, (350, 370))
            else :
                # Créer un masque noir à partir de l'image
                mask = pygame.mask.from_surface(img_sub_evo)
                img_black = mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
                screen.blit(img_black, (350, 370))
        list_rect_evo.append(pygame.Rect(350, 370, 55, 55))

        if pokedex.selected_pokemon.evo != "" :
            evo = pokedex.get_pokemon_by_id(pokedex.selected_pokemon.evo)
            img_evo = pygame.transform.scale(pygame.image.load(evo.image), (55, 55))
            if not evo.hidden :
                screen.blit(img_evo, (490, 370))
            else :
                # Créer un masque noir à partir de l'image
                mask = pygame.mask.from_surface(img_evo)
                img_black = mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))
                screen.blit(img_black, (490, 370))
        list_rect_evo.append(pygame.Rect(490, 370, 55, 55))

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
    if pokedex.selected_pokemon != None :
        if len(pokedex.displayed_pokemon) > 0 :
            for i in range(len(pokedex.displayed_pokemon[pokedex.page-1])) :
                if pokedex.displayed_pokemon[pokedex.page-1][i] == pokedex.selected_pokemon :
                    column = i % 6
                    row = i // 6
                    pygame.draw.rect(screen, (0, 100, 250), pygame.Rect(360-3+(55+5)*column, 445-3+55*row, 61+2, 61), 4, 10)


#======= Affichage de l'effet de survol =========#  
def display_hoover(pokedex, is_hover, index, page, new_rect, old_rect=None):
    if is_hover:
        column = index % 6
        row = index // 6
        # afficher l'encadrement
        if page == pokedex.page:
            if not pokedex.displayed_pokemon[page-1][index].hidden : # si pokemon trouver
                pygame.draw.rect(screen, (255, 255, 150), pygame.Rect(360+(54+5)*column, 443+55*row, 59, 57))
                if new_rect != old_rect:
                    play_sfx("Asset/sons/hover.mp3")


#========== Affichage de la fenêtre des pokemon cachés ===========#
def display_hidden_window(pokedex, is_hover, index, page) :
    if is_hover and page == pokedex.page :
        if pokedex.displayed_pokemon[page-1][index].hidden:
            font = pygame.font.SysFont('Arial', 15, bold=True)
            txt_hidden = font.render("Non découvert", 1, (0, 0, 0))
            # change la direction de la fenêtre en fonction de l'emplacement de la case
            if index % 6 <= 2 :
                x = 100
            else :
                x = 0
            pygame.draw.rect(screen, (200, 50, 50), pygame.Rect(pygame.mouse.get_pos()[0]-x, pygame.mouse.get_pos()[1]-20, 100, 20))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(pygame.mouse.get_pos()[0]-x, pygame.mouse.get_pos()[1]-20, 100, 20), 1)
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


# Initialisation de pygame
pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()
pygame.mixer.music.load("Asset/sons/music_fond.mp3")
_apply_music_volume_for_pokedex()
pygame.mixer.music.play(-1)

screen = None
pokedex_background = None

def open_pokedex(pokedex, background_surface=None) : 
    global screen, pokedex_background

    if screen is None:
        screen = get_screen("Pokedex")

    if pokedex_background is None:
        pokedex_background = pygame.image.load("Asset/image/pokedex2.png")

    if background_surface is not None and background_surface.get_size() != screen.get_size():
        background_surface = pygame.transform.scale(background_surface, screen.get_size())

    _apply_music_volume_for_pokedex()

    pokedex.pokemon = pokedex.load_pokemon_list()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    equipe_file = os.path.join(project_root, "data", "equipe.json")
    captured_ids = set()
    try:
        with open(equipe_file, "r", encoding="utf-8") as file:
            team_data = json.load(file)
            if isinstance(team_data, list):
                for member in team_data:
                    try:
                        captured_ids.add(int(member.get("id")))
                    except (TypeError, ValueError):
                        continue
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    for pokemon in pokedex.pokemon:
        try:
            if int(pokemon.id) in captured_ids:
                pokemon.hidden = False
        except (TypeError, ValueError):
            continue

    pokedex.search = ""
    pokedex.page = 1
    pokedex.selected_pokemon = None
    pokedex.displayed_pokemon = pokedex.searching()
    pokedex.num_unlock = pokedex.get_num_unlock()
    
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
    list_rect_evo = []    

    while running:
        pygame.display.flip()
        if background_surface is not None:
            screen.blit(background_surface, (0, 0))
        screen.blit(pokedex_background, (260, 0))
        btn_page = display_page(pokedex)

        display_grid(pokedex,is_hover, index_hover, page_hover, new_hover_rect, old_hover_rect)
        display_num_unlock(pokedex)

        if is_info:
            list_rect_evo = display_info(pokedex,page_info, is_writting)
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
                if btn_page[1].collidepoint(event.pos):
                    pokedex.switch_page(1)
                    play_sfx("Asset/sons/bouton.mp3")
                elif btn_page[0].collidepoint(event.pos):
                    pokedex.switch_page(-1)
                    play_sfx("Asset/sons/bouton.mp3")
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
                        page_info = pokedex.page
                        pokedex.select_pokemon(pokedex.displayed_pokemon[pokedex.page-1][i])
                        play_sfx("Asset/sons/bouton.mp3")
                # Clic sur evo
                if list_rect_evo != None :
                    for i in range(len(list_rect_evo)):
                        if list_rect_evo[i].collidepoint(event.pos):
                            list_evo = [pokedex.selected_pokemon.sub_evo, pokedex.selected_pokemon.evo]
                            if list_evo[i] != "" :
                                is_info = True
                                pokedex.select_pokemon(pokedex.get_pokemon_by_id(list_evo[i]))
                                if not pokedex.get_pokemon_by_id(list_evo[i]).hidden :
                                    play_sfx("Asset/sons/bouton.mp3")

            if event.type == pygame.MOUSEMOTION:  # si la souris bouge
                is_hover = False  # Réinitialiser le hover
                for i in range(len(list_rect)):  # Vérifier si la souris survole un Pokemon
                    if list_rect[i].collidepoint(event.pos):
                        is_hover = True
                        index_hover = i
                        page_hover = pokedex.page
                        old_hover_rect = new_hover_rect
                        new_hover_rect = list_rect[i]
                        break
                        
            # parcours avec les flèches
            if event.type == pygame.KEYDOWN:
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
                    index_info = pokedex.change_displayed_index(add_index, page_info)
                    is_info = True
                    pokedex.select_pokemon(pokedex.displayed_pokemon[pokedex.page-1][index_info])
                    page_info = pokedex.page
                    play_sfx("Asset/sons/bouton.mp3")


#===== Programme principal =====#
def afficher_interface_pokedex(background_surface=None) :
    global screen, pokedex_background
    screen = get_screen("Pokedex")
    if background_surface is not None:
        background_surface = pygame.transform.scale(background_surface, screen.get_size())
    #screen.fill((255, 255, 255), (0, 0, 1080, 720))
    pokedex_background = pygame.image.load("Asset/image/pokedex2.png")    
    pokedex = Pokedex()
    open_pokedex(pokedex, background_surface)

   