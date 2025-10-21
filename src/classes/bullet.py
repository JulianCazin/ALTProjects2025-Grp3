import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, image_path, speed=-7, vx=0, vy=-8):
        super().__init__()
        # Charger l’image de la balle
        self.image = pygame.image.load(image_path).convert_alpha()  # Transparence
        self.image = pygame.transform.scale(self.image, (8, 20))  # redimensionner
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.vx = vx
        self.vy = vy

        self.speed = speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.bottom < 0:
            self.kill()
