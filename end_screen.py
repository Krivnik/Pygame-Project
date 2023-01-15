import pygame
import sys
from pymorphy2 import MorphAnalyzer
from image_loading import load_image

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)


def end_screen(total_time, total_money, total_merges, total_purchases):
    morph = MorphAnalyzer()
    word_1 = morph.parse('секунда')[0].make_agree_with_number(total_time).word
    word_2 = morph.parse('пирог')[0].make_agree_with_number(total_purchases).word
    word_3 = morph.parse('раз')[0].make_agree_with_number(total_merges).word
    intro_text = ["СПАСИБО ЗА ИГРУ!",
                  "",
                  "За время игры вы:",
                  f"Потратили впустую {total_time} {word_1} своей жизни",
                  f"Заработали {total_money}$",
                  f"Купили {total_purchases} {word_2}",
                  f"Соединили пироги {total_merges} {word_3}"]

    font = pygame.font.SysFont('segoe script', 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, 'black')
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 15
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

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
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def update(self):
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    cake = Cake(load_image('cake.png'), 2, 2, 750, 518)
    cake.rect.x, cake.rect.y = 500, 100

    while True:
        screen.fill('#B97B56')
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN\
                    or event.type == pygame.MOUSEBUTTONDOWN:
                return

        cake_sprite.draw(screen)
        cake_sprite.update()

        morph = MorphAnalyzer()
        word_1 = morph.parse('секунда')[0].make_agree_with_number(total_time).word
        word_2 = morph.parse('пирог')[0].make_agree_with_number(total_purchases).word
        word_3 = morph.parse('раз')[0].make_agree_with_number(total_merges).word
        intro_text = ["СПАСИБО ЗА ИГРУ!",
                      "",
                      "За время игры вы:",
                      f"Потратили впустую {total_time} {word_1} своей жизни",
                      f"Заработали {total_money}$",
                      f"Купили {total_purchases} {word_2}",
                      f"Соединили пироги {total_merges} {word_3}"]

        font = pygame.font.SysFont('segoe script', 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, True, 'black')
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = 15
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(10)
