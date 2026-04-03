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
    gen_count = 0
    running = True

    while running:
        screen.fill(COLOR_BG)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                pass

if __name__ == "__main__":
    main()
