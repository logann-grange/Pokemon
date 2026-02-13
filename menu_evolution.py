import pygame
import sys
import json
from PIL import Image


pygame.init()
pygame.display.set_caption("Menu Evolution")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_apng_path = "./Asset/Evolution_anime/background_evolution.gif"
text_box_image = pygame.image.load("./Asset/Professor/dialogue_box.png")
text_box_image =pygame.transform.scale(text_box_image, (800, 200))



# Cache global pour les animations
_apng_cache = {}
_anim_state = {}


def load_animated_background(apng_path):
    """Charger et mettre en cache les frames d'un APNG."""
    if apng_path not in _apng_cache:
        apng = Image.open(apng_path)
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
                durations.append(apng.info.get("duration", 100))

                apng.seek(apng.tell() + 1)
        except EOFError:
            pass

        if frames:
            _apng_cache[apng_path] = (frames, durations)
            _anim_state[apng_path] = {
                "current_frame": 0,
                "last_update": pygame.time.get_ticks()
            }

def draw_animated_background(screen, apng_path, scale_to_screen=True):
    """Dessiner le background animé."""
    if apng_path not in _apng_cache:
        return
    
    frames, durations = _apng_cache[apng_path]
    state = _anim_state[apng_path]
    now = pygame.time.get_ticks()
    duration = durations[state["current_frame"]]
    
    if now - state["last_update"] > duration:
        state["current_frame"] = (state["current_frame"] + 1) % len(frames)
        state["last_update"] = now

    frame = frames[state["current_frame"]]
    
    if scale_to_screen:
        # Redimensionner pour couvrir tout l'écran
        frame = pygame.transform.scale(frame, screen.get_size())
    
    screen.blit(frame, (0, 0))


def draw_animated_pokemon(screen, apng_path, position, scale=1.0, white_filter=False):
    """Dessiner un pokémon animé à une position donnée."""
    if apng_path not in _apng_cache:
        return
    
    frames, durations = _apng_cache[apng_path]
    state = _anim_state[apng_path]
    now = pygame.time.get_ticks()
    duration = durations[state["current_frame"]]
    
    if now - state["last_update"] > duration:
        state["current_frame"] = (state["current_frame"] + 1) % len(frames)
        state["last_update"] = now
    
    frame = frames[state["current_frame"]].copy()
    
    if scale != 1.0:
        new_size = (int(frame.get_width() * scale), int(frame.get_height() * scale))
        frame = pygame.transform.scale(frame, new_size)
    
    # Appliquer le filtre blanc si demandé
    if white_filter:
        frame.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
    
    frame_rect = frame.get_rect(center=position)
    screen.blit(frame, frame_rect)


def animation_evolution(pokemon_name):
    with open('pokedex.json', 'r', encoding='utf-8') as f:
        pokedex_data = json.load(f)
    
    # Trouver le pokemon actuel par son nom
    pokemon = None
    for p in pokedex_data:
        if p['name'].lower() == pokemon_name.lower():
            pokemon = p
            break
    
    if not pokemon:
        print(f"Pokemon {pokemon_name} non trouvé")
        return None
    
    # Trouver le pokemon évolution (id + 1)
    next_pokemon = None
    for p in pokedex_data:
        if int(p['id']) == int(pokemon['id']) + 1:
            next_pokemon = p
            break
    
    if not next_pokemon:
        print(f"Pas d'évolution pour {pokemon_name}")
        return None
    
    # Charger les images depuis le bon dossier
    pokemon_path = f"./Asset/front/{int(pokemon['id'])}.png"
    evolution_path = f"./Asset/front/{int(next_pokemon['id'])}.png"
    
    # Charger les animations dans le cache
    load_animated_background(pokemon_path)
    load_animated_background(evolution_path)
    
    # Phase 1: Clignotement accéléré entre les deux pokémons animés en blanc (3 secondes)
    total_blinks = 300
    start_speed = 30  # Commence lentement (30 frames = 0.5 sec)
    end_speed = 3     # Finit très rapide (3 frames = 0.05 sec)
    
    current_pokemon = 0
    frames_since_switch = 0
    
    for frame in range(total_blinks):
        draw_animated_background(screen, background_apng_path)
        
        # Calculer la vitesse d'alternance en fonction de la progression
        progress = frame / total_blinks  # 0.0 à 1.0
        frames_per_switch = int(start_speed - (start_speed - end_speed) * progress)
        
        # Alterner quand on atteint le nombre de frames
        if frames_since_switch >= frames_per_switch:
            current_pokemon = 1 - current_pokemon  # Basculer entre 0 et 1
            frames_since_switch = 0
        
        # Afficher le pokémon actuel en blanc
        if current_pokemon == 0:
            draw_animated_pokemon(screen, pokemon_path, (400, 300), scale=2.0, white_filter=True)
        else:
            draw_animated_pokemon(screen, evolution_path, (400, 300), scale=2.0, white_filter=True)
        
        frames_since_switch += 1
        pygame.display.flip()
        clock.tick(60)
    
    # Phase 2: Afficher l'évolution animée pendant 2 secondes
    for _ in range(120):
        draw_animated_background(screen, background_apng_path)
        draw_animated_pokemon(screen, evolution_path, (400, 300), scale=2.0)
        pygame.display.flip()
        clock.tick(60)
    
    return next_pokemon
    
def evolution(pokemon_name):
    load_animated_background(background_apng_path)

    # Lancer l'animation une seule fois
    evolved_pokemon = animation_evolution(pokemon_name)

    # Charger l'image du pokémon évolué si l'évolution a réussi
    if evolved_pokemon:
        evolved_path = f"./Asset/front/{int(evolved_pokemon['id'])}.png"
        load_animated_background(evolved_path)
    else:
        evolved_path = None

    # Boucle d'affichage après l'animation
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_animated_background(screen, background_apng_path)
        
        # Afficher le pokémon évolué animé
        if evolved_path:
            draw_animated_pokemon(screen, evolved_path, (400, 300), scale=2.0)
        
        pygame.display.flip()
        clock.tick(60)

evolution("Spykokwak")

    