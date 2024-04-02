import pygame
import numpy as np

GAME_WIDTH = 1920
GAME_HEIGHT = 1080
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# colour scheme credit to catppuccin @ catppuccin.com
BACKGROUND = (36, 39, 58)
GRID_COLOR = (73, 77, 100)

def main():
    global SCREEN, CLOCK, RUNNING, GAME_SURF, camera_x, camera_y
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, vsync=1)
    GAME_SURF = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    CLOCK = pygame.time.Clock()
    RUNNING = True
    CELL_SIZE = 20
    camera_x = 0
    camera_y = 0
    mouse_drag = False
    screen_rect = SCREEN.get_rect()
    surf_rect = GAME_SURF.get_rect() 
    
    grid = createGrid(CELL_SIZE)

    while RUNNING:
        SCREEN.fill(BACKGROUND)
        GAME_SURF.fill(BACKGROUND)

        for row in grid:
            for cell in row:
                cell.draw()
        
        # styling
        pygame.draw.rect(GAME_SURF, GRID_COLOR, (0, 0, GAME_WIDTH, GAME_HEIGHT), 2)
        surf_rect.center = screen_rect.center

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_x += 5
        elif keys[pygame.K_RIGHT]:
            camera_x -= 5
        elif keys[pygame.K_DOWN]:
            camera_y -= 5
        elif keys[pygame.K_UP]:
            camera_y += 5

        surf_rect.x += camera_x
        surf_rect.y += camera_y
        SCREEN.blit(GAME_SURF, surf_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            elif event.type == pygame.VIDEORESIZE:
                SCREEN = pygame.display.set_mode(event.size, pygame.RESIZABLE, vsync=1)
                pygame.transform.scale(GAME_SURF, event.size)
            
            # camera controls
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 2:
                    mouse_drag = True
                    mouse_start_x, mouse_start_y = event.pos
                    camera_start_x, camera_start_y = camera_x, camera_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 2:
                    mouse_drag = False

            elif event.type == pygame.MOUSEMOTION:
                if mouse_drag:
                    curr_x, curr_y = event.pos
                    x_offset = curr_x - mouse_start_x
                    y_offset = curr_y - mouse_start_y
                    camera_x = x_offset + camera_start_x
                    camera_y = y_offset + camera_start_y
                    
        pygame.display.flip()
        CLOCK.tick(60)

class Cell: 
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = GRID_COLOR
        self.live = False
        self.coords = (x // size, y // size) # dividing a cell's screen position by its size results in its actual grid position
    def draw(self):
        pygame.draw.rect(GAME_SURF, self.colour, (self.x, self.y, self.size, self.size), 1)

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
