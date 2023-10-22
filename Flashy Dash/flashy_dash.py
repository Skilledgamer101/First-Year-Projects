import time
import random

class Player:

    def __init__(self, x: int, y: int, vel: int, length: int, width: int, color: tuple) -> None:
        self.x = x
        self.y = y
        self.vel = vel
        self.length = length
        self.width = width
        self.color = color
        self.screen_length = window.get_size()[1]
        self.screen_width = window.get_size()[0]
        self.bgcolor = (0,0,0)

    def right(self) -> None:
        self.x += self.vel
        draw_hero()

    def left(self) -> None:
        self.x -= self.vel
        draw_hero()

    def up(self) -> None:
        self.y -= self.vel
        draw_hero()

    def down(self) -> None:
        self.y += self.vel
        draw_hero()

    def crazy(self) -> None:
        self.x += random.randrange(-10, 10)
        self.y += random.randrange(-10, 10)
        draw_hero()

    def warp(self) -> None:

        if self.x >= self.screen_width - self.width:
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        elif self.x <= 10:
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        elif self.y <= 0:
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        elif self.y >= self.screen_length - self.length:          # too down. down is higher value
            self.x, self.y = self.screen_width / 2 - self.width / 2, self.screen_length / 2 - self.length / 2

        draw_hero()

class Powerup(Player):
    def __init__(self, x1: int, x2: int, x3: int, x4: int, x5: int, x6: int, y1: int, y2: int, y3: int, y4: int, y5: int, y6: int, vel: int, length: int, width: int, color: tuple):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
        self.x5 = x5
        self.x6 = x6
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.y4 = y4
        self.y5 = y5
        self.y6 = y6
        self.vel = vel
        self.length = length
        self.width = width
        self.color = color

    def crazy(self, x_start: int, x_end: int, y_start: int, y_end: int) -> None:
        x_change = random.randrange(x_start, x_end)     
        self.x1 += x_change
        self.x2 += x_change
        self.x3 += x_change
        self.x4 += x_change
        self.x5 += x_change
        self.x6 += x_change
        y_change = random.randrange(y_start, y_end)      
        self.y1 += y_change
        self.y2 += y_change
        self.y3 += y_change
        self.y4 += y_change
        self.y5 += y_change
        self.y6 += y_change
        draw_lightning(lightning)

import pygame
pygame.init()

window = pygame.display.set_mode()
pygame.display.set_caption("Flashy Dash")
hero = Player(100, 100, 6, 20, 20, (0, 0, 255))         # all the characteristics of each player
enemy1 = Player(300, 300, 2, 40, 40, (255, 0, 0))
enemy2 = Player(600, 600, 3, 40, 40, (255, 0, 0))
enemy3 = Player(900, 900, 4, 40, 40, (255, 0, 0))
width = hero.screen_width
lightning = Powerup(width - 20, width - 15, width - 17.5, width - 12, width - 12.5, width - 10, 30, 17, 17.5, 5, 15.5, 15, 6, 25, 10, (255, 255, 0))
x_center = width // 2
y_center = hero.screen_length // 2
lightning2 = Powerup(x_center - 20, x_center - 15, x_center - 17.5, x_center - 12, x_center - 12.5, x_center - 10, y_center + 30, y_center + 17, y_center + 17.5, y_center + 5, y_center + 15.5, y_center + 15, 6, 25, 10, (255, 255, 0))
run = True
powered = False
upgraded = False

def draw_hero():
    window.fill(hero.bgcolor)
    pygame.draw.rect(window, hero.color, (hero.x, hero.y, hero.length, hero.width))
    pygame.display.update()

def draw_enemies():

    window.fill(hero.bgcolor)
    pygame.draw.rect(window, enemy1.color, (enemy1.x, enemy1.y, enemy1.length, enemy1.width))
    pygame.draw.rect(window, enemy2.color, (enemy2.x, enemy2.y, enemy2.length, enemy2.width))
    pygame.draw.rect(window, enemy3.color, (enemy3.x, enemy3.y, enemy3.length, enemy3.width))
    pygame.display.update()

def draw_lightning(lightning):
    window.fill(hero.bgcolor)
    pygame.draw.polygon(window, lightning.color, ((lightning.x1, lightning.y1), (lightning.x2, lightning.y2), (lightning.x3, lightning.y3), (lightning.x4, lightning.y4), (lightning.x5, lightning.y5), (lightning.x6, lightning.y6)))
    pygame.display.update()

def draw_all():
    window.fill(hero.bgcolor)
    pygame.draw.rect(window, hero.color, (hero.x, hero.y, hero.length, hero.width))
    pygame.draw.rect(window, enemy1.color, (enemy1.x, enemy1.y, enemy1.length, enemy1.width))
    pygame.draw.rect(window, enemy2.color, (enemy2.x, enemy2.y, enemy2.length, enemy2.width))
    pygame.draw.rect(window, enemy3.color, (enemy3.x, enemy3.y, enemy3.length, enemy3.width))
    pygame.display.update()

