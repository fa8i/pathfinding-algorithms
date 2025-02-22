import pygame
from config import GRID_SIZE, NUM_COLS, NUM_ROWS, PANEL_MARGIN, TABLE_WIDTH, BLACK, WHITE, RED
from src.labyrinth import generate_maze, choose_random_goal, is_solvable
from src.algorithms import bfs, astar, dijkstra, greedy
from src.gui.panel import Panel
from src.gui.menu import run_menu

def run_gui():
    pygame.init()
    clock = pygame.time.Clock()
    panels_columns = 2
    panels_rows = 2
    panel_width = NUM_COLS * GRID_SIZE
    panel_height = NUM_ROWS * GRID_SIZE
    label_height = 30
    labyrinth_area_width = PANEL_MARGIN + (panel_width + PANEL_MARGIN) * panels_columns
    labyrinth_area_height = PANEL_MARGIN + (panel_height + label_height + PANEL_MARGIN) * panels_rows
    window_width = labyrinth_area_width + TABLE_WIDTH + PANEL_MARGIN * 3
    window_height = labyrinth_area_height + PANEL_MARGIN * 2
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Competición de Algoritmos en Laberintos")
    
    auto_mode, total_runs, tick_speed = run_menu(screen, clock, window_width, window_height)
    run_count = 0
    auto_finished = False

    algorithms = [
        ("BFS", bfs),
        ("A*", astar),
        ("Dijkstra", dijkstra),
        ("Greedy", greedy)
    ]
    panels = []
    for idx, (name, func) in enumerate(algorithms):
        x_offset = PANEL_MARGIN + (idx % panels_columns) * (panel_width + PANEL_MARGIN)
        y_offset = PANEL_MARGIN + (idx // panels_columns) * (panel_height + label_height + PANEL_MARGIN)
        panels.append(Panel(x_offset, y_offset, panel_width, panel_height, name, func))
    start = (0, 0)
    maze = generate_maze()
    goal = choose_random_goal(maze, start)
    while not is_solvable(maze, start, goal):
        maze = generate_maze()
        goal = choose_random_goal(maze, start)
    for panel in panels:
        panel.reset(maze, start, goal)
    
    competition_finished = False
    waiting_for_input = False
    cumulative_scores = {panel.algorithm_name: 0 for panel in panels}
    
    table_font = pygame.font.SysFont("Arial", 20)
    table_x = labyrinth_area_width + PANEL_MARGIN * 2
    table_y = PANEL_MARGIN + 30
    cell_height = 40
    col_widths = [100, 150, 200, 200]
    num_table_rows = 1 + len(panels)
    table_height = cell_height * num_table_rows

    cumulative_col_widths = [200, 250, 200]  # Suman 650
    cumulative_table_width = sum(cumulative_col_widths)
    cumulative_table_y = table_y + table_height + 70
    cumulative_num_rows = 1 + len(panels)
    cumulative_table_height = cell_height * cumulative_num_rows

    label_font = pygame.font.SysFont("Arial", 18)
    ranking_list = ["" for _ in panels]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if not auto_mode and waiting_for_input and event.type == pygame.KEYDOWN:
                rank_keys = []
                for panel in panels:
                    if panel.metrics.get("solvable", False):
                        rank_keys.append((panel.metrics.get("path_length", float('inf')),
                                          panel.metrics.get("nodes_expanded", float('inf'))))
                    else:
                        rank_keys.append((float('inf'), float('inf')))
                sorted_indices = sorted(range(len(panels)), key=lambda i: rank_keys[i])
                ranking_list = ["" for _ in panels]
                for pos, i in enumerate(sorted_indices, start=1):
                    ranking_list[i] = str(pos) if rank_keys[i][0] != float('inf') else "No solution"
                for i, panel in enumerate(panels):
                    if ranking_list[i] != "No solution":
                        rank = int(ranking_list[i])
                        points = 5 - rank
                    else:
                        points = 0
                    cumulative_scores[panel.algorithm_name] += points
                maze = generate_maze()
                goal = choose_random_goal(maze, start)
                while not is_solvable(maze, start, goal):
                    maze = generate_maze()
                    goal = choose_random_goal(maze, start)
                for panel in panels:
                    panel.reset(maze, start, goal)
                competition_finished = False
                waiting_for_input = False
                run_count += 1

        if auto_mode and competition_finished and not auto_finished:
            pygame.time.delay(1000)
            rank_keys = []
            for panel in panels:
                if panel.metrics.get("solvable", False):
                    rank_keys.append((panel.metrics.get("path_length", float('inf')),
                                      panel.metrics.get("nodes_expanded", float('inf'))))
                else:
                    rank_keys.append((float('inf'), float('inf')))
            sorted_indices = sorted(range(len(panels)), key=lambda i: rank_keys[i])
            ranking_list = ["" for _ in panels]
            for pos, i in enumerate(sorted_indices, start=1):
                ranking_list[i] = str(pos) if rank_keys[i][0] != float('inf') else "No solution"
            for i, panel in enumerate(panels):
                if ranking_list[i] != "No solution":
                    rank = int(ranking_list[i])
                    points = 5 - rank
                else:
                    points = 0
                cumulative_scores[panel.algorithm_name] += points
            run_count += 1
            if run_count < total_runs:
                maze = generate_maze()
                goal = choose_random_goal(maze, start)
                while not is_solvable(maze, start, goal):
                    maze = generate_maze()
                    goal = choose_random_goal(maze, start)
                for panel in panels:
                    panel.reset(maze, start, goal)
                competition_finished = False
            else:
                auto_finished = True
                waiting_for_input = True
        
        if not competition_finished:
            all_finished = True
            for panel in panels:
                if not panel.finished:
                    panel.update()
                    all_finished = False
            if all_finished:
                competition_finished = True
                waiting_for_input = True
        
        screen.fill(BLACK)
        for panel in panels:
            panel.draw(screen, maze, start, goal)
            label_surface = label_font.render(panel.algorithm_name, True, WHITE)
            label_rect = label_surface.get_rect(center=(panel.x_offset + panel.width // 2,
                                                         panel.y_offset + panel.height + label_height // 2))
            screen.blit(label_surface, label_rect)
        
        pygame.draw.rect(screen, WHITE, (table_x, table_y, TABLE_WIDTH, table_height), 2)
        x_cursor = table_x
        for width in col_widths:
            x_cursor += width
            pygame.draw.line(screen, WHITE, (x_cursor, table_y), (x_cursor, table_y + table_height), 2)
        for i in range(1, num_table_rows):
            y = table_y + i * cell_height
            pygame.draw.line(screen, WHITE, (table_x, y), (table_x + TABLE_WIDTH, y), 2)
        header = ["Posición", "Algoritmo", "Nodos Expandidos", "Longitud del Camino"]
        table_data = [header]
        for idx, panel in enumerate(panels):
            nodes_expanded = panel.metrics.get("nodes_expanded", 0)
            path_length = panel.metrics.get("path_length", 0)
            solvable = panel.metrics.get("solvable", True)
            row = [ranking_list[idx],
                   panel.algorithm_name,
                   str(nodes_expanded),
                   str(path_length) if solvable else "No solution"]
            table_data.append(row)
        for row_idx, row in enumerate(table_data):
            x_cursor = table_x
            for col_idx, cell in enumerate(row):
                cell_text = table_font.render(cell, True, WHITE)
                cell_rect = pygame.Rect(x_cursor, table_y + row_idx * cell_height, col_widths[col_idx], cell_height)
                text_rect = cell_text.get_rect(center=cell_rect.center)
                screen.blit(cell_text, text_rect)
                x_cursor += col_widths[col_idx]
        
        cumulative_table_width = sum(cumulative_col_widths)
        pygame.draw.rect(screen, WHITE, (table_x, cumulative_table_y, cumulative_table_width, cumulative_table_height), 2)
        x_cursor = table_x
        for width in cumulative_col_widths:
            x_cursor += width
            pygame.draw.line(screen, WHITE, (x_cursor, cumulative_table_y), (x_cursor, cumulative_table_y + cumulative_table_height), 2)
        for i in range(1, cumulative_num_rows):
            y = cumulative_table_y + i * cell_height
            pygame.draw.line(screen, WHITE, (table_x, y), (table_x + cumulative_table_width, y), 2)
        if run_count > 0:
            cumulative_items = list(cumulative_scores.items())
            sorted_cumulative = sorted(cumulative_items, key=lambda x: x[1], reverse=True)
            final_positions = {}
            for pos, (alg, score) in enumerate(sorted_cumulative, start=1):
                final_positions[alg] = str(pos)
        else:
            final_positions = {panel.algorithm_name: "N/A" for panel in panels}
        cumulative_header = ["Algoritmo", "Puntuación Acumulada", "Posición Final"]
        cumulative_data = [cumulative_header]
        for panel in panels:
            alg = panel.algorithm_name
            row = [alg, str(cumulative_scores[alg]), final_positions.get(alg, "")]
            cumulative_data.append(row)
        for row_idx, row in enumerate(cumulative_data):
            x_cursor = table_x
            for col_idx, cell in enumerate(row):
                cell_text = table_font.render(cell, True, WHITE)
                cell_rect = pygame.Rect(x_cursor, cumulative_table_y + row_idx * cell_height, cumulative_col_widths[col_idx], cell_height)
                text_rect = cell_text.get_rect(center=cell_rect.center)
                screen.blit(cell_text, text_rect)
                x_cursor += cumulative_col_widths[col_idx]
        
        mode_text = f"Modo Automático - Laberinto {run_count} de {total_runs}" if auto_mode else "Modo Manual"
        mode_surface = table_font.render(mode_text, True, RED)
        mode_rect = mode_surface.get_rect(midbottom=(table_x + TABLE_WIDTH // 2, table_y - 10))
        screen.blit(mode_surface, mode_rect)
        
        if not auto_mode and waiting_for_input:
            cont_text = table_font.render("Presione una tecla para continuar...", True, RED)
            cont_rect = cont_text.get_rect(midtop=(table_x + TABLE_WIDTH // 2, cumulative_table_y + cumulative_table_height + 10))
            screen.blit(cont_text, cont_rect)
        elif auto_mode and run_count >= total_runs:
            end_text = table_font.render("Ejacución finalizada.", True, RED)
            end_rect = end_text.get_rect(midtop=(table_x + TABLE_WIDTH // 2, cumulative_table_y + cumulative_table_height + 10))
            screen.blit(end_text, end_rect)
        
        pygame.display.flip()
        clock.tick(tick_speed)

if __name__ == "__main__":
    run_gui()
