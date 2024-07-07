import tkinter as tk
import random
import time

def generate_maze(canvas, maze_width, maze_height, cell_size):
    for i in range(maze_width):
        for j in range(maze_height):
            if random.uniform(0, 1) < 0.3:
                x1, y1 = i * cell_size, j * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")

def draw_player(canvas, cell_size):
    global player_pos
    player_pos = (0, 0)
    x1, y1 = player_pos[0] * cell_size, player_pos[1] * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="", fill="blue", tags="player")

def draw_goal(canvas, maze_width, maze_height, cell_size):
    global goal_pos
    goal_pos = (maze_width - 1, maze_height - 1)
    x1, y1 = goal_pos[0] * cell_size, goal_pos[1] * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="green", tags="goal")

def move_player(event):
    global player_pos
    if event.keysym == "Up":
        new_pos = (player_pos[0], max(0, player_pos[1] - 1))
    elif event.keysym == "Down":
        new_pos = (player_pos[0], min(maze_height - 1, player_pos[1] + 1))
    elif event.keysym == "Left":
        new_pos = (max(0, player_pos[0] - 1), player_pos[1])
    elif event.keysym == "Right":
        new_pos = (min(maze_width - 1, player_pos[0] + 1), player_pos[1])
    
    if is_valid_move(new_pos):
        player_pos = new_pos
        redraw_canvas()
        check_win()

def is_valid_move(new_pos):
    global maze_grid
    x, y = new_pos
    if x < 0 or x >= maze_width or y < 0 or y >= maze_height:
        return False
    return not maze_grid[y][x]

def redraw_canvas():
    canvas.delete("player")
    x1, y1 = player_pos[0] * cell_size, player_pos[1] * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="", fill="blue", tags="player")

def create_maze_grid(maze_width, maze_height):
    maze_grid = [[False] * maze_width for _ in range(maze_height)]
    for i in range(maze_width):
        for j in range(maze_height):
            if random.uniform(0, 1) < 0.3:
                maze_grid[j][i] = True
    return maze_grid

def check_win():
    global player_pos, goal_pos, timer_running
    if player_pos == goal_pos:
        canvas.create_text(window_width // 2, window_height // 2, text="You Win!", font=("Arial", 24, "bold"), fill="green")
        timer_running = False

def reset_game():
    global maze_grid, player_pos, timer_running, start_time, elapsed_time
    maze_grid = create_maze_grid(maze_width, maze_height)
    canvas.delete("all")
    draw_goal(canvas, maze_width, maze_height, cell_size)
    for i in range(maze_width):
        for j in range(maze_height):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if maze_grid[j][i]:
                canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
    draw_player(canvas, cell_size)
    timer_running = True
    start_time = time.time()
    elapsed_time = 0
    update_timer()

def update_timer():
    global timer_running, elapsed_time
    if timer_running:
        elapsed_time = int(time.time() - start_time)
        timer_label.config(text=f"Time: {elapsed_time} seconds")
        root.after(1000, update_timer)

def toggle_pause():
    global timer_running
    timer_running = not timer_running
    if timer_running:
        update_timer()

def save_maze():
    with open("maze_save.txt", "w") as file:
        for row in maze_grid:
            file.write("".join(["1" if cell else "0" for cell in row]) + "\n")

def load_maze():
    global maze_grid, player_pos, timer_running, start_time
    with open("maze_save.txt", "r") as file:
        lines = file.readlines()
    maze_grid = [[True if cell == "1" else False for cell in line.strip()] for line in lines]
    canvas.delete("all")
    draw_goal(canvas, maze_width, maze_height, cell_size)
    for i in range(maze_width):
        for j in range(maze_height):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if maze_grid[j][i]:
                canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")
            else:
                canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
    draw_player(canvas, cell_size)
    timer_running = True
    start_time = time.time()
    elapsed_time = 0
    update_timer()

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

maze_grid = create_maze_grid(maze_width, maze_height)
draw_goal(canvas, maze_width, maze_height, cell_size)

for i in range(maze_width):
    for j in range(maze_height):
        x1, y1 = i * cell_size, j * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        if maze_grid[j][i]:
            canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="black")
        else:
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")

draw_player(canvas, cell_size)
canvas.bind_all("<KeyPress>", move_player)

reset_button = tk.Button(root, text="Reset Game", command=reset_game)
reset_button.pack()

timer_label = tk.Label(root, text="Time: 0 seconds", font=("Arial", 16))
timer_label.pack()

pause_button = tk.Button(root, text="Pause/Resume", command=toggle_pause)
pause_button.pack()

save_button = tk.Button(root, text="Save Game", command=save_maze)
save_button.pack()

load_button = tk.Button(root, text="Load Game", command=load_maze)
load_button.pack()

timer_running = True
start_time = time.time()
elapsed_time = 0
update_timer()

root.mainloop()
