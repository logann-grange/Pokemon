import json
import os
import pygame
import Feuille


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
	leafs = Feuille.init_leafs(leaf, 20)
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

	minus_music_rect = pygame.Rect(360, 260, 60, 50)
	plus_music_rect = pygame.Rect(660, 260, 60, 50)
	minus_sfx_rect = pygame.Rect(360, 350, 60, 50)
	plus_sfx_rect = pygame.Rect(660, 350, 60, 50)
	mute_rect = pygame.Rect(360, 450, 360, 60)

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				raise SystemExit

			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if minus_music_rect.collidepoint(event.pos):
					options["music_volume"] = round(_clamp(options["music_volume"] - 0.1), 1)
				elif plus_music_rect.collidepoint(event.pos):
					options["music_volume"] = round(_clamp(options["music_volume"] + 0.1), 1)
				elif minus_sfx_rect.collidepoint(event.pos):
					options["sfx_volume"] = round(_clamp(options["sfx_volume"] - 0.1), 1)
				elif plus_sfx_rect.collidepoint(event.pos):
					options["sfx_volume"] = round(_clamp(options["sfx_volume"] + 0.1), 1)
				elif mute_rect.collidepoint(event.pos):
					options["mute"] = not options["mute"]
				elif button_return.get_rect(topleft=(40, 30)).collidepoint(event.pos):
					running = False

				apply_audio_options(options)
				_, sfx_volume = get_effective_volumes(options)
				hover_sound.set_volume(sfx_volume)
				save_audio_options(options)

		mouse_pos = pygame.mouse.get_pos()

		screen.blit(menu_background, (0, 0))

		for flake in leafs:
			flake.update()
		for flake in leafs:
			flake.draw(screen)

		title_surface = font_title.render("Options Audio", True, (255, 255, 255))
		screen.blit(title_surface, (390, 150))

		pygame.draw.rect(screen, (35, 35, 35), minus_music_rect, border_radius=8)
		pygame.draw.rect(screen, (35, 35, 35), plus_music_rect, border_radius=8)
		pygame.draw.rect(screen, (35, 35, 35), minus_sfx_rect, border_radius=8)
		pygame.draw.rect(screen, (35, 35, 35), plus_sfx_rect, border_radius=8)
		pygame.draw.rect(screen, (35, 35, 35), mute_rect, border_radius=8)

		music_text = font_text.render(f"Musique: {int(options['music_volume'] * 100)}%", True, (255, 255, 255))
		sfx_text = font_text.render(f"Effets: {int(options['sfx_volume'] * 100)}%", True, (255, 255, 255))
		mute_state = "ON" if options["mute"] else "OFF"
		mute_text = font_text.render(f"Mute: {mute_state}", True, (255, 255, 255))

		minus_text = font_text.render("-", True, (255, 255, 255))
		plus_text = font_text.render("+", True, (255, 255, 255))

		screen.blit(music_text, (430, 270))
		screen.blit(sfx_text, (430, 360))
		screen.blit(mute_text, (500, 465))

		screen.blit(minus_text, (385, 268))
		screen.blit(plus_text, (683, 268))
		screen.blit(minus_text, (385, 358))
		screen.blit(plus_text, (683, 358))

		if button_return.get_rect(topleft=(40, 30)).collidepoint(mouse_pos):
			screen.blit(button_return_hover, (40, 30))
			if not prev_hover_return:
				hover_sound.play()
			prev_hover_return = True
		else:
			screen.blit(button_return, (40, 30))
			prev_hover_return = False

		pygame.display.flip()
		clock.tick(60)

	return options