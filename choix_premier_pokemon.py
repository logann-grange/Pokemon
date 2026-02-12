from Pokemon import Pokemon
import json
import pygame
import os
from PIL import Image 


class MenuChoixPokemon:
    def __init__(self):
        pygame.init()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.pokemon_starter_list = [1, 4, 7]       
        self.pokemon_starter = []
        self._apng_cache = {}
        self._anim_state = {}
        self.choix_premier_pokemon()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = pygame.image.load(os.path.join(self.script_dir, "Asset", "Professor", "lab_background.jfif"))
        self.background = self._scale_to_cover(self.background, self.screen.get_size())
        self.background_rect = self.background.get_rect(center=self.screen.get_rect().center)
        self.professeur_chen = pygame.image.load(os.path.join(self.script_dir, "Asset", "Professor", "Professor_Oak.png"))
        self.professeur_chen = pygame.transform.scale(self.professeur_chen, (250, 300))
        self.dialogue_box=pygame.image.load(os.path.join(self.script_dir, "Asset", "Professor", "dialogue_box.png"))
        self.dialogue_box=pygame.transform.scale(self.dialogue_box, (800, 200))
    
    def _scale_to_cover(self, image, target_size):
        target_w, target_h = target_size
        img_w, img_h = image.get_size()

        # Scale to fully cover the screen while preserving aspect ratio.
        scale = max(target_w / img_w, target_h / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))
        return pygame.transform.smoothscale(image, new_size)
    

    def display_animated_img(self, apng_path, center_pos, state_key, scale=1.0):
        # Charger et mettre en cache les frames d'un APNG.
        if apng_path not in self._apng_cache:
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

            if not frames:
                return

            self._apng_cache[apng_path] = (frames, durations)

        frames, durations = self._apng_cache[apng_path]

        if state_key not in self._anim_state:
            self._anim_state[state_key] = {
                "last_update": pygame.time.get_ticks(),
                "current_frame": 0,
            }

        state = self._anim_state[state_key]
        now = pygame.time.get_ticks()
        duration = durations[state["current_frame"]] if durations else 100
        if now - state["last_update"] > duration:
            state["current_frame"] = (state["current_frame"] + 1) % len(frames)
            state["last_update"] = now

        frame = frames[state["current_frame"]]
        if scale != 1.0:
            new_size = (int(frame.get_width() * scale), int(frame.get_height() * scale))
            frame = pygame.transform.smoothscale(frame, new_size)
        frame_rect = frame.get_rect(center=center_pos)
        self.screen.blit(frame, frame_rect)
    
        
    def dialogue_professeur_chen(self):
        font_path = os.path.join(self.script_dir, "Asset", "menue", "Pixeled.ttf")
        if os.path.exists(font_path):
            font = pygame.font.Font(font_path, 15)
        else:
            font = pygame.font.Font(None, 15)
        text = "Bonjour, je suis le professeur Chen. Dans cette fabuleuse aventure, vous aurez besoin d'un compagnon fidèle. Choisissez votre premier Pokemon !"
        
        running = True
        char_index = 0
        clock = pygame.time.Clock()
        text_complete = False
        max_width = 700  # Largeur max du texte dans la boîte (800 - 100 pour les marges)
        
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
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    if text_complete:
                        return True
                    else:
                        char_index = len(text)
            
            # Afficher le texte petit à petit
            if char_index < len(text):
                char_index += 1
            else:
                text_complete = True
            
            self.screen.blit(self.background, self.background_rect)
            self.screen.blit(self.professeur_chen, (250, 200))
            self.screen.blit(self.dialogue_box, (0, 350))
            
            # Afficher le texte progressif avec retour à la ligne
            displayed_text = text[:char_index]
            text_lines = wrap_text(displayed_text, font, max_width)
            
            y_offset = 365
            for line in text_lines:
                text_surface = font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (50, y_offset))
                y_offset += 20  # Espacement entre les lignes
            
            pygame.display.flip()
            clock.tick(15)  # 15 caractères par seconde
    
    
    
    def choix_premier_pokemon(self):
        with open(os.path.join(self.script_dir, 'pokedex.json')) as f:
            data = json.load(f)    
        for pokemon in data:
            pokemon_id = int(pokemon['id'])
            if pokemon_id in self.pokemon_starter_list:
                stats = pokemon.get('stats', {})
                self.pokemon_starter.append(Pokemon(
                    int(pokemon['id']), 
                    pokemon['name'], 
                    pokemon['type'], 
                    pokemon['image'], 
                    pokemon.get('coord', []),
                    stats.get('hp', 0),
                    stats.get('attack', 0),
                    stats.get('defense', 0),
                    pokemon.get('level', 1),
                    pokemon.get('xp', 0)
                ))
    
    def affichage_choix_pokemon(self):
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, pokemon in enumerate(self.pokemon_starter):
                        image_path = os.path.join(self.script_dir, "Asset", "front", f"{int(pokemon.id)}.png")
                        image = pygame.image.load(image_path)
                        image_rect = image.get_rect(topleft=(200 + i*200, 300))
                        
                        if image_rect.collidepoint(mouse_pos):
                            print(f"Vous avez choisi {pokemon.name} !")
                            running = False
                            return pokemon
            
            self.screen.blit(self.background, self.background_rect)
            
            for i, pokemon in enumerate(self.pokemon_starter):
                image_path = os.path.join(self.script_dir, "Asset", "front", f"{int(pokemon.id)}.png")
                image = pygame.image.load(image_path)
                image_rect = image.get_rect(topleft=(200 + i*200, 300))
                
                # Animation APNG: zoom au survol, animation normale sinon
                if image_rect.collidepoint(mouse_pos):
                    self.display_animated_img(image_path, image_rect.center, f"starter_{pokemon.id}", scale=1.2)
                else:
                    self.display_animated_img(image_path, image_rect.center, f"starter_{pokemon.id}")
                
            pygame.display.flip()
            
        pygame.quit()

def lancer_choix_pokemon():
    
    """Fonction pour lancer le choix du premier Pokémon"""
    
    
    demarre = MenuChoixPokemon()
    if demarre.dialogue_professeur_chen():
        return demarre.affichage_choix_pokemon()
    return None

if __name__ == "__main__":
    choix = lancer_choix_pokemon()
