import pygame
from Pokedex.logic.Pokemon import Pokemon
from evolution.graphic.menu_evolution_graphics import (
    load_animated_background,
    draw_animated_pokemon,
)

CO_POKE = 150

class Mon_Pokemon(Pokemon):
    def __init__(
        self,
        id,
        name,
        type,
        image,
        coord,
        hp,
        attack,
        defense,
        level,
        xp,
        degat_recu=0,
        full_hp=True,
        evo=None,
        sub_evo=None,
        hidden=False,
    ):
        super().__init__(id, name, type, image, coord, hp, attack, defense, level, xp, evo, sub_evo, hidden)
        self.coord = CO_POKE
        self.image = pygame.transform.flip(self.image, True, False)
        self.static_image = self.image.copy()
        self.image_path = f"Asset/front/{int(self.id)}.png"

        try:
            load_animated_background(self.image_path)
            self.use_apng = True
        except Exception:
            self.use_apng = False

        self.hp_max = self.hp
        self.degat_recu = degat_recu
        self.full_hp = full_hp

    def afficher(self, screen):
        if self.use_apng:
            draw_animated_pokemon(screen, self.image_path, (self.coord + 75, 525), scale=1.8, flip_horizontal=True)
        else:
            image = pygame.transform.scale(self.static_image, (150, 150))
            screen.blit(image, (self.coord, 450))