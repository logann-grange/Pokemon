import pygame
from combats import *
from Pokemon import *

pygame.init()
pygame.display.set_caption('Pokemon')
pygame.mixer.init()
screen= pygame.display.set_mode((1080,720))
point=[(180,100),(900,100),(980,620),(100,620)]
clouds=pygame.image.load("Asset/cloud_pixel.png")
clouds.convert_alpha()
clouds=pygame.transform.scale(clouds,(250,250))
big_cloud=pygame.image.load("Asset/big_cloud.png")
big_cloud.convert_alpha()
x=-250
x2=1080
x3=-250
x4=1080


def sky (x,y):
    screen.blit(clouds,(x,y))

def fight_area():   
    
    point_pitch=[(180,100),(900,100),(980,620),(100,620)]
    
    #pitch
    pygame.draw.polygon(screen,(35,245,20),point_pitch)  
    pygame.draw.rect(screen,(33,192,22),(100,620,880,30))
    pygame.draw.ellipse(screen,(169,169,169),(180,450,200,110))
    pygame.draw.ellipse(screen,(80,80,80),(180,450,200,110),2)
    pygame.draw.ellipse(screen,(169,169,169),(690,150,170,97.5))
    pygame.draw.ellipse(screen,(80,80,80),(690,150,170,97.5),2)
    #pause
    pygame.draw.rect(screen,(0,0,0),(10,10,50,50))  
    #buttons
    pygame.draw.rect(screen,(255,0,0),(600,490,350,50))
    pygame.draw.rect(screen,(255,0,0),(600,550,350,50))



running=True
while running:
    screen.fill((101,211,255))
    if x>1080:
        x=-250
    x+=0.1
    sky(x,150)
    if x2<-250:
        x2=1080
    x2-=0.05
    sky(x2,350)
    if x4<-600:
        x4=1080
    x4-=0.02
    screen.blit(big_cloud,(x4,-150))
    fight_area()
    if x3>1080:
        x3=-250
    x3+=0.18
    sky(x3,525)


    pygame.display.flip()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            running = False