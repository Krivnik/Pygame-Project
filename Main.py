import pygame
import sys
from math import ceil
from random import choice
from loading import load_image, load_music
from start_screen import start_screen
from end_screen import end_screen


def render_environment():
    for y in range(b.height):
        for x in range(b.width):
            Cell(x, y)
            UpgradeButton(int((b.board[y][x][1] - 1) * 10 + 1), x, y)
            Panel('invP', b.left + x * b.cell_size, 90 + b.top + y * b.cell_size)
    Panel('V', 50, 135)
    Panel('H', 190, 570)
    Panel('B', 1080, 50)

    for lvl in range(1, 7):
        ShopButton(lvl)
    for i in range(6):
        Panel('P', 215 + i * 150, 685)

    for t in range(1, 4):
        BoostButton(t)
    for i in range(2):
        Panel('P', 75, 250 + i * 300)

    Cookie(1, (1, 1))


def create_particles(position):
    particle_count = 30
    numbers = range(-5, 5)
    for _ in range(particle_count):
        Particle(position, [choice(numbers), choice(numbers)])


class Board:
    def __init__(self, width_in_cells, height_in_cells):
        self.width = width_in_cells
        self.height = height_in_cells
        self.cell_size = 100
        self.board = [[[0, 1] for _ in range(self.width)] for _ in range(self.height)]
        self.left = width // 2 - self.cell_size * self.width // 2
        self.top = height // 2 - self.cell_size * self.height // 2

    def expand(self, width_in_cells, height_in_cells):
        start_width, start_height = self.width, self.height
        self.width, self.height = width_in_cells, height_in_cells
        self.left = width // 2 - self.cell_size * self.width // 2
        self.top = height // 2 - self.cell_size * self.height // 2

        for row in self.board:
            for cell in range(self.width - start_width):
                row += [[0, 1]]
        for row in range(self.height - start_height):
            self.board += [[[0, 1] for _ in range(self.width)]]

        for cell in cells_group:
            cell.kill()
        for ub in upgrade_buttons_group:
            ub.kill()
        for ipp in inisible_price_panels_group:
            ipp.kill()
        for y in range(self.height):
            for x in range(self.width):
                Cell(x, y)
                UpgradeButton(int((b.board[y][x][1] - 1) * 10 + 1), x, y)
                Panel('invP', b.left + x * b.cell_size, 90 + b.top + y * b.cell_size)

        for c in cookies_group:
            c.rect.x = 13 + b.left + c.x * b.cell_size
            c.rect.y = 13 + b.top + c.y * b.cell_size


