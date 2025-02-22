import pygame
from config import BLACK, WHITE, LIGHT_GRAY

def run_menu(screen, clock, window_width, window_height):
    font_big = pygame.font.SysFont("Arial", 36)
    font_small = pygame.font.SysFont("Arial", 24)
    
    manual_button_rect = pygame.Rect(3*window_width//8 - 100, window_height//2 - 50, 200, 50)
    auto_button_rect = pygame.Rect(5*window_width//8 - 100, window_height//2 - 50, 200, 50)
    
    total_runs = ""
    tick_speed = ""
    input_active_runs = False
    input_active_speed = False
    state = "mode_selection"  # "mode_selection" o "auto_inputs"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if state == "mode_selection":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if manual_button_rect.collidepoint(event.pos):
                        return False, 0, 40  # Manual: velocidad por defecto 40 ticks/seg
                    elif auto_button_rect.collidepoint(event.pos):
                        state = "auto_inputs"
            elif state == "auto_inputs":
                runs_box_rect = pygame.Rect(window_width//2 - 150, window_height//2 - 75, 300, 40)
                speed_box_rect = pygame.Rect(window_width//2 - 150, window_height//2 + 10, 300, 40)
                start_button_rect = pygame.Rect(window_width//2 - 100, window_height//2 + 80, 200, 50)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if runs_box_rect.collidepoint(event.pos):
                        input_active_runs = True
                        input_active_speed = False
                    elif speed_box_rect.collidepoint(event.pos):
                        input_active_speed = True
                        input_active_runs = False
                    elif start_button_rect.collidepoint(event.pos):
                        if total_runs != "" and tick_speed != "":
                            return True, int(total_runs), int(tick_speed)
                    else:
                        input_active_runs = False
                        input_active_speed = False
                if event.type == pygame.KEYDOWN:
                    if input_active_runs:
                        if event.key == pygame.K_BACKSPACE:
                            total_runs = total_runs[:-1]
                        elif event.key == pygame.K_RETURN:
                            input_active_runs = False
                        else:
                            if event.unicode.isdigit():
                                total_runs += event.unicode
                    elif input_active_speed:
                        if event.key == pygame.K_BACKSPACE:
                            tick_speed = tick_speed[:-1]
                        elif event.key == pygame.K_RETURN:
                            input_active_speed = False
                        else:
                            if event.unicode.isdigit():
                                tick_speed += event.unicode
        
        screen.fill(BLACK)
        if state == "mode_selection":
            title = font_big.render("Seleccione modo de ejecución", True, WHITE)
            screen.blit(title, title.get_rect(center=(window_width//2, window_height//4)))
            pygame.draw.rect(screen, LIGHT_GRAY, manual_button_rect)
            manual_text = font_small.render("Manual", True, WHITE)
            screen.blit(manual_text, manual_text.get_rect(center=manual_button_rect.center))
            pygame.draw.rect(screen, LIGHT_GRAY, auto_button_rect)
            auto_text = font_small.render("Automático", True, WHITE)
            screen.blit(auto_text, auto_text.get_rect(center=auto_button_rect.center))
        elif state == "auto_inputs":
            title = font_big.render("Modo Automático", True, WHITE)
            screen.blit(title, title.get_rect(center=(window_width//2, window_height//4)))
            
            runs_box_rect = pygame.Rect(window_width//2 - 150, window_height//2 - 75, 300, 40)
            pygame.draw.rect(screen, WHITE, runs_box_rect, 2)
            runs_label = font_small.render("Número de laberintos:", True, WHITE)
            screen.blit(runs_label, runs_label.get_rect(midbottom=(runs_box_rect.centerx, runs_box_rect.top - 10)))
            runs_text = font_small.render(total_runs, True, WHITE)
            screen.blit(runs_text, runs_text.get_rect(center=runs_box_rect.center))
            
            speed_box_rect = pygame.Rect(window_width//2 - 150, window_height//2 + 10, 300, 40)
            pygame.draw.rect(screen, WHITE, speed_box_rect, 2)
            speed_label = font_small.render("Velocidad (ticks/seg):", True, WHITE)
            screen.blit(speed_label, speed_label.get_rect(midbottom=(speed_box_rect.centerx, speed_box_rect.top - 10)))
            speed_text = font_small.render(tick_speed, True, WHITE)
            screen.blit(speed_text, speed_text.get_rect(center=speed_box_rect.center))
            
            start_button_rect = pygame.Rect(window_width//2 - 100, window_height//2 + 80, 200, 50)
            pygame.draw.rect(screen, LIGHT_GRAY, start_button_rect)
            start_text = font_small.render("Iniciar", True, WHITE)
            screen.blit(start_text, start_text.get_rect(center=start_button_rect.center))
        
        pygame.display.flip()
        clock.tick(30)
