#!/usr/bin/env python3
import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (66, 133, 244)
BUTTON_HOVER_COLOR = (25, 103, 210)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Colorful Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
game_over = False
winner = None
player = 'X'

# Fonts
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)

def draw_lines():
    """Draw the board lines"""
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    """Draw X's and O's on the board"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                # Draw X
                pygame.draw.line(
                    screen, CROSS_COLOR,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    ((col + 1) * SQUARE_SIZE - SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen, CROSS_COLOR,
                    ((col + 1) * SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                    (col * SQUARE_SIZE + SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                    CROSS_WIDTH
                )
            elif board[row][col] == 'O':
                # Draw O
                pygame.draw.circle(
                    screen, CIRCLE_COLOR,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )

def mark_square(row, col, player):
    """Mark a square with X or O"""
    board[row][col] = player

def available_square(row, col):
    """Check if a square is available"""
    return board[row][col] is None

def is_board_full():
    """Check if the board is full"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_win():
    """Check if someone has won"""
    # Check vertical win
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            draw_vertical_winning_line(col)
            return board[0][col]

    # Check horizontal win
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            draw_horizontal_winning_line(row)
            return board[row][0]

    # Check diagonal win (top-left to bottom-right)
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        draw_diagonal_winning_line(0)
        return board[0][0]

    # Check diagonal win (top-right to bottom-left)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        draw_diagonal_winning_line(1)
        return board[0][2]

    return None

def draw_vertical_winning_line(col):
    """Draw a vertical line for a win"""
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(
        screen, (255, 50, 50),
        (posX, 15),
        (posX, HEIGHT - 15),
        15
    )

def draw_horizontal_winning_line(row):
    """Draw a horizontal line for a win"""
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(
        screen, (255, 50, 50),
        (15, posY),
        (WIDTH - 15, posY),
        15
    )

def draw_diagonal_winning_line(direction):
    """Draw a diagonal line for a win"""
    if direction == 0:  # top-left to bottom-right
        pygame.draw.line(
            screen, (255, 50, 50),
            (15, 15),
            (WIDTH - 15, HEIGHT - 15),
            15
        )
    else:  # top-right to bottom-left
        pygame.draw.line(
            screen, (255, 50, 50),
            (WIDTH - 15, 15),
            (15, HEIGHT - 15),
            15
        )

def draw_status():
    """Draw game status text"""
    if game_over:
        if winner:
            text = f"Player {winner} wins!"
        else:
            text = "It's a draw!"
        
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        
        # Draw background for text
        pygame.draw.rect(screen, (0, 0, 0, 128), 
                         (text_rect.x - 10, text_rect.y - 10, 
                          text_rect.width + 20, text_rect.height + 20))
        
        screen.blit(text_surface, text_rect)
        
        # Draw restart button
        pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - 100, HEIGHT - 100, 200, 50), border_radius=10)
        restart_text = small_font.render("Play Again", True, TEXT_COLOR)
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 75)))
    else:
        text = f"Player {player}'s turn"
        text_surface = small_font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (20, HEIGHT - 40))

def restart():
    """Restart the game"""
    global board, game_over, winner, player
    screen.fill(BG_COLOR)
    draw_lines()
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    winner = None
    player = 'X'

def check_button_hover(pos):
    """Check if mouse is hovering over restart button"""
    if game_over:
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
        return button_rect.collidepoint(pos)
    return False

# Draw initial board
draw_lines()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            
            if clicked_row < BOARD_ROWS and clicked_col < BOARD_COLS:
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    winner = check_win()
                    if winner:
                        game_over = True
                    elif is_board_full():
                        game_over = True
                    else:
                        player = 'O' if player == 'X' else 'X'
                    
                    draw_figures()
        
        # Handle restart button click
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            
            button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)
            if button_rect.collidepoint((mouseX, mouseY)):
                restart()
        
        # Change button color on hover
        if event.type == pygame.MOUSEMOTION:
            if check_button_hover(event.pos):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, 
                                (WIDTH // 2 - 100, HEIGHT - 100, 200, 50), border_radius=10)
                restart_text = small_font.render("Play Again", True, TEXT_COLOR)
                screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 75)))
            elif game_over:
                pygame.draw.rect(screen, BUTTON_COLOR, 
                                (WIDTH // 2 - 100, HEIGHT - 100, 200, 50), border_radius=10)
                restart_text = small_font.render("Play Again", True, TEXT_COLOR)
                screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 75)))
    
    draw_status()
    pygame.display.update()
