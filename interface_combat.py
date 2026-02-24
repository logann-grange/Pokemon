import pygame
from combats import *
from Pokedex.logic.Pokemon import *
from display_manager import get_screen


etat=COMBAT
font = None
end_font = None
hp_font = None
screen = None
temps_debut=0
running=True
poke_turn=True
adv_turn=False


#initialisation des textes

txt_erreur="Ce n'est pas votre tour !"
txt_erreur_surface = None

#initialisation des nuages

x=-250
x2=1080
x3=-250
x4=1080
clouds=pygame.image.load("Asset/cloud_pixel.png")
clouds=pygame.transform.scale(clouds,(250,250))
big_cloud=pygame.image.load("Asset/big_cloud.png")
co_poke=150
co_adv=600


def _ensure_combat_context():
    global font, end_font, hp_font, screen, txt_erreur_surface

    if not pygame.get_init():
        pygame.init()
    screen = get_screen('Pokemon')

    if font is None:
        font = pygame.font.SysFont("Arial", 16)
    if end_font is None:
        end_font = pygame.font.SysFont("Arial", 45)
    if hp_font is None:
        hp_font = pygame.font.SysFont("Arial", 12)

    txt_erreur_surface = font.render(txt_erreur, True, (255, 0, 0))

#class 

class Mon_Pokemon(Pokemon):
    def __init__(self, id, name, type, image, coord, hp, attack, defense, level, xp, evo=None, sub_evo=None, hidden=False, degat_recu=0,full_hp=True):
        super().__init__(id, name, type, image, coord, hp, attack, defense, level, xp, evo=evo, sub_evo=sub_evo, hidden=hidden)
        self.coord=co_poke
        self.image = pygame.transform.flip(self.image,True,False)
        self.full_hp = full_hp
        self.degat_recu = degat_recu
    
    def afficher (self):
        self.image = pygame.transform.scale(self.image,(150,150))
        screen.blit(self.image,(self.coord,400))

class Pokemon_Adverse(Pokemon):
    def __init__(self, id, name, type, image, coord, hp, attack, defense, level, xp, evo=None, sub_evo=None, hidden=False, degat_recu=0,full_hp=True):
        super().__init__(id, name, type, image, coord, hp, attack, defense, level, xp, evo=evo, sub_evo=sub_evo, hidden=hidden)
        self.coord=co_adv
        self.full_hp = full_hp
        self.degat_recu = degat_recu

    def afficher(self):
        self.image = pygame.transform.scale(self.image,(150,150))
        screen.blit(self.image,(self.coord,400))

#initialisation des pokemon

#dracofeu = pygame.image.load("Asset/front/6.png")
#draco = Mon_Pokemon(1,"Dracofeu","Fire",dracofeu,co_poke,250,100,50,9,3500)

#carabaffe=pygame.image.load("Asset/front/8.png")
#cara=Pokemon_Adverse(1,"Carabaffe","Ice",carabaffe,co_adv,250,30,20,7,1200)

#fight=Combat(draco,cara,hp_font,end_font,COMBAT,screen=screen)

#fonctions

def sky (x,y):

    screen.blit(clouds,(x,y))



def fonctionnement (poke,adv,fight, events):

    global temps_debut
    global poke_turn
    global adv_turn
    global co_poke
    global co_adv
    global btn
    global bttn
    global btnn
    
    if poke_turn==False:
        btn = pygame.draw.rect(screen, (50,50,50), (450,500,180,30))  
        bttn = pygame.draw.rect(screen, (50,50,50), (550,500,180,30))  
        btnn = pygame.draw.rect(screen, (50,50,50), (650,500,180,30))  
        for event in events:
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    if btn.collidepoint(event.pos):
                        temps_debut=pygame.time.get_ticks()
                        if pygame.time.get_ticks()-temps_debut<=3000:
                            screen.blit(txt_erreur_surface,(500,250))
                    elif bttn.collidepoint(event.pos):
                        temps_debut=pygame.time.get_ticks()
                        if pygame.time.get_ticks()-temps_debut<=3000:
                            screen.blit(txt_erreur_surface,(500,250))
                    elif btnn.collidepoint(event.pos):
                        temps_debut=pygame.time.get_ticks()
                        if pygame.time.get_ticks()-temps_debut<=3000:
                            screen.blit(txt_erreur_surface,(500,250))
            elif event.type == pygame.QUIT:
                return False
        fight.oppo_attack()

        poke_turn=True
        adv_turn=False

    else:
        btn = pygame.draw.rect(screen,(255,0,0),(350,500,180,30))
        bttn = pygame.draw.rect(screen, (150,150,0), (350,550,180,30))  
        btnn = pygame.draw.rect(screen, (0,0,255), (350,600,180,30))
        for event in events:
            temps_debut=pygame.time.get_ticks()
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:                        
                    if btn.collidepoint(event.pos):
                        fight.attack_mult()
                        poke_turn=False
                        adv_turn=True

                    elif bttn.collidepoint(event.pos):
                        fight.attack()
                        poke_turn=False
                        adv_turn=True
                    """
                    elif btnn.collidepoint(event.pos):
                        fight.#pokeball
                    """   
            elif event.type == pygame.QUIT:
                return False

    return True



#boucle de jeu
def game_loop(poke,adv):
    global x, x2, x3, x4
    global screen
    global poke_turn, adv_turn, temps_debut

    _ensure_combat_context()
    
    # Convertir les Pokemon en Mon_Pokemon et Pokemon_Adverse avec leurs images
    poke_image = pygame.image.load(f"Asset/front/{int(poke.id)}.png")
    adv_image = pygame.image.load(f"Asset/front/{int(adv.id)}.png")
    
    mon_poke = Mon_Pokemon(poke.id, poke.name, poke.type, poke_image, poke.coord, 
                           poke.hp_base, poke.attack_base, poke.defense_base, 
                           poke.level, poke.xp, poke.evo, poke.sub_evo, poke.hidden)
    
    adv_pokemon = Pokemon_Adverse(adv.id, adv.name, adv.type, adv_image, adv.coord,
                                   adv.hp_base, adv.attack_base, adv.defense_base,
                                   adv.level, adv.xp, adv.evo, adv.sub_evo, adv.hidden)
    
    fight = Combat(adv_pokemon, mon_poke, hp_font, end_font, COMBAT, screen=screen)
    poke_turn = True
    adv_turn = False
    temps_debut = 0
    running=True
    while running:
        events = pygame.event.get()

        if fight.etat==COMBAT:

            screen.fill((101,211,255))
            pygame.draw.rect(screen,(0,255,0),(0,360,1080,360)) 
            fight.hp_lvl()
            mon_poke.afficher()
            adv_pokemon.afficher()
            running = fonctionnement(mon_poke,adv_pokemon,fight, events)
            if pygame.time.get_ticks()- temps_debut<=3000:
                screen.blit(txt_erreur_surface,(450,500))

            #clouds
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

            #button fuite
            pygame.draw.rect(screen,(0,0,0),(10,10,50,50))  

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
        