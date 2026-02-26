import os
import sys
import json

# Ajouter la racine du projet au path pour les imports absolus
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from evolution.menu_evolution import evolution

class Pokemon() :

    def __init__(self, id, name, type, image, coord, hp, attack, defense, level, xp, evo=None,sub_evo=None, hidden=False) :
        self.id = id
        self.name = name
        self.image = image
        self.coord = coord
        self.level = level
        self.hp = hp*2*level//100 + 10 + level
        self.attack = attack*2*level//100 + 5
        self.defense = defense*2*level//100 + 5
        self.xp = xp
        self.find = False
        self.type = type
        self.hidden = hidden    
        self.evo = evo
        self.sub_evo = sub_evo
        self.hp_base = hp
        self.attack_base = attack
        self.defense_base = defense
        self.full_hp = True
        self.degat_recu = 0
        #self.pokedex_id


    def __str__(self):
        return f"{self.name} {self.index_team}"

    def level_up(self) :
        while self.xp >= 1000 * self.level * 0.5 :
            self.xp -= int(1000 * self.level * 0.5)
            self.level += 1
            self.hp= (self.hp_base*2*self.level)//100 + 10 + self.level
            self.attack = (self.attack_base*2*self.level)//100 + 5
            self.defense = (self.defense_base*2*self.level)//100 + 5
            self.evolve()

    def get_inf_form(self) :
        for i in range(len(self.family)) :
            if self.family[i] == self.name and i > 0 :
                return self.family[i-1]

    def evolve(self) :
        if self.evo is not None and self.level % 25 == 0 :
            evolution(self.name, current_level=self.level, current_xp=self.xp)
    
    
    def change_team_index_in_json(self, index):
        with open("equipe.json", "r", encoding="utf-8") as file:
            content = json.load(file)
    
        for i, pokemon in enumerate(content):
            if pokemon["id"] == self.id:
                content[i]["index_team"] = index
                break
    
        with open("equipe.json", "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)