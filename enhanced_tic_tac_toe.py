#!/usr/bin/env python3
import pygame
import sys
import time
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Constants
WIDTH, HEIGHT = 600, 700  # Increased height for score display
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
STATUS_BG_COLOR = (20, 120, 110)
X_SCORE_COLOR = (255, 100, 100)
O_SCORE_COLOR = (100, 100, 255)
TIMER_COLOR = (255, 215, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Enhanced Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
game_over = False
winner = None
player = 'X'
scores = {'X': 0, 'O': 0, 'Draws': 0}
game_mode = 'PVP'  # PVP (Player vs Player) or PVC (Player vs Computer)
difficulty = 'Easy'  # Easy, Medium, Hard
animation_progress = {}  # For tracking animation progress
turn_timer = 10  # Seconds per turn
timer_start = time.time()

# Load sounds
try:
    # Create dummy sounds since we don't have real sound files
    dummy_surface = pygame.Surface((2, 2))
    dummy_array = pygame.surfarray.array3d(dummy_surface)
    # Just set sound variables to None and handle in the code
    move_sound = None
    win_sound = None
    draw_sound = None
    print("Using silent sounds.")
except:
    move_sound = None
    win_sound = None
    draw_sound = None
    print("Sound system disabled.")

# Fonts
font = pygame.font.SysFont('Arial', 40)
small_font = pygame.font.SysFont('Arial', 30)
score_font = pygame.font.SysFont('Arial', 24)
timer_font = pygame.font.SysFont('Arial', 20)

def draw_lines():
    """Draw the board lines"""
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 100), LINE_WIDTH)

def draw_figures():
    """Draw X's and O's on the board with animation"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            pos = (row, col)
            if pos in animation_progress:
                progress = animation_progress[pos]
                if board[row][col] == 'X':
                    # Animated X
                    if progress <= 0.5:
                        # Draw first line of X
                        end_point = progress * 2  # Scale from 0-0.5 to 0-1
                        pygame.draw.line(
                            screen, CROSS_COLOR,
                            (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                            (col * SQUARE_SIZE + SPACE + end_point * (SQUARE_SIZE - 2 * SPACE), 
                             row * SQUARE_SIZE + SPACE + end_point * (SQUARE_SIZE - 2 * SPACE)),
                            CROSS_WIDTH
                        )
                    else:
                        # Draw complete first line
                        pygame.draw.line(
                            screen, CROSS_COLOR,
                            (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                            ((col + 1) * SQUARE_SIZE - SPACE, (row + 1) * SQUARE_SIZE - SPACE),
                            CROSS_WIDTH
                        )
                        # Draw second line of X
                        end_point = (progress - 0.5) * 2  # Scale from 0.5-1 to 0-1
                        pygame.draw.line(
                            screen, CROSS_COLOR,
                            ((col + 1) * SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE),
                            ((col + 1) * SQUARE_SIZE - SPACE - end_point * (SQUARE_SIZE - 2 * SPACE),
                             row * SQUARE_SIZE + SPACE + end_point * (SQUARE_SIZE - 2 * SPACE)),
                            CROSS_WIDTH
                        )
                elif board[row][col] == 'O':
                    # Animated O
                    pygame.draw.arc(
                        screen, CIRCLE_COLOR,
                        (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE,
                         SQUARE_SIZE - 2 * SPACE, SQUARE_SIZE - 2 * SPACE),
                        0, progress * 2 * math.pi, CIRCLE_WIDTH
                    )
                
                # Update animation progress
                animation_progress[pos] += 0.1
                if animation_progress[pos] >= 1:
                    animation_progress[pos] = 1
            
            elif board[row][col] == 'X':
                # Draw complete X
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
                # Draw complete O
                pygame.draw.circle(
                    screen, CIRCLE_COLOR,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )

def mark_square(row, col, player):
    """Mark a square with X or O and start animation"""
    board[row][col] = player
    animation_progress[(row, col)] = 0.1  # Start animation
    try:
        if move_sound:
            move_sound.play()
    except:
        pass

def available_square(row, col):
    """Check if a square is available"""
    return board[row][col] is None

def is_board_full():
    """Check if the board is full"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    print("Board is full - it's a draw!")
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
        (posX, HEIGHT - 115),
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
            (WIDTH - 15, HEIGHT - 115),
            15
        )
    else:  # top-right to bottom-left
        pygame.draw.line(
            screen, (255, 50, 50),
            (WIDTH - 15, 15),
            (15, HEIGHT - 115),
            15
        )

