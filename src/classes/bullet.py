import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed=-7):
        super().__init__()
        # Charger l’image de la balle
        self.image = pygame.image.load(image_path).convert_alpha()  # Transparence
        self.image = pygame.transform.scale(self.image, (8, 20))  # redimensionner
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = speed

    def update(self):
        """Met à jour la position de la balle"""
        self.rect.y += self.speed

        # Supprimer la balle si elle sort de l’écran
        if self.rect.bottom < 0:
            self.kill()
