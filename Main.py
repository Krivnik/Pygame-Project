import pygame
import sys
from image_loading import load_image
from start_screen import start_screen

FPS = 60


class Board:
    def __init__(self, width_in_cells, height_in_cells):
        self.width = width_in_cells
        self.height = height_in_cells
        self.board = [[0, 1] * self.width for _ in range(self.height)]
        self.cell_size = 100
        self.left = width // 2 - self.cell_size * self.width // 2
        self.top = height // 2 - self.cell_size * self.height // 2

        for h in range(self.height):
            for w in range(self.width):
                c = Cell(w, h)
                c.rect.x = self.left + w * self.cell_size
                c.rect.y = self.top + h * self.cell_size

    def expand(self, width_in_cells, height_in_cells):
        if width_in_cells > self.width and height_in_cells > self.height:
            self.width = width_in_cells
            self.height = height_in_cells
            self.left = width // 2 - self.cell_size * self.width // 2
            self.top = height // 2 - self.cell_size * self.height // 2
            for row in self.board:
                row.append([0, 1])
            self.board.append([[0, 1]] * self.width)

            for h in range(self.height):
                for w in range(self.width):
                    c = Cell(w, h)
                    c.rect.x = self.left + w * self.cell_size
                    c.rect.y = self.top + h * self.cell_size
        else:
            print('ПОЛЕ ДОЛЖНО РАСШИРЯТЬСЯ')

    def get_cell(self, mouse_pos):
        width_in_pixels = self.width * self.cell_size
        height_in_pixels = self.height * self.cell_size
        if (self.left < mouse_pos[0] < self.left + width_in_pixels) and \
                (self.top < mouse_pos[1] < self.top + height_in_pixels):
            cell_coords = (mouse_pos[0] - self.left) // self.cell_size, \
                          (mouse_pos[1] - self.top) // self.cell_size
            return cell_coords
        return None

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        self.on_click(self.get_cell(mouse_pos))


class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cells_group)
        self.x, self.y = pos_x, pos_y
        self.image = load_image('cell.png', -1)
        self.rect = self.image.get_rect()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Merge Game')
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)

    start_screen()
    screen.fill('white')

    cells_group = pygame.sprite.Group()

    board = Board(3, 3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        cells_group.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    pygame.quit()
