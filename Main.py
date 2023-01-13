import pygame
import sys
from math import ceil
from random import choice
from image_loading import load_image
from start_screen import start_screen


def render_environment():
    cookies_info = Panel('Vl')
    cookies_info.rect.x = 25
    cookies_info.rect.y = 75

    boosts = Panel('Vr')
    boosts.rect.x = 1055
    boosts.rect.y = 125

    shop = Panel('H')
    shop.rect.x = 190
    shop.rect.y = 570

    b_panel = Panel('B')
    b_panel.rect.x = 1105
    b_panel.rect.y = 25

    for lvl in range(1, 7):
        ShopButton(lvl)
    for i in range(6):
        price = Panel('P')
        price.rect.x = 215 + i * 150
        price.rect.y = 685

    for _ in range(1, 4):
        BoostButton(_)
    for i in range(0, 3, 2):
        price = Panel('P')
        price.rect.x = 1080
        price.rect.y = 240 + i * 150
    Cookie(1, (1, 1))


def create_particles(position):
    particle_count = 30
    numbers = range(-5, 5)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


balance = 25000


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
        if width_in_cells > self.width or height_in_cells > self.height:
            start_width, start_height = self.width, self.height
            self.width = width_in_cells
            self.height = height_in_cells
            self.left = width // 2 - self.cell_size * self.width // 2
            self.top = height // 2 - self.cell_size * self.height // 2
            for row in self.board:
                for _ in range(self.width - start_width):
                    row += [[0, 1]]
            for row in range(self.height - start_height):
                self.board += [[[0, 1] for _ in range(self.width)]]

            for cell in cells_group:
                cell.kill()

            for h in range(self.height):
                for w in range(self.width):
                    c = Cell(w, h)
                    c.rect.x = self.left + w * self.cell_size
                    c.rect.y = self.top + h * self.cell_size

            for c in cookies_group:
                c.width, c.height, c.top, c.left, c.cell_size = b.get_info()
                c.rect.x = 13 + c.left + c.x * c.cell_size
                c.rect.y = 13 + c.top + c.y * c.cell_size
        else:
            print('ПОЛЕ ДОЛЖНО РАСШИРЯТЬСЯ')

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
        super().__init__()
        if t == 'Vr':
            self.image = load_image('vertical right panel.png', -1)
            self.add(panels_group)
        elif t == 'Vl':
            self.image = load_image('vertical left panel.png', -1)
            self.add(panels_group)
        elif t == 'H':
            self.image = load_image('horizontal panel.png', -1)
            self.add(panels_group)
        elif t == 'B':
            self.image = load_image('balance panel.png', -1)
            self.add(panels_group)
        elif t == 'P':
            self.image = load_image('price panel.png', -1)
            self.add(price_panels_group)
        self.rect = self.image.get_rect()


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cur_group)
        self.image = load_image("arrow.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        self.visible = True

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            self.rect.x, self.rect.y = args[0].pos[0], args[0].pos[1]
        if pygame.mouse.get_focused():
            self.visible = True
        else:
            self.visible = False


class Cookie(pygame.sprite.Sprite):
    def __init__(self, lvl, pos):
        super().__init__(cookies_group)
        self.width, self.height, self.top, self.left, self.cell_size = b.get_info()
        self.lvl = lvl
        self.income = int([0, 1, 2, 4, 9, 19, 40, 85, 178, 375, 790][self.lvl]
                          * b.board[pos[1]][pos[0]][1])
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
                           ceil((ranges.index(min(ranges)) + 1) / b.width) - 1]
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
            Cookie(self.lvl + 1, (self.x, self.y))
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
        self.price = [0, 50, 750, 2500, 7500, 25000, 75000][self.lvl]
        self.message = f'СНАЧАЛА ОТКРОЙ ПИРОГ {self.lvl + 4} УРОВНЯ'
        if self.lvl == 1:
            self.enabled = True
            self.image = load_image(f'shop_cell{str(self.lvl)}.png')
        else:
            self.enabled = False
            self.image = load_image(f'locked_cell.png')

        self.rect = self.image.get_rect()
        self.rect.x = 215 + (self.lvl - 1) * 150
        self.rect.y = 595

    def click(self):
        global balance
        if self.price <= balance:
            for row in range(len(b.board)):
                for cell in range(len(b.board[row])):
                    if b.board[row][cell][0] == 0:
                        Cookie(self.lvl, (cell, row))
                        balance -= self.price
                        self.price = int(self.price * 1.1)
                        return
                    if row == len(b.board) - 1 and cell == len(b.board[row]) - 1:
                        print('ВСЕ КЛЕТКИ ЗАНЯТЫ')  # Это будет выводиться на экран
        else:
            print('НЕДОСТАТОЧНО СРЕДСТВ')  # Это тоже

    def update_enabled(self):
        if not self.enabled:
            for row in b.board:
                for cell in row:
                    if cell[0] == self.lvl + 4:
                        self.enabled = True
                        self.image = load_image(f'shop_cell{str(self.lvl)}.png')
                        create_particles((self.rect.x + 50, self.rect.y + 50))


