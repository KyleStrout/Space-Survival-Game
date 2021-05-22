import pygame
import pygame.display
import pygame.image
import random
import time
import pygame.font
import math

pygame.init()

WIDTH = 1000
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Caption and Icon
pygame.display.set_caption("Space Survival")
icon = pygame.image.load('Assets/spaceshipicon.png').convert()
pygame.display.set_icon(icon)

# Player Ship
playerImage = pygame.image.load('Assets/spaceshipplayer.png').convert_alpha()
playerX = 480
playerY = 700
playerX_change = 0

# Background
backgroundImage = pygame.image.load('Assets/space-2.png').convert_alpha()

# Asteroid


# Asteroids
asteroid_count = 5
asteroidImage = []
asteroidX = []
asteroidY = []
asteroidY_change = []
asteroid_state = []

for i in range(asteroid_count):
    asteroidImage.append(pygame.image.load('Assets/rock.png').convert_alpha())
    asteroidX.append(random.randint(0, 936))
    asteroidY.append(-30)
    asteroidY_change.append(random.uniform(.3, .8))
    asteroid_state.append("ready")

# Missiles
missile_count = 10
available_missiles = missile_count
missileImage = []
missileX = []
missileY = []
missileY_change = []
missile_state = []

# Ammo
ammoImage = pygame.image.load('Assets/bullet.png').convert_alpha()
ammoX = random.randint(0, 968)
ammoY = -40
ammoY_change = random.uniform(.2, .6)
ammo_state = "waiting"

# HP Icon (Player Lives)
heart_count = 3
heartImage = []
heartX = []
heartY = []
heart_state = []

# Ammo Literal Text
WHITE = (255, 255, 255)
ammo_text_font = pygame.font.Font('freesansbold.ttf', 16)
ammo_text_image = ammo_text_font.render('Ammo:', True, WHITE)

# Ammo Count Text
font = pygame.font.Font('freesansbold.ttf', 16)
ammo_count_text_font = pygame.font.Font('freesansbold.ttf', 16)

# Explosion
explosionImage = pygame.image.load('Assets/explosion.png').convert_alpha()
explosionX = 0
explosionY = 0


# update missiles
def missile_init(missile_count):
    for i in range(missile_count):
        missileImage.append(pygame.image.load(
            'Assets/missile.png').convert_alpha())
        missileX.append(playerX)
        missileY.append(playerY)
        missileY_change.append(-1)
        missile_state.append("ready")


def missile_update():
    for i in range(missile_count):
        missileX[i] = playerX
        missileY[i] = playerY
        missile_state[i] = "ready"


def player(x, y):
    screen.blit(playerImage, (x, y))


def background():
    screen.blit(backgroundImage, (0, 0))


def asteroid(x, y, i):
    screen.blit(asteroidImage[i], (x, y))

# updates asteroids


def update_asteroids(asteroid_count, asteroidImage, asteroidX, asteroidY, asteroidY_change, asteroid_state):
    for i in range(asteroid_count):
        asteroidImage.append(pygame.image.load(
            'Assets/rock.png').convert_alpha())
        asteroidX.append(random.randint(0, 936))
        asteroidY.append(-30)
        asteroidY_change.append(random.uniform(.3, .8))
        asteroid_state.append("ready")

# fires missile from front of ship


def fire_missile(x, y, i):
    screen.blit(missileImage[i], (x + 16, y + 10))


def ammo(x, y):
    screen.blit(ammoImage, (x, y))


def heart(x, y, i):
    screen.blit(heartImage[i], (x, y))


def update_player_lives(heart_count):
    for i in range(heart_count):
        heartImage.append(pygame.image.load(
            'Assets/heart.png').convert_alpha())
        heartX.append(904 + (32 * i))
        heartY.append(0)
        heart_state.append("ready")


def ammo_text():
    screen.blit(ammo_text_image, (906, 40))


def ammo_count_text(available_missiles):
    ammo_count_text_image = ammo_count_text_font.render(
        str(available_missiles), True, WHITE)
    screen.blit(ammo_count_text_image, (967, 40))


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance < 32:
        return True
    else:
        return False


def explosion(x, y):
    screen.blit(explosionImage, (x, y))


start_time = time.time()
# Timer for spawning new asteroids
time_limit = 4
missile_init(missile_count)

# Update player lives
update_player_lives(heart_count)

# Ammo Timer
ammo_time_limit = 15


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.2
            if event.key == pygame.K_SPACE:
                for i in range(missile_count):
                    if missile_state[i] is "ready":
                        missile_state[i] = "fire"
                        missileX[i] = playerX
                        fire_missile(missileX[i], missileY[i], i)
                        available_missiles -= 1
                        break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    background()

    ammo_text()
    ammo_count_text(available_missiles)

    # heart display
    for i in range(heart_count):
        if heart_state[i] == "ready":
            heart(heartX[i], heartY[i], i)
        # if heart_state not ready (collision with asteroid) then dont display

    elapsed_time = time.time() - start_time

    if elapsed_time > ammo_time_limit:
        ammo_time_limit += 15
        ammo_state = "ready"
    if ammo_state == "ready":
        ammoY += ammoY_change
        ammo(ammoX, ammoY)
    if ammoY > 800:
        ammoY = -40
        ammoX = random.randint(0, 968)
        ammo_state = "waiting"

    # Timer for spawning new asteroids
    print(time_limit - int(elapsed_time))

    # Asteroids
    # Asteroid Logic
    if elapsed_time > time_limit:
        time_limit += 4
        if asteroid_count < 20:
            asteroid_count = asteroid_count + 1
            update_asteroids(asteroid_count, asteroidImage,
                             asteroidX, asteroidY, asteroidY_change, asteroid_state)

    for i in range(asteroid_count):
        asteroidY[i] += asteroidY_change[i]
        if asteroidY[i] > 800:
            asteroidY[i] = -30
            asteroidX[i] = random.randint(0, 936)
            asteroidY_change[i] = random.uniform(.3, .8)
            asteroid_state[i] = "ready"

        if asteroid_state[i] == "ready":
            asteroid(asteroidX[i], asteroidY[i], i)

    # Missiles
    for i in range(missile_count):
        if missile_state[i] is "fire":
            fire_missile(missileX[i], missileY[i], i)
            missileY[i] += missileY_change[i]
            # Missile/Asteroid Collision
            for j in range(asteroid_count):
                if isCollision(missileX[i], missileY[i], asteroidX[j], asteroidY[j]) and asteroid_state[j] == "ready":
                    explosion(asteroidX[j], asteroidY[j])
                    asteroid_state[j] = "blown up"
                    missile_state[i] = "detonated"

        if missileY[i] < 0:
            missile_state[i] = "detonated"
            missileY[i] = playerY
            missileX[i] = playerX

    # Player
    playerX += playerX_change
    if playerX > 936:
        playerX = 936
    if playerX < 0:
        playerX = 0

    # Collision

    if isCollision(playerX, playerY, ammoX, ammoY):
        missile_update()
        available_missiles = 10
    player(playerX, playerY)

    pygame.display.update()
