"""
Enhanced Snake game using tkinter with start screen and persistent high score.

Controls:
- Arrow keys (Up/Down/Left/Right) to move
- Enter to start from the title screen
- P to pause/unpause while playing
- Space to restart after game over
- Q or the Quit button to exit

Run: python3 snake_game.py
"""

import tkinter as tk
import random
import os

# Game configuration
CELL_SIZE = 20
COLUMNS = 30  # WIDTH = COLUMNS * CELL_SIZE = 600
ROWS = 20     # HEIGHT = ROWS * CELL_SIZE = 400
WIDTH = COLUMNS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
INITIAL_SNAKE_LENGTH = 4
INITIAL_SPEED = 120  # milliseconds between moves; smaller is faster
SPEED_INCREMENT = 2  # speed up (ms) every time the snake eats
HIGHSCORE_FILE = 'highscore.txt'


def load_highscore():
    try:
        with open(HIGHSCORE_FILE, 'r') as f:
            return int(f.read().strip() or 0)
    except Exception:
        return 0


def save_highscore(score):
    try:
        with open(HIGHSCORE_FILE, 'w') as f:
            f.write(str(int(score)))
    except Exception:
        pass


class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("Snake - Tkinter")

        self.score = 0
        self.highscore = load_highscore()
        self.speed = INITIAL_SPEED
        self.direction = "Right"
        self.next_direction = self.direction
        self.running = False
        self.paused = False
        self.state = 'title'  # 'title', 'playing', 'gameover'

        # UI
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.score_var = tk.StringVar()
        self.score_var.set(f"Score: {self.score}")
        self.score_label = tk.Label(self.frame, textvariable=self.score_var, font=("Helvetica", 14))
        self.score_label.grid(row=1, column=0, sticky="w", padx=10, pady=6)

        self.high_var = tk.StringVar()
        self.high_var.set(f"High: {self.highscore}")
        self.high_label = tk.Label(self.frame, textvariable=self.high_var, font=("Helvetica", 14))
        self.high_label.grid(row=1, column=1)

        self.info_label = tk.Label(self.frame, text="Enter to start — Arrows to move — P to pause", font=("Helvetica", 10))
        self.info_label.grid(row=1, column=2, sticky="e", padx=10, pady=6)

        # Buttons
        self.start_button = tk.Button(self.frame, text="Start", command=self.start_from_title)
        self.start_button.grid(row=2, column=0, pady=6)
        self.pause_button = tk.Button(self.frame, text="Pause", command=self.toggle_pause, state='disabled')
        self.pause_button.grid(row=2, column=1)
        self.quit_button = tk.Button(self.frame, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=2, column=2)

        # Bind keys
        master.bind('<Up>', lambda e: self.change_direction('Up'))
        master.bind('<Down>', lambda e: self.change_direction('Down'))
        master.bind('<Left>', lambda e: self.change_direction('Left'))
        master.bind('<Right>', lambda e: self.change_direction('Right'))
        master.bind('<space>', lambda e: self.on_space())
        master.bind('<Return>', lambda e: self.start_from_title())
        master.bind('p', lambda e: self.toggle_pause())
        master.bind('P', lambda e: self.toggle_pause())
        master.bind('q', lambda e: self.master.quit())
        master.bind('Q', lambda e: self.master.quit())

        self.reset_to_title()

    def reset_to_title(self):
        self.state = 'title'
        self.running = False
        self.paused = False
        self.canvas.delete('all')
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20, text='SNAKE', fill='white', font=("Helvetica", 36, 'bold'))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 10, text='Press Enter or Start to play', fill='yellow', font=("Helvetica", 14))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 40, text=f'High Score: {self.highscore}', fill='lightgreen', font=("Helvetica", 12))
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.score_var.set(f"Score: {self.score}")
        self.high_var.set(f"High: {self.highscore}")

    def start_from_title(self):
        if self.state == 'title' or self.state == 'gameover':
            self.reset_game()

    def restart(self):
        if not self.running:
            self.reset_game()

    def on_space(self):
        if self.state == 'gameover':
            self.reset_game()
        elif self.state == 'playing':
            self.toggle_pause()

    def toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        self.pause_button.config(text='Resume' if self.paused else 'Pause')
        if not self.paused:
            # resume loop
            self.master.after(self.speed, self.game_loop)

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

    def reset_game(self):
        # Initialize game state
        self.score = 0
        self.speed = INITIAL_SPEED
        self.direction = 'Right'
        self.next_direction = self.direction
        self.running = True
        self.paused = False
        self.state = 'playing'

        # Place snake in center
        mid_x = COLUMNS // 2
        mid_y = ROWS // 2
        self.snake = [(mid_x - i, mid_y) for i in range(INITIAL_SNAKE_LENGTH)]

        # Place first food
        self.place_food()

        # Clear canvas and start game loop
        self.canvas.delete('all')
        self.draw()
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal', text='Pause')
        # Start loop
        self.master.after(self.speed, self.game_loop)

    def game_loop(self):
        if not self.running or self.paused:
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

        # HUD
        self.canvas.create_text(60, 12, text=f'Score: {self.score}', fill='white', font=("Helvetica", 12), anchor='w')
        self.canvas.create_text(WIDTH-60, 12, text=f'High: {self.highscore}', fill='lightgreen', font=("Helvetica", 12), anchor='e')

    def game_over(self):
        self.running = False
        self.state = 'gameover'
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20, text='GAME OVER', fill='white', font=("Helvetica", 30, 'bold'))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 10, text=f'Score: {self.score}', fill='white', font=("Helvetica", 16))

        # High score handling
        if self.score > self.highscore:
            self.highscore = self.score
            save_highscore(self.highscore)
            self.high_var.set(f"High: {self.highscore}")
            self.canvas.create_text(WIDTH//2, HEIGHT//2 + 40, text='NEW HIGH SCORE!', fill='yellow', font=("Helvetica", 12, 'bold'))
        else:
            self.canvas.create_text(WIDTH//2, HEIGHT//2 + 40, text=f'High Score: {self.highscore}', fill='lightgreen', font=("Helvetica", 12))

        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 70, text='Press Space or Start to play again', fill='yellow', font=("Helvetica", 12))
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')


if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