def draw_status_area():
    """Draw the status area at the bottom of the screen"""
    # Clear the status area
    pygame.draw.rect(screen, STATUS_BG_COLOR, (0, HEIGHT - 100, WIDTH, 100))
    
    # Draw scores
    x_score_text = score_font.render(f"X: {scores['X']}", True, X_SCORE_COLOR)
    o_score_text = score_font.render(f"O: {scores['O']}", True, O_SCORE_COLOR)
    draws_text = score_font.render(f"Draws: {scores['Draws']}", True, TEXT_COLOR)
    
    screen.blit(x_score_text, (20, HEIGHT - 90))
    screen.blit(o_score_text, (20, HEIGHT - 60))
    screen.blit(draws_text, (20, HEIGHT - 30))
    
    # Draw game mode
    mode_text = score_font.render(f"Mode: {game_mode}", True, TEXT_COLOR)
    screen.blit(mode_text, (WIDTH - 150, HEIGHT - 90))
    
    if game_mode == 'PVC':
        diff_text = score_font.render(f"AI: {difficulty}", True, TEXT_COLOR)
        screen.blit(diff_text, (WIDTH - 150, HEIGHT - 60))

def draw_status():
    """Draw game status text"""
    draw_status_area()
    
    if game_over:
        if winner:
            text = f"Player {winner} wins!"
            try:
                if win_sound:
                    win_sound.play()
            except:
                pass
        else:
            text = "It's a draw!"
            try:
                if draw_sound:
                    draw_sound.play()
            except:
                pass
        
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        screen.blit(text_surface, text_rect)
        
        # Draw restart button
        pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 2 - 100, HEIGHT - 40, 200, 30), border_radius=10)
        restart_text = small_font.render("Play Again", True, TEXT_COLOR)
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 25)))
    else:
        # Draw player turn indicator with background
        indicator_width = 180
        indicator_height = 40
        indicator_x = WIDTH // 2 - indicator_width // 2
        indicator_y = HEIGHT - 70
        
        # Draw background for turn indicator
        if player == 'X':
            indicator_color = X_SCORE_COLOR
        else:
            indicator_color = O_SCORE_COLOR
            
        pygame.draw.rect(screen, indicator_color, 
                        (indicator_x, indicator_y, indicator_width, indicator_height), 
                        border_radius=10)
        
        text = f"Player {player}'s turn"
        text_surface = small_font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50)))
        
        # Draw timer
        remaining_time = max(0, turn_timer - (time.time() - timer_start))
        timer_text = timer_font.render(f"Time: {int(remaining_time)}s", True, TIMER_COLOR)
        screen.blit(timer_text, (WIDTH // 2 - 40, HEIGHT - 30))
        
        # Draw timer bar
        timer_width = 150
        timer_height = 10
        timer_x = WIDTH // 2 - timer_width // 2
        timer_y = HEIGHT - 15
        
        # Background bar
        pygame.draw.rect(screen, (100, 100, 100), 
                        (timer_x, timer_y, timer_width, timer_height), 
                        border_radius=5)
        
        # Remaining time bar
        remaining_ratio = remaining_time / turn_timer
        pygame.draw.rect(screen, TIMER_COLOR, 
                        (timer_x, timer_y, int(timer_width * remaining_ratio), timer_height), 
                        border_radius=5)

def restart():
    """Restart the game"""
    global board, game_over, winner, player, timer_start
    screen.fill(BG_COLOR)
    draw_lines()
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    winner = None
    player = 'X'
    timer_start = time.time()
    animation_progress.clear()

def check_button_hover(pos):
    """Check if mouse is hovering over restart button"""
    if game_over:
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 40, 200, 30)
        return button_rect.collidepoint(pos)
    return False

def check_mode_button_hover(pos):
    """Check if mouse is hovering over mode button"""
    mode_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 90, 130, 25)
    return mode_button_rect.collidepoint(pos)

def check_difficulty_button_hover(pos):
    """Check if mouse is hovering over difficulty button"""
    if game_mode == 'PVC':
        diff_button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 60, 130, 25)
        return diff_button_rect.collidepoint(pos)
    return False

