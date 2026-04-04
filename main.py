import pygame
import field

SCREEN_W, SCREEN_H = 1000, 800
SIDEBAR_W = 200
RES = 10

GRID_W = SCREEN_W - SIDEBAR_W
COLS, ROWS = GRID_W // RES, SCREEN_H // RES

COLOR_BG = (30, 30, 35)
COLOR_SIDEBAR = (45, 45, 50)
COLOR_ALIVE = (0, 255, 150)
COLOR_TEXT = (255, 255, 255)
rules_standard = [[0,0,0,1,0,0,0,0,0],[0,0,1,1,0,0,0,0,0]]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Game of Life")
    font = pygame.font.SysFont("Arial", 18)

    grid = field.Field([GRID_W, SCREEN_H], rules_standard)
    playing = False
    fps = 10
    running = True

    while running:
        screen.fill(COLOR_BG)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            fps += 0.4  # Augmentation progressive
        if keys[pygame.K_DOWN]:
            fps -= 0.4
            if fps < 1: fps = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if not playing:
                    if event.key == pygame.K_c:
                        grid = field.Field([GRID_W, SCREEN_H], rules_standard)


        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if mx > SIDEBAR_W:
                grid.value[my // RES][(mx - SIDEBAR_W) // RES] = 1

        if pygame.mouse.get_pressed()[1]:
            mx, my = pygame.mouse.get_pos()
            if mx > SIDEBAR_W:
                grid.value[my // RES][(mx - SIDEBAR_W) // RES] = 0

        if playing:
            grid.refresh()

        for x in range(COLS):
            for y in range(ROWS):
                if grid.value[y][x] == 1:
                    pygame.draw.rect(screen, COLOR_ALIVE,(SIDEBAR_W + x * RES, y * RES, RES - 1, RES - 1))

        pygame.draw.rect(screen, COLOR_SIDEBAR, (0, 0, SIDEBAR_W, SCREEN_H))

        labels = [
                f"Statut: {'PLAY' if playing else 'PAUSE'}",
                f"Génération: {grid.gen_count}",
                f"Vitesse (FPS): {int(fps)}",
                "",
                "COMMANDES:",
                "[ESPACE] : Play/Pause",
                "[C] : Effacer",
                "[HAUT/BAS] : Vitesse",
                "SOURIS : Dessiner"
        ]

        for i, text in enumerate(labels):
            img = font.render(text, True, COLOR_TEXT)
            screen.blit(img, (20, 30 + i * 30))

        pygame.display.flip()
        pygame.time.Clock().tick(fps if playing else 60)

    pygame.quit()


if __name__ == "__main__":
    main()