class BoostButton(pygame.sprite.Sprite):
    def __init__(self, t):
        super().__init__(buttons_group, boost_buttons_group)
        self.type = t
        if self.type == 1:
            self.lvl = 1
            self.price = [0, 1000, 7500, 25000, -1][self.lvl]
        elif self.type == 2:
            pass
        elif self.type == 3:
            pass
        self.message = f'СНАЧАЛА ОТКРОЙ ПИРОГ {self.type + 3} УРОВНЯ'
        self.enabled = False
        self.image = load_image(f'locked_cell.png')

        self.rect = self.image.get_rect()
        self.rect.x = 1080
        self.rect.y = 150 + (self.type - 1) * 150

    def click(self):
        global balance
        if self.type == 1:
            if self.price <= balance and self.lvl < 4:
                if self.lvl % 2 != 0:
                    b.expand(b.width + 1, b.height)
                else:
                    b.expand(b.width, b.height + 1)
                balance -= self.price
                self.lvl += 1
                self.price = [0, 1000, 7500, 25000, -1][self.lvl]
            elif self.lvl == 4:
                print('ДОСТИГНУТ МАКСИМАЛЬНЫЙ УРОВЕНЬ ДОСКИ')
            else:
                print('НЕДОСТАТОЧНО СРЕДСТВ')
        elif self.type == 2:
            pass
        elif self.type == 3:
            pass

    def update_enabled(self):
        if not self.enabled:
            for row in b.board:
                for cell in row:
                    if cell[0] == self.type + 3:
                        self.enabled = True
                        self.image = load_image(f'boost_cell{str(self.type)}.png')
                        create_particles((self.rect.x + 50, self.rect.y + 50))


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (15, 20, 25):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particle_group)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 0.09

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
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
    price_panels_group = pygame.sprite.Group()
    cookies_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    shop_buttons_group = pygame.sprite.Group()
    boost_buttons_group = pygame.sprite.Group()
    particle_group = pygame.sprite.Group()

    cur = Cursor()

    start_screen()

    b = Board(3, 3)
    board_info = b.get_info()
    render_environment()

    counter = 0
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
                    collided_buttons = pygame.sprite.spritecollide(cur, buttons_group, False)
                    for btn in collided_buttons:
                        if btn.enabled:
                            btn.click()
                        else:
                            print(btn.message)  # Это тоже будет выводиться на экран
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
        for btn in buttons_group:
            btn.update_enabled()
        particle_group.update()
        cells_group.draw(screen)
        panels_group.draw(screen)
        buttons_group.draw(screen)
        price_panels_group.draw(screen)

        cookies_price = [f'{sh_b.price}$' for sh_b in shop_buttons_group]
        boost1 = [boost for boost in boost_buttons_group if boost.type == 1][0]
        boost1_price = ['0$', '1000$', '7500$', '25000$', 'макс. ур.'][boost1.lvl]
        font = pygame.font.SysFont('segoe script', 16)  # Шрифт не конечный
        text_coord = 215
        for line in cookies_price:
            string_rendered = font.render(line, True, 'black')
            intro_rect = string_rendered.get_rect()
            intro_rect.y = 685  # Зависит от шрифта
            text_coord += (50 - intro_rect.width / 2)
            intro_rect.x = text_coord
            screen.blit(string_rendered, intro_rect)
            text_coord += 100 + intro_rect.width / 2

        string_rendered = font.render(boost1_price, True, 'black')
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 1080 + (50 - intro_rect.width / 2)
        intro_rect.y = 240
        screen.blit(string_rendered, intro_rect)

        balance_text = [f'{balance}$', f'{sum([c.income for c in cookies_group])}$/c']
        font_size = 30
        text_coord = 0
        for line in balance_text:
            font_size -= 5  # Согласен, структура дебильная, но как сказал один великий лентяй:
            text_coord += 30  # "Итак сойдет"
            font = pygame.font.SysFont('segoe script', font_size)  # Шрифт не конечный
            string_rendered = font.render(line, True, 'black')
            intro_rect = string_rendered.get_rect()
            intro_rect.y = text_coord
            intro_rect.x = 1105 + (75 - intro_rect.width / 2)
            screen.blit(string_rendered, intro_rect)

        cookies_group.draw(screen)
        particle_group.draw(screen)
        if cur.visible:
            cur_group.draw(screen)
        pygame.display.flip()
        if counter % 60 == 0:  # Я не понимаю, почему так происходит,
            # но если поставить 120, то прибыль будет приходить раз в 2 секунды
            # (Возможно на мониторе со 120 Гц картина будет другая)
            balance += sum([c.income for c in cookies_group])
        counter += 1
        pygame.time.Clock().tick(120)
    pygame.quit()
