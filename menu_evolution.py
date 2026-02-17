import pygame
import sys
import json
from PIL import Image


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Menu Evolution")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
background_apng_path = "./Asset/Evolution_anime/background_evolution.gif"
text_box_image = pygame.image.load("./Asset/Professor/dialogue_box.png")
text_box_image =pygame.transform.scale(text_box_image, (800, 200))
font=pygame.font.Font("./Asset/menue/Pixeled.ttf", 15)

evolve_sound = pygame.mixer.Sound("./Asset/Evolution_anime/music/Evolve.mp3")
congrats_sound = pygame.mixer.Sound("./Asset/Evolution_anime/music/congratulation.mp3")



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


def animation_evolution(pokemon_name, evolve_channel=None):
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

    # La musique d'evolution est deja lancee a l'ouverture
    
    # Phase 1: Clignotement accelere entre les deux pokemons animes en blanc
    phase1_seconds = 16.0
    total_blinks = int(phase1_seconds * 60)
    start_speed = 30  # Commence lentement (30 frames = 0.5 sec)
    end_speed = 3     # Finit très rapide (3 frames = 0.05 sec)
    
    current_pokemon = 0
    frames_since_switch = 0
    
    # Texte progressif phase 1
    text_phase1 = f"Quoi ? {pokemon_name} évolue !"
    char_index_p1 = 0
    char_delay = 3
    frame_counter_p1 = 0
    
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
        
        # Afficher le texte progressivement
        screen.blit(text_box_image, (0, 350))
        
        if char_index_p1 < len(text_phase1):
            frame_counter_p1 += 1
            if frame_counter_p1 >= char_delay:
                char_index_p1 += 1
                frame_counter_p1 = 0
        
        displayed_text = text_phase1[:char_index_p1]
        wrapped_lines = wrap_text(displayed_text, font, 780)
        for i, line in enumerate(wrapped_lines):
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (50, 370 + i * 20))
        
        frames_since_switch += 1
        pygame.display.flip()
        clock.tick(60)
            
    # Phase 2: Afficher l'evolution animee apres le clignotement avec texte progressif
    if evolve_channel is not None:
        evolve_channel.stop()
    congrats_sound.play()
    phase2_seconds = 6.0
    phase2_frames = int(phase2_seconds * 60)
    
    # Texte progressif phase 2
    text_phase2 = f"Félicitations ! {pokemon_name} a évolué en {next_pokemon['name']} !"
    char_index_p2 = 0
    frame_counter_p2 = 0
    
    for _ in range(phase2_frames):
        draw_animated_background(screen, background_apng_path)
        draw_animated_pokemon(screen, evolution_path, (400, 300), scale=2.0)
        
        # Afficher le texte progressivement
        screen.blit(text_box_image, (0, 350))
        
        if char_index_p2 < len(text_phase2):
            frame_counter_p2 += 1
            if frame_counter_p2 >= char_delay:
                char_index_p2 += 1
                frame_counter_p2 = 0
        
        displayed_text = text_phase2[:char_index_p2]
        wrapped_lines = wrap_text(displayed_text, font, 780)
        for i, line in enumerate(wrapped_lines):
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (50, 370 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    return next_pokemon
 
def wrap_text(text, font, max_width):
            """Divise le texte en lignes selon la largeur maximale"""
            words = text.split(' ')
            lines = []
            current_line = ''
            
            for word in words:
                test_line = current_line + word + ' '
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.rstrip())
                    current_line = word + ' '
            
            if current_line:
                lines.append(current_line.rstrip())
            
            return lines 
 
    
def evolution(pokemon_name):
    try:
        with open('equipe.json', 'r', encoding='utf-8') as f:
            equipe = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        equipe = []
    if not isinstance(equipe, list):
        equipe = []
    
    load_animated_background(background_apng_path)

    # Demarrer la musique des l'ouverture de la page d'evolution
    evolve_channel = evolve_sound.play()

    # Lancer l'animation une seule fois
    evolved_pokemon = animation_evolution(pokemon_name, evolve_channel=evolve_channel)

    # Charger l'image du pokémon évolué si l'évolution a réussi
    if evolved_pokemon:
        # Remplacer l'ancien pokémon dans l'equipe
        for i, p in enumerate(equipe):
            if str(p.get('name', '')).lower() == pokemon_name.lower():
                # Recuperer les stats du pokemon de base
                current_hp = p.get('hp', 0)
                current_attack = p.get('attack', 0)
                current_defense = p.get('defense', 0)
                
                # Recuperer les stats de l'evolution
                evo_hp = evolved_pokemon.get('stats', {}).get('hp', 0)
                evo_attack = evolved_pokemon.get('stats', {}).get('attack', 0)
                evo_defense = evolved_pokemon.get('stats', {}).get('defense', 0)
                
                # Comparer et garder les meilleures stats + 5
                final_hp = current_hp if current_hp > evo_hp else evo_hp
                final_attack = current_attack if current_attack > evo_attack else evo_attack
                final_defense = current_defense if current_defense > evo_defense else evo_defense
                
                # Ajouter 5 aux stats gardees
                if current_hp > evo_hp:
                    final_hp += 5
                if current_attack > evo_attack:
                    final_attack += 5
                if current_defense > evo_defense:
                    final_defense += 5
                
                
                equipe[i] = {
                    "id": evolved_pokemon['id'],
                    "name": evolved_pokemon['name'],
                    "type": evolved_pokemon.get('type'),
                    "hp": final_hp,
                    "attack": final_attack,
                    "defense": final_defense,
                    "level": p.get('level', 1),
                    "xp": p.get('xp', 0)
                }
                break
        with open('equipe.json', 'w', encoding='utf-8') as f:
            json.dump(equipe, f, indent=4, ensure_ascii=False)
        evolved_path = f"./Asset/front/{int(evolved_pokemon['id'])}.png"
        with open('pokedex.json', 'r', encoding='utf-8') as f:
            pokedex_data = json.load(f)
        for p in pokedex_data:
            if int(p['id']) == int(evolved_pokemon['id']):
                p['hidden'] = False
        
        with open('pokedex.json', 'w', encoding='utf-8') as f:
            json.dump(pokedex_data, f, indent=4, ensure_ascii=False)
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

#evolution("Carapuce")  # Test - commenter pour eviter l'execution automatique
