# Arcademia 🎮

A collection of retro arcade games built with Python and Pygame, featuring Space Invaders and Ultimate Tic Tac Toe.

## Features

### 🚀 Space Invader
- Defend against incoming enemies
- Shoot to eliminate targets and earn points
- Progressive difficulty as the game advances
- Smooth animations and sound effects
- **Controls:**
  - `A` / `Left Arrow` - Move left
  - `D` / `Right Arrow` - Move right
  - `Space` - Fire bullet
  - `ESC` - Return to menu

### ⭕ Ultimate Tic Tac Toe
- Play the advanced version of classic Tic Tac Toe
- 9x9 grid divided into 3x3 sub-grids
- Win individual grids to claim the main board sections
- First to win 3 grids in a row wins the game
- **Controls:**
  - `Mouse Click` - Place your piece
  - `ESC` - Return to menu

## Installation

### Requirements
- Python 3.7+
- Pygame

### Setup
```bash
# Clone or navigate to the project directory
cd Arcademia

# Install dependencies
pip install pygame

# Run the game
python main.py
```

## Project Structure
```
Arcademia/
├── main.py                 # Main menu and game launcher
├── space_arcade.py         # Space Invader game logic
├── tic_tac_toe.py         # Ultimate Tic Tac Toe game logic
├── assets/                # Game graphics and audio
│   ├── background.png
│   ├── player.png
│   ├── enemy.png
│   ├── bomb.png
│   ├── menu_background.png
│   ├── select_box_space.png
│   ├── select_box_ttt.png
│   ├── laser.wav
│   └── explosion.wav
└── README.md
```

## Performance Optimizations (v1.1)

### Recent Improvements
- **Collision Detection Optimization**: Collision checks now only execute when a bullet is actively firing, reducing unnecessary calculations
- **Overlay Caching**: Tic Tac Toe winner overlays are cached to prevent recreating surfaces every frame
- **Efficient Rendering**: Reduced redundant screen updates and frame processing

These optimizations eliminate the previous lagging issues that occurred during intense gameplay.

## Technical Details

### Architecture
- **Async Game Loop**: Uses asyncio for non-blocking gameplay suitable for web/browser environments
- **Pygame Foundation**: Built on Pygame for cross-platform compatibility
- **Modular Design**: Separate modules for each game with independent game loops

### Key Classes & Functions
- `run_space_arcade()` - Space Invader game async function
- `run_tic_tac_toe()` - Ultimate Tic Tac Toe async function
- `show_loading_screen()` - Animated loading screen between games

## Controls Reference

| Key | Action |
|-----|--------|
| `ESC` | Return to main menu |
| `Left/Right Arrows` or `A/D` | Move player (Space) |
| `Space` | Fire bullet (Space) |
| `Mouse Click` | Place piece (Tic Tac Toe) |

## Game States

### Menu
- Select between Space Invader and Ultimate Tic Tac Toe
- Animated loading screen before each game

### Space Invader
- Enemies move left-right and drop down
- Game ends when enemies reach the bottom
- Score increases with each enemy destroyed

### Tic Tac Toe
- Alternate turns between X and O
- Win a 3x3 grid to claim that section
- Game ends when one player wins 3 grids in a row

## Assets

All game assets are included in the `assets/` directory:
- PNG images for backgrounds, sprites, and UI elements
- WAV audio files for sound effects

## Future Enhancements

- [ ] Leaderboard system
- [ ] Difficulty levels for Space Invader
- [ ] Network multiplayer for Tic Tac Toe
- [ ] Additional game modes
- [ ] Mobile touch controls

## License

This project is provided as-is for educational and entertainment purposes.

## Credits

Built with Python and Pygame - The cross-platform set of Python modules designed for writing video games.

---

**Version:** 1.1  
**Last Updated:** January 2, 2026  
**Status:** Stable - Performance optimizations complete
