import tkinter as tk
import random

def generate_maze(canvas, maze_width, maze_height, cell_size):
    for i in range(maze_width):
        for j in range(maze_height):
            if random.uniform(0, 1) < 0.3:
                x1, y1 = i * cell_size, j * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")

root = tk.Tk()
root.title("Maze Game")

window_width = 600
window_height = 600
root.geometry(f"{window_width}x{window_height}")

canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

maze_width = 10
maze_height = 10
cell_size = window_width // maze_width

for i in range(maze_width):
    for j in range(maze_height):
        x1, y1 = i * cell_size, j * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

generate_maze(canvas, maze_width, maze_height, cell_size)

root.mainloop()
