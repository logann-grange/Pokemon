import os
import sys
import pygame

# Ajouter la racine du projet au path pour les imports absolus
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
os.chdir(project_root)

from menue.graphic import menu_option
from evolution.graphic.menu_evolution_animation import run_phase1_blink, run_phase2_congrats
from evolution.graphic.menu_evolution_loop import handle_post_evolution_event, draw_post_evolution_frame
from evolution.graphic.menu_evolution_graphics import (
    load_animated_background,
    draw_animated_background,
    draw_animated_pokemon,
    wrap_text,
)
from evolution.logic.menu_evolution_logic import (
    load_pokedex_data,
    find_pokemon_and_evolution,
    build_pokemon_image_path,
    load_team,
    save_team,
    update_team_with_evolution,
    reveal_pokedex_entry,
)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption("Menu Evolution")
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
background_apng_path = "./Asset/Evolution_anime/background_evolution.gif"
text_box_image = pygame.image.load("./Asset/Professor/dialogue_box.png")
text_box_image =pygame.transform.scale(text_box_image, (1080, 200))
font=pygame.font.Font("./Asset/menue/Pixeled.ttf", 15)

evolve_sound = pygame.mixer.Sound("./Asset/Evolution_anime/music/Evolve.mp3")
congrats_sound = pygame.mixer.Sound("./Asset/Evolution_anime/music/congratulation.mp3")


def apply_evolution_audio_options():
    audio_options = menu_option.load_audio_options()
    _, sfx_volume = menu_option.get_effective_volumes(audio_options)
    evolve_sound.set_volume(sfx_volume)
    congrats_sound.set_volume(sfx_volume)



def animation_evolution(pokemon_name, evolve_channel=None):
    pokedex_data = load_pokedex_data()
    pokemon, next_pokemon = find_pokemon_and_evolution(pokedex_data, pokemon_name)

    if not pokemon:
        print(f"Pokemon {pokemon_name} non trouvé")
        return None

    if not next_pokemon:
        print(f"Pas d'évolution pour {pokemon_name}")
        return None

    pokemon_path = build_pokemon_image_path(pokemon["id"])
    evolution_path = build_pokemon_image_path(next_pokemon["id"])
    
    # Charger les animations dans le cache
    load_animated_background(pokemon_path)
    load_animated_background(evolution_path)

    # La musique d'evolution est deja lancee a l'ouverture
    
    run_phase1_blink(
        screen,
        clock,
        pokemon_name,
        pokemon_path,
        evolution_path,
        background_apng_path,
        text_box_image,
        font,
        draw_animated_background,
        draw_animated_pokemon,
        wrap_text,
    )
            
    # Phase 2: Afficher l'evolution animee apres le clignotement avec texte progressif
    if evolve_channel is not None:
        evolve_channel.stop()
    congrats_sound.play()

    run_phase2_congrats(
        screen,
        clock,
        pokemon_name,
        next_pokemon["name"],
        evolution_path,
        background_apng_path,
        text_box_image,
        font,
        draw_animated_background,
        draw_animated_pokemon,
        wrap_text,
    )
    return next_pokemon
 
    
def evolution(pokemon_name, current_level=None, current_xp=None):
    apply_evolution_audio_options()
    team = load_team()
    
    load_animated_background(background_apng_path)

    # Demarrer la musique des l'ouverture de la page d'evolution
    evolve_channel = evolve_sound.play()

    # Lancer l'animation une seule fois
    evolved_pokemon = animation_evolution(pokemon_name, evolve_channel=evolve_channel)

    # Charger l'image du pokémon évolué si l'évolution a réussi
    if evolved_pokemon:
        team = update_team_with_evolution(
            team,
            pokemon_name,
            evolved_pokemon,
            current_level=current_level,
            current_xp=current_xp,
        )
        save_team(team)
        reveal_pokedex_entry(evolved_pokemon["id"])
        evolved_path = build_pokemon_image_path(evolved_pokemon["id"])
        load_animated_background(evolved_path)
    else:
        evolved_path = None

    continue_text = "Appuyez sur une touche pour revenir a la carte"
    continue_char_index = 0
    continue_char_delay = 3
    continue_frame_counter = 0

    # Boucle d'affichage après l'animation
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            handle_post_evolution_event(event)

        draw_post_evolution_frame(
            screen,
            background_apng_path,
            evolved_path,
            draw_animated_background,
            draw_animated_pokemon,
        )

        screen.blit(text_box_image, (0, 450))
        if continue_char_index < len(continue_text):
            continue_frame_counter += 1
            if continue_frame_counter >= continue_char_delay:
                continue_char_index += 1
                continue_frame_counter = 0

        displayed_continue_text = continue_text[:continue_char_index]
        wrapped_lines = wrap_text(displayed_continue_text, font, 980)
        for index, line in enumerate(wrapped_lines):
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (250, 520 + index * 20))

        pygame.display.flip()
        clock.tick(60)

#evolution("Bulbizarre")  # Test - commenter pour eviter l'execution automatique
