import pygame
import numpy as np

GAME_WIDTH = 1920
GAME_HEIGHT = 1080
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# colour scheme credit to catppuccin @ catppuccin.com
BASE = (36, 39, 58)
GRID_COLOR = (73, 77, 100)
HIGHLIGHT = (110, 115, 141)
LIVE_CELL = (183, 189, 248)

def main():
    global SCREEN, CLOCK, RUNNING, GAME_SURFACE, camera_x, camera_y
    pygame.init()
    pygame.display.set_caption("PyGame of Life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, vsync=1)
    GAME_SURFACE = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    CLOCK = pygame.time.Clock()
    RUNNING = True
    CELL_SIZE = 20
    camera_x = 0
    camera_y = 0
    mouse_drag = False
    screen_rect = SCREEN.get_rect()
    surface_rect = GAME_SURFACE.get_rect() 
    
    grid = createGrid(CELL_SIZE)

    while RUNNING:
        SCREEN.fill(BASE)
        GAME_SURFACE.fill(BASE)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for row in grid:
            for cell in row:
                cell.draw()
                cell.update(mouse_x - surface_rect.x, mouse_y - surface_rect.y)
        
        # styling
        pygame.draw.rect(GAME_SURFACE, GRID_COLOR, (0, 0, GAME_WIDTH, GAME_HEIGHT), 2)
        surface_rect.center = screen_rect.center
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            elif event.type == pygame.VIDEORESIZE:
                SCREEN = pygame.display.set_mode(event.size, pygame.RESIZABLE, vsync=1)
                pygame.transform.scale(GAME_SURFACE, event.size)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_drag = True
                    mouse_start_x, mouse_start_y = event.pos
                    camera_start_x, camera_start_y = camera_x, camera_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_drag = False
                if event.button == 3:
                    for row in grid:
                        for cell in row:
                            cell.event(event)

            elif event.type == pygame.MOUSEMOTION:
                if mouse_drag:
                    curr_x, curr_y = event.pos
                    x_offset = curr_x - mouse_start_x
                    y_offset = curr_y - mouse_start_y
                    camera_x = x_offset + camera_start_x
                    camera_y = y_offset + camera_start_y
            
        surface_rect.x += camera_x
        surface_rect.y += camera_y
        SCREEN.blit(GAME_SURFACE, surface_rect)
                    
        pygame.display.flip()
        CLOCK.tick(60)

class Cell: 
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.color = GRID_COLOR
        self.alive = False
        self.hovered = False
        self.coords = (x // size, y // size) # dividing a cell's screen position by its size results in its actual grid position

    def draw(self):
        if self.alive:
            pygame.draw.rect(GAME_SURFACE, LIVE_CELL, self.rect)
        elif self.hovered:
            pygame.draw.rect(GAME_SURFACE, HIGHLIGHT, self.rect)
        else:
            pygame.draw.rect(GAME_SURFACE, self.color, self.rect, 1)

    def update(self, mouse_x, mouse_y):
        self.hovered = False
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.hovered = True
    
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.hovered:
                self.alive = not self.alive

def createGrid(size):
    grid_width = GAME_WIDTH // size
    grid_height = GAME_HEIGHT // size
    grid = np.empty(shape=(grid_width, grid_height), dtype=object)
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x][y] = Cell((x * size), (y * size), size)
    return grid
            
main()
pygame.quit()
