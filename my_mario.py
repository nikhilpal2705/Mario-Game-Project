import random, pygame, sys, os
from pygame.locals import *

w = 1200
h = 700
global dirc, ranvar, rect_fireball, flag, i, flame, scaled_fireball, gameend, score, topscore, scorefont, level, lastLevel
score = 0
topscore = 0
level = 1
lastLevel = False
flame = [1]
i = 0
flag = 1
rect_fireball = []
dirc = "goingup"
BLACK = (0, 0, 0)
ranvar = [60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510]
pygame.init()
pygame.key.set_repeat(5, 5)
window = pygame.display.set_mode((w, h))
pygame.display.set_caption("Mario Game")


def screen_init():
    start_img = pygame.image.load("start.png")
    rect_simg = start_img.get_rect()
    rect_simg.left = (w - rect_simg.right) // 2
    rect_simg.top = (h - rect_simg.bottom) // 2
    window.blit(start_img, rect_simg)
    while True:
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    window.fill(BLACK)
                    screen_design()
                    driver()
        pygame.display.update()

        # look out termination


def screen_design():
    global dirc, flame, i, flag, rect_fireball, score, topscore, scorefont, level
    score = 0
    flame = [1]
    level = 1
    i = 0
    flag = 1
    rect_fireball = []
    dirc = "goingup"
    scorefont = pygame.font.SysFont(None, 30)
    global gameend
    global mario_img, rect_mario
    mario_img = pygame.image.load("maryo.png")
    rect_mario = mario_img.get_rect()
    rect_mario.left = 63
    rect_mario.bottom = h - 180
    window.blit(mario_img, rect_mario)

    global dragon_img, rect_dragon
    dragon_img = pygame.image.load("dragon.png")
    rect_dragon = dragon_img.get_rect()
    rect_dragon.left = w - 150
    rect_dragon.bottom = h - 100
    # print(rect_dragon.top)
    window.blit(dragon_img, rect_dragon)

    global fire_img, rect_fire
    fire_img = pygame.image.load("fire.png")
    rect_fire = fire_img.get_rect()
    rect_fire.top = h - rect_fire.bottom
    rect_fire.bottom = h
    window.blit(fire_img, rect_fire)

    global cactus_img, rect_cactus
    cactus_img = pygame.image.load("cactus.png")
    rect_cactus = cactus_img.get_rect()
    # print(rect_cactus.bottom)
    window.blit(cactus_img, rect_cactus)
    pygame.display.update()

    pygame.mixer.music.load("mario_theme.wav")
    gameend = pygame.mixer.Sound("mario_dies.wav")
    pygame.mixer.music.play(-1, 0.0)


def driver():
    while True:
        mario_handler()
        dragon_handler()
        fireball_handler()
        drawtext(
            "Score : %s | Top score : %s | Level : %s" % (score, topscore, level),
            scorefont,
            window,
            350,
            rect_cactus.bottom + 10,
        )
        screen_updater()


def drawtext(text, font, surface, x, y):  # to display text on the screen
    textobj = font.render(text, 1, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    window.blit(textobj, textrect)
    pygame.display.update()


def mario_handler():
    global mario_img, rect_mario, score, topscore

    for e in pygame.event.get():
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif e.key == K_UP:
                rect_mario.top -= 4
                rect_mario.bottom -= 4
                score += 1
            elif e.key == K_DOWN:
                rect_mario.top += 1
                rect_mario.bottom += 1
    rect_mario.top += 1
    rect_mario.bottom += 1


def collision_handler(f):
    global topscore, level
    if (
        rect_mario.collidepoint(f.left + 10, f.top + 10)
        or rect_mario.collidepoint(f.left + 10, f.bottom - 10)
        or rect_cactus.collidepoint(rect_mario.right, rect_mario.top + 10)
        or rect_fire.collidepoint(rect_mario.right, rect_mario.bottom - 10)
    ):
        level = 1
        if score > topscore:
            topscore = score
        pygame.mixer.music.stop()
        gameend.play()
        window.fill(BLACK)
        end_img = pygame.image.load("end.png")
        rect_eimg = end_img.get_rect()
        rect_eimg.left = (w - rect_eimg.right) // 2
        rect_eimg.top = (h - rect_eimg.bottom) // 2
        window.blit(end_img, rect_eimg)
        while True:
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        window.fill(BLACK)
                        screen_design()
                        driver()
            pygame.display.update()


def screen_updater():
    global scaled_fireball
    window.fill(BLACK)
    window.blit(mario_img, rect_mario)
    window.blit(dragon_img, rect_dragon)
    window.blit(fire_img, rect_fire)
    window.blit(cactus_img, rect_cactus)
    for f in rect_fireball:
        window.blit(scaled_fireball, f)
        collision_handler(f)
    pygame.display.update()


def dragon_handler():
    global dirc
    if (rect_dragon.top > 50 and dirc == "goingup") or (
        rect_dragon.bottom >= rect_fire.top
    ):
        dirc = "goingup"
        rect_dragon.top -= 3
        rect_dragon.bottom -= 3
    elif (rect_dragon.top <= 50) or (rect_dragon.top > 50 and dirc == "goingdown"):
        dirc = "goingdown"
        rect_dragon.top += 3
        rect_dragon.bottom += 3


def fireball_handler():
    global fireball_img, rect_fireball, ranvar, dirc, flame, flag, i, scaled_fireball, level, lastLevel
    if score in range(0, 250):
        level = 1
    elif score in range(250, 500):
        level = 2
        # flame.clear()
        flame = random.sample(ranvar, level)
        flame.sort()
        if flag == 1:
            flame.reverse()
            flag = 0
    elif score > 500 and not lastLevel:
        level = 3
        # flame.clear()
        flame = random.sample(ranvar, level)
        flame.sort()
        if flag == 1:
            flame.reverse()
            flag = 0
        lastLevel = True

    # creating random coordinates for fireballs
    if dirc == "goingdown" and flag == 0:
        i = 0
        # flame.clear()
        flame = random.sample(ranvar, level)
        flame.sort()
        flag = 1
    elif dirc == "goingup" and flag == 1:
        i = 0
        # flame.clear()
        flame = random.sample(ranvar, level)
        flame.sort()
        flame.reverse()
        flag = 0

    # creating fireball
    if i < level and rect_dragon.top == flame[i] - 2:
        fireball_img = pygame.image.load("fireball.png")
        scaled_fireball = pygame.transform.scale(fireball_img, (45, 45))
        rect_fireball.append(scaled_fireball.get_rect())
        rect_fireball[-1].left = rect_dragon.left - rect_fireball[-1].right + 20
        rect_fireball[-1].top = rect_dragon.top + 10
        i += 1

    # Decrementing fireball

    for f in rect_fireball:
        f.left -= 5

    # Removing fireballs from list
    for f in rect_fireball:
        if f.left < -20:
            rect_fireball.remove(f)


screen_init()
