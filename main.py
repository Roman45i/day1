import pygame
import random
import math
pygame.init()

display_size = [800, 600]

display = pygame.display.set_mode(display_size)
pygame.display.set_caption('Game')

icon = pygame.image.load('assets/ufo.png')
pygame.display.set_icon(icon)
background = pygame.image.load('assets/background.png')

PlayerImg = pygame.image.load('assets/player.png')
EnemyImg = pygame.image.load('assets/enemy.png')

PlayerX = display_size[0] / 2 - PlayerImg.get_size()[0] / 2
PlayerY = display_size[1] - PlayerImg.get_size()[1] - 30

PlayerMoveX = 0
PlayerSpeed = 4

Score = 0
Score_x = 5
Score_y = 30
HP = 100
HP_x = 5
HP_y = 5

run = True
Time1 = 0
Reload1 = 25


Time2 = 0
Reload2 = 100

Enemy = []
EnemyCount = 5

Bullet = []
BulletSpeed = 5
font = pygame.font.SysFont('None', 32)


BulletImg = pygame.image.load('assets/bullet.png')




pygame.mixer.music.load('sound/background.wav')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound('sound/laser.wav')
bullet_sound.set_volume(0.2)
enemy_sound = pygame.mixer.Sound('sound/explosion.wav')
enemy_sound.set_volume(0.2)

def show_text():
     text_hp = font.render('HP: ' + str(HP), True, (255, 255, 255))
     display.blit(text_hp, (HP_x, HP_y))

     text_score = font.render('SCORE: ' + str(Score), True, (255, 255, 255))
     display.blit(text_score, (Score_x, Score_y))


def PlayerUpdate():
    global PlayerX, PlayerMoveX
    PlayerX += PlayerMoveX

    if PlayerX < 0:
        PlayerX = 0

    if PlayerX + PlayerImg.get_size()[0] > display_size[0]:
        PlayerX = display_size[0] - PlayerImg.get_size()[0]


def EnemyCreate():
    EnemyX = random.randrange(0, display_size[0] - EnemyImg.get_size()[0])
    EnemyY = 30

    EnemyMoveX = random.randrange(-2, 3)
    EnemyMoveY = random.randrange(1, 3) / 2

    return [EnemyX, EnemyY, EnemyMoveX, EnemyMoveY]


def EnemyUpdate(Enemy):
    global HP

    Enemy[1] += Enemy[3]
    Enemy[0] += Enemy[2]

    if Enemy[0] < 0:
        Enemy[0] = 0
        Enemy[2] = -Enemy[2]

    if Enemy[0] + EnemyImg.get_size()[0] > display_size[0]:
        Enemy[0] = display_size[0] - EnemyImg.get_size()[0]
        Enemy[2] = -Enemy[2]

    if Enemy[1] > display_size[1]:
        HP -= 5
        Enemy = EnemyCreate()

    return Enemy



def isCollision(X1, Y1, Img1, X2, Y2, Img2):
    first = pygame.Rect(X1, Y1, Img1.get_width(), Img1.get_height())
    second = pygame.Rect(X2, Y2, Img2.get_width(), Img2.get_height())

    return first.colliderect(second)


def BulletCreate(shotgun):
    BulletX = PlayerX + PlayerImg.get_width() / 2 - BulletImg.get_width() / 2
    BulletY = PlayerY - BulletImg.get_height()
    BulletMoveX = random.randrange(-2, 3)

    if not shotgun:
        BulletMoveX = 0

    BulletMoveY = -1 * math.sqrt(BulletSpeed * BulletSpeed - BulletMoveX * BulletMoveX)
    Bullet.append([BulletX, BulletY, BulletMoveX, BulletMoveY])

def BulletUdpate(Bullet):
    Bullet[0] += Bullet[2]
    Bullet[1] += Bullet[3]
    return Bullet


for i in range(EnemyCount):
    Enemy.append(EnemyCreate())

while run:
    if Time1 != 0:
        Time1 += 1
    if Time1 > Reload1:
        Time1 = 0

    if Time2 != 0:
        Time2 += 1
    if Time2 > Reload2:
        Time2 = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                PlayerMoveX = -PlayerSpeed
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                PlayerMoveX = PlayerSpeed

        if event.type == pygame.MOUSEBUTTONDOWN:
            key = pygame.mouse.get_pressed()
            if key[0] and Time1 == 0:
                Time1 = 1
                bullet_sound.play()
                BulletCreate(False)

            if key[2] and Time2 == 0:
                Time2 = 1
                bullet_sound.play()
                for i in range(7):
                    BulletCreate(True)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT,
                             pygame.K_a, pygame.K_d):
                PlayerMoveX = 0

    for i in range(EnemyCount):
        Enemy[i] = EnemyUpdate(Enemy[i])

    for bullet in Bullet:
        bullet = BulletUdpate(bullet)
        if bullet[1] < 0:
            Bullet.remove(bullet)

    PlayerUpdate()


    for enemy in Enemy:
        if isCollision(PlayerX, PlayerY, PlayerImg,
                       enemy[0], enemy[1], EnemyImg):
            enemy_sound.play()
            Enemy.remove(enemy)
            Enemy.append(EnemyCreate())
            HP -= 10
            continue

        for bullet in Bullet:
            if isCollision(bullet[0], bullet[1], BulletImg,
                           enemy[0], enemy[1], EnemyImg):
                enemy_sound.play()
                Bullet.remove(bullet)
                Enemy.remove(enemy)
                Enemy.append(EnemyCreate())
                Score += 5
                break



    display.blit(background, (0, 0))


    display.blit(PlayerImg, (PlayerX, PlayerY))

    for enemy in Enemy:
        display.blit(EnemyImg, (enemy[0], enemy[1]))

    for bullet in Bullet:
        display.blit(BulletImg, (bullet[0], bullet[1]))

    show_text()

    pygame.display.update()