import tkinter as tk
import numpy as np
import time
import random

ROWS, COLS = 15, 15
CELL_SIZE = 30
SPEED = 0.03 

# Colors
WALL = "black"
PATH = "white"
VISITED = "lightblue"
FINAL_PATH = "green"
START = "orange"
END = "red"
def generate_maze(rows, cols):
    maze = np.zeros((rows, cols), dtype=int)

    def carve_passages(r, c):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0:
                maze[r + dr//2][c + dc//2] = 1
                maze[nr][nc] = 1
                carve_passages(nr, nc)

    maze[0][0] = 1
    carve_passages(0, 0)
    maze[rows-1][cols-1] = 1
    return maze

maze = generate_maze(ROWS, COLS)

root = tk.Tk()
root.title("Maze Solver Visualizer")

canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE)
canvas.pack()

rects = {}
for r in range(ROWS):
    for c in range(COLS):
        color = PATH if maze[r][c] == 1 else WALL
        rects[(r, c)] = canvas.create_rectangle(
            c*CELL_SIZE, r*CELL_SIZE,
            (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
            fill=color, outline="gray"
        )

canvas.itemconfig(rects[(0, 0)], fill=START)
canvas.itemconfig(rects[(ROWS-1, COLS-1)], fill=END)

def visualize(r, c, color):
    canvas.itemconfig(rects[(r, c)], fill=color)
    root.update()
    time.sleep(SPEED)

def solve_maze():
    visited = np.zeros_like(maze)
    path = []

    def dfs(r, c):
        if r < 0 or c < 0 or r >= ROWS or c >= COLS:
            return False
        if maze[r][c] == 0 or visited[r][c]:
            return False

        visited[r][c] = 1
        visualize(r, c, VISITED)
        path.append((r, c))

        if (r, c) == (ROWS-1, COLS-1):
            for pr, pc in path:
                visualize(pr, pc, FINAL_PATH)
            return True

        
        if dfs(r+1, c) or dfs(r, c+1) or dfs(r-1, c) or dfs(r, c-1):
            return True

        
        path.pop()
        visualize(r, c, PATH)
        return False

    dfs(0, 0)
    visualize(0, 0, START)
    visualize(ROWS-1, COLS-1, END)
btn = tk.Button(root, text="Solve Maze", font=("Arial", 14), bg="lightgreen", command=solve_maze)
btn.pack(pady=10)
root.mainloop()
