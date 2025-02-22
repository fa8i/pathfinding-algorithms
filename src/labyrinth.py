import random
from collections import deque
from config import NUM_COLS, NUM_ROWS, WALL_PROB

def generate_maze(seed=None, wall_prob=WALL_PROB):
    if seed is not None:
        random.seed(seed)
    maze = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if random.random() < wall_prob:
                maze[r][c] = 1
    maze[0][0] = 0  # Aseguramos que el inicio esté libre
    return maze

def get_free_cells(maze):
    free = []
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            if maze[r][c] == 0:
                free.append((c, r))
    return free

def choose_random_goal(maze, start):
    free = get_free_cells(maze)
    free = [cell for cell in free if cell != start]
    return random.choice(free) if free else start

def get_neighbors(maze, pos):
    x, y = pos
    neighbors = []
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < NUM_COLS and 0 <= ny < NUM_ROWS:
            if maze[ny][nx] == 0:
                neighbors.append((nx, ny))
    return neighbors

def is_solvable(maze, start, goal):
    q = deque([start])
    visited = {start}
    while q:
        current = q.popleft()
        if current == goal:
            return True
        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return False
