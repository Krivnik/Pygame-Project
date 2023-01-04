import pygame
import math
import sys
from image_loading import load_image
from start_screen import start_screen

FPS = 60


def render_environment():
    upgrades = Panel('V')
    upgrades.rect.x = 75
    upgrades.rect.y = 135

    boosts = Panel('V')
    boosts.rect.x = 1055
    boosts.rect.y = 135

    shop = Panel('H')
    shop.rect.x = 190
    shop.rect.y = 570

    Cookie(1, (1, 1), board_info)
    Cookie(1, (0, 0), board_info)
    Cookie(2, (2, 2), board_info)


class Board:
    def __init__(self, width_in_cells, height_in_cells):
        self.width = width_in_cells
        self.height = height_in_cells
        self.board = [[[0, 1] for _ in range(self.width)] for _ in range(self.height)]
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

    def get_info(self):
        return self.width, self.height, self.top, self.left, self.cell_size


class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cells_group)
        self.x, self.y = pos_x, pos_y
        self.image = load_image('cell.png')
        self.rect = self.image.get_rect()


class Panel(pygame.sprite.Sprite):
    def __init__(self, t):
        super().__init__(panels_group)
        if t == 'V':
            self.image = load_image('vertical panel.png', -1)
        elif t == 'H':
            self.image = load_image('horizontal panel.png', -1)
        self.rect = self.image.get_rect()


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cur_group)
        self.image = load_image("arrow.png")
        self.rect = self.image.get_rect()
        self.visible = True

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            self.rect.x, self.rect.y = args[0].pos[0], args[0].pos[1]
        if pygame.mouse.get_focused():
            self.visible = True
        else:
            self.visible = False


class Cookie(pygame.sprite.Sprite):
    def __init__(self, lvl, pos, info):
        super().__init__(cookies_group)
        self.width, self.height, self.top, self.left, self.cell_size = info
        self.lvl = lvl
        self.image = load_image(f'lvl{str(lvl)}_sprite.png', -1)
        self.mask = pygame.mask.from_surface(self.image)
        # Думаю лучше работать с прямоугольниками, а не с маской
        b.board[pos[1]][pos[0]][0] = lvl  # В этой строчке ошибка,
        # она меняет уровень печеньки не в одной ячейке, а во всем ряду. Как это пофиксить хз

        self.x, self.y = pos[0], pos[1]
        self.rect = self.image.get_rect()
        self.rect.x = self.left + self.x * self.cell_size
        self.rect.y = self.top + self.y * self.cell_size

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def go_to_nearest_cell(self):
        self_c = self.rect.center
        ranges = []
        for cell in cells_group:
            cell_c = cell.rect.center
            if b.board[cell.y][cell.x][0] == 0 or b.board[cell.y][cell.x][0] == self.lvl:
                ranges.append(((self_c[0] - cell_c[0]) ** 2 + (self_c[1] - cell_c[1]) ** 2) ** 0.5)

            else:
                ranges.append(1000000)

        # НЕ ПЫТАЙСЯ РАЗОБРАТЬСЯ В ТОМ, ЧТО НИЖЕ
        target_cell_pos = [(ranges.index(min(ranges)) + 1) % b.width - 1,
                           math.ceil((ranges.index(min(ranges)) + 1) / b.width) - 1]
        if target_cell_pos[0] == -1:
            target_cell_pos[0] = b.width - 1
        # НЕ ПЫТАЙСЯ РАЗОБРАТЬСЯ В ТОМ, ЧТО ВЫШЕ

        b.board[self.y][self.x][0] = 0  # Тут та же самая ошибка
        self.x, self.y = target_cell_pos[0], target_cell_pos[1]
        self.rect.x = self.left + self.x * self.cell_size
        self.rect.y = self.top + self.y * self.cell_size
        if b.board[self.y][self.x][0] == self.lvl:
            self.lvl += 1
            del_sprite = pygame.sprite.spritecollideany(self, cookies_group)
            del_sprite.kill()
            self.image = load_image(f'lvl{str(self.lvl)}_sprite.png', -1)
        b.board[self.y][self.x][0] = self.lvl  # Тут тоже


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Merge Game')
    pygame.mouse.set_visible(False)
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))

    cur_group = pygame.sprite.Group()
    cells_group = pygame.sprite.Group()
    panels_group = pygame.sprite.Group()
    cookies_group = pygame.sprite.Group()

    cur = Cursor()

    start_screen()

    b = Board(3, 3)
    board_info = b.get_info()
    render_environment()

    running = True
    moving = False
    while running:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                point = pygame.mouse.get_pos()
                x0, y0 = event.pos
                if pygame.sprite.spritecollideany(cur, cookies_group):
                    collided_cookies = pygame.sprite.spritecollide(cur, cookies_group, False)
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if moving:
                    for cookie in collided_cookies:
                        cookie.go_to_nearest_cell()
                moving = False
            if event.type == pygame.MOUSEMOTION:
                if moving:
                    dx, dy = event.pos[0] - x0, event.pos[1] - y0
                    for cookie in collided_cookies:
                        cookie.update(dx, dy)
                    x0, y0 = event.pos
            cur.update(event)
        cells_group.draw(screen)
        panels_group.draw(screen)
        cookies_group.draw(screen)
        if cur.visible:
            cur_group.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    pygame.quit()
