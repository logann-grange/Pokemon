import pygame
from PIL import Image


_apng_cache = {}
_anim_state = {}


def load_animated_background(apng_path):
    if apng_path not in _apng_cache:
        apng = Image.open(apng_path)
        frames = []
        durations = []

        try:
            while True:
                frame = apng.convert("RGBA")

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
                "last_update": pygame.time.get_ticks(),
            }


def draw_animated_background(screen, apng_path, scale_to_screen=True):
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
        frame = pygame.transform.scale(frame, screen.get_size())

    screen.blit(frame, (0, 0))


def draw_animated_pokemon(screen, apng_path, position, scale=1.0, white_filter=False):
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

    if white_filter:
        frame.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)

    frame_rect = frame.get_rect(center=position)
    screen.blit(frame, frame_rect)


def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.rstrip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.rstrip())

    return lines
