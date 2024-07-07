import tkinter as tk
import random

def generate_maze(canvas, maze_width, maze_height, cell_size):
    for i in range(maze_width):
        for j in range(maze_height):
            if random.uniform(0, 1) < 0.3:
                x1, y1 = i * cell_size, j * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")

def draw_player(canvas, cell_size):
    player_pos = (0, 0)
    x1, y1 = player_pos[0] * cell_size, player_pos[1] * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="", fill="blue")

def draw_goal(canvas, maze_width, maze_height, cell_size):
    goal_pos = (maze_width - 1, maze_height - 1)
    x1, y1 = goal_pos[0] * cell_size, goal_pos[1] * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="green")

def move_player(event):
    global player_pos
    if event.keysym == "Up":
        player_pos = (player_pos[0], max(0, player_pos[1] - 1))
    elif event.keysym == "Down":
        player_pos = (player_pos[0], min(maze_height - 1, player_pos[1] + 1))
    elif event.keysym == "Left":
        player_pos = (max(0, player_pos[0] - 1), player_pos[1])
    elif event.keysym == "Right":
        player_pos = (min(maze_width - 1, player_pos[0] + 1), player_pos[1])
    redraw_canvas()

def redraw_canvas():
    canvas.delete("player")
    x1, y1 = player_pos[0] * cell_size, player_pos[1] * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="", fill="blue", tags="player")

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

player_pos = (0, 0)
draw_player(canvas, cell_size)
draw_goal(canvas, maze_width, maze_height, cell_size)

canvas.bind_all("<KeyPress>", move_player)

root.mainloop()
