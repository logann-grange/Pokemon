class Pokemon() :

    def __init__(self, id, name, image, coord, hp, attack, defense, level, xp, type, degat_recu=0,full_hp=True) :
        self.id = id
        self.name = name
        self.image = image
        self.coord = coord
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.xp = xp
        self.type = type
        self.full_hp=full_hp
        self.degat_recu=degat_recu

    def level_up(self) :
        if self.xp <= 1000 * self.level*0.5 : #multiplier par un facteur d'xp
            self.level += 1
            self.xp -=  1000 * self.level
