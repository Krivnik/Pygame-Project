import pygame
import sys
from image_loading import load_image
from start_screen import start_screen

FPS = 60

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Merge Game')
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)

    start_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    pygame.quit()
