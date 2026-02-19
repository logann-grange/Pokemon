import menu_evolution

class Pokemon() :

    def __init__(self, id, name, type, image, coord, hp, attack, defense, level, xp, evo=None,sub_evo=None, hidden=False) :
        self.id = id
        self.name = name
        self.image = image
        self.coord = coord
        self.hp = hp*2*level//100 + 10 + level
        self.attack = attack*2*level//100 + 5
        self.defense = defense*2*level//100 + 5
        self.level = level
        self.xp = xp
        self.find = False
        self.type = type
        self.hidden = hidden    
        self.evo = evo
        self.sub_evo = sub_evo
        self.hp_base = hp
        self.attack_base = attack
        self.defense_base = defense
        #self.pokedex_id

    def level_up(self) :
        if self.xp <= 1000 * self.level*0.5 : #multiplier par un facteur d'xp
            self.level += 1
            self.xp -=  1000 * self.level
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
            menu_evolution.evolution(self.name)
    