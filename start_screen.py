import pygame
import sys
from image_loading import load_image

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_icon(load_image('icon.ico'))


def start_screen(flp):
    cake_sprite = pygame.sprite.Group()

    class Cake(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(cake_sprite)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    cake = Cake(load_image('cake.png'), 2, 2, 750, 518)
    cake.rect.x, cake.rect.y = 550, 100

    intro_text = ["MERGE CAKES",
                  "",
                  "Покупайте пироги и",
                  "соединяйте одинаковые между собой",
                  "для увеличения прибыли",
                  "",
                  "Используйте разнообразные бусты",
                  "для ускорения прогресса",
                  "",
                  "Для выключения музыки нажмите",
                  "ПРОБЕЛ"]

    while True:
        screen.fill('#B97B56')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flp = not flp
                if flp:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        cake_sprite.draw(screen)
        cake_sprite.update()

        font = pygame.font.SysFont('comic sans', 30)
        text_coord = 15
        for line in intro_text:
            string_rendered = font.render(line, True, 'black')
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = 30
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(10)
