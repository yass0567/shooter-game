from pygame import *
from random import randint

lost = 0
number_score=0
finish=False
window_w = 700
window_h = 500

#classes:
#1
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, w, h, speed):
        super().__init__()
        self.w = w
        self.h = h
        self.image = transform.scale(image.load(player_image), (w, h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#2
class Player(GameSprite):
    
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 0: 
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < window_w - self.w:
            self.rect.x += self.speed

    def fire(self):
        b=Bullet("bullet.png",self.rect.centerx - 5 , self.rect.y, 15,20,10)
        bullets.add(b)
       

#3
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed # increase y
        if self.rect.y > window_h: # check 
            self.rect.y = 0
            self.rect.x = randint(0, window_w - self.w)
            lost += 1
#4
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed 
        if self.rect.y < 0:
            self.kill()
                          


#create the window:
window = display.set_mode((window_w, window_h))
display.set_caption("shooter game")

# background image
background = transform.scale(image.load("galaxy.jpg"), (window_w, window_h))

# objects inside the game
player = Player("rocket.png", 330, 430, 60, 70, 5)

monsters = sprite.Group()
for i in range(5):
    m = Enemy("ufo.png", randint(0, window_w - 60), randint(-50, 50), 60, 50, 2)
    monsters.add(m)

bullets = sprite.Group()

# music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
shot = mixer.Sound("fire.ogg")

# font
font.init()
style = font.SysFont('Arial', 36)
style1=font.SysFont('Arial',100)
miss_text = style.render( "Missed: " + str(lost) , 1, (255, 255, 255) )
score =style.render("Score:"+str(number_score) ,1,(255,255,255) )
game = True
fps = 60
clock = time.Clock()

# gameloop
while game:
    # exit door
    for e in event.get():
        if e.type == QUIT:
            game = False
        #shot fire by click or by space key:
        if e.type ==KEYDOWN and e.key == K_SPACE:
            shot.play()
            player.fire()    
        if e.type == MOUSEBUTTONDOWN:
            if e.button == True:    
                shot.play()
                player.fire()

    if finish == False:
        window.blit(background, (0, 0))

        miss_text = style.render( "Missed: " + str(lost) , 1, (255, 255, 255) )
        window.blit(miss_text, (10, 20))
        score =style.render("Score:"+str(number_score) ,1,(255,255,255) )
        window.blit(score,(10,40))
        win_text=style1.render("YOU WIN",1,(255,99,43))
        lose_text=style1.render("YOU LOSE",1,(255,88,41))
       

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()
        
        #collision between bullets and monsters:
        monsters_list= sprite.groupcollide(monsters, bullets, True, True)
        for i in monsters_list:
            number_score += 1
            m = Enemy("ufo.png", randint(0, window_w - 60), randint(-50, 50), 60, 50, 2)
            monsters.add(m)
            
        sprite_list= sprite.spritecollide(player,monsters, False)

        if len(sprite_list) != 0 or lost >= 4:
            finish= True
            window.blit(lose_text,(215,210))
        
        #win:
        if number_score >= 11:
            finish = True
            window.blit(win_text,(215,210))




    display.update()
    clock.tick(fps)