class Cell(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(cells_group)
        self.x, self.y = pos_x, pos_y
        self.image = load_image('cell.png')
        self.rect = self.image.get_rect()
        self.rect.x = b.left + pos_x * b.cell_size
        self.rect.y = b.top + pos_y * b.cell_size


class Panel(pygame.sprite.Sprite):
    def __init__(self, t, x, y):
        super().__init__()
        if t == 'V':
            self.image = load_image('vertical panel.png', -1)
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
        elif t == 'invP':
            self.image = load_image('price panel.png', -1)
            self.add(inisible_price_panels_group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cur_group)
        self.image = load_image("arrow.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pygame.mouse.get_pos()
        self.visible = True

    def move(self, pos):
        if pygame.mouse.get_focused():
            self.rect.x, self.rect.y = pos[0], pos[1]
            self.visible = True
        else:
            self.visible = False


class Cookie(pygame.sprite.Sprite):
    def __init__(self, lvl, pos):
        super().__init__(cookies_group)
        self.lvl = lvl
        self.x, self.y = pos[0], pos[1]
        b.board[self.y][self.x][0] = lvl
        self.income = int([0, 1, 2, 5, 12, 30, 70, 150, 320, 700, 1500][self.lvl]
                          * b.board[self.y][self.x][1])

        self.image = load_image(f'lvl{str(lvl)}_sprite.png')
        self.rect = self.image.get_rect()
        self.rect.x = 13 + b.left + self.x * b.cell_size
        self.rect.y = 13 + b.top + self.y * b.cell_size

    def move(self, x, y):
        self.rect.x, self.rect.y = x, y

    def go_to_nearest_cell(self):
        global total_merges, flPause
        self_c = self.rect.center
        ranges = [((self_c[0] - c.rect.center[0]) ** 2 + (self_c[1] - c.rect.center[1]) ** 2) ** 0.5
                  for c in cells_group]

        target_cell_pos = [(ranges.index(min(ranges)) + 1) % b.width - 1,
                           ceil((ranges.index(min(ranges)) + 1) / b.width) - 1]
        if target_cell_pos[0] == -1:
            target_cell_pos[0] = b.width - 1

        start_x, start_y = self.x, self.y
        self.x, self.y = target_cell_pos[0], target_cell_pos[1]
        self.rect.x = 13 + b.left + self.x * b.cell_size
        self.rect.y = 13 + b.top + self.y * b.cell_size
        if (self.x, self.y) == (start_x, start_y):
            pass
        elif b.board[self.y][self.x][0] == 0:
            b.board[start_y][start_x][0] = 0
            b.board[self.y][self.x][0] = self.lvl
        elif b.board[self.y][self.x][0] == self.lvl:
            if self.lvl != 10:
                b.board[start_y][start_x][0] = 0
                pygame.sprite.spritecollide(self, cookies_group, True)
                Cookie(self.lvl + 1, (self.x, self.y))
                total_merges += 1
            else:
                end_screen(flPause, total_time, total_money, total_merges, total_purchases, 'passed')
                pygame.quit()
                sys.exit()
        else:
            another_cookie = [c for c in pygame.sprite.spritecollide(self, cookies_group, False)
                              if c != self][0]
            another_cookie.x, another_cookie.y = start_x, start_y
            another_cookie.rect.x = 13 + b.left + another_cookie.x * b.cell_size
            another_cookie.rect.y = 13 + b.top + another_cookie.y * b.cell_size
            b.board[self.y][self.x][0], b.board[start_y][start_x][0] = \
                b.board[start_y][start_x][0], b.board[self.y][self.x][0]

    def update(self):
        self.income = int([0, 1, 2, 5, 12, 30, 70, 150, 320, 700, 1500][self.lvl]
                          * b.board[self.y][self.x][1])


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
        global balance, total_purchases, message, message_counter
        if self.price <= balance:
            for row in range(len(b.board)):
                for cell in range(len(b.board[row])):
                    if b.board[row][cell][0] == 0:
                        Cookie(self.lvl, (cell, row))
                        balance -= self.price
                        total_purchases += 1
                        self.price = int(self.price * 1.1)
                        return
                    if row == len(b.board) - 1 and cell == len(b.board[row]) - 1:
                        message = 'ВСЕ КЛЕТКИ ЗАНЯТЫ'
                        message_counter = 1
        else:
            message = 'НЕДОСТАТОЧНО СРЕДСТВ'
            message_counter = 1

    def update(self):
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
            self.price = int(sum([c.income for c in cookies_group]) * 150)
        self.message = f'СНАЧАЛА ОТКРОЙ ПИРОГ {self.type + 3} УРОВНЯ'
        self.enabled = False
        self.image = load_image(f'locked_cell.png')

        self.rect = self.image.get_rect()
        self.rect.x = 75
        self.rect.y = 160 + (self.type - 1) * 150

    def click(self):
        global balance, x3boost_counter, cookies_visible, message, message_counter
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
                message = 'ДОСТИГНУТ МАКСИМАЛЬНЫЙ УРОВЕНЬ ДОСКИ'
                message_counter = 1
            else:
                message = 'НЕДОСТАТОЧНО СРЕДСТВ'
                message_counter = 1

        elif self.type == 2:
            cookies_visible = not cookies_visible

        elif self.type == 3:
            if self.price <= balance and x3boost_counter % 300 == 0:
                x3boost_counter += 1
                balance -= self.price
            elif x3boost_counter % 300 != 0:
                message = 'БУСТ УЖЕ ДЕЙСТВУЕТ'
                message_counter = 1
            else:
                message = 'НЕДОСТАТОЧНО СРЕДСТВ'
                message_counter = 1

    def update(self):
        if not self.enabled:
            for row in b.board:
                for cell in row:
                    if cell[0] == self.type + 3:
                        self.enabled = True
                        self.image = load_image(f'boost_cell{str(self.type)}.png')
                        create_particles((self.rect.x + 50, self.rect.y + 50))
        if self.type == 2 and self.enabled:
            if cookies_visible:
                self.image = load_image(f'boost_cell{str(self.type)}.png')
            else:
                self.image = load_image(f'cross_cell.png')
        if self.type == 3:
            self.price = int(sum([c.income for c in cookies_group]) * 150)


class UpgradeButton(pygame.sprite.Sprite):
    def __init__(self, lvl, pos_x, pos_y):
        super().__init__(upgrade_buttons_group)
        self.x, self.y = pos_x, pos_y
        self.lvl = lvl
        self.price = [0, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, -1][self.lvl]
        self.image = load_image(f'upgrade_button{str(self.lvl)}.png')
        self.rect = self.image.get_rect()
        self.rect.x = 13 + b.left + pos_x * b.cell_size
        self.rect.y = 13 + b.top + pos_y * b.cell_size

    def click(self):
        global balance, message, message_counter
        if self.price <= balance and self.lvl < 11:
            b.board[self.y][self.x][1] += 0.1
            balance -= self.price
            self.lvl += 1
            self.price = [0, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, -1][self.lvl]
            self.image = load_image(f'upgrade_button{str(self.lvl)}.png')
        elif self.lvl == 11:
            message = 'ДОСТИГНУТ МАКСИМАЛЬНЫЙ УРОВЕНЬ ТАРЕЛКИ'
            message_counter = 1
        else:
            message = 'НЕДОСТАТОЧНО СРЕДСТВ'
            message_counter = 1


class Particle(pygame.sprite.Sprite):
    fire = [load_image('star.png')]
    for scale in (15, 20, 25):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, delta):
        super().__init__(particle_group)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = delta
        self.rect.x, self.rect.y = pos

        self.gravity = 0.1

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
    pygame.display.set_icon(load_image('icon.ico'))
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))

    cur_group = pygame.sprite.Group()
    cells_group = pygame.sprite.Group()
    panels_group = pygame.sprite.Group()
    price_panels_group = pygame.sprite.Group()
    inisible_price_panels_group = pygame.sprite.Group()
    cookies_group = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    shop_buttons_group = pygame.sprite.Group()
    boost_buttons_group = pygame.sprite.Group()
    upgrade_buttons_group = pygame.sprite.Group()
    particle_group = pygame.sprite.Group()

    flPause = False
    load_music('music.mp3')
    pygame.mixer.music.play(-1)

    start_screen(flPause)

    cur = Cursor()

    b = Board(3, 3)
    render_environment()

    balance = 25000

    cookies_visible = True
    collided_cookie = None

    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    x3boost_counter = 0

    message_counter = 3
    message = ''

    total_time = 0
    total_merges = 0
    total_money = 0
    total_purchases = 0

    running = True
    moving = False
    while running:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if x3boost_counter % 300 != 0:
                    balance += 3 * sum([c.income for c in cookies_group])
                    total_money += 3 * sum([c.income for c in cookies_group])
                    x3boost_counter += 1
                else:
                    balance += sum([c.income for c in cookies_group])
                    total_money += sum([c.income for c in cookies_group])
                if message_counter != 3:
                    message_counter += 1
                total_time += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.sprite.spritecollideany(cur, cookies_group) and cookies_visible:
                    collided_cookie = pygame.sprite.spritecollide(cur, cookies_group, False)[0]
                    dx = collided_cookie.rect.x - event.pos[0]
                    dy = collided_cookie.rect.y - event.pos[1]
                    moving = True
                elif pygame.sprite.spritecollideany(cur, buttons_group):
                    collided_button = pygame.sprite.spritecollide(cur, buttons_group, False)[0]
                    if cookies_visible or \
                            (not cookies_visible and
                             collided_button in boost_buttons_group and
                             collided_button.type == 2):
                        if collided_button.enabled:
                            collided_button.click()
                        else:
                            message = collided_button.message
                            message_counter = 1
                    else:
                        message = 'ВЫ НАХОДИТЕСЬ В РЕЖИМЕ УЛУЧШЕНИЯ ТАРЕЛОК'
                        message_counter = 1
                elif pygame.sprite.spritecollideany(cur, upgrade_buttons_group):
                    if not cookies_visible:
                        pygame.sprite.spritecollide(cur, upgrade_buttons_group, False)[0].click()
            if event.type == pygame.MOUSEMOTION:
                cur.move(event.pos)
                if moving:
                    collided_cookie.move(event.pos[0] + dx, event.pos[1] + dy)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if moving:
                    collided_cookie.go_to_nearest_cell()
                    collided_cookie = None
                    moving = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flPause = not flPause
                if flPause:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

        buttons_group.update()
        cookies_group.update()
        particle_group.update()

        cells_group.draw(screen)
        panels_group.draw(screen)
        buttons_group.draw(screen)
        price_panels_group.draw(screen)
        if not cookies_visible:
            upgrade_buttons_group.draw(screen)
            inisible_price_panels_group.draw(screen)

        font = pygame.font.SysFont('comic sans', 16)

        cookies_price = [f'{sh_b.price}$' for sh_b in shop_buttons_group]
        text_coord1 = 215
        for line in cookies_price:
            string_rendered = font.render(line, True, 'black')
            intro_rect = string_rendered.get_rect()
            intro_rect.y = 685
            text_coord1 += (50 - intro_rect.width / 2)
            intro_rect.x = text_coord1
            screen.blit(string_rendered, intro_rect)
            text_coord1 += 100 + intro_rect.width / 2

        boost1 = [boost for boost in boost_buttons_group if boost.type == 1][0]
        boost1_price = ['0$', '1000$', '7500$', '25000$', 'макс. ур.'][boost1.lvl]
        boost3 = [boost for boost in boost_buttons_group if boost.type == 3][0]
        boost3_price = f'{boost3.price}$'
        text_coord2 = -50
        for line in [boost1_price, boost3_price]:
            string_rendered = font.render(line, True, 'black')
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 75 + (50 - intro_rect.width / 2)
            text_coord2 += 300
            intro_rect.y = text_coord2
            screen.blit(string_rendered, intro_rect)

        if not cookies_visible:
            upgrades_price = [(['0$', '50$', '100$', '250$', '500$', '1000$', '2500$', '5000$',
                                '10000$', '25000$', '50000$', 'макс. ур.'][ub.lvl], ub.x, ub.y)
                              for ub in upgrade_buttons_group]
            for line in upgrades_price:
                string_rendered = font.render(line[0], True, 'black')
                intro_rect = string_rendered.get_rect()
                intro_rect.x = b.left + line[1] * b.cell_size + (50 - intro_rect.width / 2)
                intro_rect.y = 90 + b.top + line[2] * b.cell_size
                screen.blit(string_rendered, intro_rect)

        balance_text = [f'{balance}$', f'{sum([c.income for c in cookies_group])}$/c']
        if x3boost_counter % 300 != 0:
            balance_text[1] = f'{3 * sum([c.income for c in cookies_group])}$/c'
        font_size = 30
        text_coord = 25
        for line in balance_text:
            font_size -= 5
            text_coord += 30
            font = pygame.font.SysFont('comic sans', font_size)
            string_rendered = font.render(line, True, 'black')
            intro_rect = string_rendered.get_rect()
            intro_rect.y = text_coord
            intro_rect.x = 1080 + (75 - intro_rect.width / 2)
            screen.blit(string_rendered, intro_rect)

        if message_counter != 3:
            font = pygame.font.SysFont('comic sans', 30, True)
            string_rendered = font.render(message, True, 'black')
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 640 - intro_rect.width / 2
            intro_rect.y = 40
            screen.blit(string_rendered, intro_rect)

        if cookies_visible:
            if collided_cookie:
                pygame.sprite.Group([c for c in cookies_group if c != collided_cookie]).draw(screen)
                pygame.sprite.Group(collided_cookie).draw(screen)
            else:
                cookies_group.draw(screen)

        particle_group.draw(screen)

        if cur.visible:
            cur_group.draw(screen)
        pygame.display.flip()
        clock.tick(90)
    end_screen(flPause, total_time, total_money, total_merges, total_purchases, 'failed')
    pygame.quit()
    sys.exit()
