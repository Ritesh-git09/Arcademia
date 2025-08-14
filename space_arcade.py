import pygame
import random
import math
import sys
from pygame import mixer

def run_space_arcade(screen, assets):
    # Pull preloaded assets
    background_orig = assets['space_background_orig']
    playerimg = assets['player_img']
    enemyimg_asset = assets['enemy_img']
    bulletimg = assets['bullet_img']
    bullet_sound = assets['laser_sound']
    explosion_sound = assets['explosion_sound']

    # Speed tuning
    PLAYER_SPEED = 7.0
    ENEMY_X_SPEED = 3.0
    ENEMY_Y_DROP = 60

    # Scale background ONCE
    bg_scaled = pygame.transform.scale(background_orig, (screen.get_width(), screen.get_height()))

    try:
        mixer.music.load('assets/backgroundsong.mp3')
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)
    except pygame.error as e:
        print(f"Could not load space arcade music: {e}")

    playerX = 370
    playerY = 800
    playerx_change = 0

    enemyimg = []
    enemyX, enemyY, enemyx_change, enemyy_change = [], [], [], []
    num_enemy = 6
    for i in range(num_enemy):
        enemyimg.append(enemyimg_asset)
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyx_change.append(ENEMY_X_SPEED)
        enemyy_change.append(ENEMY_Y_DROP)

    bulletX, bulletY = 0, playerY
    bullet_state = "ready"
    bullety_change = 10

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    game_over = False

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (screen.get_width()//2 - 180, screen.get_height()//2 - 50))

    def show_score():
        score_render = font.render("Score :" + str(score_value), True, (255, 255, 255))
        screen.blit(score_render, (10, 10))

    def player(x, y):
        screen.blit(playerimg, (x, y))

    def enemy(x, y, i):
        screen.blit(enemyimg[i], (x, y))

    def fire_bullet(x, y):
        nonlocal bullet_state
        bullet_state = "fire"
        screen.blit(bulletimg, (x + 16, y + 10))

    def is_collision(ex, ey, bx, by):
        distance = math.sqrt((math.pow(ex - bx, 2)) + (math.pow(ey - by, 2)))
        return distance < 27

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.blit(bg_scaled, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if not game_over:
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        playerx_change = -PLAYER_SPEED
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        playerx_change = PLAYER_SPEED
                    if event.key == pygame.K_SPACE and bullet_state == "ready":
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT):
                    playerx_change = 0.0

        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()

        if not game_over:
            playerX += playerx_change
            if playerX <= 0: playerX = 0
            elif playerX >= SCREEN_WIDTH - 64: playerX = SCREEN_WIDTH - 64

            for i in range(num_enemy):
                if enemyY[i] > SCREEN_HEIGHT - 150:
                    game_over = True
                    break

                enemyX[i] += enemyx_change[i]
                if not 0 <= enemyX[i] <= SCREEN_WIDTH - 64:
                    enemyx_change[i] *= -1
                    enemyY[i] += enemyy_change[i]

                if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
                    explosion_sound.play()
                    bulletY = playerY
                    bullet_state = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, SCREEN_WIDTH - 65)
                    enemyY[i] = random.randint(50, 150)

                enemy(enemyX[i], enemyY[i], i)

            if bulletY <= 0:
                bulletY = playerY
                bullet_state = "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bullety_change

            player(playerX, playerY)
        else:
            game_over_text()

        show_score()
        pygame.display.update()
        clock.tick(60)

    mixer.music.stop()
    return
