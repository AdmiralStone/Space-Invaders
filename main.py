import pygame
import random
import math
from pygame import mixer

#Initialize the pygame
pygame.init()

#create a window
screen = pygame.display.set_mode((800, 600))

#Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#Player
player = pygame.image.load("player.png")
playerX = 365
playerY = 480
playerX_change = 0

#Score Value
score = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Enemy
enemy = pygame.image.load("enemy.png")
enemyX = random.randint(64, 736)
enemyY = random.randint(64,300)
enemyX_change = 0.3
enemyY_change = 40


#Bullet
bullet = pygame.image.load("bullet.png")
bulletY = playerY - 25
bulletY_change = 0.4
bullet_state = 0 #Loaded in gun but not fired

#Sounds
##Background
mixer.music.load("background.wav")
mixer.music.play(-1)

##Bulet
bullet_sound = mixer.Sound('laser.wav')

##collision
collision_sound = mixer.Sound('explosion.wav')

def show_score(x,y):
    score_render = font.render("Score: "+ str(score) , True , (255,255,255))
    screen.blit(score_render,(x,y))

def draw_enemy(x,y):
    screen.blit(enemy,(x,y))

def draw_player(x, y):
    screen.blit(player , (x , y)) #Blit is used to draw sprites on the scrren

def bullet_fire(x,y):
    global bullet_state
    bullet_state = 1
    screen.blit(bullet,(x+20,y))

def isCollision(enemyX,enemyY,bulletX , bulletY):
    distance = math.sqrt((math.pow((enemyX-bulletX),2)) + (math.pow((enemyY - bulletY),2)))
    if distance < 27:
        return True
    else:
        return False

def playerColision(playerX,playerY,enemyX,enemyY):
    distance = math.sqrt((math.pow((playerX-enemyX),2)) + (math.pow((playerY - enemyY),2)))
    if distance < 27:
        return True
    else:
        return False



#Game Loop 
running = True
while running:
    #RGB
    screen.fill((255, 150, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #If keystroke is pressedcheck wether its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE and bullet_state == 0:
                bulletX = playerX
                bullet_fire(playerX,bulletY)
                bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0    
        
#Pleyer movement controller
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

#Enemy movement controller
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY += enemyY_change
    if enemyX >= 736:
        enemyX_change = -0.3
        enemyY += enemyY_change

#Bullet movement
    if bulletY <= 0:
        bullet_state = 0
        bulletY = playerY + 20
        
    if bullet_state == 1:
        bullet_fire(bulletX,bulletY)
        bulletY -= bulletY_change

#Collision detection
        collision = isCollision(enemyX , enemyY , bulletX , bulletY)
        if collision:
            collision_sound.play()
            bulletY = playerY+20
            bullet_state = 0
            score += 1
            # print("Score: " + str(score))
            enemyX = random.randint(64, 736)
            enemyY = random.randint(64,150)
            draw_enemy(enemyX,enemyY) 

    show_score(textX,textY)
    draw_enemy(enemyX,enemyY)
    draw_player(playerX,playerY)
    
    #Detect if enemy hit player
    gameover = playerColision(playerX,playerY , enemyX , enemyY)
    if gameover:
        # print("GAMEOVER")
        running = False
        
    pygame.display.update()
