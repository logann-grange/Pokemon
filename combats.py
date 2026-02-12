from Pokemon import *
from random import randint
from dic_type import type_poke

class Combat:
    def __init__(self,opponent,poke):
        self.opponent=opponent
        self.poke=poke

    def heads_or_tails(self):
        hot=int(input("Heads or Tails ? (1 or 2)"))
        if hot==randint(1,2):
            print("You start !")
            return fight.attack()
        else:
            print("Your oppenent starts !")
            return fight.oppo_attack()

    def attack(self):
        mult=1
        for element in type_poke:
            if element==self.poke.type:
                for types in type_poke[element]:
                    nv_dico=type_poke[element]
                    if types==self.opponent.type:
                        mult=nv_dico[types]

        damage=self.poke.attack
        self.opponent.hp-=damage*mult
        if self.opponent.hp<=0:
            return fight.end_game()
        print(f"{self.opponent.name} a {self.opponent.hp} HP")
        return fight.oppo_attack()
    
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
            return fight.end_game()
        print(f"{self.poke.name} a {self.poke.hp} HP")
        return fight.attack()

    def end_game(self):
        if self.poke.hp>self.opponent.hp<=0:
            return f"{self.poke.name} win the fight"
        elif self.opponent.hp>self.poke.hp<=0:
            return f"{self.opponent.name} win the fight"
        
fight=Combat()