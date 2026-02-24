import pygame
from combats import *
from Pokemon import *


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

#=========CLASS=========#

class Mon_Pokemon(Pokemon):
    def __init__(self, id, name, type, image, coord, hp, attack, defense, level, xp, degat_recu=0, full_hp=True, evo=None, sub_evo=None, hidden=False):
        super().__init__(id, name, type, image, coord, hp, attack, defense, level, xp, degat_recu, full_hp, evo, sub_evo, hidden)
        self.coord=co_poke
        self.image = pygame.transform.flip(self.image,True,False)
    
    def afficher (self):
        self.image = pygame.transform.scale(self.image,(150,150))
        screen.blit(self.image,(self.coord,450))

class Pokemon_Adverse(Pokemon):
    def __init__(self, id, name, type, image, coord, hp, attack, defense, level, xp, degat_recu=0, full_hp=True, evo=None, sub_evo=None, hidden=False):
        super().__init__(id, name, type, image, coord, hp, attack, defense, level, xp, degat_recu, full_hp, evo, sub_evo, hidden)
        self.coord=co_adv

    def afficher(self):
        self.image = pygame.transform.scale(self.image,(150,150))
        screen.blit(self.image,(self.coord,450))

#=========INITIALISATION DES POKEMON=========#

dracofeu = pygame.image.load("Asset/front/dracofeu.png")
draco = Mon_Pokemon(1,"Dracofeu","Fire",dracofeu,co_poke,250,100,50,9,3500)

carabaffe=pygame.image.load("Asset/front/carabaffe.png")
cara=Pokemon_Adverse(1,"Carabaffe","Water",carabaffe,co_adv,250,30,20,7,1200)

fight=Combat(cara,draco,hp_font,end_font,COMBAT,screen=screen)


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

def fuite(confirmation_fuite, event):
    global running
    if confirmation_fuite:
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if pygame.Rect(400,400,100,40).collidepoint(event.pos):
                    running = False
                    confirmation_fuite = False
                    screen.fill((0,0,0))
                    txt_fui = end_font.render(f"{draco.name} a fui le combat !", True, (255,255,255))
                    screen.blit(txt_fui, (200,300))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                elif pygame.Rect(560,400,100,40).collidepoint(event.pos):
                    confirmation_fuite = False
    return confirmation_fuite

def fonctionnement(poke, adv, events):
    global running
    global co_poke
    global co_adv
    global btn
    global bttn
    global btnn

    if fight.poke_turn==False:
        fight.oppo_attack()
        fight.poke_turn=True
        fight.adv_turn=False

    else:
        mult=1
        for element in type_poke:
            if element==poke.type:
                for types in type_poke[element]:
                    nv_dico=type_poke[element]
                    if types==adv.type:
                        mult=nv_dico[types]

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

        if events.type==pygame.MOUSEBUTTONUP:
            if events.button==1:
                if btn.collidepoint(events.pos):
                    if pygame.time.get_ticks()-temps_debut<=1500:
                        co_poke+=5
                    co_poke-=5
                    fight.attack_mult()
                    fight.poke_turn=False
                    fight.adv_turn=True
                elif bttn.collidepoint(events.pos):
                    if pygame.time.get_ticks()-temps_debut<=1500:
                        co_poke+=5
                    co_poke-=5
                    fight.attack()
                    fight.poke_turn=False
                    fight.adv_turn=True
                elif btnn.collidepoint(events.pos):
                    fight.attraper()

#=========BOUCLE DE JEU=========#

confirmation_fuite=False
running=True
while running:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if out.collidepoint(event.pos):
                    confirmation_fuite = True
        elif event.type==pygame.QUIT:
            running=False
            
        confirmation_fuite = fuite(confirmation_fuite, event)
            

    if fight.etat==COMBAT:

        screen.fill((101,211,255))
        screen.blit(ground,(0,180))
        fight.hp_lvl()
        draco.afficher()
        cara.afficher()
        fonctionnement(draco,cara,event)

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

        out = pygame.draw.rect(screen, (0,0,0), (10,10,50,50))
        if confirmation_fuite:
            fuite_affichage()

    pygame.display.flip()