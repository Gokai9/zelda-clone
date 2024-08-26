import pygame
class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.direction = pygame.math.Vector2()
        
    def move(self, speed):
        # if both x, y value not == 0
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.y += self.direction.y * speed
        self.collission_detector('vertical')
        self.hitbox.x += self.direction.x * speed
        self.collission_detector('horizontal')
        self.rect.center = self.hitbox.center

    def collission_detector(self, direction):
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
