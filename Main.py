import random

import pygame
import math
import sys
from image_loading import load_image
from start_screen import start_screen


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

    for lvl in range(1, 7):
        ShopButton(lvl)

    Cookie(1, (1, 1), board_info)
    Cookie(5, (2, 1), board_info)
    Cookie(5, (0, 1), board_info)

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


balance = 0


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
        self.income = 0  # Тут будет формула для расчета дохода печеньки определенного уровня
        self.image = load_image(f'lvl{str(lvl)}_sprite.png')
        self.mask = pygame.mask.from_surface(self.image)
        b.board[pos[1]][pos[0]][0] = lvl

        self.x, self.y = pos[0], pos[1]
        self.rect = self.image.get_rect()
        self.rect.x = 13 + self.left + self.x * self.cell_size
        self.rect.y = 13 + self.top + self.y * self.cell_size

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def go_to_nearest_cell(self):
        self_c = self.rect.center
        ranges = []

        for cell in cells_group:
            cell_c = cell.rect.center
            ranges.append(((self_c[0] - cell_c[0]) ** 2 + (self_c[1] - cell_c[1]) ** 2) ** 0.5)

        target_cell_pos = [(ranges.index(min(ranges)) + 1) % b.width - 1,
                           math.ceil((ranges.index(min(ranges)) + 1) / b.width) - 1]
        if target_cell_pos[0] == -1:
            target_cell_pos[0] = b.width - 1

        start_x, start_y = self.x, self.y
        self.x, self.y = target_cell_pos[0], target_cell_pos[1]
        self.rect.x = 13 + self.left + self.x * self.cell_size
        self.rect.y = 13 + self.top + self.y * self.cell_size
        if (self.x, self.y) == (start_x, start_y):
            pass
        elif b.board[self.y][self.x][0] == 0:
            b.board[start_y][start_x][0] = 0
            b.board[self.y][self.x][0] = self.lvl
        elif b.board[self.y][self.x][0] == self.lvl:
            b.board[start_y][start_x][0] = 0
            pygame.sprite.spritecollide(self, cookies_group, True)
            Cookie(self.lvl + 1, (self.x, self.y), b.get_info())
        else:
            for c in pygame.sprite.spritecollide(self, cookies_group, False):
                if c != self:
                    c.x, c.y = start_x, start_y
                    c.rect.x = 13 + c.left + c.x * c.cell_size
                    c.rect.y = 13 + c.top + c.y * c.cell_size
            b.board[self.y][self.x][0], b.board[start_y][start_x][0] = \
                b.board[start_y][start_x][0], b.board[self.y][self.x][0]


class ShopButton(pygame.sprite.Sprite):
    def __init__(self, lvl):
        super().__init__(buttons_group, shop_buttons_group)
        self.lvl = lvl
        self.price = 0  # Тут будет формула для расчета цены печеньки определенного уровня
        if self.lvl == 1:
            self.enabled = True
            self.image = load_image(f'shop_cell{str(self.lvl)}.png')
        else:
            self.enabled = False
            self.image = load_image(f'locked_shop_cell.png')

        self.rect = self.image.get_rect()
        self.rect.x = 215 + (self.lvl - 1) * 150
        self.rect.y = 595

    def click(self):
        global balance
        if self.price <= balance:
            for row in range(len(b.board)):
                for cell in range(len(b.board[row])):
                    if b.board[row][cell][0] == 0:
                        Cookie(self.lvl, (cell, row), b.get_info())
                        balance -= self.price
                        self.price = int(self.price * 1)  # 1 это затычка
                        return
                    if row == len(b.board) - 1 and cell == len(b.board[row]) - 1:
                        print('ВСЕ КЛЕТКИ ЗАНЯТЫ')  # Это будет выводиться на экран
        else:
            print('ТЫ БОМЖАРА')  # Это тоже (только сообщение будет более гуманным)

    def update_enabled(self):
        if not self.enabled:
            for row in b.board:
                for cell in row:
                    if cell[0] == self.lvl + 4:
                        self.enabled = True
                        self.image = load_image(f'shop_cell{str(self.lvl)}.png')
                        create_particles((self.rect.x + 50, self.rect.y + 50))


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particle_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 0.1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Merge Cakes')
    pygame.mouse.set_visible(False)
    size = width, height = 1280, 720
    screen_rect = (0, 0, width, height)
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))

    cur_group = pygame.sprite.Group()
    cells_group = pygame.sprite.Group()
    panels_group = pygame.sprite.Group()
    cookies_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    shop_buttons_group = pygame.sprite.Group()
    particle_group = pygame.sprite.Group()

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
                x0, y0 = event.pos
                if pygame.sprite.spritecollideany(cur, cookies_group):
                    collided_cookies = pygame.sprite.spritecollide(cur, cookies_group, False)
                    moving = True
                elif pygame.sprite.spritecollideany(cur, buttons_group):
                    collided_buttons = pygame.sprite.spritecollide(cur, shop_buttons_group, False)
                    for btn in collided_buttons:
                        if btn.enabled:
                            btn.click()
                        else:
                            print(f'СНАЧАЛА ОТКРОЙ ПИРОГ {btn.lvl + 4} УРОВНЯ')  # Это тоже будет
                            # выводиться на экран
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
        for btn in shop_buttons_group:
            btn.update_enabled()
        particle_group.update()
        cells_group.draw(screen)
        panels_group.draw(screen)
        shop_buttons_group.draw(screen)
        cookies_group.draw(screen)
        if cur.visible:
            cur_group.draw(screen)
        particle_group.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(120)
    pygame.quit()
