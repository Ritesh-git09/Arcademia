import asyncio
import pygame
import random
import math

async def run_space_arcade(screen, assets):
    """
    Faster Space Invader for Pybag/web:
    - No background music (to avoid browser audio blocking)
    - Background image scaled once from preloaded asset
    - Quick async init so loading splash displays
    """

    # ---------- SETTINGS ----------
    PLAYER_SPEED = 7.0
    ENEMY_X_SPEED = 3.0
    ENEMY_Y_DROP = 60
    BULLET_SPEED = 10
    NUM_ENEMY = 6

    # ---------- ASSETS ----------
    # Use pre-scaled background from preloaded image
    background = pygame.transform.scale(
        assets['space_background_orig'], screen.get_size()
    )
    playerimg = assets['player_img']
    enemyimg_asset = assets['enemy_img']
    bulletimg = assets['bullet_img']
    bullet_sound = assets['laser_sound']
    explosion_sound = assets['explosion_sound']

    # ---------- QUICK INIT ----------
    # Player setup
    playerX, playerY = 370, screen.get_height() - 100
    playerx_change = 0

    # Enemy setup
    enemyimg, enemyX, enemyY, enemyx_change, enemyy_change = [], [], [], [], []
    for _ in range(NUM_ENEMY):
        enemyimg.append(enemyimg_asset)
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyx_change.append(ENEMY_X_SPEED)
        enemyy_change.append(ENEMY_Y_DROP)

    # Bullet setup
    bulletX, bulletY = 0, playerY
    bullet_state = "ready"

    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 32)
    over_font = pygame.font.Font('freesansbold.ttf', 64)

    # ---------- HELPERS ----------
    def show_score():
        score_render = font.render(f"Score : {score_value}", True, (255, 255, 255))
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
        return math.hypot(ex - bx, ey - by) < 27

    # ---------- GAME LOOP ----------
    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        screen.blit(background, (0, 0))

        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit to menu
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
            if event.type == pygame.KEYUP and event.key in (
                pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT
            ):
                playerx_change = 0

        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

        # GAME LOGIC
        if not game_over:
            # Move player
            playerX += playerx_change
            playerX = max(0, min(SCREEN_WIDTH - 64, playerX))

            # Enemy movement
            for i in range(NUM_ENEMY):
                if enemyY[i] > SCREEN_HEIGHT - 150:
                    game_over = True
                    break
                enemyX[i] += enemyx_change[i]
                if enemyX[i] <= 0 or enemyX[i] >= SCREEN_WIDTH - 64:
                    enemyx_change[i] *= -1
                    enemyY[i] += enemyy_change[i]

                # Collision check (only when bullet is firing)
                if bullet_state == "fire" and is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
                    explosion_sound.play()
                    bulletY = playerY
                    bullet_state = "ready"
                    score_value += 1
                    enemyX[i] = random.randint(0, SCREEN_WIDTH - 64)
                    enemyY[i] = random.randint(50, 150)

                enemy(enemyX[i], enemyY[i], i)

            # Bullet movement
            if bulletY <= 0:
                bulletY = playerY
                bullet_state = "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= BULLET_SPEED

            # Draw player
            player(playerX, playerY)
        else:
            over_txt = over_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(
                over_txt,
                (SCREEN_WIDTH // 2 - over_txt.get_width() // 2,
                 SCREEN_HEIGHT // 2 - over_txt.get_height() // 2)
            )

        # HUD and refresh
        show_score()
        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)  # Allow browser event loop to run

    # No music stop needed (music removed)
