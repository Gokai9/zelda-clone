from typing import Iterable
import pygame
from pygame.sprite import AbstractGroup
from code.settings import WORLD_MAP, TILESIZE
from code.player import Player
from code.tile import Tile

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.create_map()
        
    def create_map(self) -> None:
        for x_i, x_arr in enumerate(WORLD_MAP):
            for y_i, y_arr in enumerate(x_arr):
                x = x_i * TILESIZE
                y = y_i * TILESIZE
                if y_arr == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                if y_arr == "p":
                    Player((x, y), [self.visible_sprites], self.obstacles_sprites)

    def run(self) -> None:
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()


class YCamera(pygame.sprite.Group):
    def __init__() -> None:
        super().__init__()