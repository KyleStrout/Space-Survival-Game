import pygame
import pygame.display
import pygame.image
import random
import time
import pygame.font
import math
from pygame import mixer

pygame.init()

# Screen Boundaries
WIDTH = 1000
HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Caption and Icon
pygame.display.set_caption("Space Survival")
icon = pygame.image.load('Assets/spaceshipicon.png').convert()
pygame.display.set_icon(icon)

# Background
backgroundImage = pygame.image.load('Assets/space-2.png').convert_alpha()


def background():
    screen.blit(backgroundImage, (0, 0))


def start_screen():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        background()

        title_font = pygame.font.Font('freesansbold.ttf', 60)
        title_text = title_font.render('Space Survival', True, WHITE)
        screen.blit(title_text, (280, 150))

        description_font = pygame.font.Font('freesansbold.ttf', 22)
        description_text_1 = description_font.render(
            '- Dodge Asteroids To Survive', True, WHITE)
        description_text_2 = description_font.render(
            '- Shoot Aliens For Bonus Score', True, WHITE)
        description_text_3 = description_font.render(
            '- Pick Up Ammo To Rearm', True, WHITE)
        description_text_4 = description_font.render(
            'Controls: Space to fire, Arrow keys to move, P to pause', True, WHITE)

        continue_font = pygame.font.Font('freesansbold.ttf', 25)
        continue_text = continue_font.render(
            'Press C to continue, Or Q to quit', True, WHITE)

        screen.blit(description_text_1, (335, 250))
        screen.blit(description_text_2, (335, 275))
        screen.blit(description_text_3, (335, 300))
        screen.blit(description_text_4, (215, 400))
        screen.blit(continue_text, (315, 500))

        pygame.display.update()


def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        background()

        paused_font = pygame.font.Font('freesansbold.ttf', 30)
        paused_text = paused_font.render('Paused', True, WHITE)
        screen.blit(paused_text, (450, 200))
        info_font = pygame.font.Font('freesansbold.ttf', 15)
        info_text = info_font.render(
            'Press C to continue, or Q to quit', True, WHITE)
        screen.blit(info_text, (390, 250))

        pygame.display.update()


# initialize the start screen
start_screen()


