import os
import sys
import pygame

pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".\data")
    return os.path.join(base_path, relative_path)


def load_image(name, colorkey=None):
    fullname = resource_path(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_music(name):
    fullname = resource_path(name)
    pygame.mixer.music.load(fullname)


def load_text(name, t):
    fullname = resource_path(name)
    return open(fullname, t)
