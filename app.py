import random
import gradio as gr
import matplotlib.pyplot as plt
import numpy as np

BOARD_SIZE = 5
NUM_SHIPS = 3

def place_ships(board, num_ships):
    """ Randomly place 'num_ships' single-cell ships on 'board'. """
    placed = 0
    while placed < num_ships:
        r, c = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
        if board[r][c] == 0:  # empty spot
            board[r][c] = 1
            placed += 1

def init_game():
    """ Create initial state for a new Battleship game. """
    user_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    ai_board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    
    place_ships(user_board, NUM_SHIPS)
    place_ships(ai_board, NUM_SHIPS)

    return {
        "user_board": user_board,
        "ai_board": ai_board,
        "user_ships_remaining": NUM_SHIPS,
        "ai_ships_remaining": NUM_SHIPS,
        "game_over": False,
        "message": "Game started! Enter row and column to fire.",
        "ai_guesses": set()
    }

def plot_board(board, is_user_board=True):
    """
    Visual representation of the game board using Matplotlib.
    Different colors are used for ships, hits, and misses.
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = {
        0: "#D3D3D3",  # Empty - Light Gray
        1: "#1E90FF" if is_user_board else "#D3D3D3",  # Ship - Blue for User, Hidden for AI
        2: "#FF0000",  # Hit - Red
        3: "#FFFFFF"   # Miss - White
    }

    grid = np.array(board)
    if not is_user_board:
        # Hide AI's ships by turning cells with '1' into '0'
        grid = np.where(grid == 1, 0, grid)

    colored_grid = np.vectorize(colors.get)(grid)
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            rect = plt.Rectangle((c, BOARD_SIZE - r - 1), 1, 1,
                                 facecolor=colored_grid[r][c],
                                 edgecolor="black")
            ax.add_patch(rect)

    ax.set_xticks(np.arange(BOARD_SIZE) + 0.5, labels=[str(i) for i in range(BOARD_SIZE)])
    ax.set_yticks(np.arange(BOARD_SIZE) + 0.5, labels=[str(i) for i in range(BOARD_SIZE)][::-1])
    ax.set_xticks(np.arange(BOARD_SIZE + 1), minor=True)
    ax.set_yticks(np.arange(BOARD_SIZE + 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=1)
    ax.set_xlim(0, BOARD_SIZE)
    ax.set_ylim(0, BOARD_SIZE)
    ax.set_frame_on(False)

    return fig

def plot_color_key():
    """ Generates a small color-coded key explaining the board symbols. """
    fig, ax = plt.subplots(figsize=(5, 1))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    color_labels = [
        ("#1E90FF", "Your Ship"),
        ("#FF0000", "Hit Ship"),
        ("#FFFFFF", "Miss"),
        ("#D3D3D3", "Hidden")
    ]

    for i, (color, label) in enumerate(color_labels):
        rect = plt.Rectangle((i, 0), 1, 1, facecolor=color, edgecolor="black")
        ax.add_patch(rect)
        ax.text(i + 0.5, 0.5, label, ha='center', va='center', fontsize=10)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    return fig

def ai_guess(state):
    """ AI randomly picks an unguessed cell in the user's board and marks hit/miss. """
    user_board = state["user_board"]
    valid_positions = [
        (r, c) for r in range(BOARD_SIZE) 
        for c in range(BOARD_SIZE) 
        if (r, c) not in state["ai_guesses"]
    ]
    if not valid_positions:
        return

    r, c = random.choice(valid_positions)
    state["ai_guesses"].add((r, c))

    if user_board[r][c] == 1:
        user_board[r][c] = 2  # AI hit
        state["user_ships_remaining"] -= 1
        state["message"] += f"\nAI hit your ship at ({r}, {c})!"
    else:
        user_board[r][c] = 3  # AI miss
        state["message"] += f"\nAI missed at ({r}, {c})."

