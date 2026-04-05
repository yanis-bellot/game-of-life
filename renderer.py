import pygame
import numpy as np

STATE_SANDBOX, STATE_ANALYSIS = 0,1
SUBMODE_FINDER, SUBMODE_GROUPER, SUBMODE_TUNNELER = 0, 1, 2

class UIRenderer:
    def __init__(self, screen, font, sidebar_w, res):
        self.screen = screen
        self.font = font
        self.sidebar_w = sidebar_w
        self.res = res
        self.colors = [{
            "bg": (30, 30, 35),
            "sidebar": (45, 45, 50),
            "alive": (0, 255, 150),
            "text": (200, 200, 200),
            "inactive_boxes": (70, 70, 75),
            "subtext": (150, 150, 150)
        },{
            "bg": (30, 30, 35),
            "sidebar": (45, 45, 50),
            "alive": (0, 255, 150),
            "text": (200, 200, 200),
            "inactive_boxes": (70, 70, 75),
            "subtext": (150, 150, 150)
        }]

    def draw_grid(self, grid_value, current_state):
        rgb_array = np.zeros((grid_value.shape[1], grid_value.shape[0], 3), dtype=np.uint8)
        if current_state == STATE_SANDBOX:
            rgb_array[grid_value.T == 1] = self.colors[0]["alive"]
        elif current_state == STATE_ANALYSIS:
            rgb_array[grid_value.T == 1] = self.colors[1]["alive"]

        small_surf = pygame.surfarray.make_surface(rgb_array)
        full_width = grid_value.shape[1] * self.res
        full_height = grid_value.shape[0] * self.res
        scaled_surf = pygame.transform.scale(small_surf, (full_width, full_height))
        self.screen.blit(scaled_surf, (self.sidebar_w, 0))

    def draw_sandbox_ui(self, stats, rule_buttons, rules, dropdown_info, input_info):
        labels = [
            "SANDBOX MODE",
            "",
            f"Statut: {stats['playing']}",
            f"Génération: {stats['gen']}",
            f"Vitesse (FPS): {stats['fps']}",
            "",
            "COMMANDES:",
            "[ESPACE] : Play/Pause",
            "[C] : Effacer",
            "[HAUT/BAS] : Vitesse",
            "SOURIS : Dessiner",
            "A : Mode Analyse"
            "",
            "RULES:"
        ]
        pygame.draw.rect(self.screen, self.colors[0]["sidebar"], (0, 0, self.sidebar_w, 800))
        for i, txt in enumerate(labels):
            if txt:
                img = self.font.render(txt, True, self.colors[0]["text"])
                self.screen.blit(img, (20, 30 + i * 30))
        self.draw_rule_selectors(rules, rule_buttons)
        self.draw_input_box(
            input_info["rect"],
            input_info["text"],
            input_info["active"]
        )
        self.draw_dropdown(dropdown_info)

    def draw_analysis_ui(self, dropdown_info, current_submode):
        labels = [
            f"ANALYSIS MODE ({current_submode})",
            "",
            "COMMANDES:",
            "[ESPACE] : Play/Pause",
            "C : Changer de sous-mode",
            "S : Mode Sandbox",
            "",
        ]
        self.draw_dropdown(dropdown_info)

    def draw_sidebar(self, stats, rule_buttons, rules, dropdown_info, input_info ,current_state, current_submode):
        if current_state == STATE_SANDBOX:
            self.draw_sandbox_ui(stats, rule_buttons, rules, dropdown_info, input_info)
        elif current_state == STATE_ANALYSIS:
            self.draw_analysis_ui(dropdown_info, current_submode)


    def draw_rule_selectors(self, rules, buttons):
        base_y = buttons[0]["rect"].y
        self.screen.blit(self.font.render("Naissance (B):", True, self.colors[0]["text"]), (20, base_y - 25))
        self.screen.blit(self.font.render("Survie (S):", True, self.colors[0]["text"]), (20, base_y + 20))

        for btn in buttons:
            active = rules[btn["r_idx"]][btn["val"]] == 1
            color = self.colors[0]["alive"] if active else self.colors[0]["inactive_boxes"]

            pygame.draw.rect(self.screen, color, btn["rect"])
            if btn["r_idx"] == 0:
                num_txt = self.font.render(btn["label"], True, self.colors[0]["subtext"])
                self.screen.blit(num_txt, (btn["rect"].x + 2, base_y + 60))

    def draw_dropdown(self, info):
        rect = info["rect"]
        title = info["title"]
        current_name = info["current"]
        options = info["options"]
        is_open = info["is_open"]
        pygame.draw.rect(self.screen, (60, 60, 70), rect)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        txt = self.font.render(f" {title}: {current_name}", True, self.colors[0]["text"])
        self.screen.blit(txt, (rect.x + 10, rect.y + 5))

        if is_open:
            for i, name in enumerate(options):
                opt_rect = pygame.Rect(rect.x, rect.y + (i + 1) * 30, rect.width, 30)
                pygame.draw.rect(self.screen, (80, 80, 90), opt_rect)
                pygame.draw.rect(self.screen, self.colors[0]["subtext"], opt_rect, 1)

                opt_txt = self.font.render(name, True, self.colors[0]["text"])
                self.screen.blit(opt_txt, (opt_rect.x + 10, opt_rect.y + 5))

    def draw_input_box(self, rect, text, is_active):
        title = self.font.render("Taille Cellule (px):", True, self.colors[0]["text"])
        self.screen.blit(title, (rect.x, rect.y - 25))

        color = (100, 100, 110) if is_active else (60, 60, 70)
        pygame.draw.rect(self.screen, color, rect)

        border_color = (0, 255, 150) if is_active else (150, 150, 150)
        pygame.draw.rect(self.screen, border_color, rect, 2)

        txt_surface = self.font.render(text, True, self.colors[0]["text"])
        self.screen.blit(txt_surface, (rect.x + 10, rect.y + 5))