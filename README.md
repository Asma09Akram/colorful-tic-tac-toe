# 🎮 Enhanced Colorful Tic Tac Toe Game

A visually appealing and feature-rich Tic Tac Toe game built with Pygame featuring colorful graphics, smooth animations, and multiple game modes.

## ✨ New Features & Improvements

### 🛠️ Fixed Issues
- **Overlapping Player Text**: Fixed the issue where player X and player O text were overlapping on the game console
- **Improved Layout**: Extended the game window with a dedicated status area at the bottom
- **Visual Clarity**: Added proper background clearing before drawing status text

### 🎨 Visual Enhancements
- **Animated Game Pieces**: X's and O's now appear with smooth animations when placed
- **Color-Coded Players**: Each player has their own distinct color (X: red, O: blue)
- **Turn Indicator**: Clear visual indicator showing whose turn it is
- **Timer Bar**: Visual countdown bar showing remaining time for the current turn
- **Button Hover Effects**: Interactive feedback when hovering over buttons
- **Status Area**: Dedicated area for game information and controls

### 🎲 Gameplay Features
- **Score Tracking System**: Keeps track of X wins, O wins, and draws across multiple games
- **Turn Timer**: Players have 10 seconds to make a move before their turn is skipped
- **Game Modes**:
  - **Player vs Player (PVP)**: Play against a friend on the same computer
  - **Player vs Computer (PVC)**: Challenge the AI opponent
- **AI Difficulty Levels**:
  - **Easy**: Makes random moves
  - **Medium**: Tries to win or block opponent's winning moves
  - **Hard**: Uses strategic play (prioritizes center, corners, and edges)
- **Interactive Mode Toggle**: Switch between PVP and PVC with a simple click
- **Difficulty Toggle**: Cycle through AI difficulty levels with a click
- **Draw Detection**: Game correctly identifies draws when all 9 squares are filled with no winner

## 🚀 How to Run

Run the enhanced version of the game using Python:

```bash
python3 enhanced_tic_tac_toe.py
```

## 🎯 How to Play

1. Click on any empty square to place your mark (X or O)
2. The game will automatically detect wins or draws
3. If you don't make a move within 10 seconds, your turn will be skipped
4. The score is tracked at the bottom of the screen
5. Click the "Play Again" button to restart after a game ends
6. Click on "Mode: PVP/PVC" to toggle between playing against another player or the computer
7. In PVC mode, click on "AI: Easy/Medium/Hard" to change the computer's difficulty level

## 🎮 Game Controls

- **Mouse Click**: Place X or O on the board
- **Close Window**: Exit the game
- **Mode Toggle**: Click on the mode text to switch between PVP and PVC
- **Difficulty Toggle**: Click on the AI difficulty text to cycle through levels (in PVC mode)
- **Play Again**: Click the button to restart the game after it ends

## 🧩 Game Logic

The game follows standard Tic Tac Toe rules:
- Players take turns placing their marks (X or O) on the 3x3 grid
- The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins
- If all 9 squares are filled and no player has won, the game is a draw
- If a player doesn't make a move within 10 seconds, their turn is skipped

### AI Logic
- **Easy**: Makes completely random moves
- **Medium**: Tries to win if possible, blocks opponent's winning moves, otherwise makes random moves
- **Hard**: Uses strategy - tries to win, blocks opponent, prioritizes center, corners, and edges in that order

## 🔧 Technical Details

- **Animation System**: Smooth transitions when placing game pieces
- **Timer System**: Visual and functional timer for each player's turn
- **Event-Driven Programming**: Responsive user interactions
- **State Management**: Tracks game state, scores, and settings
- **AI Algorithm**: Three-tiered difficulty system for computer opponent
- **Draw Detection**: Automatically detects when all squares are filled with no winner

## 🛠️ Installation Requirements

Before running the game, you need to install Pygame:

```bash
# For most systems
pip install pygame

# For Debian/Ubuntu systems
sudo apt-get install python3-pygame
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Pygame](https://www.pygame.org/) - The game development library used

## 🔄 Future Enhancements

Potential features for future versions:
- Sound effects for game actions
- Background music options
- Customizable player colors and board themes
- Game history and statistics tracking
- Network multiplayer support
- Adjustable board size (4x4, 5x5, etc.)
- Save/load game functionality