def make_move(state, row, col):
    """ Handles the user's move, updates the board, and checks win conditions. """
    if state["game_over"]:
        return (
            plot_board(state["user_board"]),
            plot_board(state["ai_board"], is_user_board=False),
            state["message"],
            plot_color_key()
        )

    # Validate row/col input
    if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
        state["message"] = "Invalid input. Row/Col must be between 0 and 4."
        return (
            plot_board(state["user_board"]),
            plot_board(state["ai_board"], is_user_board=False),
            state["message"],
            plot_color_key()
        )

    # Check if user already attacked this cell
    if state["ai_board"][row][col] in (2, 3):
        state["message"] = f"You already attacked ({row}, {col})!"
        return (
            plot_board(state["user_board"]),
            plot_board(state["ai_board"], is_user_board=False),
            state["message"],
            plot_color_key()
        )

    # If there's a ship at the target
    if state["ai_board"][row][col] == 1:
        state["ai_board"][row][col] = 2  # User hit
        state["ai_ships_remaining"] -= 1
        state["message"] = f"Hit! You hit AI's ship at ({row}, {col})."
    else:
        state["ai_board"][row][col] = 3  # User miss
        state["message"] = f"Miss! No ship at ({row}, {col})."

    # Check if user just won
    if state["ai_ships_remaining"] == 0:
        state["message"] += "\nYou sank all the AI's ships. You win!"
        state["game_over"] = True
        return (
            plot_board(state["user_board"]),
            plot_board(state["ai_board"], is_user_board=False),
            state["message"],
            plot_color_key()
        )

    # Otherwise, let the AI guess
    ai_guess(state)

    # Check if AI just won
    if state["user_ships_remaining"] == 0:
        state["message"] += "\nAI sank all your ships. You lose!"
        state["game_over"] = True

    return (
        plot_board(state["user_board"]),
        plot_board(state["ai_board"], is_user_board=False),
        state["message"],
        plot_color_key()
    )

def reset_game():
    """ Reset the game state completely. """
    return init_game()

def update_display(state):
    """
    Helper function to pull out the boards and message
    so we can show them immediately or after any reset.
    """
    return (
        plot_board(state["user_board"]),
        plot_board(state["ai_board"], is_user_board=False),
        state["message"],
        plot_color_key()
    )

with gr.Blocks() as demo:
    gr.Markdown("""
    # Battleship Game
    
    **Welcome to Battleship!**
    
    In your opponent's 5x5 grid, there are three hidden ships (size=1). 
    Select the row (0-4) and column (0-4) you want to fire at, then hit "Fire!" 
    Follow the messages to see who gets hit and eventually wins.
    """)

    # Initialize game state
    state = gr.State(init_game())

    # Layout
    with gr.Row():
        with gr.Column():
            user_board_display = gr.Plot(label="Your Board")
        with gr.Column():
            ai_board_display = gr.Plot(label="AI Board")

    message_display = gr.Textbox(label="Game Messages", interactive=False)
    color_key_display = gr.Plot(label="Color Key")  # Will be updated automatically

    row_in = gr.Number(label="Row (0-4)", value=0, precision=0)
    col_in = gr.Number(label="Column (0-4)", value=0, precision=0)
    fire_button = gr.Button("Fire!")
    reset_button = gr.Button("Reset Game")

    # Render boards on initial load
    demo.load(fn=update_display, inputs=state,
              outputs=[user_board_display, ai_board_display, message_display, color_key_display])

    # Fire action
    fire_button.click(
        fn=make_move,
        inputs=[state, row_in, col_in],
        outputs=[user_board_display, ai_board_display, message_display, color_key_display]
    )

    # Reset action
    # 1. Reset the state
    # 2. Then re-render the boards using update_display
    reset_button.click(fn=reset_game, inputs=[], outputs=state).then(
        fn=update_display,
        inputs=state,
        outputs=[user_board_display, ai_board_display, message_display, color_key_display]
    )

demo.launch()
