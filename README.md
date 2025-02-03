---
title: Battleship Game
emoji: 🚢
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.14.0
app_file: app.py
pinned: false
short_description: Play a simple Battleship game against an AI in a 5x5 grid.
---

# Battleship Game

A simple, interactive Battleship game built with Gradio, Matplotlib, and NumPy.  
The game sets up two 5x5 grids: one for the user and one for an AI. Each grid has three single-cell ships. Enter row and column values to fire at the AI’s ships.

## Features

- **Random Ship Placement**: Both player and AI boards are randomized at the start.  
- **Simple Firing Mechanics**: Input row and column to fire on the AI’s board.  
- **AI Guessing**: AI randomly selects a cell on the user’s board to fire back.  
- **Instant Feedback**: Real-time messages show hits, misses, and status updates.  
- **Visual Boards**: Two Matplotlib-based grids visually render hits, misses, and your own ships.

## Getting Started

### 1. Install Dependencies
Make sure you have [Python 3.7+](https://www.python.org/downloads/) installed.  
Install required libraries via:

```bash
pip install -r requirements.txt
```

### 2. Run the App

To run the app, use the following command:

```bash
python app.py
```

### 3. Open in Browser
Once the server starts, Gradio will print a local URL (e.g., http://127.0.0.1:7860).
Open it to start playing the game.


## How to Play

1. **Initial Load**  
   - You’ll see two boards: “Your Board” (with your ships) and “AI Board” (ships hidden).  
   - A “Color Key” plot also displays how ships, hits, and misses are represented.

2. **Firing**  
   - Enter a row (0–4) and column (0–4) in the input boxes.  
   - Press **Fire!** to attempt hitting an AI ship.

3. **Receiving Feedback**  
   - A **Game Messages** box updates each time you fire. It will show whether you hit or missed.  
   - The AI then fires back, and you’ll see if your ship got hit.  

4. **Winning and Losing**  
   - If you sink all three of the AI’s ships, you win!  
   - If the AI sinks all three of your ships, you lose.

5. **Resetting the Game**  
   - Press the **Reset Game** button to start over with brand new boards.

## Code Overview

- **`init_game()`**: Initializes two 5x5 boards for user and AI, randomly placing three ships on each.  
- **`plot_board(board, is_user_board=True)`**: Generates a Matplotlib plot of a board. It hides AI ships if `is_user_board=False`.  
- **`plot_color_key()`**: Generates a legend explaining the colors for ships, hits, and misses.  
- **`ai_guess(state)`**: Makes a random guess on the user’s board, marking hits and misses.  
- **`make_move(state, row, col)`**: Validates user guess and updates boards accordingly.  
- **`reset_game()`**: Resets the game state to start fresh.  
- **`update_display(state)`**: Helper that returns the plots and game message for quick updates.  

### Gradio Interface:
- The user can input row and column to fire; the interface displays live board updates.  
- `demo.load(...)` ensures the boards show as soon as the app loads.  
- The **Reset Game** button re-initializes the state and re-draws the boards.

## Requirements

The following dependencies are required to run the game:

```plaintext
gradio
matplotlib
numpy
```
