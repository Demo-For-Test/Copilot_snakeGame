"""
A simple Snake game using tkinter.

Controls:
- Arrow keys (Up/Down/Left/Right) to move
- Space to restart after game over

Run: python3 snake_game.py
"""

import tkinter as tk
import random

# Game configuration
CELL_SIZE = 20
COLUMNS = 30  # WIDTH = COLUMNS * CELL_SIZE = 600
ROWS = 20     # HEIGHT = ROWS * CELL_SIZE = 400
WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
INITIAL_SNAKE_LENGTH = 4
INITIAL_SPEED = 120  # milliseconds between moves; smaller is faster
SPEED_INCREMENT = 2  # speed up (ms) every time the snake eats


class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("Snake - Tkinter")

        self.score = 0
        self.speed = INITIAL_SPEED
        self.direction = "Right"
        self.next_direction = self.direction
        self.running = False

        # UI
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.score_var = tk.StringVar()
        self.score_var.set(f"Score: {self.score}")
        self.score_label = tk.Label(self.frame, textvariable=self.score_var, font=("Helvetica", 14))
        self.score_label.grid(row=1, column=0, sticky="w", padx=10, pady=6)

        self.info_label = tk.Label(self.frame, text="Arrows to move — Space to restart", font=("Helvetica", 10))
        self.info_label.grid(row=1, column=1, sticky="e", padx=10, pady=6)

        # Bind keys
        master.bind('<Up>', lambda e: self.change_direction('Up'))
        master.bind('<Down>', lambda e: self.change_direction('Down'))
        master.bind('<Left>', lambda e: self.change_direction('Left'))
        master.bind('<Right>', lambda e: self.change_direction('Right'))
        master.bind('<space>', lambda e: self.restart())

        self.reset_game()

    def reset_game(self):
        # Initialize game state
        self.score = 0
        self.speed = INITIAL_SPEED
        self.direction = 'Right'
        self.next_direction = self.direction
        self.running = True

        # Place snake in center
        mid_x = COLUMNS // 2
        mid_y = ROWS // 2
        self.snake = [(mid_x - i, mid_y) for i in range(INITIAL_SNAKE_LENGTH)]

        # Place first food
        self.place_food()

        # Clear canvas and start game loop
        self.canvas.delete('all')
        self.draw()
        # Start loop
        self.master.after(self.speed, self.game_loop)

    def restart(self):
        if not self.running:
            self.reset_game()

    def change_direction(self, new_dir):
        # Prevent direct reversal
        opposites = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if new_dir == opposites.get(self.direction):
            return
        # Save as next direction to avoid multiple turns in one tick
        self.next_direction = new_dir

    def place_food(self):
        available = [(x, y) for x in range(COLUMNS) for y in range(ROWS) if (x, y) not in self.snake]
        if not available:
            # No more space: player wins
            self.food = None
            return
        self.food = random.choice(available)

    def game_loop(self):
        if not self.running:
            return

        # Update direction
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        if self.direction == 'Up':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'Down':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'Left':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'Right':
            new_head = (head_x + 1, head_y)
        else:
            new_head = (head_x, head_y)

        # Check collisions with walls
        x, y = new_head
        if x < 0 or x >= COLUMNS or y < 0 or y >= ROWS:
            self.game_over()
            return

        # Check collisions with self
        if new_head in self.snake:
            self.game_over()
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check food
        if self.food and new_head == self.food:
            self.score += 1
            self.score_var.set(f"Score: {self.score}")
            # speed up slightly
            self.speed = max(20, self.speed - SPEED_INCREMENT)
            self.place_food()
        else:
            # remove tail
            self.snake.pop()

        self.draw()
        # Continue loop
        self.master.after(self.speed, self.game_loop)

    def draw(self):
        self.canvas.delete('all')
        # Draw food
        if self.food:
            fx, fy = self.food
            x1 = fx * CELL_SIZE
            y1 = fy * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            self.canvas.create_oval(x1+2, y1+2, x2-2, y2-2, fill='red', outline='orange')

        # Draw snake
        for idx, (sx, sy) in enumerate(self.snake):
            x1 = sx * CELL_SIZE
            y1 = sy * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            color = '#00FF00' if idx == 0 else '#00CC00'
            self.canvas.create_rectangle(x1+1, y1+1, x2-1, y2-1, fill=color, outline='')

        # Grid optional (comment out if you don't want grid lines)
        # for i in range(COLUMNS+1):
        #     self.canvas.create_line(i*CELL_SIZE, 0, i*CELL_SIZE, HEIGHT, fill='#111')
        # for j in range(ROWS+1):
        #     self.canvas.create_line(0, j*CELL_SIZE, WIDTH, j*CELL_SIZE, fill='#111')

    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20, text='GAME OVER', fill='white', font=("Helvetica", 30, 'bold'))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 10, text=f'Score: {self.score}', fill='white', font=("Helvetica", 16))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 40, text='Press Space to restart', fill='yellow', font=("Helvetica", 12))


if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
