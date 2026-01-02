import asyncio
import pygame

from tic_tac_toe import run_tic_tac_toe
from space_arcade import run_space_arcade

pygame.init()
pygame.font.init()

# ---------- SCREEN ----------
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Arcademia")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ---------- ASSETS ----------
assets = {}

def load_assets():
    try:
        # Menu UI graphics
        assets['menu_background'] = pygame.image.load('assets/menu_background.png').convert()
        assets['space_box_original'] = pygame.image.load('assets/select_box_space.png').convert_alpha()
        assets['ttt_box_original'] = pygame.image.load('assets/select_box_ttt.png').convert_alpha()

        # Fonts
        assets['title_font'] = pygame.font.Font('freesansbold.ttf', 50)
        assets['loading_font'] = pygame.font.Font('freesansbold.ttf', 40)

        # Space Invader graphics and sounds
        assets['space_background_orig'] = pygame.image.load('assets/background.png').convert()
        assets['player_img'] = pygame.image.load('assets/player.png').convert_alpha()
        assets['enemy_img'] = pygame.image.load('assets/enemy.png').convert_alpha()
        assets['bullet_img'] = pygame.image.load('assets/bomb.png').convert_alpha()
        assets['laser_sound'] = pygame.mixer.Sound('assets/laser.wav')
        assets['explosion_sound'] = pygame.mixer.Sound('assets/explosion.wav')

    except Exception as e:
        print("Asset loading error:", e)

load_assets()

# ---------- MENU ELEMENTS ----------
BOX_WIDTH, BOX_HEIGHT = 300, 400
assets['space_box'] = pygame.transform.scale(assets['space_box_original'], (BOX_WIDTH, BOX_HEIGHT))
assets['ttt_box'] = pygame.transform.scale(assets['ttt_box_original'], (BOX_WIDTH, BOX_HEIGHT))

title_text = assets['title_font'].render("ARCADEMIA", True, WHITE)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 70))

space_box_rect = assets['space_box'].get_rect(center=(SCREEN_WIDTH * 0.28, SCREEN_HEIGHT / 2))
ttt_box_rect = assets['ttt_box'].get_rect(center=(SCREEN_WIDTH * 0.72, SCREEN_HEIGHT / 2))

space_play_button = pygame.Rect(0, 0, 150, 50)
space_play_button.center = (space_box_rect.centerx, space_box_rect.bottom - 60)

ttt_play_button = pygame.Rect(0, 0, 150, 50)
ttt_play_button.center = (ttt_box_rect.centerx, ttt_box_rect.bottom - 60)

# ---------- LOADING SCREEN ----------
async def show_loading_screen(message="Loading...", min_time=500):
    """
    Displays a quick animated 'Loading...' before game start.
    min_time = minimum display time in ms
    """
    clock = pygame.time.Clock()
    dot_count = 0
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < min_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill(BLACK)
        dots = "." * (dot_count % 4)
        text_surface = assets['loading_font'].render(message + dots, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        dot_count += 1
        clock.tick(5)  # Update dots 5 times/sec
        await asyncio.sleep(0)

    return True

# ---------- MAIN LOOP ----------
async def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if space_play_button.collidepoint(event.pos):
                    ok = await show_loading_screen("Loading Space Invader", min_time=400)
                    if ok:
                        await run_space_arcade(screen, assets)

                if ttt_play_button.collidepoint(event.pos):
                    ok = await show_loading_screen("Loading Ultimate Tic Tac Toe", min_time=400)
                    if ok:
                        await run_tic_tac_toe(screen)

        # Draw menu
        screen.blit(assets['menu_background'], (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(assets['space_box'], space_box_rect)
        screen.blit(assets['ttt_box'], ttt_box_rect)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
