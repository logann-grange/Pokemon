import pygame
from map import Map
from entity import Entity
from switch import Switch
from interface_pokedex import open_pokedex
from Pokedex import Pokedex
from pc import Pc
from interface_pc import open_pc


pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/sons/music_fond.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1080, 720))
running = True
map = Map(screen)
player = Entity()
map.add_player(player)
pokedex = Pokedex()
pc = Pc()
while running:
    clock.tick(60)
    pygame.display.flip()
    map.update()
    player.update()
    player.walk_animation()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.unicode == "p" :
                pygame.mixer.Sound("assets/sons/bouton.mp3").play()
                open_pokedex(pokedex, screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        player.move_up()
    if keys[pygame.K_s]:
        player.move_down()
    if keys[pygame.K_q]:
        player.move_left()
    if keys[pygame.K_d]:
        player.move_right()
    if (keys[pygame.K_z], keys[pygame.K_s], keys[pygame.K_q], keys[pygame.K_d]) == (False, False, False, False)  :
        player.animation_walk = False
        player.image = player.all_images[player.direction][0]
    if keys[pygame.K_f] and player.able_pc:
        open_pc(pc, screen)
