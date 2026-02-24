import os
import sys
import json
import pygame

# Ajouter la racine du projet au path pour les imports absolus
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
os.chdir(project_root)

from menue.graphic.Feuille import init_leafs
from menue.events.menu_option_events import handle_menu_option_event
from menue.graphic.menu_option_render import draw_menu_option_frame


OPTIONS_FILE = "options.json"
DEFAULT_OPTIONS = {
	"music_volume": 0.7,
	"sfx_volume": 0.7,
	"mute": False,
}


def _clamp(value, minimum=0.0, maximum=1.0):
	return max(minimum, min(maximum, value))


def load_audio_options():
	if not os.path.exists(OPTIONS_FILE):
		save_audio_options(DEFAULT_OPTIONS)
		return DEFAULT_OPTIONS.copy()

	try:
		with open(OPTIONS_FILE, "r", encoding="utf-8") as file:
			data = json.load(file)
	except (json.JSONDecodeError, OSError):
		save_audio_options(DEFAULT_OPTIONS)
		return DEFAULT_OPTIONS.copy()

	options = DEFAULT_OPTIONS.copy()
	options.update(data)
	options["music_volume"] = _clamp(float(options.get("music_volume", 0.7)))
	options["sfx_volume"] = _clamp(float(options.get("sfx_volume", 0.7)))
	options["mute"] = bool(options.get("mute", False))
	return options


def save_audio_options(options):
	with open(OPTIONS_FILE, "w", encoding="utf-8") as file:
		json.dump(options, file, indent=4, ensure_ascii=False)


def get_effective_volumes(options):
	if options["mute"]:
		return 0.0, 0.0
	return options["music_volume"], options["sfx_volume"]


def apply_audio_options(options):
	music_volume, _ = get_effective_volumes(options)
	pygame.mixer.music.set_volume(music_volume)


def menu_option(screen):
	pygame.display.set_caption("Options Audio")
	clock = pygame.time.Clock()

	menu_background = pygame.image.load("./Asset/menue/background_menu.jpg")
	leaf = pygame.image.load("./Asset/menue/leaf.png")
	leafs = init_leafs(leaf, 20)
	button_return = pygame.image.load("./Asset/menue/button_return.png")
	button_return_hover = pygame.image.load("./Asset/menue/button_return_hover.png")
	hover_sound = pygame.mixer.Sound("./Asset/menue/hover.mp3")

	font_title = pygame.font.Font(None, 64)
	font_text = pygame.font.Font(None, 42)

	options = load_audio_options()
	apply_audio_options(options)
	_, sfx_volume = get_effective_volumes(options)
	hover_sound.set_volume(sfx_volume)

	prev_hover_return = False
	running = True

	rects = {
		"minus_music": pygame.Rect(360, 260, 60, 50),
		"plus_music": pygame.Rect(660, 260, 60, 50),
		"minus_sfx": pygame.Rect(360, 350, 60, 50),
		"plus_sfx": pygame.Rect(660, 350, 60, 50),
		"mute": pygame.Rect(360, 450, 360, 60),
	}
	button_return_rect = button_return.get_rect(topleft=(40, 30))

	while running:
		for event in pygame.event.get():
			running, has_changed = handle_menu_option_event(event, rects, options, button_return_rect)
			if has_changed:
				apply_audio_options(options)
				_, sfx_volume = get_effective_volumes(options)
				hover_sound.set_volume(sfx_volume)
				save_audio_options(options)

		prev_hover_return = draw_menu_option_frame(
			screen,
			menu_background,
			leafs,
			font_title,
			font_text,
			options,
			rects,
			button_return,
			button_return_hover,
			button_return_rect,
			prev_hover_return,
			hover_sound,
		)

		pygame.display.flip()
		clock.tick(60)

	return options