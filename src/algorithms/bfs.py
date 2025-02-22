from collections import deque
from src.labyrinth import get_neighbors

def bfs(maze, start, goal):
    queue = deque([start])
    visited = {start: None}
    nodes_expanded = 0
    while queue:
        current = queue.popleft()
        nodes_expanded += 1
        yield {"current": current, "visited": set(visited.keys()),
               "queue": list(queue), "nodes_expanded": nodes_expanded}
        if current == goal:
            break
        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)
    path = []
    solvable = True
    if goal in visited:
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = visited[cur]
        path.reverse()
        if len(path) == 0:
            solvable = False
    else:
        solvable = False
    yield {"path": path, "nodes_expanded": nodes_expanded,
           "path_length": len(path), "solvable": solvable}
