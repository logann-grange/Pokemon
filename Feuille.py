import random
import math
import pygame

_leafs = None


def init_leafs(image, count=25):
    global _leafs
    if _leafs is None:
        _leafs = [Feuille(image) for _ in range(count)]
    return _leafs


def get_leafs():
    return _leafs or []


class Feuille:
    def __init__(self, image):
        self.image = image
        self.x=random.randint(800, 900)
        self.y=random.randint(100, 450)
        self.speed_y=random.uniform(-0.5, 0.5)
        self.speed_x=random.uniform(-2, -4)
        self.rotation=random.randint(0, 360)
        self.rotation_speed=random.uniform(-2, 2)
        self.frenquence=random.uniform(0.02, 0.05)
        self.time=random.uniform(0, 100)
        
        self.scale=random.uniform(0.04, 0.08)
        weight=int(self.image.get_width()*self.scale)
        height=int(self.image.get_height()*self.scale)
        self.image=pygame.transform.scale(self.image,(weight,height))
        
    def update(self):
        self.x +=self.speed_x
        self.y +=self.speed_y + math.sin(self.time)*self.frenquence*50
        
        self.rotation+=self.rotation_speed
        
        if self.y < -50:
            self.y = 600 + 50
        elif self.y > 600 + 50:
            self.y = -50
        
        
        if self.x < -50:
            self.x = random.randint(800, 900)
            self.y = random.randint(100, 450)
            
    def draw(self, screen):
        rotated_image=pygame.transform.rotate(self.image,self.rotation)
        rect=rotated_image.get_rect(center=(self.x,self.y))
        screen.blit(rotated_image, rect)    
        
        
            