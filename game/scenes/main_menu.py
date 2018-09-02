# -*- coding: utf-8 -*-

import pygame
import pygame.freetype
from .abc_scene import ABCScene


class MainMenu(ABCScene):
    def __init__(self):
        super().__init__()
        self.__time = 0
        self.__font = pygame.freetype.SysFont(None, 24)

    def load(self):
        self.load_info['percent'] = 1

    def update(self, delta_time):
        self.__time += delta_time * 10

    def draw(self, surface):
        surface.fill((64, 64, 64))
