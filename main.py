import pygame
from pygame.locals import *
import os
import random

pygame.init()

W, H = 800, 415
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Pokeball Factory Escape')

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

bg = pygame.image.load(os.path.join(image_path, 'background.png')).convert()
bgX = 0
bgX2 = bg.get_width() 

clock = pygame.time.Clock()

class player(object):
    roller = pygame.transform.scale(pygame.image.load(os.path.join(image_path, 'Electrode.png')).convert(), (64,64))
    duck = [
        pygame.image.load(os.path.join(image_path, 'Duck_Frame_1.png')), 
        pygame.image.load(os.path.join(image_path, 'Duck_Frame_2.png')), 
        pygame.image.load(os.path.join(image_path, 'Duck_Frame_3.png')),  
        pygame.image.load(os.path.join(image_path, 'Duck_Frame_4.png'))
    ]

    duckAnim = [
        0,0,0,
        1,1,1,
        2,2,2,2,2,2,2,
        3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
        3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,
        2,2,2,2,2,2,2,
        1,1,1,
        0,0,0
    ]

    rip = [
        pygame.image.load(os.path.join(image_path, 'dead_1.png')),
        pygame.image.load(os.path.join(image_path, 'dead_2.png')),
        pygame.image.load(os.path.join(image_path, 'dead_3.png')),
        pygame.image.load(os.path.join(image_path, 'dead_4.png'))
    ]

    ripAnim = [
        0,0,0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,1,1,
        2,2,2,2,2,2,2,2,2,2,
        3,3,3,3,3,3,3,3,3,3
    ]
    jumpList = [
        1,1,1,1,1,1,1,1,1,1,1,1,
        2,2,2,2,2,2,2,2,2,2,2,2,
        3,3,3,3,3,3,3,3,3,3,3,3,
        4,4,4,4,4,4,4,4,4,4,4,4,
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
        -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
        -2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,
        -3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,
        -4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4
    ]

    def __init__(self, x, y, width, height):
        self.x = int(x)
        self.y = int(y + height / 2)
        self.resetY = self.y
        self.width = width
        self.height = height
        self.jumping = False
        self.ducking = False
        self.riping = False
        self.duckCount = 0
        self.ripCount = 0
        self.jumpCount = 0
        self.angle = 0
        self.duckYCount = 0

    def draw(self, win):
        self.roller.set_colorkey((0,0,0))
        rotated = pygame.transform.rotate(self.roller, self.angle)
        
        # Death stuff
        if self.riping:
            deathStartingPoint = (int(self.x - self.width / 2), int(self.y - self.height / 2))
            if self.ripCount <= len(self.ripAnim) - 1:
                win.blit(pygame.transform.scale(self.rip[self.ripAnim[self.ripCount]], (64,64)), deathStartingPoint)
                self.ripCount += 1
        # Jump stuff
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount]
            self.jumpCount += 1
            win.blit(rotated, (int(self.x - rotated.get_width() / 2), int(self.y - rotated.get_height() / 2)))
            self.angle -= 3
            if self.jumpCount >= 112:
                self.jumpCount = 0
                self.jumping = False
            self.hitbox = (
                int((self.x - self.width / 2) + 10),
                int((self.y - self.height / 2) + 10),
                self.width - 20, 
                self.height - 20)
        # Duck stuff
        elif self.ducking:
            if self.duckCount == len(self.duckAnim):
                self.ducking = False
                self.duckCount = 0
                self.angle = 0
            elif self.duckCount < (len(self.duckAnim) / 2) - 38:
                self.duckYCount += 1
            elif self.duckCount > (len(self.duckAnim) / 2) + 38:
                self.duckYCount -= 1
            self.hitbox = (
                int((self.x - self.width / 2) + 10), 
                int((self.y - self.height / 2) + 10 + self.duckYCount), 
                self.width - 20, 
                self.height - 20 - self.duckYCount)
            win.blit(
                pygame.transform.scale(
                    self.duck[self.duckAnim[self.duckCount]], 
                    (64,64)),
                (int((self.x - self.width / 2)), 
                int((self.y - self.height / 2))))
            self.duckCount += 1
        # Rolling stuff
        else:
            if self.angle <= -360:
                self.angle = 0
            win.blit(
                rotated, 
                (int(self.x - rotated.get_width() / 2), 
                int(self.y - rotated.get_height() / 2)))
            self.angle -= 3
            self.hitbox = (
                int((self.x - self.width / 2) + 10),
                int((self.y - self.height / 2) + 10),
                self.width - 20, 
                self.height - 20)
        # pygame.draw.rect(win, (255,0,0),self.hitbox, 2)

