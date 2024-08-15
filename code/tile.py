import pygame, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image_rock = pygame.image.load(os.path.join('../resources/graphics/test', 'rock.png')).convert_alpha()
        self.rect = self.image_rock.get_rect(topleft = pos)