def gameLoop():
    running = True
    gameOver = False

    # Player Ship
    playerImage = pygame.image.load(
        'Assets/spaceshipplayer.png').convert_alpha()
    playerX = 480
    playerY = 700
    playerX_change = 0

    # Asteroids
    asteroid_count = 5
    asteroidImage = []
    asteroidX = []
    asteroidY = []
    asteroidY_change = []
    asteroid_state = []

    # Asteroids Init
    for i in range(asteroid_count):
        asteroidImage.append(pygame.image.load(
            'Assets/rock.png').convert_alpha())
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
    current_lives = 3
    heart_count = 3
    heartImage = []
    heartX = []
    heartY = []
    heart_state = []

    # Ammo Literal Text
    ammo_text_font = pygame.font.Font('freesansbold.ttf', 16)
    ammo_text_image = ammo_text_font.render('Ammo:', True, WHITE)

    # Ammo Count Text
    font = pygame.font.Font('freesansbold.ttf', 16)
    ammo_count_text_font = pygame.font.Font('freesansbold.ttf', 16)

    # Explosion
    explosionImage = pygame.image.load('Assets/explosion.png').convert_alpha()
    explosionX = 0
    explosionY = 0

    # Score Var
    score = 0

    # Score Literal Text
    score_text_font = pygame.font.Font('freesansbold.ttf', 19)
    score_text_image = score_text_font.render('Score:', True, WHITE)

    # Alien Space Ships
    alienImage = pygame.image.load('Assets/ufo.png').convert_alpha()
    alienX = random.randint(0, 936)
    alienY = -64
    alienX_change = 0
    alienY_change = random.uniform(.4, .6)
    alien_state = "waiting"

    # Stats
    asteroids_destroyed = 0
    aliens_destroyed = 0
    time_survived = 0

    # Hearts (Spawning)
    heartImage_spawn = pygame.image.load('Assets/heart.png').convert_alpha()
    heartX_spawn = random.randint(0, 968)
    heartY_spawn = -40
    heartY_change = .2
    heart_spawn_state = "waiting"

    # Powerups
    # TODO

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

    def update_asteroids(asteroidImage, asteroidX, asteroidY, asteroidY_change, asteroid_state):
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

    def init_player_lives(heart_count):
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

    def score_text():
        screen.blit(score_text_image, (440, 2))

    def score_count(score):
        score_count_image = score_text_font.render(str(score), True, WHITE)
        screen.blit(score_count_image, (510, 2))

    def alien(x, y):
        screen.blit(alienImage, (x, y))

    def heart_spawn(x, y):
        screen.blit(heartImage_spawn, (x, y))

    start_time = time.time()

    # Timer for spawning new asteroids
    time_limit = 4
    missile_init(missile_count)

    # Update player lives
    init_player_lives(heart_count)

    # Ammo Timer
    ammo_time_limit = 15

    # Score Time Limit (How often score increases)
    score_timer = 1

    # Alien spawn timer
    alien_timer = 5

    # Heart spawn Timer
    heart_spawn_timer = 60

    while running:
        # Player loses, game over screen
        while gameOver == True:
            background()

            gameOver_message_font = pygame.font.Font('freesansbold.ttf', 60)
            gameOver_message_text = gameOver_message_font.render(
                'Game Over', True, RED)

            continue_font = pygame.font.Font('freesansbold.ttf', 25)
            continue_text = continue_font.render(
                'Press C to play again, or press Q to quit', True, WHITE)

            stats_font = pygame.font.Font('freesansbold.ttf', 20)
            final_score = stats_font.render('Score:', True, WHITE)
            time_survived_text = stats_font.render(
                'Time Survived:', True, WHITE)
            asteroids_destroyed_text = stats_font.render(
                'Asteroids Destroyed:', True, WHITE)
            aliens_destroyed_text = stats_font.render(
                'Aliens Destroyed:', True, WHITE)

            # stat numbers
            stats_score = stats_font.render(str(score), True, GREEN)
            stats_time_survived = stats_font.render(
                str(time_survived), True, GREEN)
            stats_asteroids_destroyed = stats_font.render(
                str(asteroids_destroyed), True, GREEN)
            stats_aliens_destroyed = stats_font.render(
                str(aliens_destroyed), True, GREEN)

            screen.blit(gameOver_message_text, (335, 150))

            screen.blit(final_score, (400, 300))
            screen.blit(time_survived_text, (400, 325))
            screen.blit(asteroids_destroyed_text, (400, 350))
            screen.blit(aliens_destroyed_text, (400, 375))

            screen.blit(stats_score, (475, 300))
            screen.blit(stats_time_survived, (555, 325))
            screen.blit(stats_asteroids_destroyed, (612, 350))
            screen.blit(stats_aliens_destroyed, (585, 375))

            screen.blit(continue_text, (275, 600))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running == False
                    gameOver == False
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -1
                if event.key == pygame.K_RIGHT:
                    playerX_change = 1
                if event.key == pygame.K_SPACE:
                    for i in range(missile_count):
                        if missile_state[i] is "ready":
                            missile_state[i] = "fire"
                            missileX[i] = playerX
                            fire_missile(missileX[i], missileY[i], i)
                            available_missiles -= 1
                            break
                elif event.key == pygame.K_p:
                    pause()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Print BG
        background()

        # Print Static Text and Dynamic Ammo Count
        ammo_text()
        ammo_count_text(available_missiles)
        score_text()

        elapsed_time = time.time() - start_time

        # Base score increase
        if elapsed_time > score_timer:
            score += 10
            score_timer += 1
            time_survived += 1
        score_count(score)

        # Asteroids
        # Asteroid Spawning
        if elapsed_time > time_limit:
            time_limit += 4
            if asteroid_count < 25:
                asteroid_count = asteroid_count + 1
                update_asteroids(asteroidImage,
                                 asteroidX, asteroidY, asteroidY_change, asteroid_state)

        # Asteroid Resetting
        for i in range(asteroid_count):
            asteroidY[i] += asteroidY_change[i]
            if asteroidY[i] > 800:
                asteroidY[i] = -30
                asteroidX[i] = random.randint(0, 936)
                asteroidY_change[i] = random.uniform(.3, .8)
                asteroid_state[i] = "ready"

            if asteroid_state[i] == "ready":
                asteroid(asteroidX[i], asteroidY[i], i)
                # Asteroid/Player Collision
                if isCollision(asteroidX[i], asteroidY[i], playerX, playerY):
                    asteroid_state[i] = "blown up"
                    if heart_state[0] is "ready":
                        heart_state[0] = "used"
                    elif heart_state[1] is "ready":
                        heart_state[1] = "used"
                    elif heart_state[2] is "ready":
                        heart_state[2] = "used"
                    if heart_state[0] is not "ready" and heart_state[1] is not "ready" and heart_state[2] is not "ready":
                        gameOver = True

        # Missiles
        for i in range(missile_count):
            if missile_state[i] is "fire":
                fire_missile(missileX[i], missileY[i], i)
                missileY[i] += missileY_change[i]
                # Alien/Missile Collision
                if isCollision(missileX[i], missileY[i], alienX, alienY):
                    explosion(alienX, alienY)
                    alien_state = "waiting"
                    alienX = random.randint(0, 936)
                    alienY = -64
                    alienY_change = random.uniform(.4, .85)
                    missile_state[i] = "detonated"
                    score += 500
                    aliens_destroyed += 1
                # Missile/Asteroid Collision
                for j in range(asteroid_count):
                    if isCollision(missileX[i], missileY[i], asteroidX[j], asteroidY[j]) and asteroid_state[j] == "ready":
                        explosion(asteroidX[j], asteroidY[j])
                        asteroid_state[j] = "blown up"
                        missile_state[i] = "detonated"
                        score += 20
                        asteroids_destroyed += 1

            if missileY[i] < 0:
                missile_state[i] = "detonated"
                missileY[i] = playerY
                missileX[i] = playerX

        # Alien
        if elapsed_time > alien_timer and alien_state is "waiting":
            alien_state = "spawning"
            alien_timer += 5
        if alien_state is "spawning":
            alienX += alienX_change
            alienY += alienY_change
            alien(alienX, alienY)
        if alienY > 800:
            alien_state = "waiting"
            alienX = random.randint(0, 936)
            alienY = -64
            alienY_change = random.uniform(.4, .6)

        # Ammo spawning, resetting
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

        # Player Picking Up Ammo
        if isCollision(playerX, playerY, ammoX, ammoY):
            if ammo_state is "ready":
                missile_update()
                available_missiles = 10
                ammo_state = "waiting"

        # Heart spawning, resetting
        if elapsed_time > heart_spawn_timer:
            heart_spawn_timer += 60
            heart_spawn_state = "ready"
        if heart_spawn_state == "ready":
            heartY_spawn += heartY_change
            heart_spawn(heartX_spawn, heartY_spawn)
        if heartY_spawn > 800:
            heartY_spawn = -40
            heartX_spawn = random.randint(0, 968)
            heart_spawn_state = "waiting"

        if isCollision(playerX, playerY, heartX_spawn, heartY_spawn):
            if heart_spawn_state == "ready":
                if heart_state[1] == "used":
                    heart_state[1] = "ready"
                elif heart_state[0] == "used":
                    heart_state[0] = "ready"

            heart_spawn_state = "waiting"
            heartY_spawn = -40
            heartX_spawn = random.randint(0, 968)

        # heart display
        for i in range(heart_count):
            if heart_state[i] == "ready":
                heart(heartX[i], heartY[i], i)
            # if heart_state not ready (collision with asteroid) then dont display

        # Player
        playerX += playerX_change
        if playerX > 936:
            playerX = 936
        if playerX < 0:
            playerX = 0
        player(playerX, playerY)
        pygame.display.update()


gameLoop()
