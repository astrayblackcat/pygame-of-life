import pygame
import numpy as np

GAME_WIDTH = 2560
GAME_HEIGHT = 1440
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# colour scheme credit to catppuccin @ catppuccin.com
BASE = (36, 39, 58)
GRID_COLOR = (73, 77, 100)
HIGHLIGHT = (110, 115, 141)
LIVE_CELL = (183, 189, 248)
TEXT = (202, 211, 245)

def main():
    global SCREEN, CLOCK, RUNNING, GAME_SURFACE, CELL_SIZE, state, camera_x, camera_y
    pygame.init()
    pygame.display.set_caption("PyGame of Life")
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE, vsync=1)
    GAME_SURFACE = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    CLOCK = pygame.time.Clock()
    RUNNING = True
    CELL_SIZE = 20
    GAMEUPDATE = pygame.USEREVENT + 1
    pygame.time.set_timer(GAMEUPDATE, 100) # game tick timer
    paused = True
    camera_x = 0
    camera_y = 0
    mouse_drag = False

    screen_rect = SCREEN.get_rect()
    surface_rect = GAME_SURFACE.get_rect() 

    # ui elements
    font = pygame.freetype.Font(None, 18)
    controls = font.render("Pan: LMB | Place: RMB | Pause: Space", TEXT)
    paused_text = font.render("PAUSED", TEXT, size = 24)
    controls[1].midbottom = (screen_rect.centerx, screen_rect.bottom - (screen_rect.bottom / 25))
    paused_text[1].midtop = (screen_rect.centerx, 25)
    
    grid = create_grid(CELL_SIZE)
    state = np.zeros(shape=(GAME_WIDTH // CELL_SIZE, GAME_HEIGHT // CELL_SIZE))

    while RUNNING:
        SCREEN.fill(BASE)
        GAME_SURFACE.fill(BASE)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for row in grid[1:-1]:
            for cell in row[1:-1]:
                cell.update(mouse_x - surface_rect.x, mouse_y - surface_rect.y)
                cell.draw()
        
        # styling
        pygame.draw.rect(GAME_SURFACE, GRID_COLOR, (0, 0, GAME_WIDTH, GAME_HEIGHT), 2)
        surface_rect.center = screen_rect.center
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

            if event.type == pygame.VIDEORESIZE:
                pygame.transform.scale(GAME_SURFACE, event.size)
                pygame.transform.scale(controls[0], event.size)
                resized = SCREEN.get_rect()
                controls[1].midbottom = (resized.centerx, resized.bottom - (resized.bottom / 25))
                paused_text[1].midtop = (resized.centerx, 25)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_drag = True
                    mouse_start_x, mouse_start_y = event.pos
                    camera_start_x, camera_start_y = camera_x, camera_y

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_drag = False
                if event.button == 3:
                    for row in grid[1:-1]:
                        for cell in row[1:-1]:
                            cell.event(event)

            if event.type == pygame.MOUSEMOTION:
                if mouse_drag:
                    curr_x, curr_y = event.pos
                    x_offset = curr_x - mouse_start_x
                    y_offset = curr_y - mouse_start_y
                    camera_x = x_offset + camera_start_x
                    camera_y = y_offset + camera_start_y
                    # camera clamping to prevent panning off of the grid
                    camera_x = max((SCREEN.get_size()[0] - ((GAME_WIDTH + WINDOW_WIDTH) / 2) + CELL_SIZE), 
                                   min(camera_x, (GAME_WIDTH - WINDOW_WIDTH) / 2) - CELL_SIZE)
                    camera_y = max((SCREEN.get_size()[1] - ((GAME_HEIGHT + WINDOW_HEIGHT) / 2) + CELL_SIZE), 
                                   min(camera_y, (GAME_HEIGHT - WINDOW_HEIGHT) / 2) - CELL_SIZE)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

            if event.type == GAMEUPDATE:
                if not paused:
                    state = calculate_gen()

        surface_rect.x += camera_x
        surface_rect.y += camera_y
        SCREEN.blit(GAME_SURFACE, surface_rect)
        SCREEN.blit(controls[0], controls[1])
        if paused:
            SCREEN.blit(paused_text[0], paused_text[1])
                    
        pygame.display.flip()
        CLOCK.tick(144)

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
        if state[self.coords[0]][self.coords[1]] == 1:
            self.alive = True
        else:
            self.alive = False
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.hovered = True
    
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.hovered:
                state[self.coords[0]][self.coords[1]] = 1 - state[self.coords[0]][self.coords[1]]
                print(self.coords)
                

def create_grid(size):
    grid_width = GAME_WIDTH // size
    grid_height = GAME_HEIGHT // size
    grid = np.empty(shape=(grid_width, grid_height), dtype=object)
    for x in range(grid_width):
        for y in range(grid_height):
            grid[x][y] = Cell((x * size), (y * size), size)
    return grid

def calculate_gen():
    new_state = np.zeros(shape=(GAME_WIDTH // CELL_SIZE, GAME_HEIGHT // CELL_SIZE))
    for i in range(1, len(new_state) - 1):
        for j in range(1, len(new_state[i]) - 1):
            num_neighbors = 0
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx != 0 or dy != 0:
                        if state[i + dx][j + dy]:
                            num_neighbors += 1
            if state[i][j]:
                if num_neighbors == 2 or num_neighbors == 3:
                    new_state[i][j] = 1
            if not state[i][j] and num_neighbors == 3:
                    new_state[i][j] = 1
    return new_state

main()
pygame.quit()