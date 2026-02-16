from Pokemon import *
from random import randint
from dic_type import type_poke
import pygame

end_font=pygame.font.SysFont("Arial",45)

txt_win="YOU WIN !"
txt_win= end_font.render(txt_win,True,(0,0,155))
txt_lose="YOU LOSE !"
txt_lose= end_font.render(txt_lose,True,(255,0,0))
txt_catch="YOU CATCH IT"
txt_catch=end_font.render(txt_catch,True,(0,0,255))

class Combat:
    def __init__(self,opponent,poke,screen=None):
        self.opponent=opponent
        self.poke=poke
        self.screen=screen

    def attack_mult(self):
        mult=1
        for element in type_poke:
            if element==self.poke.type:
                for types in type_poke[element]:
                    nv_dico=type_poke[element]
                    if types==self.opponent.type:
                        mult=nv_dico[types]
        print(f"{self.opponent.name} a {self.opponent.hp} HP")
        damage=self.poke.attack
        self.opponent.hp-=damage*mult
        if self.opponent.hp<=0:
            return self.end_game()
        
        self.opponent.degat_recu+=damage
        self.opponent.full_hp=False
    
    def attack (self):
        damage=self.poke.attack
        self.opponent.hp-=damage
        print(f"{self.opponent.name} a {self.opponent.hp} HP")
        self.opponent.degat_recu+=damage
        self.opponent.full_hp=False
        if self.opponent.hp<=0:
            return self.end_game()
        else:
            return self.oppo_attack()
        

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
        print(f"{self.poke.name} a {self.poke.hp} HP")
        self.poke.degat_recu+=damage
        self.poke.full_hp=False
        return self.attack()

    #barre de vie 
    def hp_lvl(self):
        pygame.draw.rect(self.screen,(255,255,255),(150,650,150,30))
        if self.poke.full_hp==True:
            pygame.draw.rect(self.screen,(0,0,0),(155,655,140,20))
        else:
            if self.poke.degat_recu>0:
                longueur=140/self.poke.degat_recu
                pygame.draw.rect(self.screen,(0,0,0),(155,655,longueur,20))
        pygame.draw.rect(self.screen,(255,255,255),(750,650,150,30))
        if self.opponent.full_hp==True:
            pygame.draw.rect(self.screen,(0,0,0),(755,655,140,20))
        else:
            longueur=140/self.opponent.degat_recu
            pygame.draw.rect(self.screen,(0,0,0),(755,655,longueur,20))

    def end_game(self):
        if self.opponent.hp<=0:
            screen.blit(txt_win,(380,160))
        elif self.poke.hp<=0:
            screen.blit(txt_lose,(380,160))
        else:
            screen.blit(txt_catch,(380,160))


    



#ajout attaque avec et sans multiplicateur
#ajout pokball
#ajout fuite