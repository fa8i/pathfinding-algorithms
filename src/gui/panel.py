# panel.py
import pygame
from config import GRID_SIZE, NUM_ROWS, NUM_COLS, BLACK, WHITE, GRAY, ORANGE, RED, BLUE, GREEN

class Panel:
    def __init__(self, x_offset, y_offset, width, height, algorithm_name, algorithm_func):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height   # Laberinto sin etiqueta
        self.algorithm_name = algorithm_name
        self.algorithm_func = algorithm_func
        self.generator = None
        self.state = {}
        self.finished = False
        self.metrics = {}

    def reset(self, maze, start, goal):
        self.generator = self.algorithm_func(maze, start, goal)
        self.state = {}
        self.finished = False
        self.metrics = {}

    def update(self):
        if not self.finished:
            try:
                self.state = next(self.generator)
            except StopIteration:
                self.finished = True
                self.metrics = self.state
            if "nodes_expanded" in self.state:
                self.metrics["nodes_expanded"] = self.state["nodes_expanded"]
            if "path_length" in self.state:
                self.metrics["path_length"] = self.state.get("path_length", 0)
            if "solvable" in self.state:
                self.metrics["solvable"] = self.state["solvable"]
            if "path" in self.state:
                self.finished = True

    def draw(self, surface, maze, start, goal):
        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                rect = pygame.Rect(self.x_offset + c * GRID_SIZE,
                                   self.y_offset + r * GRID_SIZE,
                                   GRID_SIZE, GRID_SIZE)
                color = BLACK if maze[r][c] == 1 else WHITE
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, GRAY, rect, 1)
        start_rect = pygame.Rect(self.x_offset + start[0]*GRID_SIZE,
                                 self.y_offset + start[1]*GRID_SIZE,
                                 GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, ORANGE, start_rect)
        goal_rect = pygame.Rect(self.x_offset + goal[0]*GRID_SIZE,
                                self.y_offset + goal[1]*GRID_SIZE,
                                GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, goal_rect)
        if "visited" in self.state:
            for (x, y) in self.state["visited"]:
                rect = pygame.Rect(self.x_offset + x*GRID_SIZE,
                                   self.y_offset + y*GRID_SIZE,
                                   GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, BLUE, rect)
        if "queue" in self.state:
            for (x, y) in self.state["queue"]:
                rect = pygame.Rect(self.x_offset + x*GRID_SIZE,
                                   self.y_offset + y*GRID_SIZE,
                                   GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, GREEN, rect)
        if "open_set" in self.state:
            for (x, y) in self.state["open_set"]:
                rect = pygame.Rect(self.x_offset + x*GRID_SIZE,
                                   self.y_offset + y*GRID_SIZE,
                                   GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, GREEN, rect)
        if "current" in self.state:
            x, y = self.state["current"]
            rect = pygame.Rect(self.x_offset + x*GRID_SIZE,
                               self.y_offset + y*GRID_SIZE,
                               GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, ORANGE, rect)
        if "path" in self.state and self.state["path"]:
            for (x, y) in self.state["path"]:
                rect = pygame.Rect(self.x_offset + x*GRID_SIZE,
                                   self.y_offset + y*GRID_SIZE,
                                   GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(surface, RED, rect)
