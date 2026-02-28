from pygame import *
from random import randint



condition=True
fps=60
clock=time.Clock()
lostmonsters=1
#how to create window :
width=500
height=300
win=display.set_mode((width,height))
display.set_caption("shoter game")
background_image=transform.scale(image.load("galaxy.jpg"),(width,height))


#How to create class of sprites:
class TheSprites(sprite.Sprite):
    def __init__(self,playerImage,x,y,w,h,speed):
        super().__init__()
        self.image=transform.scale(image.load(playerImage),(w,h))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.w=w
        self.h=h
        self.speed=speed
    def Blit(self):
        win.blit(self.image,(self.rect.x,self.rect.y))

class player(TheSprites):
    def movement(self):
        keys= key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < width - self.w:
            self.rect.x += self.speed

    def fire(self):
        pass

class Enemy(TheSprites):
    def update(self):
        global lostmonsters
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y =0
            self.rect.x= randint(0,width-self.w)#
            lostmonsters +=1

# the objects:
rocket=player("rocket.png",250,225,50,70,4)

monsters=sprite.Group()
for i in range(5):
    m=Enemy("ufo.png",randint(0,width-70),55,70,40,5)
    monsters.add(m)
    





while condition:
    #how to close the game:
    for e in event.get():
        if e.type == QUIT:
            condition = False
        

    win.blit(background_image,(0,0))   

    rocket.Blit() 
    rocket.movement()

    monsters.draw(win)
    monsters.update()

    display.update()
    clock.tick(fps)