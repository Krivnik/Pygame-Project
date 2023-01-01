import pygame
import sys
from image_loading import load_image

FPS = 60

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)


def start_screen():
    intro_text = ["MERGE GAME",
                  "",
                  "Здесь будут",
                  "правила"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('comic sans', 60)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, 'black')
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 15
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
