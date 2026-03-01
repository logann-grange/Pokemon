import pygame
from game.logic.map import Map
from game.logic.entity import Entity
from Pokedex.graphic.interface_pokedex import open_pokedex
from Pokedex.logic.Pokedex import Pokedex
from Pokedex.logic.pc import Pc
from Pokedex.graphic.interface_pc import open_pc
import game.logic.Sauvegarde as Sauvegarde
from game.graphic.display_manager import get_screen


def run_game(load_saved=False):
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load("Asset/sons/music_fond.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    screen = get_screen("Pokemon")
    running = True
    game_map = Map(screen)
    player = Entity()
    pc= Pc()
    if load_saved:
        player, loaded_switch = Sauvegarde.load_game(player, game_map.current_map)
        game_map.change_map(loaded_switch)

    game_map.add_player(player)
    pokedex = Pokedex()

    while running:
        clock.tick(60)
        pygame.display.flip()
        game_map.update()
        player.update()
        player.walk_animation()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Sauvegarde.save_game(player, game_map.current_map)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode == "p" :
                    pygame.mixer.Sound("Asset/sons/bouton.mp3").play()
                    open_pokedex(pokedex, screen)
                elif event.key == pygame.K_f:
                    pygame.mixer.Sound("Asset/sons/bouton.mp3").play()
                    open_pc(pc, screen)

        # Maintenir un état de proximité PC plus stable même sans déplacement
        player.able_pc = player.check_collision_pc(player.hitbox.inflate(4, 4))

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
    pygame.quit()
    return


if __name__ == "__main__":
    run_game()
