import tkinter as tk
from tkinter import messagebox
import random

# Constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2

# Initialize board
board = [[EMPTY] * COLS for _ in range(ROWS)]
current_player = PLAYER

def drop_piece(col):
    global current_player
    row = get_next_open_row(col)
    if row is not None:
        board[row][col] = current_player
        draw_board()

        if check_winner(row, col):
            show_winner(current_player)
        else:
            current_player = 3 - current_player
            if current_player == AI:
                root.after(500, ai_move)

def ai_move():
    valid_cols = [c for c in range(COLS) if get_next_open_row(c) is not None]
    if valid_cols:
        col = random.choice(valid_cols)
        drop_piece(col)

def get_next_open_row(col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None

def check_winner(row, col):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        count = 1 + check_line(row, col, dr, dc) + check_line(row, col, -dr, -dc)
        if count >= 4:
            return True
    return False

def check_line(row, col, dr, dc):
    count = 0
    while 0 <= row + dr < ROWS and 0 <= col + dc < COLS and board[row][col] == board[row + dr][col + dc]:
        count += 1
        row += dr
        col += dc
    return count

def draw_board():
    canvas.delete("all")
    cell_size = 60
    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size

            canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")
            color = "white" if board[row][col] == EMPTY else ("red" if board[row][col] == PLAYER else "yellow")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color, outline="black")

def show_winner(player):
    winner = "You (Red)" if player == PLAYER else "Computer (Yellow)"
    messagebox.showinfo("Game Over", f"{winner} wins!")
    reset_board()

def reset_board():
    global board, current_player
    board = [[EMPTY] * COLS for _ in range(ROWS)]
    current_player = PLAYER
    draw_board()

# Main Window
root = tk.Tk()
root.title("Connect 4 (AI Mode)")
root.configure(bg="lightgray")
root.resizable(False, False)

# Canvas
canvas = tk.Canvas(root, width=COLS*60, height=ROWS*60, bg="white")
canvas.grid(row=0, column=0, columnspan=COLS, padx=10, pady=10)

# Buttons
for col in range(COLS):
    btn = tk.Button(root, text=str(col+1), width=6, height=1, command=lambda col=col: drop_piece(col))
    btn.grid(row=1, column=col, padx=1, pady=5)

# Restart
restart_btn = tk.Button(root, text="Restart Game", command=reset_board, bg="orange", fg="white", font=("Arial", 10, "bold"))
restart_btn.grid(row=2, column=0, columnspan=COLS, pady=10)

# Initial draw
draw_board()

# Run app
root.mainloop()
