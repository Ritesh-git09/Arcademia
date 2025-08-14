import asyncio
import pygame

async def run_tic_tac_toe(screen):
    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()
    CELL_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 9

    LINE_COLOR = (0, 0, 0)
    BACKGROUND_COLOR = (255, 255, 255)
    X_COLOR = (66, 66, 66)
    O_COLOR = (200, 20, 20)
    MAIN_X_COLOR = (70, 70, 210, 150)
    MAIN_O_COLOR = (210, 70, 70, 150)
    PIECE_LINE_WIDTH = 10
    MAIN_PIECE_LINE_WIDTH = 25

    game_over_font = pygame.font.Font('freesansbold.ttf', 70)

    def create_new_board():
        return [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)], [[' ' for _ in range(3)] for _ in range(3)]]

    def draw_grid():
        for i in range(1, 9):
            width = 4 if i % 3 == 0 else 1
            pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, 9 * CELL_SIZE), width)
            pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (9 * CELL_SIZE, i * CELL_SIZE), width)

    def draw_pieces(main_board):
        for main_row in range(3):
            for main_col in range(3):
                for sub_row in range(3):
                    for sub_col in range(3):
                        mark = main_board[main_row][main_col][sub_row][sub_col]
                        if mark != ' ':
                            row = main_row * 3 + sub_row
                            col = main_col * 3 + sub_col
                            x, y = col * CELL_SIZE, row * CELL_SIZE
                            if mark == 'X':
                                pygame.draw.line(screen, X_COLOR, (x + 15, y + 15), (x + CELL_SIZE - 15, y + CELL_SIZE - 15), PIECE_LINE_WIDTH)
                                pygame.draw.line(screen, X_COLOR, (x + CELL_SIZE - 15, y + 15), (x + 15, y + CELL_SIZE - 15), PIECE_LINE_WIDTH)
                            else:
                                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                                radius = (CELL_SIZE // 2) - 15
                                pygame.draw.circle(screen, O_COLOR, center, radius, PIECE_LINE_WIDTH)

    def draw_main_winners(main_grid_status):
        for main_row in range(3):
            for main_col in range(3):
                if main_grid_status[main_row][main_col] in ['X', 'O']:
                    sub_grid_x = main_col * (3 * CELL_SIZE)
                    sub_grid_y = main_row * (3 * CELL_SIZE)
                    sub_grid_size = 3 * CELL_SIZE
                    overlay = pygame.Surface((sub_grid_size, sub_grid_size), pygame.SRCALPHA)
                    if main_grid_status[main_row][main_col] == 'X':
                        pygame.draw.line(overlay, MAIN_X_COLOR, (25, 25), (sub_grid_size - 25, sub_grid_size - 25), MAIN_PIECE_LINE_WIDTH)
                        pygame.draw.line(overlay, MAIN_X_COLOR, (sub_grid_size - 25, 25), (25, sub_grid_size - 25), MAIN_PIECE_LINE_WIDTH)
                    else:
                        center = (sub_grid_size // 2, sub_grid_size // 2)
                        radius = (sub_grid_size // 2) - 25
                        pygame.draw.circle(overlay, MAIN_O_COLOR, center, radius, MAIN_PIECE_LINE_WIDTH)
                    screen.blit(overlay, (sub_grid_x, sub_grid_y))

    def check_win(grid):
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] != ' ':
                return grid[i][0]
            if grid[0][i] == grid[1][i] == grid[2][i] != ' ':
                return grid[0][i]
        if grid[0][0] == grid[1][1] == grid[2][2] != ' ':
            return grid[0][0]
        if grid[0][2] == grid[1][1] == grid[2][0] != ' ':
            return grid[0][2]
        return None

    def draw_game_over(winner):
        text = game_over_font.render(f"Winner: {winner}!", True, (20, 150, 20))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        screen.blit(overlay, (0,0))
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))

    main_board, main_grid_status = create_new_board()
    player = 'X'
    game_winner = None

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            if event.type == pygame.MOUSEBUTTONDOWN and not game_winner:
                mouseX, mouseY = event.pos
                if mouseX < 9 * CELL_SIZE and mouseY < 9 * CELL_SIZE:
                    clicked_col, clicked_row = mouseX // CELL_SIZE, mouseY // CELL_SIZE
                    main_row, main_col = clicked_row // 3, clicked_col // 3
                    sub_row, sub_col = clicked_row % 3, clicked_col % 3
                    if main_grid_status[main_row][main_col] == ' ' and main_board[main_row][main_col][sub_row][sub_col] == ' ':
                        main_board[main_row][main_col][sub_row][sub_col] = player
                        winner = check_win(main_board[main_row][main_col])
                        if winner:
                            main_grid_status[main_row][main_col] = winner
                        game_winner = check_win(main_grid_status)
                        if not game_winner:
                            player = 'O' if player == 'X' else 'X'

        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_pieces(main_board)
        draw_main_winners(main_grid_status)
        if game_winner:
            draw_game_over(game_winner)
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
