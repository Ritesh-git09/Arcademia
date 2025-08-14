import asyncio
import pygame
import random
import math
from pygame import mixer

async def run_space_arcade(screen, assets):
    background_orig = assets['space_background_orig']
    playerimg = assets['player_img']
    enemyimg_asset = assets['enemy_img']
    bulletimg = assets['bullet_img']
    bullet_sound = assets['laser_sound']
    explosion_sound = assets['explosion_sound']

    PLAYER_SPEED = 7.0
    ENEMY_X_SPEED = 3.0
    ENEMY_Y_DROP = 60
    BULLET_SPEED = 10

    bg_scaled = pygame.transform.scale(background_orig, (screen.get_width(), screen.get_height()))

    try:
        mixer.music.load('assets/backgroundsong.mp3')
        mixer.music.set_volume(0.4)
        mixer.music.play(-1)
    except pygame.error:
        pass

    playerX, playerY = 370, 800
    playerx_change = 0

    enemyimg, enemyX, enemyY, enemyx_change, enemyy_change = [], [], [], [], []
    num_enemy = 6
    for i in range(num_enemy):
        enemyimg.append(enemyimg_asset)
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyx_change.append(ENEMY_X_SPEED)
        enemyy_change.append(ENEMY_Y_DROP)

    bulletX, bulletY = 0, playerY
    bullet_state = "ready"

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    over_font = pygame.font.Font('freesansbold.ttf', 64)

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
    game_over = False

    while running:
        screen.blit(bg_scaled, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
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
                    playerx_change = 0

        SCREEN_WIDTH = screen.get_width()
        SCREEN_HEIGHT = screen.get_height()

        if not game_over:
            playerX += playerx_change
            playerX = max(0, min(SCREEN_WIDTH - 64, playerX))

            for i in range(num_enemy):
                if enemyY[i] > SCREEN_HEIGHT - 150:
                    game_over = True
                    break
                enemyX[i] += enemyx_change[i]
                if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:
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
                bulletY -= BULLET_SPEED

            player(playerX, playerY)
        else:
            game_over_text()
        show_score()
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

    mixer.music.stop()
