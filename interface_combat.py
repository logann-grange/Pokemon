import pygame
from combats import *
from Pokemon import *

pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()
font = pygame.font.SysFont("Arial",16)
screen= pygame.display.set_mode((1080,720))
temps_debut=0
running=True
poke_turn=False
adv_turn=False

#initialisation des textes
txt_erreur="Ce n'est pas votre tour !"
txt_erreur=font.render(txt_erreur,True,(255,0,0))
#initialisation des nuages
x=-250
x2=1080
x3=-250
x4=1080
clouds=pygame.image.load("Asset/cloud_pixel.png")
clouds=pygame.transform.scale(clouds,(250,250))
big_cloud=pygame.image.load("Asset/big_cloud.png")

#fonctions
heads_or_tails_fait=False


def sky (x,y):
    screen.blit(clouds,(x,y))

def fonctionnement (poke,adv):
    global heads_or_tails_fait
    global temps_debut
    global running
    global poke_turn
    global adv_turn
    
    if heads_or_tails_fait==False:
        resultat=fight.heads_or_tails()
        if resultat== "You start !":
            poke_turn=True
            adv_turn=False
            heads_or_tails_fait=True
        else:
            adv_turn=True
            poke_turn=False
            heads_or_tails_fait=True
    
    if poke_turn==False:
        btn = pygame.draw.rect(screen, (50,50,50), (450,500,180,50))  
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    if btn.collidepoint(event.pos):
                        temps_debut=pygame.time.get_ticks()
            elif event.type == pygame.QUIT:
                running = False

    else:
        btn = pygame.draw.rect(screen,(255,0,0),(450,500,180,50))
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:                        
                    if btn.collidepoint(event.pos):
                        poke.attack()
            elif event.type == pygame.QUIT:
                running = False

    

#class 

class Mon_Pokemon(Pokemon):
    def __init__(self, id, name, image, coord, hp, attack, defense, level, xp, type):
        super().__init__(id, name, image, coord, hp, attack, defense, level, xp, type)
        self.coord=(150,400)
        self.image = pygame.transform.flip(self.image,True,False)
    
    def afficher (self):
        self.image = pygame.transform.scale(self.image,(150,150))
        screen.blit(self.image,self.coord)

class Pokemon_Adverse(Pokemon):
    def __init__(self, id, name, image, coord, hp, attack, defense, level, xp, type):
        super().__init__(id, name, image, coord, hp, attack, defense, level, xp, type)
        self.coord=(780,400)

    def afficher(self):
        self.image = pygame.transform.scale(self.image,(150,150))
        screen.blit(self.image,self.coord)

#initialisation des pokemon
co_x=0
co_y=0
dracofeu = pygame.image.load("Asset/front/dracofeu.png")
draco = Mon_Pokemon(1,"Dracofeu",dracofeu,(co_x,co_y),250,100,50,9,3500,"Fire")

carabaffe=pygame.image.load("Asset/front/carabaffe.png")
cara=Pokemon_Adverse(1,"Carabaffe",carabaffe,(co_x,co_y),120,30,20,7,1200,"Water")


#boucle de jeu
running=True
while running:

    screen.fill((101,211,255))
    pygame.draw.rect(screen,(255,255,255),(0,360,1080,360))  
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

    draco.afficher()
    cara.afficher()
    fonctionnement(draco,cara)
    if pygame.time.get_ticks()- temps_debut<=3000:
        screen.blit(txt_erreur,(500,500))
    #button pause
    pygame.draw.rect(screen,(0,0,0),(10,10,50,50))  

    

    pygame.display.flip()
    