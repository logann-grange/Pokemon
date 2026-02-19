import pygame
import pytmx
import pyscroll
from entity import Entity
from switch import Switch
from interface_pokedex import open_pokedex

class Map :
    def __init__(self, screen):
        self.screen = screen
        self.data = None
        self.layer = None
        self.group = None
        self.switch : list[tuple] = []
        self.current_map = Switch("switch", "labo", pygame.Rect(0,0,0,0), 0)
        self.player = None
        self.collision = []
        self.pc = []
        self.change_map(self.current_map)
        
        

    def change_map(self, switch):
        self.data = pytmx.load_pygame(f"assets/images/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.data)
        self.layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.layer.zoom = 3 
        self.group = pyscroll.PyscrollGroup(map_layer=self.layer, default_layer=7)

        self.switch = []
        self.collision = []
        for obj in self.data.objects :
            if obj.name is not None and obj.name == "collision" :
                self.collision.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            if self.player and obj.name is not None and obj.name == "pc" :
                self.player.able_pc = True
                print(self.player.able_pc) # ajouter un rect à un attribut pc



            if obj.name is not None :
                type = obj.name.split(" ")[0]
                if type == "switch" :
                    self.switch.append(Switch(type, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height), int(obj.name.split(" ")[-1])))
        
        if self.player:
            self.pos_player(switch)
            self.player.add_switch(self.switch)
            self.player.add_collision(self.collision)

            self.group.add(self.player)

        self.current_map = switch


    def update(self) :
        self.group.draw(self.screen)
        self.group.center(self.player.rect.center)
        self.player.map = self.current_map.name
        if self.player.change_map :
            self.change_map(self.player.change_map)
            self.player.change_map = None

    def add_player(self, player) :
         self.group.add(player)
         self.player = player
         self.player.add_switch(self.switch)
         self.player.add_collision(self.collision)
    
    def pos_player(self, switch):
        name = f"spawn {self.current_map.name} {switch.port}"
        position = self.data.get_object_by_name(name)
        self.player.hitbox.topleft = (position.x, position.y)