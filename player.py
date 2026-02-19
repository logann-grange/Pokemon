import pygame
from entity import Entity
from map import screen

class Player(Entity):
    def __init__(self):
        super().__init__()