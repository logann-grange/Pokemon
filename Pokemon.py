import json

class Pokemon() :

    def __init__(self, id, name, pokedex_id, type, image, coord, hp, attack, defense, level, xp, evo=None,sub_evo=None, hidden=False, index_team=None) :
        self.id = id
        self.name = name
        self.image = image
        self.coord = coord
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.xp = xp
        self.find = False
        self.type = type
        self.hidden = hidden
        self.evo = evo
        self.sub_evo = sub_evo
        self.index_team = index_team
        self.pokedex_id = pokedex_id

    def __str__(self):
        return f"{self.name} {self.index_team}"
    
    def level_up(self) :
        if self.xp <= 1000 * self.level*0.5 : #multiplier par un facteur d'xp
            self.level += 1
            self.xp -=  1000 * self.level

    def get_inf_form(self) :
        for i in range(len(self.family)) :
            if self.family[i] == self.name and i > 0 :
                return self.family[i-1]
            

    def change_team_index_in_json(self, index):
        with open("equipe.json", "r", encoding="utf-8") as file:
            content = json.load(file)
    
        for i, pokemon in enumerate(content):
            if pokemon["id"] == self.id:
                content[i]["index_team"] = index
                break
    
        with open("equipe.json", "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)