def toggle_game_mode():
    """Toggle between PVP and PVC modes"""
    global game_mode
    game_mode = 'PVC' if game_mode == 'PVP' else 'PVP'
    restart()

def toggle_difficulty():
    """Cycle through difficulty levels"""
    global difficulty
    if difficulty == 'Easy':
        difficulty = 'Medium'
    elif difficulty == 'Medium':
        difficulty = 'Hard'
    else:
        difficulty = 'Easy'

def computer_move():
    """Make a move for the computer based on difficulty"""
    if difficulty == 'Easy':
        # Random move
        available_moves = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    available_moves.append((row, col))
        
        if available_moves:
            row, col = random.choice(available_moves)
            return row, col
    
    elif difficulty == 'Medium':
        # Try to win, then block, then random
        # Check for winning move
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 'O'  # Try move
                    if check_win() == 'O':
                        board[row][col] = None  # Undo move
                        return row, col
                    board[row][col] = None  # Undo move
        
        # Check for blocking move
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 'X'  # Try opponent's move
                    if check_win() == 'X':
                        board[row][col] = None  # Undo move
                        return row, col
                    board[row][col] = None  # Undo move
        
        # Random move
        available_moves = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    available_moves.append((row, col))
        
        if available_moves:
            row, col = random.choice(available_moves)
            return row, col
    
    else:  # Hard
        # Try to win, block, take center, take corners, then edges
        # Check for winning move
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 'O'  # Try move
                    if check_win() == 'O':
                        board[row][col] = None  # Undo move
                        return row, col
                    board[row][col] = None  # Undo move
        
        # Check for blocking move
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 'X'  # Try opponent's move
                    if check_win() == 'X':
                        board[row][col] = None  # Undo move
                        return row, col
                    board[row][col] = None  # Undo move
        
        # Take center
        if available_square(1, 1):
            return 1, 1
        
        # Take corners
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for row, col in corners:
            if available_square(row, col):
                return row, col
        
        # Take edges
        edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
        random.shuffle(edges)
        for row, col in edges:
            if available_square(row, col):
                return row, col
    
    return None, None  # Should never reach here unless board is full

# Draw initial board
draw_lines()
draw_status_area()

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            
            # Handle game board clicks
            if not game_over and mouseY < HEIGHT - 100:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                
                if clicked_row < BOARD_ROWS and clicked_col < BOARD_COLS:
                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, player)
                        winner = check_win()
                        if winner:
                            game_over = True
                            scores[winner] += 1
                        elif is_board_full():
                            game_over = True
                            scores['Draws'] += 1
                        else:
                            player = 'O' if player == 'X' else 'X'
                            timer_start = time.time()  # Reset timer for next player
            
            # Handle restart button click
            if game_over and check_button_hover((mouseX, mouseY)):
                restart()
            
            # Handle mode button click
            if check_mode_button_hover((mouseX, mouseY)):
                toggle_game_mode()
            
            # Handle difficulty button click
            if check_difficulty_button_hover((mouseX, mouseY)):
                toggle_difficulty()
        
        # Change button color on hover
        if event.type == pygame.MOUSEMOTION:
            if check_button_hover(event.pos) and game_over:
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, 
                                (WIDTH // 2 - 100, HEIGHT - 40, 200, 30), border_radius=10)
                restart_text = small_font.render("Play Again", True, TEXT_COLOR)
                screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 25)))
    
    # Computer's turn
    if not game_over and player == 'O' and game_mode == 'PVC':
        # Add a small delay to make it feel more natural
        pygame.time.delay(500)
        row, col = computer_move()
        if row is not None and col is not None:
            mark_square(row, col, 'O')
            winner = check_win()
            if winner:
                game_over = True
                scores[winner] += 1
            elif is_board_full():
                game_over = True
                scores['Draws'] += 1
            else:
                player = 'X'
                timer_start = time.time()  # Reset timer for next player
    
    # Check for timer expiration
    if not game_over and time.time() - timer_start > turn_timer:
        # Time's up, switch players
        player = 'O' if player == 'X' else 'X'
        timer_start = time.time()  # Reset timer
    
    # Redraw the screen
    screen.fill(BG_COLOR, (0, 0, WIDTH, HEIGHT - 100))  # Clear game area but not status area
    draw_lines()
    draw_figures()
    draw_status()
    
    pygame.display.update()
    clock.tick(60)  # 60 FPS
