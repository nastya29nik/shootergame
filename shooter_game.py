#Создай собственный Шутер!

from pygame import *
import random
from time import time as timer
# timer - нужно для засечения времени

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Meteor(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
        

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fireSound = mixer.Sound('fire_2.ogg')

# шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (0, 255, 0))
lose = font1.render('YOU LOSE!', True, (255, 0, 0))
font2 = font.SysFont('Arial', 36)

img_back = "space_2.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_meteor = "asteroid.png"
img_bullet = "bullet.png"

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter')
background = transform.scale(image.load(img_back), (win_width, win_height))

# переменные счета
lost = 0
score = 0
life = 3
#герои игры
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy(img_enemy, random.randint(80, win_width - 80), -40, 80, 40, random.randint(1,5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(2):
    asteroid = Meteor(img_meteor, random.randint(80, win_width - 80), -40, 40, 40, random.randint(5,10))
    asteroids.add(asteroid)
bullets = sprite.Group()


run = True
finish = False
# будет отвечать за перезарядку
rel_time = False
# подсчет выпущенных пуль
num_fire = 0

clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5: 
                    fireSound.play()
                    ship.fire()

    if finish != True:
        window.blit(background, (0,0))
        # счетчики
       
        
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        # проверка столкновения пуль и монстров (ОБА ИСЧЕЗАЮТ ПРИ КАСАНИИ)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        # цикл работает столько раз сколько монстров сбито
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, random.randint(80, win_width - 80), -40, 80, 40, random.randint(1,5))
            monsters.add(monster)


        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()

        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asteroids, True):
            life -=1

        # условие проигрыша
        if lost >= 10 or life <= 0:
            finish = True
            window.blit(lose, (win_width//4, win_height//2))
            
        # условие выигрыша
        if score >= 10:
            finish = True
            window.blit(win, (win_width//4, win_height//2))

        if life == 3:
            life_color = (0, 225 ,0)
        if life == 2:
            life_color = (225, 238, 0)
        else:
            life_color = (225, 0, 0)


        text = font2.render('Счет: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_life = font2.render('Жизни: ' + str(life), 1, life_color)
        window.blit(text_life, (10, 80))    

        display.update()
    else:
        finish = False
        lost = 0
        score = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in asteroids:
            m.kill()
        for ufo in monsters:
            ufo.kill()

        time.delay(3000)
        for i in range(5):
            monster = Enemy(img_enemy, random.randint(80, win_width - 80), -40, 80, 40, random.randint(1,5))
            monsters.add(monster)
        for i in range(2):
            asteroid = Meteor(img_meteor, random.randint(80, win_width - 80), -40, 40, 40, random.randint(5,10))
            asteroids.add(asteroid)

    time.delay(50)