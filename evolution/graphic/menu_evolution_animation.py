import pygame


def run_phase1_blink(
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
):
    phase1_seconds = 16.0
    total_blinks = int(phase1_seconds * 60)
    start_speed = 30
    end_speed = 3

    current_pokemon = 0
    frames_since_switch = 0

    text_phase1 = f"Quoi ? {pokemon_name} évolue !"
    char_index_p1 = 0
    char_delay = 3
    frame_counter_p1 = 0

    for frame in range(total_blinks):
        draw_animated_background(screen, background_apng_path)

        progress = frame / total_blinks
        frames_per_switch = int(start_speed - (start_speed - end_speed) * progress)

        if frames_since_switch >= frames_per_switch:
            current_pokemon = 1 - current_pokemon
            frames_since_switch = 0

        if current_pokemon == 0:
            draw_animated_pokemon(screen, pokemon_path, (540, 360), scale=3.0, white_filter=True)
        else:
            draw_animated_pokemon(screen, evolution_path, (540, 360), scale=3.0, white_filter=True)

        screen.blit(text_box_image, (0, 450))

        if char_index_p1 < len(text_phase1):
            frame_counter_p1 += 1
            if frame_counter_p1 >= char_delay:
                char_index_p1 += 1
                frame_counter_p1 = 0

        displayed_text = text_phase1[:char_index_p1]
        wrapped_lines = wrap_text(displayed_text, font, 980)
        for index, line in enumerate(wrapped_lines):
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (350, 520 + index * 20))

        frames_since_switch += 1
        pygame.display.flip()
        clock.tick(60)


def run_phase2_congrats(
    screen,
    clock,
    pokemon_name,
    evolved_name,
    evolution_path,
    background_apng_path,
    text_box_image,
    font,
    draw_animated_background,
    draw_animated_pokemon,
    wrap_text,
):
    phase2_seconds = 6.0
    phase2_frames = int(phase2_seconds * 60)

    text_phase2 = f"Félicitations ! {pokemon_name} a évolué en {evolved_name} !"
    char_index_p2 = 0
    char_delay = 3
    frame_counter_p2 = 0

    for _ in range(phase2_frames):
        draw_animated_background(screen, background_apng_path)
        draw_animated_pokemon(screen, evolution_path, (540, 360), scale=3.0)

        screen.blit(text_box_image, (0, 450))

        if char_index_p2 < len(text_phase2):
            frame_counter_p2 += 1
            if frame_counter_p2 >= char_delay:
                char_index_p2 += 1
                frame_counter_p2 = 0

        displayed_text = text_phase2[:char_index_p2]
        wrapped_lines = wrap_text(displayed_text, font, 980)
        for index, line in enumerate(wrapped_lines):
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (250, 520 + index * 20))

        pygame.display.flip()
        clock.tick(60)
