class Pokemon() :

    def __init__(self, id, name, type, image, coord, hp, attack, defense, level, xp, hidden=False) :
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
        #self.pokedex_id

    def level_up(self) :
        if self.xp <= 1000 * self.level*0.5 : #multiplier par un facteur d'xp
            self.level += 1
            self.xp -=  1000 * self.level
