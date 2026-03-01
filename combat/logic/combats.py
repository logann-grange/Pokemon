from Pokedex.logic.Pokemon import *
from random import randint
from combat.logic.dic_type import type_poke
import pygame
import json
import os

FIN="fin"
COMBAT="combat"
temps_debut=0

class Combat:
    def __init__(self,opponent,poke,hp_font,font,etat,poke_turn=True,adv_turn=False,screen=None):
        self.opponent=opponent
        self.poke=poke
        self.hp_font=hp_font
        self.font=font
        self.etat=etat
        self.screen=screen
        global px_hp
        global px_hp_a
        px_hp=140/self.poke.hp
        px_hp_a=140/self.opponent.hp
        self.poke_turn=poke_turn
        self.adv_turn=adv_turn
        self.xp_gain = 0
        self.xp_given = False
        self.effectiveness_text = ""
        self.effectiveness_color = (0,0,0)
        self.effectiveness_until = 0
        self.player_accuracy = 85
        self.enemy_accuracy = 85

    def add_captured_pokemon_to_team(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        equipe_file = os.path.join(project_root, "data", "equipe.json")

        try:
            with open(equipe_file, "r", encoding="utf-8") as file:
                equipe = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            equipe = []

        if not isinstance(equipe, list):
            equipe = []

        used_indexes = set()
        for member in equipe:
            idx = member.get("index_team")
            if isinstance(idx, int) and 0 <= idx <= 5:
                used_indexes.add(idx)

        assigned_index = None
        for idx in range(6):
            if idx not in used_indexes:
                assigned_index = idx
                break

        captured_data = {
            "id": int(self.opponent.id),
            "name": self.opponent.name,
            "type": self.opponent.type,
            "hp": int(max(self.opponent.hp, 1)),
            "hp_base": int(self.opponent.hp_base),
            "attack": int(self.opponent.attack),
            "attack_base": int(self.opponent.attack_base),
            "defense": int(self.opponent.defense),
            "defense_base": int(self.opponent.defense_base),
            "level": int(self.opponent.level),
            "xp": int(self.opponent.xp),
            "index_team": assigned_index,
        }

        equipe.append(captured_data)

        with open(equipe_file, "w", encoding="utf-8") as file:
            json.dump(equipe, file, indent=4, ensure_ascii=False)

    def set_battle_message(self, text, color=(0,0,0), duration_ms=1500):
        self.effectiveness_text = text
        self.effectiveness_color = color
        self.effectiveness_until = pygame.time.get_ticks() + duration_ms

    def attack_lands(self, accuracy):
        return randint(1, 100) <= accuracy

    def normalize_types(self, poke_type):
        if isinstance(poke_type, list):
            raw_types = []
            for value in poke_type:
                if isinstance(value, str):
                    parts = [item.strip() for item in value.split(",") if item.strip()]
                    raw_types.extend(parts)
        elif isinstance(poke_type, str):
            raw_types = [item.strip() for item in poke_type.split(",") if item.strip()]
        else:
            raw_types = []

        type_alias = {
            "Insect": "Bug",
            "Psychic": "Psy",
        }

        normalized = []
        for element in raw_types:
            normalized.append(type_alias.get(element, element))

        return normalized

    def get_type_multiplier(self, attacker, defender):
        attacker_types = self.normalize_types(attacker.type)
        defender_types = self.normalize_types(defender.type)

        if not attacker_types:
            return 1

        attack_type = attacker_types[0]

        if not defender_types:
            return 1

        mult = 1
        for defend_type in defender_types:
            defend_chart = type_poke.get(defend_type, {})
            mult *= defend_chart.get(attack_type, 1)

        return mult



    #=====NEUTRE=====#
    def calculate_xp_gain(self):
        level_gap = self.opponent.level - self.poke.level
        base_xp = 30
        enemy_level_xp = self.opponent.level * 12
        bonus = max(0, level_gap * 6)
        return max(10, int(base_xp + enemy_level_xp + bonus))

    def give_xp(self):
        if self.xp_given:
            return
        self.xp_gain = self.calculate_xp_gain()
        self.poke.xp += self.xp_gain
        self.poke.level_up()
        self.xp_given = True

    def set_effectiveness_text(self, mult, enemy=False):
        if mult > 1:
            if enemy:
                self.set_battle_message("Attaque ennemie super efficace !", (220, 30, 30))
            else:
                self.set_battle_message("C'est super efficace !", (220, 30, 30))
        elif mult < 1:
            if enemy:
                self.set_battle_message("Attaque ennemie peu efficace...", (80, 80, 80))
            else:
                self.set_battle_message("Ce n'est pas tres efficace...", (80, 80, 80))
        

    def attraper(self):
        self.give_xp()
        self.add_captured_pokemon_to_team()
        self.etat=FIN
        self.opponent.hidden=False
        self.opponent.find=True
        self.end_game()
            
      
      
        
    #======DEFENSE======#   
    def defensive (self):

        if self.poke_turn:
            while self.opponent.defense>self.poke.attack:
                self.opponent.defense = int(self.opponent.defense / 1.5)
                if self.opponent.defense <= 0:
                    self.opponent.defense = 0
                    break
            return int(self.opponent.defense)
        
        elif self.adv_turn:
            while self.poke.defense>self.opponent.attack:
                self.poke.defense = int(self.poke.defense / 1.5)
                if self.poke.defense <= 0:
                    self.poke.defense = 0
                    break
            return int(self.poke.defense)


    #======ATTAQUE======#
    def attack_mult(self):
        mult = self.get_type_multiplier(self.poke, self.opponent)

        if not self.attack_lands(self.player_accuracy):
            self.set_battle_message("Votre attaque a rate !", (120, 120, 120))
            return 0
    
        damage = self.poke.attack
        damage -= self.defensive()
        damage = max(1, int(damage * mult))
        self.set_effectiveness_text(mult)
        self.opponent.hp = max(0, int(self.opponent.hp - damage))
        self.opponent.full_hp=False
        if self.opponent.hp<=0:
            return self.end_game()
        return damage
        
    def attack (self):

        if not self.attack_lands(self.player_accuracy):
            self.set_battle_message("Votre attaque a rate !", (120, 120, 120))
            return 0

        damage = self.poke.attack
        damage -= self.defensive()
        damage = max(1, int(damage))
        self.set_effectiveness_text(1)
        self.opponent.hp = max(0, int(self.opponent.hp - damage))
        self.opponent.full_hp=False
        if self.opponent.hp<=0:
            return self.end_game()
        
    def oppo_attack(self):
        mult = self.get_type_multiplier(self.opponent, self.poke)

        if not self.attack_lands(self.enemy_accuracy):
            self.set_battle_message("L'attaque ennemie a rate !", (120, 120, 120))
            return 0

        damage = self.opponent.attack
        damage -= self.defensive()
        damage = max(1, int(damage * mult))
        self.set_effectiveness_text(mult, enemy=True)
        self.poke.hp = max(0, int(self.poke.hp - damage))
        if self.poke.hp<=0:
            return self.end_game()
        self.poke.full_hp=False
        

    #======AFFICHAGE======# 
    def hp_lvl(self):

        longueur = 140
        hauteur = 20
    
        ratio_poke = max(self.poke.hp, 0) / self.poke.hp_max
        longueur_poke = int(longueur * ratio_poke)
        couleur_poke = (0,200,0) if ratio_poke > 0.5 else (255,165,0) if ratio_poke > 0.25 else (200,0,0)
    
        pygame.draw.rect(self.screen, (100,100,100), (155, 655, longueur, hauteur))
        pygame.draw.rect(self.screen, couleur_poke, (155, 655, longueur_poke, hauteur))
    
        ratio_adv = max(self.opponent.hp, 0) / self.opponent.hp_max
        longueur_adv = int(longueur * ratio_adv)
        couleur_adv = (0,200,0) if ratio_adv > 0.5 else (255,165,0) if ratio_adv > 0.25 else (200,0,0)
    
        pygame.draw.rect(self.screen, (100,100,100), (750, 655, longueur, hauteur))
        pygame.draw.rect(self.screen, couleur_adv, (750, 655, longueur_adv, hauteur))
    
        txt_hp_poke = self.hp_font.render(str(max(int(self.poke.hp), 0)) + " HP", True, (0,0,0))
        txt_hp_adv  = self.hp_font.render(str(max(int(self.opponent.hp), 0)) + " HP", True, (0,0,0))
        txt_lvl_poke = self.hp_font.render(f"Niv. {self.poke.level}", True, (0,0,0))
        txt_lvl_adv = self.hp_font.render(f"Niv. {self.opponent.level}", True, (0,0,0))
        self.screen.blit(txt_hp_poke, (200, 690))
        self.screen.blit(txt_hp_adv,  (800, 690))
        self.screen.blit(txt_lvl_poke, (165, 632))
        self.screen.blit(txt_lvl_adv,  (760, 632))
        if self.effectiveness_text and pygame.time.get_ticks() <= self.effectiveness_until:
            txt_effective = self.hp_font.render(self.effectiveness_text, True, self.effectiveness_color)
            self.screen.blit(txt_effective, (430, 610))


    def end_game(self):

        txt_win=f"TU AS GAGNé ! Ton {self.poke.name} a battu {self.opponent.name}"
        txt_win= self.font.render(txt_win,True,(0,0,155))
        txt_lose=f"TU AS PERDU ! {self.opponent.name} a battu ton {self.poke.name}"
        txt_lose= self.font.render(txt_lose,True,(255,0,0))
        txt_catch=f"TU L'AS ATTRAPé ! {self.opponent.name} a été ajouté a ton pokedex"
        txt_catch=self.font.render(txt_catch,True,(0,0,255))
        txt_xp=f"+{self.xp_gain} XP"
        txt_xp=self.font.render(txt_xp,True,(255,255,255))
        

        if self.etat==COMBAT:

            if self.opponent.hp<=0:
                self.give_xp()
                self.screen.blit(txt_win,(380,160))
                self.etat=FIN

            elif self.poke.hp<=0:
                self.screen.blit(txt_lose,(380,160))
                self.etat=FIN

            else:
                self.screen.blit(txt_catch,(380,160))
                self.etat=FIN

    
        elif self.etat==FIN:

            self.screen.fill((0,0,0))

            if self.poke.hp<=0:
                self.screen.blit(txt_lose,(50,250))

            elif self.opponent.hp<=0:
                self.screen.blit(txt_win,(50,250))
                if self.xp_gain>0:
                    self.screen.blit(txt_xp,(50,300))

            else:
                self.screen.blit(txt_catch,(50,250))
                if self.xp_gain>0:
                    self.screen.blit(txt_xp,(50,300))