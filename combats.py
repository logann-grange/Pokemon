from Pokemon import *
from random import randint
from dic_type import type_poke
import pygame

FIN="fin"
COMBAT="combat"
temps_debut=0

class Combat:

    def __init__(self, opponent, poke, hp_font, font, etat, poke_turn=True, adv_turn=False, screen=None):
        self.opponent=opponent
        self.poke=poke
        self.hp_font=hp_font
        self.font=font
        self.etat=etat
        self.screen=screen
        self.poke_turn=poke_turn
        self.adv_turn=adv_turn



    #======NEUTRE======#
    def attraper(self):

        if self.opponent.hidden:
            self.etat==FIN
            self.opponent.hidden=False
            self.opponent.find=True
            self.end_game()

        else:
            self.etat=FIN
            txt_deja_catch = "Vous l'avez deja !"
            txt_deja_catch = self.font.render(txt_deja_catch,True, (255,255,255))
            self.screen.fill((0,0,0))
            self.screen.blit(txt_deja_catch,(500,250))

        
    #======DEFENSE======#   
    def defensive (self):

        if self.poke_turn:
            while self.opponent.defense>self.poke.attack:
                self.opponent.defense=self.opponent.defense/1.5
            return self.opponent.defense
        
        elif self.adv_turn:
            while self.poke.defense>self.opponent.attack:
                self.poke.defense=self.poke.defense/1.5
            return self.poke.defense



    #======ATTAQUE======#
    def attack_mult(self):
        self.temps_debut=pygame.time.get_ticks()
        mult=1
        for element in type_poke:
            if element==self.poke.type:
                for types in type_poke[element]:
                    nv_dico=type_poke[element]
                    if types==self.opponent.type:
                        mult=nv_dico[types]
    
        damage=self.poke.attack
        damage-=self.defensive()
        damage=damage*mult
        self.opponent.hp-=damage
        self.opponent.full_hp=False
        if self.opponent.hp<=0:
            return self.end_game()
        return int(damage)
        
    def attack (self):

        self.temps_debut=pygame.time.get_ticks()
        damage=self.poke.attack
        damage-=self.defensive()
        self.opponent.hp-=damage
        self.opponent.full_hp=False
        if self.opponent.hp<=0:
            return self.end_game()
        
    def oppo_attack(self):

        self.temps_debut=pygame.time.get_ticks()
        mult=1
        for element in type_poke:
            if element==self.opponent.type:
                for types in type_poke[element]:
                    nv_dico=type_poke[element]
                    if types==self.poke.type:
                        mult=nv_dico[types]

        damage=self.opponent.attack
        damage-=self.defensive()
        self.poke.hp-=damage*mult
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
    
        txt_hp_poke = self.hp_font.render(str(max(self.poke.hp, 0)) + " HP", True, (0,0,0))
        txt_hp_adv  = self.hp_font.render(str(max(self.opponent.hp, 0)) + " HP", True, (0,0,0))
        self.screen.blit(txt_hp_poke, (200, 690))
        self.screen.blit(txt_hp_adv,  (800, 690))

    def end_game(self):

        txt_win=f"TU AS GAGNé ! Ton {self.poke.name} a battu {self.opponent.name}"
        txt_win= self.font.render(txt_win,True,(0,0,155))
        txt_lose=f"TU AS PERDU ! {self.opponent.name} a battu ton {self.poke.name}"
        txt_lose= self.font.render(txt_lose,True,(255,0,0))
        txt_catch=f"TU L'AS ATTRAPé ! {self.opponent.name} a été ajouté a ton pokedex"
        txt_catch=self.font.render(txt_catch,True,(0,0,255))
        

        if self.etat==COMBAT:

            if self.opponent.hp<=0:
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

            else:
                self.screen.blit(txt_catch(50,250))

            


#ajout pokball (images)