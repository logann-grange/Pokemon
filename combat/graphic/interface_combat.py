import pygame
from combat.logic.combats import *
from Pokedex.logic.Pokemon import *
from combat.logic.mon_pokemon import Mon_Pokemon
from combat.logic.pokemon_adverse import Pokemon_Adverse

etat=COMBAT
pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()
font = pygame.font.SysFont("Arial",16)
end_font = pygame.font.SysFont("Arial",45)
hp_font = pygame.font.SysFont("Arial", 12)
screen= pygame.display.set_mode((1080,720))
running=True


#=========INITIALISATION DES TEXTES=========#

txt_erreur="Ce n'est pas votre tour !"
txt_erreur=font.render(txt_erreur,True,(255,0,0))

#=========INITIALISATION DU FOND=========#

ground=pygame.image.load("Asset/fond_jeu.png")
ground=pygame.transform.scale(ground, (1080,720))
x=-250
x2=1080
x3=-250
x4=1080
lil_clouds=pygame.image.load("Asset/cloud_pixel.png")
lil_clouds=pygame.transform.scale(lil_clouds,(250,250))
big_cloud=pygame.image.load("Asset/big_cloud.png")
co_poke=150
co_adv=750

#=========FONCTIONS=========#

def sky (x,y):

    screen.blit(lil_clouds,(x,y))

def fuite_affichage():
    txt_fuite = font.render("Voulez-vous fuir ?", True, (255,255,255))
    screen.blit(txt_fuite, (380, 350))
    btn_oui = pygame.draw.rect(screen, (0,200,0), (400,400,100,40))
    btn_non = pygame.draw.rect(screen, (200,0,0), (560,400,100,40))
    txt_oui = font.render("OUI", True, (0,0,0))
    txt_non = font.render("NON", True, (0,0,0))
    screen.blit(txt_oui, (430,410))
    screen.blit(txt_non, (590,410))

def fuite(confirmation_fuite, event, poke, running):
    if confirmation_fuite:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pygame.Rect(400,400,100,40).collidepoint(event.pos):
                    running = False
                    confirmation_fuite = False
                    screen.fill((0,0,0))
                    txt_fui = end_font.render(f"{poke.name} a fui le combat !", True, (255,255,255))
                    screen.blit(txt_fui, (200,300))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                elif pygame.Rect(560,400,100,40).collidepoint(event.pos):
                    confirmation_fuite = False
    return confirmation_fuite, running


def render_combat_scene(mon_poke, adv_pokemon, fight, confirmation_fuite):
    global x, x2, x3, x4

    screen.fill((101,211,255))
    screen.blit(ground,(0,180))
    #pygame.draw.rect(screen,(0,255,0),(0,360,1080,360))
    fight.hp_lvl()
    mon_poke.afficher(screen)
    adv_pokemon.afficher(screen)

    if x>1080:
        x=-250
    x+=0.1
    sky(x,150)
    if x2<-250:
        x2=1080
    x2-=0.1
    sky(x2,75)
    if x4<-600:
        x4=1080
    x4-=0.1
    screen.blit(big_cloud,(x4,-150))
    if x3>1080:
        x3=-250
    x3+=0.2
    sky(x3,50)

    out = pygame.draw.rect(screen, (0,0,0), (10,10,50,50))

    if confirmation_fuite:
        fuite_affichage()

    return out


def animate_attack_motion(attacker, mon_poke, adv_pokemon, fight, confirmation_fuite=False):
    direction = 1 if attacker is mon_poke else -1
    initial_coord = attacker.coord

    for _ in range(6):
        attacker.coord += direction * 8
        render_combat_scene(mon_poke, adv_pokemon, fight, confirmation_fuite)
        pygame.display.flip()
        pygame.time.delay(20)
        for event in pygame.event.get([pygame.QUIT]):
            if event.type == pygame.QUIT:
                return False

    for _ in range(6):
        attacker.coord -= direction * 8
        render_combat_scene(mon_poke, adv_pokemon, fight, confirmation_fuite)
        pygame.display.flip()
        pygame.time.delay(20)
        for event in pygame.event.get([pygame.QUIT]):
            if event.type == pygame.QUIT:
                return False

    attacker.coord = initial_coord
    return True

