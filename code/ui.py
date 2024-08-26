import pygame
from code.player import Player
from code.settings import *

class UI:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.health_bar = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar = pygame.Rect(10, 40, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.weapon_graphics = []
        for val in weapon_data.values():
            weapon = val['graphic']
            image = pygame.image.load(weapon).convert_alpha()
            self.weapon_graphics.append(image)

    def draw_bar(self, health, stats, bar_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bar_rect)
        ratio = health / stats
        current_width = bar_rect.width * ratio # 200 * (health / 100)
        rect_copy = bar_rect.copy()
        rect_copy.width = current_width
        pygame.draw.rect(self.display_surface, color, rect_copy)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bar_rect, 3)
    def select_box(self, top, left, switch):
        box = pygame.Rect(top, left, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, box)
        if switch:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, box, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, box, 3)
        return box

    def change_weapon(self, index_weapon, switch):
        box = self.select_box(10, 620, switch)
        image = self.weapon_graphics[index_weapon]
        rect = image.get_rect(center = box.center)
        self.display_surface.blit(image, rect)

    def change_magic(self):
        box = self.select_box(100, 620, True)
        
    def show_exp(self, text):
        text_surf = self.font.render(str(int(text)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)

    def display(self, player: Player):
        self.draw_bar(player.health, player.stats["health"] ,self.health_bar, HEALTH_COLOR)
        self.draw_bar(player.mana, player.stats["mana"], self.mana_bar, ENERGY_COLOR)

        self.show_exp(player.exp)
        self.change_weapon(player.weapon_index, not player.can_switch_weapon)