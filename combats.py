from Pokedex.logic.Pokemon import *
from random import randint
from dic_type import type_poke
import pygame

FIN="fin"
COMBAT="combat"

class Combat:
    def __init__(self,opponent,poke,hp_font,font,etat,screen=None):
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
        self.xp_gain = 0
        self.xp_given = False

    def calculate_xp_gain(self):
        level_gap = self.opponent.level - self.poke.level
        base_xp = 30
        enemy_level_xp = self.opponent.level * 12
        bonus = max(0, level_gap * 6)
        return max(10, int(base_xp + enemy_level_xp + bonus))
        


    def attack_mult(self):
        mult=1
        for element in type_poke:
            if element==self.poke.type:
                for types in type_poke[element]:
                    nv_dico=type_poke[element]
                    if types==self.opponent.type:
                        mult=nv_dico[types]
        damage=self.poke.attack
        self.opponent.hp-=damage*mult
        self.opponent.degat_recu+=damage
        self.opponent.full_hp=False
        if self.opponent.hp<=0:
            return self.end_game()
        
        
        
    
    def attack (self):
        damage=self.poke.attack
        self.opponent.hp-=damage
        self.opponent.degat_recu+=damage
        self.opponent.full_hp=False
        if self.opponent.hp<=0:
            return self.end_game()
        

    def oppo_attack(self):
        mult=1
        for element in type_poke:
            if element==self.opponent.type:
                for types in type_poke[element]:
                    nv_dico=type_poke[element]
                    if types==self.poke.type:
                        mult=nv_dico[types]
        damage=self.opponent.attack
        self.poke.hp-=damage*mult
        if self.poke.hp<=0:
            return self.end_game()
        self.poke.degat_recu+=damage
        self.poke.full_hp=False
        

    #barre de vie 
    def hp_lvl(self):

        txt_hp_poke = str(self.poke.hp)
        txt_hp_poke += "HP"
        txt_hp_poke=self.hp_font.render(txt_hp_poke, True, (0,0,0))
        txt_hp_adv = str(self.opponent.hp)
        txt_hp_adv += "HP"
        txt_hp_adv=self.hp_font.render(txt_hp_adv, True, (0,0,0))

        pygame.draw.rect(self.screen,(255,255,255),(150,650,150,30))
        self.screen.blit(txt_hp_poke,(200,690))
        self.screen.blit(txt_hp_adv,(800,690))
        if self.poke.full_hp==True:
            pygame.draw.rect(self.screen,(0,0,0),(155,655,140,20))
        else:
            longueur=px_hp*self.poke.hp
            pygame.draw.rect(self.screen,(0,0,0),(155,655,longueur,20))
        pygame.draw.rect(self.screen,(255,255,255),(750,650,150,30))
        if self.opponent.full_hp==True:
            pygame.draw.rect(self.screen,(0,0,0),(755,655,140,20))
        else:
            longueur_a=px_hp_a*self.opponent.hp
            pygame.draw.rect(self.screen,(0,0,0),(755,655,longueur_a,20))

    def end_game(self):

        txt_win="YOU WIN !"
        txt_win= self.font.render(txt_win,True,(0,0,155))
        txt_lose="YOU LOSE !"
        txt_lose= self.font.render(txt_lose,True,(255,0,0))
        txt_catch="YOU CATCH IT"
        txt_catch=self.font.render(txt_catch,True,(0,0,255))
        temps_debut=0
        temps_debut=pygame.time.get_ticks()
        

        if self.etat==COMBAT:
            if self.opponent.hp<=0:
                if pygame.time.get_ticks()- temps_debut<=100000:
                    self.screen.blit(txt_win,(380,160))
                    if not self.xp_given:
                        self.xp_gain = self.calculate_xp_gain()
                        self.poke.xp += self.xp_gain
                        self.poke.level_up()
                        self.xp_given = True
                    self.etat=FIN
            elif self.poke.hp<=0:
                if pygame.time.get_ticks()- temps_debut<=100000:
                    self.screen.blit(txt_lose,(380,160))
                    self.etat=FIN
            else:
                if pygame.time.get_ticks()- temps_debut<=100000:
                    self.screen.blit(txt_catch,(380,160))
                    self.etat=FIN

    
        elif self.etat==FIN:
            self.screen.fill((0,0,0))
            if self.poke.hp<=0:
                self.screen.blit(txt_lose,(500,240))
            elif self.opponent.hp<=0:
                self.screen.blit(txt_win,(500,240))
                txt_xp = self.hp_font.render(f"+{self.xp_gain} XP", True, (255, 255, 255))
                self.screen.blit(txt_xp, (530, 300))
            else:
                self.screen.blit(txt_catch,(500,240))

            


#ajout pokball
#ajout fuite