def fonctionnement(poke, adv, fight, events, animate_player_attack):
    global running
    global co_poke
    global co_adv
    global btn
    global bttn
    global btnn

    if fight.poke_turn:
        mult = fight.get_type_multiplier(poke, adv)

        damage_mult = int(poke.attack * mult)
        damage_simple = int(poke.attack)

        btn = pygame.draw.rect(screen,(255,0,0),(350,500,180,30))
        bttn = pygame.draw.rect(screen,(150,150,0),(350,540,180,30))
        btnn = pygame.draw.rect(screen,(0,0,255),(350,580,180,30))

        txt_btn = font.render(f"Attaque {damage_mult}", True, (255,255,255))
        txt_bttn = font.render(f"Attaque {damage_simple}", True, (255,255,255))
        txt_btnn = font.render("Capturer", True, (255,255,255))

        screen.blit(txt_btn, (355,503))
        screen.blit(txt_bttn, (355,543))
        screen.blit(txt_btnn, (355,583))

        for event in events:
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    if btn.collidepoint(event.pos):
                        if not animate_player_attack():
                            return False
                        fight.attack_mult()
                        if fight.etat == COMBAT:
                            fight.poke_turn=False
                            fight.adv_turn=True
                    elif bttn.collidepoint(event.pos):
                        if not animate_player_attack():
                            return False
                        fight.attack()
                        if fight.etat == COMBAT:
                            fight.poke_turn=False
                            fight.adv_turn=True
                    elif btnn.collidepoint(event.pos):
                        fight.attraper()

    return True

#=========BOUCLE DE JEU=========#

def game_loop(poke,adv):
    global x, x2, x3, x4
    global screen
    global poke_turn, adv_turn, temps_debut
    
    # Convertir les Pokemon en Mon_Pokemon et Pokemon_Adverse avec leurs images
    poke_image = pygame.image.load(f"Asset/front/{int(poke.id)}.png")
    adv_image = pygame.image.load(f"Asset/front/{int(adv.id)}.png")
    
    mon_poke = Mon_Pokemon(
        poke.id, poke.name, poke.type, poke_image, poke.coord,
        poke.hp_base, poke.attack_base, poke.defense_base,
        poke.level, poke.xp,
        evo=poke.evo, sub_evo=poke.sub_evo, hidden=poke.hidden
    )

    adv_pokemon = Pokemon_Adverse(
        adv.id, adv.name, adv.type, adv_image, adv.coord,
        adv.hp_base, adv.attack_base, adv.defense_base,
        adv.level, adv.xp,
        evo=adv.evo, sub_evo=adv.sub_evo, hidden=adv.hidden
    )

    fight = Combat(adv_pokemon, mon_poke, hp_font, end_font, COMBAT, screen=screen)
    poke_turn = True
    adv_turn = False
    temps_debut = 0
    confirmation_fuite = False
    out = pygame.Rect(10,10,50,50)
    enemy_attack_due = None
    running=True
    while running:

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
               if event.button == 1 :
                   if out.collidepoint(event.pos):
                       confirmation_fuite = True
            elif event.type == pygame.QUIT:
                running = False

            confirmation_fuite, running = fuite(confirmation_fuite, event, mon_poke, running)
            if not running:
                break

        if not running:
            continue
        
        if fight.etat==COMBAT:
            out = render_combat_scene(mon_poke, adv_pokemon, fight, confirmation_fuite)

            if enemy_attack_due is not None and pygame.time.get_ticks() >= enemy_attack_due and not confirmation_fuite and fight.poke_turn==False:
                if not animate_attack_motion(adv_pokemon, mon_poke, adv_pokemon, fight, confirmation_fuite):
                    running = False
                    continue
                fight.oppo_attack()
                enemy_attack_due = None
                if fight.etat == COMBAT:
                    fight.poke_turn=True
                    fight.adv_turn=False

            if not confirmation_fuite:
                running = fonctionnement(
                    mon_poke,
                    adv_pokemon,
                    fight,
                    events,
                    lambda: animate_attack_motion(mon_poke, mon_poke, adv_pokemon, fight, confirmation_fuite),
                )

                if fight.etat == COMBAT and fight.poke_turn == False and enemy_attack_due is None:
                    enemy_attack_due = pygame.time.get_ticks() + 400
        
        elif fight.etat==FIN:
            fight.end_game()
            txt_continue = font.render("Appuyez sur une touche pour revenir a la carte", True, (255, 255, 255))
            screen.blit(txt_continue, (300, 320))

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif fight.etat == FIN and event.type == pygame.KEYDOWN:
                running = False
        pygame.display.flip()

    poke.xp = mon_poke.xp
    poke.level = mon_poke.level
    poke.hp = mon_poke.hp
    poke.attack = mon_poke.attack
    poke.defense = mon_poke.defense
