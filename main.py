import pygame
import sys
import time

from tic_tac_toe import run_tic_tac_toe
from space_arcade import run_space_arcade

pygame.init()
pygame.font.init()
pygame.mixer.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("My Python Arcade")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

assets = {}

try:
    assets['menu_background'] = pygame.image.load('assets/menu_background.png').convert()
    assets['space_box_original'] = pygame.image.load('assets/select_box_space.png').convert_alpha()
    assets['ttt_box_original'] = pygame.image.load('assets/select_box_ttt.png').convert_alpha()
    assets['title_font'] = pygame.font.Font('freesansbold.ttf', 50)
    assets['loading_font'] = pygame.font.Font('freesansbold.ttf', 40)

    assets['space_background_orig'] = pygame.image.load('assets/background.png').convert()
    assets['player_img'] = pygame.image.load('assets/player.png').convert_alpha()
    assets['enemy_img'] = pygame.image.load('assets/enemy.png').convert_alpha()
    assets['bullet_img'] = pygame.image.load('assets/bomb.png').convert_alpha()
    assets['laser_sound'] = pygame.mixer.Sound('assets/laser.wav')
    assets['explosion_sound'] = pygame.mixer.Sound('assets/explosion.wav')

    pygame.mixer.music.load('assets/background_music_menu.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"FATAL: Could not load critical asset: {e}")
    sys.exit()

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

app_state = 'main_menu'
clock = pygame.time.Clock()
running = True

def show_loading_screen_until_ready(message, launch_function, *args):
    """Show animated loading screen until launch_function finishes loading and returns."""
    dot_count = 0
    loading_complete = False

    # We'll spawn a flag changed by launch_function
    # Launch the game function in a way that loading happens first, then execution

    # To simulate this effectively without threads, call launch_function
    # just after displaying loading screen for a moment.

    # This example assumes launch_function does all loading instantly,
    # but you can extend for threaded loading.

    # Display loading animation for at least a short moment for UX
    start_time = time.time()
    min_loading_time = 1.0  # seconds minimum

    # Show first frame
    screen.fill(BLACK)
    text_surface = assets['loading_font'].render(message, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

    # brief pause to allow user to see loading screen before launch
    pygame.time.delay(300)

    # Now call the function (e.g. run game) which will run and block here for game duration
    launch_function(*args)

    # When game returns, loading is complete, so this function ends and control returns.

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if app_state == 'main_menu':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if space_play_button.collidepoint(event.pos):
                    show_loading_screen_until_ready("Loading Space Invader...", run_space_arcade, screen, assets)
                    app_state = 'main_menu'
                if ttt_play_button.collidepoint(event.pos):
                    show_loading_screen_until_ready("Loading Ultimate Tic Tac Toe...", run_tic_tac_toe, screen)
                    app_state = 'main_menu'

    if app_state == 'main_menu':
        screen.blit(assets['menu_background'], (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(assets['space_box'], space_box_rect)
        screen.blit(assets['ttt_box'], ttt_box_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
