from Pokemon import *
from random import randint

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
        
        for element in dico_type:
            if element==self.poke.type:
                for types in dico_type[element]:
                    nv_dico=dico_type[element]
                    if types==self.opponent.type:
                        mult=nv_dico[types]

        damage=self.poke.attack
        self.opponent.hp-=damage*mult
        if self.opponent.hp<=0:
            return fight.end_game()
        print(f"{self.opponent.name} a {self.opponent.hp} HP")
        return fight.oppo_attack()
    
    def oppo_attack(self):
        for element in dico_type:
            if element==self.opponent.type:
                for types in dico_type[element]:
                    nv_dico=dico_type[element]
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
        
    

pika=Pokemon(1,"Pika",1,1,180,50,50,5,780,"feu")
leviator=Pokemon(1,"Leviator",1,1,180,50,50,5,780,"acier")
fight=Combat(pika,leviator)
print(fight.heads_or_tails())
