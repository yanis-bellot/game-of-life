import pygame


class UIRenderer:
    def __init__(self, screen, font, sidebar_w, res):
        self.screen = screen
        self.font = font
        self.sidebar_w = sidebar_w
        self.res = res
        self.colors = {
            "bg": (30, 30, 35),
            "sidebar": (45, 45, 50),
            "alive": (0, 255, 150),
            "text": (200, 200, 200),
            "boxes": ()
        }

    def draw_grid(self, grid_value):
        for y, row in enumerate(grid_value):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(self.screen, self.colors["alive"],
                                     (self.sidebar_w + x * self.res, y * self.res, self.res - 1, self.res - 1))

    def draw_sidebar(self, stats, rule_buttons, rules, dropdown_info, input_info):
        pygame.draw.rect(self.screen, self.colors["sidebar"], (0, 0, self.sidebar_w, 800))

        labels = [
            f"Statut: {stats['playing']}",
            f"Génération: {stats['gen']}",
            f"Vitesse (FPS): {stats['fps']}",
            "",
            "COMMANDES:",
            "[ESPACE] : Play/Pause",
            "[C] : Effacer",
            "[HAUT/BAS] : Vitesse",
            "SOURIS : Dessiner",
            "",
            "RULES:"
        ]

        for i, txt in enumerate(labels):
            if txt:
                img = self.font.render(txt, True, self.colors["text"])
                self.screen.blit(img, (20, 30 + i * 30))


        self.draw_rule_selectors(rules, rule_buttons)
        self.draw_input_box(
            input_info["rect"],
            input_info["text"],
            input_info["active"]
        )
        self.draw_dropdown(
            dropdown_info['rect'],
            dropdown_info['current_name'],
            dropdown_info['options'],
            dropdown_info['is_open']
        )

    def draw_rule_selectors(self, rules, buttons):
        base_y = buttons[0]["rect"].y
        self.screen.blit(self.font.render("Naissance (B):", True, self.colors["text"]), (20, base_y - 25))
        self.screen.blit(self.font.render("Survie (S):", True, self.colors["text"]), (20, base_y + 20))

        for btn in buttons:
            active = rules[btn["r_idx"]][btn["val"]] == 1
            color = self.colors["alive"] if active else (70, 70, 75)

            pygame.draw.rect(self.screen, color, btn["rect"])
            if btn["r_idx"] == 0:
                num_txt = self.font.render(btn["label"], True, (150, 150, 150))
                self.screen.blit(num_txt, (btn["rect"].x + 2, base_y + 60))

    def draw_dropdown(self, rect, current_name, options, is_open):
        pygame.draw.rect(self.screen, (60, 60, 70), rect)
        pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        txt = self.font.render(f"Mode: {current_name}", True, self.colors["text"])
        self.screen.blit(txt, (rect.x + 10, rect.y + 5))

        if is_open:
            for i, name in enumerate(options):
                opt_rect = pygame.Rect(rect.x, rect.y + (i + 1) * 30, rect.width, 30)
                pygame.draw.rect(self.screen, (80, 80, 90), opt_rect)
                pygame.draw.rect(self.screen, (150, 150, 150), opt_rect, 1)

                opt_txt = self.font.render(name, True, self.colors["text"])
                self.screen.blit(opt_txt, (opt_rect.x + 10, opt_rect.y + 5))

    def draw_input_box(self, rect, text, is_active):
        title = self.font.render("Taille Cellule (px):", True, self.colors["text"])
        self.screen.blit(title, (rect.x, rect.y - 25))

        color = (100, 100, 110) if is_active else (60, 60, 70)
        pygame.draw.rect(self.screen, color, rect)

        border_color = (0, 255, 150) if is_active else (150, 150, 150)
        pygame.draw.rect(self.screen, border_color, rect, 2)

        txt_surface = self.font.render(text, True, self.colors["text"])
        self.screen.blit(txt_surface, (rect.x + 10, rect.y + 5))