import pygame
from code.settings import *
from code.player import Player
from code.tile import Tile
from code.help import *
from random import choice
from code.ui import UI
from code.weapon import Weapon

class Level:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YCamera()
        self.obstacles_sprites = pygame.sprite.Group()
        self.ui = UI()
        self.weapon = None
        self.create_map()
        
    def create_map(self) -> None:
        layouts = {
            "block": csv_tolist("./resources/map/map_FloorBlocks.csv"),
            "grass": csv_tolist("./resources/map/map_Grass.csv"),
            "object": csv_tolist("./resources/map/map_Objects.csv")
        }
        grap = {
            "grass": import_folder("./resources/graphics/grass"),
            "objects": import_folder("./resources/graphics/objects"),
        }
        for layout, val in layouts.items():
            for row_i, x_arr in enumerate(val):
                for col_i, y_arr in enumerate(x_arr):
                    if y_arr != '-1':
                        x = col_i * TILESIZE
                        y = row_i * TILESIZE
                        if layout == "block":
                            Tile((x, y), [self.obstacles_sprites], 'invisible')
                        if layout == "grass":
                            Tile((x, y), [self.obstacles_sprites, self.visible_sprites], "grass", choice(grap.get("grass")))
                        if layout == "object":
                            obj = grap["objects"][int(y_arr)]
                            Tile((x, y), [self.obstacles_sprites, self.visible_sprites], "object", obj)
        self.player = Player((1945, 900), [self.visible_sprites], self.obstacles_sprites, self.set_attack, self.destroy_weapon)
    def set_attack(self):
        self.weapon = Weapon(self.player, [self.visible_sprites])

    def destroy_weapon(self):
        if self.weapon:
            self.weapon.kill()
        self.weapon = None

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.visible_sprites.update()
        
class YCamera(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.ground_img = pygame.image.load("./resources/graphics/tilemap/ground.png").convert()
        self.ground_rect = self.ground_img.get_rect(topleft = (0, 0))
        
    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width #centerx - 640 = -480 centerx = 160
        self.offset.y = player.rect.centery - self.half_height
        ground_pos = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_img, ground_pos)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset # first rect pos is (0, 0) offset pos = (480, 120)
            self.display_surface.blit(sprite.image, offset_pos)
        