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

        """
        t1=self.poke.type
        t2=self.opponent.type
        first_type=t1[0]
        o_first_type=t2[0]
        for weak in first_type.weaknesses:
            if o_first_type==weak:
                damage=(self.poke.attack)*2

        for resist in first_type.resistances:
            if o_first_type==resist:
                damage=(self.poke.attack)/2

        for immun in first_type.immunities:
            if o_first_type==immun:
                damage=0
        """

        damage=self.poke.attack
        self.opponent.hp-=damage
        if self.opponent.hp<=0:
            return fight.end_game()
        print(self.opponent.hp)
        return fight.oppo_attack()
    
    def oppo_attack(self):
        """
        t1=self.poke.type
        t2=self.opponent.type
        first_type=t1[0]
        o_first_type=t2[0]
        for weak in o_first_type.weaknesses:
            if first_type==weak:
                damage=(self.opponent.attack)*2

        for resist in o_first_type.resistances:
            if first_type==resist:
                damage=(self.opponent.attack)/2

        for immun in o_first_type.immunities:
            if first_type==immun:
                damage=0
        """

        damage=self.opponent.attack
        self.poke.hp-=damage
        if self.poke.hp<=0:
            return fight.end_game()
        print(self.poke.hp)
        return fight.attack()

    def end_game(self):
        if self.poke.hp>self.opponent.hp<=0:
            return f"{self.poke.name} win the fight"
        elif self.opponent.hp>self.poke.hp<=0:
            return f"{self.opponent.name} win the fight"
        
    

pika=Pokemon(1,"Pika",1,1,180,50,50,5,780)
leviator=Pokemon(1,"Leviator",1,1,180,50,50,5,780)
fight=Combat(pika,leviator)
toast=randint(1,2)
print(fight.heads_or_tails())