class Pokeball(object):
    balls = [
        pygame.image.load(os.path.join(image_path, 'pokeball1.png')), 
        pygame.image.load(os.path.join(image_path, 'pokeball2.png')), 
        pygame.image.load(os.path.join(image_path, 'pokeball3.png')), 
        pygame.image.load(os.path.join(image_path, 'pokeball4.png')),
        pygame.image.load(os.path.join(image_path, 'pokeball5.png')),
        pygame.image.load(os.path.join(image_path, 'pokeball6.png'))
        ]
    
    def __init__(self, x, y, width, height, r):
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.r = r

    def draw(self, win):
        self.hitbox = (
            int(self.x + 5), 
            int(self.y + 5), 
            self.width - 10,
            self.height- 10)
        win.blit(
            pygame.transform.scale(
                self.balls[self.r], 
                (32,32)), 
            (int(self.x), 
            int(self.y)))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

class High_Ball(Pokeball):
    high_balls = [
        pygame.image.load(os.path.join(image_path, 'high_pokeball_v1.png')),
        pygame.image.load(os.path.join(image_path, 'high_pokeball_v2.png')),
        pygame.image.load(os.path.join(image_path, 'high_pokeball_v3.png'))
        ]

    def draw(self, win):
        self.hitbox = (
            int(self.x), 
            int(self.y), 
            self.width, 
            self.height)
        win.blit(
            pygame.transform.scale(
                self.high_balls[self.r], 
                (32,415)), 
            (int(self.x), 
            int(self.y)))
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[1] + self.hitbox[3]:
                return True
        return False

def updateFile():
    scoresPath =  os.path.join(current_path, 'scores.txt')
    f = open(scoresPath,'r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open(scoresPath, 'w')
        file.write(str(score))
        file.close()
        return score
    return last

def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 60
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                electrode.jumping = False
                electrode.ducking = False
                electrode.riping = False
                electrode.duckCount = 0
                electrode.ripCount = 0
                electrode.jumpCount = 0
                electrode.angle = 0
                electrode.duckYCount = 0
                electrode.y = electrode.resetY

        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (int(W/2 - lastScore.get_width()/2), 150))
        win.blit(currentScore, (int(W/2 - currentScore.get_width()/2), 240))
        pygame.display.update()
    score = 0

def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (int(bgX), 0))
    win.blit(bg, (int(bgX2),0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    electrode.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)

    win.blit(text, (700, 10))
    pygame.display.update()


pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, 3000)
speed = 60

score = 0

run = True
electrode = player(200, 258, 64, 64)

obstacles = []
pause = 0
fallSpeed = 0

while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = speed//10 - 6

    for obstacle in obstacles:
        if obstacle.collide(electrode.hitbox):
            electrode.riping = True

            if pause == 0:
                pause = 1
                fallSpeed = speed
        if obstacle.x < -32:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.4

    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

        if event.type == USEREVENT+1:
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randrange(0,2)
            if r == 0:
                obstacles.append(Pokeball(810, 288, 32, 32, random.randrange(0,6)))
            elif r == 1:
                obstacles.append(High_Ball(810, -140, 32, 415, random.randrange(0,3)))

    if electrode.riping == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(electrode.jumping):
                electrode.jumping = True

        if keys[pygame.K_DOWN]:
            if not(electrode.ducking):
                electrode.ducking = True

    clock.tick(speed)
    redrawWindow()
