import heapq
from src.labyrinth import get_neighbors

def dijkstra(maze, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    distance = {start: 0}
    nodes_expanded = 0
    open_set_hash = {start}
    while open_set:
        current_priority, current = heapq.heappop(open_set)
        open_set_hash.remove(current)
        nodes_expanded += 1
        yield {"current": current, "visited": set(came_from.keys()),
               "open_set": list(open_set_hash), "nodes_expanded": nodes_expanded}
        if current == goal:
            break
        for neighbor in get_neighbors(maze, current):
            tentative_d = distance[current] + 1
            if neighbor not in distance or tentative_d < distance[neighbor]:
                came_from[neighbor] = current
                distance[neighbor] = tentative_d
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (tentative_d, neighbor))
                    open_set_hash.add(neighbor)
    path = []
    solvable = True
    if goal in came_from:
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = came_from[cur]
        path.reverse()
        if len(path) == 0:
            solvable = False
    else:
        solvable = False
    yield {"path": path, "nodes_expanded": nodes_expanded,
           "path_length": len(path), "solvable": solvable}
