import pygame
from code.player import Player
from code.settings import *

class UI:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.health_bar = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar = pygame.Rect(10, 40, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def draw_bar(self, health, stats, bar_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bar_rect)
        ratio = health / stats
        current_width = bar_rect.width * ratio # 200 * (health / 100)
        rect_copy = bar_rect.copy()
        rect_copy.width = current_width
        pygame.draw.rect(self.display_surface, color, rect_copy)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bar_rect, 3)

    def display(self, player: Player):
        self.draw_bar(player.health, player.stats["health"] ,self.health_bar, HEALTH_COLOR)
        self.draw_bar(player.mana, player.stats["mana"], self.mana_bar, ENERGY_COLOR)