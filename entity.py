import pygame
import json
import os
from Pokedex.logic.Pokemon import Pokemon
from game.logic.apparition_pokemon import apparition_pokemon
from switch import Switch
import random
import interface_combat

class Entity(pygame.sprite.Sprite) :

    def __init__(self):
        super().__init__()
        self.sprite_sheet = pygame.image.load("Asset/player_walk.png")
        self.image = self.split_image(0, 0, 24, 32)
        self.all_images = self.get_all_images()
        self.pos = [350, 150]#[219, 155]
        self.rect = pygame.Rect(0, 0, 16, 32)
        self.hitbox = self.hitbox = pygame.Rect(self.pos[0], self.pos[1] + 16, 16, 16)
        self.is_walking = False
        self.speed = 1
        self.step = 0
        self.animation_walk = False
        self.direction = "down"
        self.animation_clock = 0
        self.index_image = 0
        self.list_pokemon = self.load_pokemon_list()
        self.switch : list[Switch] = None
        self.change_map = None
        self.collision = None
        self.attack_chance = 0
        self.map = ""
        self.able_pc = False
        self.pc = None



    def split_image(self, x, y, width, height) :
        return self.sprite_sheet.subsurface(pygame.Rect(x, y, width, height))

    def update(self) :
        self.rect.topleft = (self.pos[0], self.pos[1])
        self.pos[0] = self.hitbox.x
        self.pos[1] = self.hitbox.y - 16  # sprite 16px au-dessus de la hitbox
        self.rect.topleft = (self.pos[0], self.pos[1])
    
    def move_right(self) :
        self.direction = "right"
        self.animation_walk = True
        self.move()

    def move_left(self) :
        self.direction = "left"
        self.animation_walk = True
        self.move()


    def move_down(self) :
        self.direction = "down"
        self.animation_walk = True
        self.move()

    
    def move_up(self) :
        self.direction = "up"
        self.animation_walk = True
        self.move()
    
    def move(self):
        self.check_collision_switch()
        if self.animation_walk:
            if self.step < 16:
                next_pos = self.hitbox.copy()
                if self.direction == "left":  next_pos.x -= self.speed
                if self.direction == "right": next_pos.x += self.speed
                if self.direction == "up":    next_pos.y -= self.speed
                if self.direction == "down":  next_pos.y += self.speed

                if not self.check_collision(next_pos):
                    self.step += 1
                    self.hitbox.topleft = next_pos.topleft
                    if self.map == "foret" :
                        self.attack_chance += 1
                        self.attack()

                if self.check_collision_pc(next_pos):
                    self.able_pc = True
                else :
                    self.able_pc = False
            else:
                self.step = 0
                self.animation_walk = False
                


    def get_all_images(self) :
        all_images = {
            "down" : [],
            "left" : [],
            "right" : [],
            "up" : []
        }
        for i in range(4) :
            for j, key in enumerate(all_images.keys()) :
                all_images[key].append( self.split_image(i*24, j*32, 24, 32))
        return all_images
    

    def load_pokemon_list(self) :
        list_pokemon = []
        project_root = os.path.abspath(os.path.dirname(__file__))
        equipe_file = os.path.join(project_root, "equipe.json")
        pokedex_file = os.path.join(project_root, "pokedex.json")
        
        with open(equipe_file, "r", encoding="utf-8") as file :
            equipe_content = json.load(file)
        
        with open(pokedex_file, "r", encoding="utf-8") as file :
            pokedex_content = json.load(file)
        
        for pokemon_data in equipe_content:
            # Trouver les infos complètes dans le pokedex
            pokemon_info = None
            for poke in pokedex_content:
                if int(poke["id"]) == int(pokemon_data["id"]):
                    pokemon_info = poke
                    break
            
            if pokemon_info:
                list_pokemon.append(Pokemon(
                    pokemon_data["id"], 
                    pokemon_data["name"], 
                    pokemon_data["type"],  
                    pokemon_info.get("image", ""),
                    pokemon_info.get("coord", []), 
                    pokemon_data["hp_base"], 
                    pokemon_data["attack_base"], 
                    pokemon_data["defense_base"], 
                    pokemon_data.get("level", 1), 
                    pokemon_data.get("xp", 0), 
                    pokemon_info.get("evo", ""), 
                    pokemon_info.get("sub_evo", ""), 
                    pokemon_info.get("hidden", True)
                ))

        return list_pokemon

    def save_pokemon_list(self):
        project_root = os.path.abspath(os.path.dirname(__file__))
        equipe_file = os.path.join(project_root, "equipe.json")

        equipe_content = []
        for pokemon in self.list_pokemon:
            equipe_content.append({
                "id": int(pokemon.id),
                "name": pokemon.name,
                "type": pokemon.type,
                "hp": int(pokemon.hp),
                "hp_base": int(pokemon.hp_base),
                "attack": int(pokemon.attack),
                "attack_base": int(pokemon.attack_base),
                "defense": int(pokemon.defense),
                "defense_base": int(pokemon.defense_base),
                "level": int(pokemon.level),
                "xp": int(pokemon.xp)
            })

        with open(equipe_file, "w", encoding="utf-8") as file:
            json.dump(equipe_content, file, indent=4, ensure_ascii=False)
    
    def walk_animation(self) :
        self.animation_clock+=1
        if self.animation_walk and self.animation_clock >= 10:
            self.index_image += 1
            self.index_image %= 4
            self.animation_clock = 0
            self.image = self.all_images[self.direction][self.index_image]

    def add_switch(self, switchs) :
        self.switch = switchs

    def check_collision_switch(self) :
        for switch in self.switch :
            if self.hitbox.colliderect(switch.hitbox) :
                self.change_map = switch
                return True
    
        self.speed = 1

    def add_collision(self, collision) :
        self.collision = collision

    def check_collision(self, rect=None):
        if rect is None:
            rect = self.hitbox
        for collision in self.collision:
            if rect.colliderect(collision):
                return True
        return False
    
    def check_collision_pc(self, rect=None):
        if rect is None:
            rect = self.hitbox
        for pc in self.pc:
            if rect.colliderect(pc):
                return True
        return False
    
    def attack(self) :
        proba = random.randint(self.attack_chance, 1000)
        if proba == 1000 :
            if self.list_pokemon and len(self.list_pokemon) > 0:
                ennemy= apparition_pokemon()
                interface_combat.game_loop(self.list_pokemon[0], ennemy)
                self.save_pokemon_list()
            self.attack_chance = 0