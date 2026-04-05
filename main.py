import numpy as np
import pygame
import field
import renderer






def main():
    SCREEN_W, SCREEN_H = 1080, 720
    SIDEBAR_W = 250
    RES = 10
    GRID_W = SCREEN_W - SIDEBAR_W
    COLS, ROWS = GRID_W // RES, SCREEN_H // RES
    COLOR_BG = (30, 30, 35)
    rules_standard = [[0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0]]

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Game of Life")
    font = pygame.font.SysFont("Arial", 18)

    grid = field.Field([COLS, ROWS], rules_standard)
    view = renderer.UIRenderer(screen, font, SIDEBAR_W, RES)

    playing = False
    fps = 30
    running = True
    last_mouse_pos = None
    rule_buttons = []
    start_y_rules = 440
    for r_idx in range(2):
        for n_neighbors in range(9):
            rect = pygame.Rect(20 + n_neighbors * 18, start_y_rules + r_idx * 45, 14, 14)
            rule_buttons.append({
                "rect": rect,
                "r_idx": r_idx,
                "val": n_neighbors,
                "label": str(n_neighbors)
            })
    PRESETS = {
        "Conway": [[0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0]],
        "Seeds": [[0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "HighLife": [[0, 0, 0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0, 0]],
        "Maze": [[0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 0, 0, 0]]
    }

    current_preset = "Conway"
    STATE_SANDBOX, STATE_ANALYSIS = 0, 1
    current_state = STATE_SANDBOX
    ALGOS = ["A*", "BFS", "Dijkstra"]
    current_algo = "A*"
    SUBMODE_FINDER, SUBMODE_GROUPER, SUBMODE_TUNNELER = 0, 1, 2
    current_submode = "Grouper"
    menu_open = False
    dropdown_rect = pygame.Rect(20, 530, 160, 30)
    input_rect = pygame.Rect(20, 650, 160, 32)
    input_text = str(RES)
    input_active = False

    while running:
        keys = pygame.key.get_pressed()


        if keys[pygame.K_UP]:
            fps += 0.4  # Augmentation progressive
        if keys[pygame.K_DOWN]:
            fps -= 0.4
            if fps < 1: fps = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    input_active = input_rect.collidepoint(event.pos)
                    for btn in rule_buttons:
                        if btn["rect"].collidepoint(mouse_pos):
                            r, v = btn["r_idx"], btn["val"]
                            grid.rules[r][v] = 1 - grid.rules[r][v]

                    if dropdown_rect.collidepoint(mouse_pos):
                        menu_open = not menu_open
                    elif menu_open:
                        for i, name in enumerate(PRESETS.keys()):
                            opt_rect = pygame.Rect(dropdown_rect.x, dropdown_rect.y + (i + 1) * 30, dropdown_rect.width, 30)
                            if opt_rect.collidepoint(mouse_pos):
                                grid.rules = [np.array(r, dtype=np.int8) for r in PRESETS[name]]
                                current_preset = name
                                menu_open = False
                                grid.reset()
                                playing = False
                                break
                        else:
                            menu_open = False


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_a and current_state == STATE_SANDBOX:
                    current_state = STATE_ANALYSIS
                    playing = False
                if event.key == pygame.K_s and current_state == STATE_ANALYSIS:
                    current_state = STATE_SANDBOX


                if not playing:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            try:
                                new_res = int(input_text)
                                if 2 <= new_res <= 100:
                                    RES = new_res
                                    COLS, ROWS = GRID_W // RES, SCREEN_H // RES
                                    grid = field.Field([COLS, ROWS], grid.rules)
                                    view.res = RES
                                    last_mouse_pos = None
                            except ValueError:
                                input_text = str(RES)
                            input_active = False

                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            if event.unicode.isdigit():
                                input_text += event.unicode

                    if event.key == pygame.K_c:
                        grid.reset()

        mx, my = pygame.mouse.get_pos()
        mouse_left = pygame.mouse.get_pressed()[0]
        mouse_right = pygame.mouse.get_pressed()[2]
        if mouse_left or mouse_right:
            if mx > SIDEBAR_W:
                if last_mouse_pos is None:
                    last_mouse_pos = (mx, my)

                start_x, start_y = last_mouse_pos
                dist = max(abs(mx - start_x), abs(my - start_y), 1)

                for i in range(dist + 1):
                    lerp_x = start_x + (mx - start_x) * (i / dist)
                    lerp_y = start_y + (my - start_y) * (i / dist)

                    gx = int((lerp_x - SIDEBAR_W) // RES)
                    gy = int(lerp_y // RES)

                    if 0 <= gy < grid.value.shape[0] and 0 <= gx < grid.value.shape[1]:
                        grid.value[gy, gx] = 1 if mouse_left else 0

                last_mouse_pos = (mx, my)
        else:
            last_mouse_pos = None

        if playing:
            grid.refresh()

        screen.fill(COLOR_BG)
        view.draw_grid(grid.value, current_state)
        stats = {
            "gen": grid.gen_count,
            "fps": int(fps),
            "playing": "PLAY" if playing else "PAUSE"
        }

        if current_state == STATE_SANDBOX:
            dropdown_info = {
                "rect": dropdown_rect,
                "title": "Mode",
                "current": current_preset,
                "options": list(PRESETS.keys()),
                "is_open": menu_open
            }
        else:  # On est en mode FINDER
            dropdown_info = {
                "rect": dropdown_rect,
                "title": "Algo",
                "current": current_algo,
                "options": ALGOS,
                "is_open": menu_open
            }

        input_info = {
            "rect": input_rect,
            "text": input_text,
            "active": input_active
        }

        view.draw_sidebar(stats, rule_buttons, grid.rules, dropdown_info, input_info, current_state, current_submode)

        pygame.display.flip()
        pygame.time.Clock().tick(fps if playing else 60)

    pygame.quit()


if __name__ == "__main__":
    main()
