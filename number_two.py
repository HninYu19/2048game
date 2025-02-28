import pygame


class Target1(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.image_source = pygame.image.load("static/images/2.png")
        self.image = pygame.transform.scale(self.image_source, (100, 100))
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.scale = 1
        self.scale_delta = 0.01

    def update(self):
        self.scale += self.scale_delta
        if self.scale > 1.1 or self.scale < 0.9:
            self.scale_delta *= -1
        self.image = pygame.transform.scale(self.image_source, (100 * self.scale * 0.8, 100 * self.scale * 0.8))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