def follow(enemy, hero):            # enemy and hero must be objects of the Player class

    global run

    if enemy.x < hero.x - 10:
        enemy.right()

    elif enemy.x > hero.x + 10:
        enemy.left()

    if enemy.y > hero.y + 10:
        enemy.up()

    elif enemy.y < hero.y - 10:
        enemy.down()
        
    # draw_hero()

    # check(enemy1, hero)
    # check(enemy2, hero)

def check(enemy, hero):

    global run
    font = pygame.font.Font('CascadiaCode-Light.ttf', 32)
    text8 = font.render('You died!', True, (255, 0, 0))
    textRect8 = text8.get_rect()
    textRect8.center = (hero.screen_width // 2, hero.screen_length // 2 + 300)
    if enemy.x - hero.width <= hero.x <= enemy.x + enemy.width and enemy.y - hero.length <= hero.y <= enemy.y + enemy.length:
        pygame.mixer.Channel(0).stop()
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('death.mp3'))
        window.blit(text8, textRect8)
        pygame.display.update()
        time.sleep(0.5)
        run = False

def check_power(powerup, hero, x_start, x_end, y_start, y_end):
    global powered

    if powerup.x3 - hero.width <= hero.x <= powerup.x6 and powerup.y4 - hero.length <= hero.y <= powerup.y1:
        hero.vel += 6
        powered = True
        powerup.crazy(x_start, x_end, y_start, y_end)


