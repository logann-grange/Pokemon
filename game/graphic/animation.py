import os
import sys
import pygame
from PIL import Image

# Ajouter la racine du projet au path pour les imports absolus
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
os.chdir(project_root)

from Pokedex.logic.Pokedex import Pokedex
from Pokedex.graphic.interface_pokedex import screen

clock = pygame.time.Clock()
last_update = pygame.time.get_ticks()
current_frame = 0

def display_animated_img(last_update, current_frame) :
    # Charger le PNG animé
    apng = Image.open("Asset/image/pokemon/dardargnan.png")
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