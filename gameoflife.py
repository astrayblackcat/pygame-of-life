import pygame

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
# colour scheme credit to catppuccin @ catppuccin.com
BACKGROUND = (36, 39, 58)
GRID_COLOR = (73, 77, 100)

def main():
    global SCREEN, CLOCK, RUNNING
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    RUNNING = True
    CELL_SIZE = 20

    SCREEN.fill(BACKGROUND)
    createGrid(CELL_SIZE)

    while RUNNING:
        for cell in grid:
            cell.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

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
        pygame.draw.rect(SCREEN, self.colour, (self.x, self.y, self.size, self.size), 1)

grid = []
def createGrid(size):
    for x in range(0, WINDOW_WIDTH, size):
        for y in range(0, WINDOW_HEIGHT, size):
            grid.append(Cell(x, y, size))

main()
pygame.quit()