def main():
    speed = 50
    global run
    global powered
    global upgraded
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('prismatic.mp3'))

    font = pygame.font.Font('CascadiaCode-Light.ttf', 32)
    text1 = font.render('Use the arrow keys to move', True, (255, 255, 255))
    text2 = font.render('Avoid the red squares.', True, (255, 255, 255))
    text3 = font.render('You will only see flashes of the red squares.', True, (255, 255, 255))
    text4 = font.render('If you go outside the screen, you will be placed back in the center.', True, (255, 255, 255))
    text5 = font.render('Go!', True, (255, 255, 255))
    text6 = font.render('You win!', True, (7, 186, 13))
    text7 = font.render('*Double speed*', True, (255, 255, 0))
    

    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect4 = text4.get_rect()
    textRect5 = text5.get_rect()
    textRect6 = text6.get_rect()
    textRect7 = text7.get_rect()
    textRect1.center = textRect2.center = textRect3.center = textRect4.center = textRect5.center = textRect6.center = textRect7.center = (hero.screen_width // 2, hero.screen_length // 2 + 300)

    while run:
        ticks = pygame.time.get_ticks()
        print(ticks)
        pygame.time.delay(speed)
        
        draw_enemies()
        hero.right()
 
        hero.warp()
   
        enemy1.warp()
        enemy2.warp()
        enemy3.warp()
        check(enemy1, hero)
        check(enemy2, hero)
        check(enemy3, hero)
        follow(enemy1, hero)
        follow(enemy2, hero)
        follow(enemy3, hero)


                
        while ticks <= 8000:
            if ticks <= 2000:
                draw_hero()
                window.blit(text1, textRect1)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()
            if 2000 < ticks <= 4000:
                draw_enemies()
                window.blit(text2, textRect2)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()  
            
            if 4000 < ticks <= 6000:
                draw_all()
                window.blit(text3, textRect3)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()
           
            if 6000 < ticks <= 8000:
                draw_all()
                window.blit(text4, textRect4)
                pygame.display.update()
                time.sleep(2)
                ticks = pygame.time.get_ticks()
            ticks = pygame.time.get_ticks()

        if 8250 <= ticks <= 10500:                                                # blue
            while ticks <= 10500:
                hero.bgcolor = (0, 0, ticks % 255)                                  
                hero.color = enemy1.color = enemy2.color = enemy3.color = (0, 0, 0)
                window.fill(hero.bgcolor)                                         # have to expand draw_all() function here to make sure one display update satisfies both text and players (to avoid flashing and still see both)
                pygame.draw.rect(window, hero.color, (hero.x, hero.y, hero.length, hero.width))
                pygame.draw.rect(window, enemy1.color, (enemy1.x, enemy1.y, enemy1.length, enemy1.width))
                pygame.draw.rect(window, enemy2.color, (enemy2.x, enemy2.y, enemy2.length, enemy2.width))
                pygame.draw.rect(window, enemy3.color, (enemy3.x, enemy3.y, enemy3.length, enemy3.width))
                window.blit(text5, textRect5)
                pygame.display.update()
                ticks = pygame.time.get_ticks()

            hero.bgcolor = (0, 0, 100)
            hero.color = (0, 0, 255)
            enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            draw_hero()
            speed = 40

        if ticks > 11000:
            draw_lightning(lightning)
            lightning.crazy(-6, 0, 0, 6)
            check_power(lightning, hero, 1600, 1605, 800, 850)
            if powered == True:
                hero.color = (hero.x % 255, hero.y % 255, random.randrange(0, 255))
                if upgraded == False:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('electric2.mp3'))
                    draw_all()
                    window.blit(text7, textRect7)
                    pygame.display.update()
                    time.sleep(1)
                    upgraded = True
                


        if 17500 <= ticks <= 19000:                                               # green
            while ticks <= 19000:
                hero.bgcolor = (0, ticks % 255, 0)
                enemy1.color = enemy2.color = enemy3.color = (0, 0, 0)
                draw_all()
                ticks = pygame.time.get_ticks()
            hero.bgcolor = (0, 100, 0)
            
            enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            draw_hero()
            speed = 30

        if 26000 <= ticks <= 27750:                                                 # yellow
            while ticks <= 27750:
                hero.bgcolor = (ticks % 255, ticks % 255, 0)
                enemy1.color = enemy2.color = enemy3.color = (0, 0, 0)
                draw_all()
                ticks = pygame.time.get_ticks()
            hero.bgcolor = (100, 100, 0)
            
            enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            draw_hero()
            speed = 20   

        if 34000 <= ticks <= 36000:                                                 # cyan
            while ticks <+ 36000:
                hero.bgcolor = (0, ticks % 255, ticks % 255)
                enemy1.color = enemy2.color = enemy3.color = (0, 0, 0)
                draw_all()
                ticks = pygame.time.get_ticks()
            hero.bgcolor = (0, 100, 100)
            
            enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            draw_hero()
            speed = 10            

        if 43000 <= ticks <= 45000:                                                 # purple
            while ticks <= 45000:
                hero.bgcolor = (ticks % 255, 0, ticks % 255)
                enemy1.color = enemy2.color = enemy3.color = (0, 0, 0)
                draw_all()
                ticks = pygame.time.get_ticks()
            hero.bgcolor = (100, 0, 100)
            
            enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            draw_hero()
            speed = 5


        if 52000 <= ticks <= 53500:                                                 # white
            while ticks <= 53500:
                hero.bgcolor = (ticks % 255, ticks % 255, ticks % 255)
                enemy1.color = enemy2.color = enemy3.color = (0, 0, 0)
                draw_all()
                ticks = pygame.time.get_ticks()
            hero.bgcolor = (100, 100, 100)
            hero.color = (0, 0, 255)
            enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            draw_hero()
            speed = 3
            hero.vel = 6
            powered = False
            upgraded = False


        if 68070 <= ticks <= 70007:                                               # slow red flashes
            while ticks <= 70007:
                for i in range(255):
                    hero.bgcolor = (i, 0, 0)
                    hero.color = enemy1.color = enemy2.color = enemy3.color = (0, 0, 0)
                    draw_all()
                time.sleep(0.6)
                ticks = pygame.time.get_ticks()
            hero.bgcolor = (100, 0, 0)
            hero.color = (0, 0, 255)
            enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            draw_hero()
            speed = 2

        if ticks > 70500:
            draw_lightning(lightning2)
            check_power(lightning2, hero, 1600, 1605, 800, 850)
            if powered == True:
                hero.color = (hero.x % 255, hero.y % 255, random.randrange(0, 255))
                if upgraded == False:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('electric2.mp3'))
                    draw_all()
                    window.blit(text7, textRect7)
                    pygame.display.update()
                    time.sleep(1)
                    upgraded = True

        if 87500 <= ticks <= 88500:                                                 # pink
            hero.bgcolor = (245, 66, 215)
            enemy1.length = enemy2.length = enemy3.length = 80
            enemy1.width = enemy2.width = enemy3.width = 80
            

        if 104500 <= ticks <= 105500:                                               # purple
            hero.bgcolor = (161, 66, 245)
            enemy1.color = enemy2.color = enemy3.color = (255, 255, 0)
            enemy1.vel = 8
            enemy2.vel = 7
            enemy3.vel = 6
            if powered == False:
                hero.vel = 8
                hero.color = (0, 255, 255)

        if 121000 <= ticks <= 122000:                                             # ending fade out to white
            for i in range(255):
                hero.bgcolor = (i, i, i)
                hero.color = enemy1.color = enemy2.color = enemy3.color = (i, i, i)
                draw_all()
                time.sleep(1/255)
            
            for i in range(255):                                                            # ending display message and hero slowly turns from cyan to blue
                if powered == False:
                    hero.color = (0, 255 - i, 255)
                else:
                    hero.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
                time.sleep(22/255)
                
                pygame.draw.rect(window, hero.color, (hero.x, hero.y, hero.length, hero.width))
                window.blit(text6, textRect6)
                pygame.display.update()
            # enemy1.color = enemy2.color = enemy3.color = (255, 0, 0)
            # powered = False
            # draw_hero()
            # speed = 50

        if ticks > 144000:
            run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            pygame.time.delay(1)
            for i in range(3):
                hero.left()

        if keys[pygame.K_RIGHT]:
            hero.right()

        if keys[pygame.K_UP]:
            hero.up()

        if keys[pygame.K_DOWN]:
            hero.down()

    pygame.quit()

main()
